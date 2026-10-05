# Eleições 2026 — atualização após o primeiro turno

## Escopo desta entrega

Adicionar três páginas ao relatório existente, preservando as seis originais. Primeiro preparar fontes, medidas e fundos; depois montar e testar os visuais em uma cópia do Power BI. O PBIX original não deve ser sobrescrito.

O pacote contém um retrato dos resultados oficiais extraídos em 05/10/2026. Brasil, 27 UFs e exterior para Presidente; 27 UFs para os outros cargos principais. Não inclui votação municipal nesta versão. Cadastro de candidaturas: arquivo BRASIL gerado pelo TSE em 05/10/2026. Situações e resultados podem mudar com atualizações e decisões judiciais.

## Página 7 — Eleitos, QP e segundo turno

Perguntas: quantos foram eleitos por quociente partidário? Quantos por média? Como isso varia por partido, UF e cargo? Quem foi para o segundo turno?

- Cards: Eleitos por QP; Eleitos por média; % dos eleitos proporcionais por QP; Candidatos no segundo turno.
- Gráfico principal: barras empilhadas horizontais por partido, separando QP e média. Mostrar os dez maiores e oferecer tabela com todos. Não somar votos para determinar cadeiras.
- Gráfico de apoio: comparação QP/média por cargo proporcional.
- Tabela: nome de urna, partido, UF, cargo e forma de eleição. Filtros de situação permitem consultar QP, média e segundo turno.
- Filtros: UF, cargo e partido. Card de segundo turno respeita os mesmos filtros e pode ser zero em cargo proporcional.
- Tooltip: explicar QP e QE e informar a data da fonte.
- O QE oficial por UF e cargo está em `dados/quociente_eleitoral_por_uf.csv` e pode aparecer no tooltip após relacionamento por UF + cargo. Não confundir o valor do QE com a quantidade de eleitos por QP.

QP significa quociente partidário. QE significa quociente eleitoral. A classificação `ELEITO POR QP` não prova que alguém foi individualmente “puxado” por um candidato específico. O relatório deve usar a expressão oficial. Para uma análise de puxadores de votos seria necessário estudar votação, federação, distribuição de vagas e regras aplicáveis; essa inferência não entra neste retrato.

Medidas baseadas em candidatos únicos, primeiro turno, cargos principais. Excluir vice-presidente, vice-governador e suplentes de senador. Denominador do percentual por QP: eleitos por QP + eleitos por média nos cargos 6, 7 e 8. Não incluir senador, governador ou presidente.

## Página 8 — Votação do primeiro turno

Perguntas: quem recebeu mais votos no cargo selecionado? Qual a distribuição por UF? Quão avançada está a totalização?

- Cards: Votos válidos; Votos nominais; Votos de legenda; % de seções totalizadas.
- Gráfico principal: ranking de candidatos por votos, dez maiores. Para Presidente, mostrar todos quando couberem.
- Gráfico de apoio: distribuição de votos por UF do candidato selecionado. Mapa só após validar nomes e geocodificação; barras por UF são a opção sem dependência externa.
- Tabela: nome, partido, UF, votos, percentual oficial e resultado.
- Filtros: UF e cargo; seleção única de cargo obrigatória. Partido filtra candidatos, mas não deve reduzir o denominador dos votos válidos do cargo.
- Presidente sem UF: usar BR. Presidente com UF: usar somente a UF. Exterior aparece explicitamente como ZZ, nunca como estado brasileiro.
- Outros cargos sem UF: somar resultados estaduais. Percentuais e ranking são dentro do cargo; deixar claro que a comparação nacional de deputados agrega disputas estaduais diferentes.

Nunca somar a linha BR com as linhas UF e ZZ. Nunca somar votos de cargos diferentes. Senado tem duas vagas em 2026: votos não equivalem ao número de pessoas que compareceram.

## Página 9 — Participação eleitoral

Perguntas: onde a abstenção foi maior? Quanto do voto foi branco ou nulo? A cobertura da apuração permite comparar os estados?

- Cards: Comparecimento; % de abstenção; % de votos brancos; % de votos nulos.
- Gráfico principal: ranking de UFs por taxa de abstenção.
- Gráfico de apoio: barras 100% empilhadas de votos válidos, brancos, nulos e anulados por UF.
- Tabela: UF, eleitorado de seções apuradas, comparecimento, abstenções e cobertura de seções.
- Filtros: UF. Usar somente cargo Presidente, primeiro turno. Sem filtro partido/candidato porque participação não pertence a um candidato.
- Abstenção: ausentes / (comparecimento + ausentes). Brancos e nulos: votos respectivos / total de votos, não / votos válidos. Taxas nacionais devem ser calculadas com numeradores e denominadores nacionais, não pela média das taxas estaduais.

## Layout e legibilidade

Canvas 1280 × 720, igual ao original. Fundo azul-marinho, destaques verde-turquesa e linha dourada discreta. Valores, gráficos e filtros são visuais nativos, não imagens. Os fundos não contêm dados.

| Região | X | Y | Largura | Altura |
| --- | ---: | ---: | ---: | ---: |
| Cabeçalho e título | 32 | 20 | 1216 | 98 |
| Filtro UF | 865 | 38 | 110 | 62 |
| Filtro cargo | 985 | 38 | 120 | 62 |
| Filtro partido | 1115 | 38 | 112 | 62 |
| Card 1 | 40 | 140 | 288 | 110 |
| Card 2 | 344 | 140 | 288 | 110 |
| Card 3 | 648 | 140 | 288 | 110 |
| Card 4 | 952 | 140 | 288 | 110 |
| Gráfico principal | 40 | 270 | 744 | 232 |
| Gráfico de apoio | 800 | 270 | 440 | 232 |
| Tabela | 40 | 520 | 1200 | 142 |
| Fonte e atualização | 40 | 682 | 1200 | 20 |

Os retângulos definem os painéis externos. Reservar 44 px no topo dos painéis para títulos; visuais começam abaixo dessa faixa. Tabelas com cabeçalhos de 12–14 px, dados de 12 px e rolagem. Labels de gráficos de 12 px, valores dos cards de 28–32 px. Títulos longos não podem virar texto cortado. Se a tabela precisar de mais espaço, usar drillthrough para detalhe, sem reduzir fontes. Na página 9 só existe filtro UF.

## Modelo de dados

- `ResultadosAbrangencia`: uma linha por eleição, turno, abrangência e cargo. Chave `chave_resultado`. Votos e comparecimento são medidas, sem soma automática entre cargos/níveis.
- `VotosCandidatos`: uma linha por chave de resultado e SQ_CANDIDATO. Relação muitos-para-um com ResultadosAbrangencia, filtro unidirecional.
- `VotosPartidos`: uma linha por chave de resultado e partido. Manter fora do ranking de candidatos; legenda não pertence a candidato.
- `CandidaturasPerfilResultado`: uma linha por SQ_CANDIDATO do primeiro turno, cargos principais. Serve à página QP e aos perfis; não tem CPF, e-mail nem título eleitoral.
- Usar dimensões compartilhadas de cargo/UF quando forem adicionadas. Não criar relacionamento muitos-para-muitos por nome de candidato. SQ_CANDIDATO deve permanecer texto.
- Evitar relacionamento direto entre as duas tabelas de fatos. Presidente por UF tem múltiplas linhas por candidato na votação, mas uma candidatura no cadastro.

## Fontes

- [Candidatos 2026 — TSE](https://dadosabertos.tse.jus.br/dataset/candidatos-2026)
- [Informações técnicas de divulgação — TSE](https://www.tse.jus.br/eleicoes/informacoes-tecnicas-sobre-a-divulgacao-de-resultados)
- [Resultado unificado EA20 — TSE](https://www.tse.jus.br/eleicoes/eleicoes-2026-content/arquivos/divulgacao-de-resultados/tse-ea20-arquivo-de-resultado-unificado)
- Endpoints e hash SHA-256 de cada JSON constam em `docs/manifesto_qualidade.json`.

## Critérios antes de aprovar o PBIX

1. Nenhuma falha de download nas 137 fontes previstas; registrar todos os horários de geração.
2. Chaves únicas nas abrangências e candidaturas; nenhuma duplicação BR + UF na mesma medida.
3. Comparecimento + abstenções = eleitores das seções apuradas.
4. Total de votos = válidos + brancos + nulos totais + anulados + anulados sub judice.
5. Válidos = nominais + legenda.
6. Contagens QP/média conferidas no cadastro principal; denominador proporcional confirmado.
7. Testar Presidente nacional, uma UF, deputado federal, deputado distrital no DF, senador e seleção sem dados.
8. Conferir interação partido/candidato: não mudar indevidamente os denominadores do cargo.
9. Valores sem dados devem aparecer como indisponíveis, não zeros inventados.
10. Abrir a cópia do PBIX, atualizar e revisar as nove páginas. Fundos prontos e CSVs validados não significam que a montagem do PBIX já terminou.
