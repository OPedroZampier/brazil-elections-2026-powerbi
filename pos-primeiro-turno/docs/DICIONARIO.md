# Dicionário dos arquivos

Todos os CSVs usam UTF-8 com BOM e separador ponto e vírgula. Ausência numérica é campo vazio, não zero. IDs são texto. Percentuais no CSV são frações decimais, por exemplo 0.25 corresponde a 25%.

| Arquivo | Granularidade e uso |
| --- | --- |
| resultados_abrangencia.csv | Eleição + turno + abrangência + cargo. Controle de votação, participação e cobertura. |
| votos_candidatos.csv | Chave de resultado + candidato. Ranking e votação geográfica. |
| votos_partidos.csv | Chave de resultado + partido. Nominais, legenda e anulados; valores indisponíveis permanecem vazios. |
| candidaturas_perfil_resultado.csv | Candidato único do primeiro turno, cargos principais. Perfil, QP, média e segundo turno. |
| eleitos_proporcionais_detalhe.csv | Subconjunto do cadastro: cargos 6/7/8 com resultado QP ou média. Lista completa para conferir. |
| eleitos_qp_media_resumo.csv | UF + cargo + partido + forma de eleição. Contagem do cadastro, não votação. |
| quociente_eleitoral_por_uf.csv | UF + cargo proporcional. QE e número de vagas publicados no resultado unificado. Não é cálculo do QP. |
| validacoes.csv | Teste por chave de resultado. Não usar como tabela de negócio. |

## Campos compartilhados

`chave_resultado`: eleição-turno-UF-cargo; liga o controle às tabelas de votos. `eleicao`: 6257 para Presidente, 6259 para cargos estaduais. `turno`: 1. `abrangencia`: Brasil/UF/Exterior. `uf`: BR nacional, sigla estadual ou ZZ exterior. `codigo_cargo`: 1 Presidente, 3 Governador, 5 Senador, 6 Deputado Federal, 7 Deputado Estadual, 8 Deputado Distrital. `cargo`: rótulo. `sq_candidato`: identificador TSE, não CPF. `partido`: sigla registrada.

## Controle de resultados

`data_geracao`/`hora_geracao` e `data_totalizacao`/`hora_totalizacao`: horários publicados pelo TSE, preservados sem conversão de fuso. `totalizacao_finalizada`: valor oficial `tf`, não uma conclusão judicial. `secoes_total`/`secoes_totalizadas`: campos ts/st. `eleitorado`: te. `eleitores_secoes_apuradas`: esa, denominador de comparecimento + abstenções. `comparecimento`: c. `abstencoes`: a.

`votos_total`: tv. `votos_validos`: vv. `votos_nominais`: vnom. `votos_legenda`: vl, quando aplicável; para majoritários a ausência é zero por não haver legenda. `votos_brancos`: vb. `votos_nulos_total`: tvn = vn + vnt. `votos_nulos`: vn. `votos_nulos_tecnicos`: vnt. `votos_anulados`: van. `votos_anulados_sub_judice`: vansj. Não somar `votos_nulos_total` com seus dois componentes novamente.

## Votação de candidatos

`numero_candidato`, `nome`, `nome_urna`: identificação pública do candidato. `resultado`: situação st do resultado unificado. `destino_votos`: dvt, usado para distinguir válido/anulado. `votos`: vap. `percentual_oficial`: pvapn dividido por 100; percentual e denominador conforme o cargo e a abrangência definidos pelo TSE. Não somar percentuais entre UFs, candidatos ou cargos.

## Cadastro e QP

`genero`, `raca_cor`, `escolaridade`: atributos declarados na fonte, sem enriquecimento. `resultado`: DS_SIT_TOT_TURNO do cadastro. `eleito`: 1 para ELEITO, ELEITO POR QP ou ELEITO POR MÉDIA. `segundo_turno`: 1 para 2º TURNO. `#NULO` é informação ausente na fonte, não candidatura com zero votos.

`forma_eleicao` e `quantidade` no resumo: contagem de candidatos por classificação oficial. Não usar para inferir quem foi “puxado” por uma pessoa. QE e QP são conceitos diferentes; os CSVs de resumo não calculam quocientes.

## Proveniência e cobertura

`docs/manifesto_qualidade.json` registra URLs, SHA-256, horários de origem, horário UTC de extração, falhas e contagem de linhas. `fontes-json/` conserva os 137 arquivos de divulgação. Dados municipais não estão incluídos. As contagens do cadastro e as situações do JSON têm horários diferentes: uma divergência deve ser investigada, nunca mesclada silenciosamente.
