"""Snapshot oficial do primeiro turno. Não altera o PBIX nem as fontes locais."""
import argparse
import csv
import hashlib
import json
import time
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

UFS = 'AC AL AP AM BA CE DF ES GO MA MT MS MG PA PB PR PE PI RJ RN RS RO RR SC SP SE TO'.split()
CARGOS = {1: 'Presidente', 3: 'Governador', 5: 'Senador', 6: 'Deputado Federal', 7: 'Deputado Estadual', 8: 'Deputado Distrital'}
URL = 'https://resultados.tse.jus.br/oficial/ele2026/{ele}/dados/{uf}/{uf}-c{cargo:04d}-e{ele:06d}-u.json'


def salvar_csv(path, rows):
    if not rows:
        raise ValueError(f'Sem linhas: {path}')
    with path.open('w', encoding='utf-8-sig', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter=';')
        writer.writeheader()
        writer.writerows(rows)


def inteiro(value):
    return int(value) if value not in (None, '') else None


def baixar(task, cache):
    uf, ele, cargo = task
    url = URL.format(uf=uf.lower(), ele=ele, cargo=cargo)
    target = cache / f'{uf.lower()}-c{cargo:04d}-e{ele:06d}-u.json'
    last = None
    for attempt in range(3):
        try:
            request = urllib.request.Request(url, headers={'User-Agent': 'TSE-PowerBI-public-data/1.0'})
            with urllib.request.urlopen(request, timeout=45) as response:
                raw = response.read()
            data = json.loads(raw)
            if data['f'] != 'o' or int(data['ele']) != ele or int(data['t']) != 1:
                raise ValueError('Resposta não corresponde à eleição oficial de primeiro turno')
            if len(data['carg']) != 1 or int(data['carg'][0]['cd']) != cargo:
                raise ValueError('Cargo inesperado')
            target.write_bytes(raw)
            return task, data, {'url': url, 'arquivo': target.name, 'sha256': hashlib.sha256(raw).hexdigest(), 'geracao_tse': data['dg']+' '+data['hg'], 'totalizacao_tse': data['dt']+' '+data['ht']}
        except Exception as error:
            last = str(error)
            time.sleep(attempt + 1)
    return task, None, {'url': url, 'erro': last}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--candidatos', type=Path, default=Path(r'D:\TSE2026\dados\candidatos\consulta_cand_2026_BRASIL.csv'))
    args = parser.parse_args()
    out = args.output
    for folder in ['dados', 'fontes-json', 'fundos', 'docs', 'powerquery']:
        (out / folder).mkdir(parents=True, exist_ok=True)
    tasks = [('BR',6257,1)] + [(uf,6257,1) for uf in UFS+['ZZ']]
    tasks += [(uf,6259,cargo) for uf in UFS for cargo in [3,5,6,8 if uf=='DF' else 7]]
    results, manifests, failures = [], [], []
    with ThreadPoolExecutor(max_workers=4) as pool:
        jobs = [pool.submit(baixar, task, out/'fontes-json') for task in tasks]
        for future in as_completed(jobs):
            task, data, manifest = future.result()
            if data is None:
                failures.append(manifest)
            else:
                results.append((task,data))
                manifests.append(manifest)
            if (len(results)+len(failures)) % 20 == 0:
                print(f'JSONs: {len(results)} obtidos, {len(failures)} falhas', flush=True)

    facts, candidates, parties, checks = [], [], [], []
    for (uf,ele,cargo), data in sorted(results):
        key = f'{ele}-1-{uf}-{cargo}'
        section, electors, votes = data['s'], data['e'], data['v']
        common = dict(chave_resultado=key, eleicao=ele, turno=1, abrangencia='Brasil' if uf=='BR' else ('Exterior' if uf=='ZZ' else 'UF'), uf=uf, codigo_cargo=cargo, cargo=CARGOS[cargo])
        row = dict(common, data_geracao=data['dg'], hora_geracao=data['hg'], data_totalizacao=data['dt'], hora_totalizacao=data['ht'], totalizacao_finalizada=data['tf'], secoes_total=inteiro(section['ts']), secoes_totalizadas=inteiro(section['st']), eleitorado=inteiro(electors['te']), eleitores_secoes_apuradas=inteiro(electors['esa']), comparecimento=inteiro(electors['c']), abstencoes=inteiro(electors['a']), votos_total=inteiro(votes['tv']), votos_validos=inteiro(votes['vv']), votos_nominais=inteiro(votes['vnom']), votos_legenda=inteiro(votes.get('vl','0')), votos_brancos=inteiro(votes['vb']), votos_nulos_total=inteiro(votes['tvn']), votos_nulos=inteiro(votes['vn']), votos_nulos_tecnicos=inteiro(votes['vnt']), votos_anulados=inteiro(votes['van']), votos_anulados_sub_judice=inteiro(votes['vansj']))
        facts.append(row)
        for agr in data['carg'][0]['agr']:
            for party in agr['par']:
                parties.append(dict(common, numero_partido=party['n'], partido=party['sg'], nome_partido=party['nm'], votos_nominais=inteiro(party.get('tvtn')), votos_legenda=inteiro(party.get('tvtl')), votos_anulados=inteiro(party.get('tvan'))))
                for cand in party.get('cand',[]):
                    candidates.append(dict(common, sq_candidato=cand['sqcand'], numero_candidato=cand['n'], nome=cand['nm'], nome_urna=cand['nmu'], partido=party['sg'], resultado=cand['st'], destino_votos=cand['dvt'], votos=inteiro(cand['vap']), percentual_oficial=float(cand['pvapn'].replace(',','.'))/100))
        checks.append(dict(chave_resultado=key, teste='comparecimento + abstencoes = eleitores das secoes apuradas', aprovado=row['comparecimento']+row['abstencoes']==row['eleitores_secoes_apuradas']))
        checks.append(dict(chave_resultado=key, teste='reconciliacao do total de votos', aprovado=row['votos_total']==sum(row[k] for k in ['votos_validos','votos_brancos','votos_nulos_total','votos_anulados','votos_anulados_sub_judice'])))
        checks.append(dict(chave_resultado=key, teste='validos = nominais + legenda', aprovado=row['votos_validos']==row['votos_nominais']+row['votos_legenda']))

    local = []
    elected = {'ELEITO','ELEITO POR MÉDIA','ELEITO POR QP'}
    source_counts = Counter()
    with args.candidatos.open(encoding='cp1252', newline='') as handle:
        for source in csv.DictReader(handle, delimiter=';'):
            if source['CD_CARGO'] not in {str(k) for k in CARGOS} or source['NR_TURNO'] != '1':
                continue
            status = source['DS_SIT_TOT_TURNO']
            source_counts[status] += 1
            local.append(dict(sq_candidato=source['SQ_CANDIDATO'], turno=1, uf=source['SG_UF'], codigo_cargo=int(source['CD_CARGO']), cargo=source['DS_CARGO'], nome_urna=source['NM_URNA_CANDIDATO'], partido=source['SG_PARTIDO'], genero=source['DS_GENERO'], raca_cor=source['DS_COR_RACA'], escolaridade=source['DS_GRAU_INSTRUCAO'], resultado=status, eleito=1 if status in elected else 0, segundo_turno=1 if status=='2º TURNO' else 0, data_geracao=source['DT_GERACAO'], hora_geracao=source['HH_GERACAO']))
    assert len(local) == len({r['sq_candidato'] for r in local}), 'SQ_CANDIDATO duplicado no cadastro principal de primeiro turno'
    assert len(facts) == len({r['chave_resultado'] for r in facts}), 'Chave de resultados duplicada'
    keys = [(r['chave_resultado'],r['sq_candidato']) for r in candidates]
    assert len(keys) == len(set(keys)), 'Candidato duplicado dentro da mesma abrangência'
    salvar_csv(out/'dados'/'resultados_abrangencia.csv',facts)
    salvar_csv(out/'dados'/'votos_candidatos.csv',candidates)
    salvar_csv(out/'dados'/'votos_partidos.csv',parties)
    salvar_csv(out/'dados'/'candidaturas_perfil_resultado.csv',local)
    salvar_csv(out/'dados'/'validacoes.csv',checks)
    report = {'extraido_em_utc':datetime.now(timezone.utc).isoformat(), 'escopo':'Primeiro turno. Presidente: BR, 27 UFs e exterior. Demais cargos principais: 27 UFs. Sem municípios.', 'jsons_previstos':len(tasks),'jsons_obtidos':len(results),'falhas_download':failures,'testes_falharam':[r for r in checks if not r['aprovado']], 'linhas':{'resultados_abrangencia':len(facts),'votos_candidatos':len(candidates),'votos_partidos':len(parties),'candidaturas_perfil_resultado':len(local)}, 'situacoes_cadastro_cargos_principais':dict(source_counts), 'fonte_cadastro':str(args.candidatos),'fontes_oficiais':sorted(manifests,key=lambda r:r['arquivo'])}
    (out/'docs'/'manifesto_qualidade.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='fontes_oficiais'},ensure_ascii=True,indent=2),flush=True)
    if failures or report['testes_falharam']:
        raise SystemExit('Há falhas documentadas. Não importar como cobertura completa antes de revisar.')


if __name__ == '__main__':
    main()
