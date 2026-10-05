# Montagem no Power BI

Este pacote contém dados e fundos preparados. Não altera automaticamente o modelo do PBIX.

1. Trabalhar em uma cópia do relatório existente; preservar o original e suas seis páginas.
2. Importar os CSVs UTF-8 com separador `;`. A função em `powerquery/LerCSV.pq` evita interpretar IDs como números.
3. Nomear as tabelas como `ResultadosAbrangencia`, `VotosCandidatos`, `VotosPartidos` e `CandidaturasPerfilResultado`.
4. Tipar `codigo_cargo`, `turno`, `eleicao`, contagens e votos como inteiro. SQ_CANDIDATO, chaves e números de candidatos/partidos permanecem texto. `percentual_oficial` é decimal com ponto no CSV e deve ser convertido com localidade English (United States), depois formatado como percentual.
5. Não importar os resumos QP junto com o cadastro para somar ambos. Os resumos são conferência independente e alternativa de consumo.
6. Criar os relacionamentos descritos no plano. Instalar e verificar as medidas de `docs/MEDIDAS.dax` uma a uma; são definições separadas, não um script executável único.
7. Criar páginas 1280 × 720, fundo PNG correspondente com ajuste Fill e transparência 0%. O texto dos títulos já existe no fundo; não duplicar títulos nos visuais.
8. Posicionar cards, filtros e gráficos nas áreas do plano. Visuais com fundo transparente, labels legíveis e contagens sem decimais.
9. Configurar cargo e UF de votação com seleção única. A página de participação não recebe filtro de partido/candidato.
10. Executar todos os testes do plano e revisar visualmente antes de considerar o PBIX pronto.

Os JSONs oficiais preservam a fonte e seus horários. O script `scripts/preparar.py` baixa novamente os resultados oficiais e refaz os CSVs. Cada execução substitui os arquivos deste pacote: arquivar o retrato anterior se precisar comparar datas.
