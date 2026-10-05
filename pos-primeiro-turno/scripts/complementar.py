"""Gera resumos QP/média e documentação de importação a partir dos CSVs preparados."""
import csv
import json
import shutil
from collections import Counter
from pathlib import Path
import sys

out=Path(sys.argv[1])
with (out/'dados'/'candidaturas_perfil_resultado.csv').open(encoding='utf-8-sig',newline='') as handle:
    rows=list(csv.DictReader(handle,delimiter=';'))
prop=[r for r in rows if r['codigo_cargo'] in ('6','7','8')]
elected=[r for r in prop if r['resultado'] in ('ELEITO POR QP','ELEITO POR MÉDIA')]
def export(name, data):
    with (out/'dados'/name).open('w',encoding='utf-8-sig',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=list(data[0]),delimiter=';');writer.writeheader();writer.writerows(data)
export('eleitos_proporcionais_detalhe.csv',elected)
groups=Counter((r['uf'],r['cargo'],r['partido'],r['resultado']) for r in elected)
export('eleitos_qp_media_resumo.csv',[dict(uf=uf,cargo=cargo,partido=party,forma_eleicao=status,quantidade=count) for (uf,cargo,party,status),count in sorted(groups.items())])
counts=Counter(r['resultado'] for r in elected)
bycargo={cargo:dict(Counter(r['resultado'] for r in elected if r['cargo']==cargo)) for cargo in sorted({r['cargo'] for r in elected})}
summary={'eleitos_por_qp':counts['ELEITO POR QP'],'eleitos_por_media':counts['ELEITO POR MÉDIA'],'total_eleitos_proporcionais':len(elected),'percentual_qp':counts['ELEITO POR QP']/len(elected),'por_cargo':bycargo,'fonte':'Cadastro TSE BRASIL gerado em '+rows[0]['data_geracao']+' '+rows[0]['hora_geracao'],'definicao':'Classificação oficial, não inferência de candidato puxado por outra pessoa.'}
(out/'docs'/'resumo_qp_media.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
quotients=[]
for source in sorted((out/'fontes-json').glob('*.json')):
    data=json.loads(source.read_bytes());cargo=data['carg'][0]
    if int(cargo['cd']) in (6,7,8):
        quotients.append(dict(uf=data['cdabr'],codigo_cargo=int(cargo['cd']),cargo=cargo['nmn'],quociente_eleitoral=int(cargo['qe']),vagas=int(cargo['nv']),data_geracao=data['dg'],hora_geracao=data['hg']))
export('quociente_eleitoral_por_uf.csv',quotients)
with (out/'dados'/'votos_candidatos.csv').open(encoding='utf-8-sig',newline='') as handle:
    official=list(csv.DictReader(handle,delimiter=';'))
jsoncounts=Counter(r['resultado'] for r in official if r['codigo_cargo'] in ('6','7','8'))
assert jsoncounts['Eleito por QP']==counts['ELEITO POR QP']
assert jsoncounts['Eleito por média']==counts['ELEITO POR MÉDIA']
summary['conferencia_json_oficial']={'qp':jsoncounts['Eleito por QP'],'media':jsoncounts['Eleito por média'],'contagens_conferem':True}
(out/'docs'/'resumo_qp_media.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
theme={'name':'Eleições 2026 — primeiro turno','dataColors':['#22C5A4','#548BC0','#E3BA55','#86D6D2','#738BA3','#DB746B'],'background':'#031529','foreground':'#F4F7FC','tableAccent':'#22C5A4'}
(out/'fundos'/'tema-eleicoes-2026.json').write_text(json.dumps(theme,ensure_ascii=False,indent=2),encoding='utf-8')
payload=json.dumps(rows,ensure_ascii=False).replace('<','\\u003c')
html='''<!doctype html><html lang="pt-BR"><meta charset="utf-8"><title>Prévia — Eleitos por QP e média</title>
<style>body{margin:0;background:#031529;color:#f4f7fc;font:16px 'Segoe UI',sans-serif}main{max-width:1200px;margin:24px auto;padding:0 20px}h1{margin-bottom:5px}p{color:#b6c8d9}select{background:#0b2239;color:white;padding:9px;border:1px solid #22c5a4;border-radius:4px;margin:0 20px 18px 6px}.cards{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}.card,.panel{background:#0b2239;border:1px solid #29495f;border-radius:8px;padding:20px}.card{border-top:3px solid #22c5a4}.card span{display:block;color:#b6c8d9;font-size:13px}.card b{display:block;font-size:32px;margin-top:10px}.charts{display:grid;grid-template-columns:2fr 1fr;gap:16px;margin-top:20px}h2{font-size:17px;margin-top:0}.row{display:grid;grid-template-columns:100px 1fr 80px;align-items:center;gap:8px;margin-top:14px;font-size:13px}.bar{display:flex;height:18px}.qp{background:#22c5a4}.media{background:#548bc0}.legend{font-size:13px;color:#b6c8d9}table{width:100%;border-collapse:collapse;font-size:13px}td,th{padding:9px;text-align:left;border-bottom:1px solid #29495f}.panel.detail{margin-top:20px}.note{line-height:1.6}a{color:#22c5a4}</style>
<main><h1>ELEIÇÕES 2026</h1><p>Eleitos, QP e segundo turno — prévia dos dados e das interações, ainda fora do Power BI</p>
<label>UF <select id="uf"></select></label><label>Cargo <select id="cargo"></select></label><label>Partido <select id="partido"></select></label>
<div class="cards"><div class="card"><span>ELEITOS POR QP</span><b id="qp"></b></div><div class="card"><span>ELEITOS POR MÉDIA</span><b id="media"></b></div><div class="card"><span>% PROPORCIONAIS POR QP</span><b id="pct"></b></div><div class="card"><span>CANDIDATOS NO 2º TURNO</span><b id="segundo"></b></div></div>
<div class="charts"><section class="panel"><h2>Forma de eleição por partido</h2><div class="legend">Verde: QP · Azul: média · Top 10 por total de eleitos</div><div id="parties"></div></section><section class="panel"><h2>QP e média por cargo</h2><div id="cargos"></div><p class="note">QP é quociente partidário. QE é quociente eleitoral. A classificação não identifica, sozinha, quem foi “puxado” por outro candidato.</p></section></div>
<section class="panel detail"><h2>Consulta de eleitos e segundo turno</h2><p id="coverage"></p><div style="max-height:320px;overflow:auto"><table><thead><tr><th>Nome de urna</th><th>Partido</th><th>UF</th><th>Cargo</th><th>Resultado</th></tr></thead><tbody id="detail"></tbody></table></div></section>
<p>Fonte: cadastro de candidaturas do TSE, gerado em 05/10/2026 às 10:14:11. Contagens QP/média conferidas também nos JSONs de resultados. <a href="docs/PLANO.md">Planejamento das três páginas</a>.</p></main>
<script>const data=PAYLOAD;const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
for(const k of ['uf','cargo','partido']){document.getElementById(k).innerHTML='<option value="">Todos</option>'+[...new Set(data.map(r=>r[k]))].sort().map(s=>`<option>${esc(s)}</option>`).join('');document.getElementById(k).onchange=update;}
function update(){const selected=data.filter(r=>['uf','cargo','partido'].every(k=>!document.getElementById(k).value||r[k]===document.getElementById(k).value));const elected=selected.filter(r=>['ELEITO POR QP','ELEITO POR MÉDIA'].includes(r.resultado));const qp=elected.filter(r=>r.resultado==='ELEITO POR QP').length,media=elected.length-qp;document.getElementById('qp').textContent=qp.toLocaleString('pt-BR');document.getElementById('media').textContent=media.toLocaleString('pt-BR');document.getElementById('pct').textContent=elected.length?(qp/elected.length).toLocaleString('pt-BR',{style:'percent',minimumFractionDigits:2,maximumFractionDigits:2}):'—';document.getElementById('segundo').textContent=selected.filter(r=>r.segundo_turno==='1').length;
function chart(key,target){const m={};for(const r of elected){const a=m[r[key]]||(m[r[key]]=[0,0]);a[r.resultado==='ELEITO POR QP'?0:1]++;}const pairs=Object.entries(m).sort((a,b)=>(b[1][0]+b[1][1])-(a[1][0]+a[1][1])).slice(0,10),max=Math.max(1,...pairs.map(p=>p[1][0]+p[1][1]));document.getElementById(target).innerHTML=pairs.length?pairs.map(([name,[q,m]])=>`<div class="row"><span>${esc(name)}</span><div class="bar"><div class="qp" style="width:${q/max*100}%" title="QP: ${q}"></div><div class="media" style="width:${m/max*100}%" title="Média: ${m}"></div></div><span>${q} / ${m}</span></div>`).join(''):'Sem eleitos proporcionais neste recorte.';}chart('partido','parties');chart('cargo','cargos');const detail=selected.filter(r=>r.eleito==='1'||r.segundo_turno==='1').sort((a,b)=>a.nome_urna.localeCompare(b.nome_urna));document.getElementById('coverage').textContent=`${detail.length.toLocaleString('pt-BR')} candidaturas no recorte. A tabela mostra até 100; a lista completa está nos CSVs.`;document.getElementById('detail').innerHTML=detail.slice(0,100).map(r=>'<tr>'+['nome_urna','partido','uf','cargo','resultado'].map(k=>'<td>'+esc(r[k])+'</td>').join('')+'</tr>').join('');}update();</script></html>'''
(out/'PREVIA-QP.html').write_text(html.replace('PAYLOAD',payload),encoding='utf-8')
for name in ['PLANO.md','MEDIDAS.dax','IMPORTAR.md','DICIONARIO.md','preparar.py','complementar.py','fundos.mjs']:
    target=out/('docs' if name.endswith('.md') or name.endswith('.dax') else 'scripts')/name
    target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(Path(__file__).parent/name,target)
shutil.copy2(Path(__file__).parent/'LerCSV.pq',out/'powerquery'/'LerCSV.pq')
print(json.dumps(summary,ensure_ascii=True,indent=2))
