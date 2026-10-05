# Eleições 2026 — atualização após o primeiro turno

Abra `Eleicoes-2026-Pos-Primeiro-Turno.pbix` no Power BI Desktop. O arquivo contém os dados importados; não é necessário atualizar as fontes para visualizar o relatório.

As seis páginas do relatório anterior foram preservadas, com os dados que já estavam no arquivo original. Esta atualização acrescenta três páginas com o retrato do primeiro turno extraído em 5 de outubro de 2026:

- **Eleitos, QP e segundo turno:** eleitos por quociente partidário e por média, distribuição por partido e cargo, consulta de eleitos e candidatos no segundo turno. Os filtros de UF, cargo e partido modificam os indicadores.
- **Votação do primeiro turno:** votos válidos, nominais e de legenda, cobertura das seções, ranking de candidatos, distribuição por UF e resultados detalhados. Selecione um cargo de cada vez; a visão inicial é Presidente.
- **Participação eleitoral:** comparecimento, abstenção, brancos, nulos e composição dos votos. Usa a eleição presidencial para não contar o mesmo eleitor várias vezes entre os cargos. `ZZ` identifica o exterior.

## Validação

Foram obtidos 137 arquivos JSON oficiais do TSE, sem falhas de download ou de reconciliação dos totais. Nas páginas de votação e participação, a linha BR foi excluída do modelo; o total nacional é a soma das UFs e do exterior, sem duplicação.

O cadastro registra **1.287 eleitos por QP**, **285 por média**, total de **1.572 eleitos proporcionais**, e **14 candidaturas de cargos principais no segundo turno**. No teste do filtro Deputado Distrital, o relatório mostrou 16 por QP e 8 por média.

QP significa **quociente partidário**; QE significa **quociente eleitoral**. “Eleito por QP” é a classificação oficial e não prova, isoladamente, que uma pessoa foi “puxada” por um candidato específico.

Esta versão cobre Brasil, UFs e exterior, conforme o cargo. Não inclui votação por município ou seção. Os dados são um retrato da extração, não uma conexão em tempo real. A versão editável PBIP, os CSVs, as fontes, os fundos e a documentação ficam nesta pasta. Para atualizar as tabelas novas, mantenha os CSVs no caminho configurado `D:\eleicoes-2026-powerbi\pos-primeiro-turno\dados`.

O PBIX original não foi substituído. Esta versão é distribuída neste repositório; a publicação no Power BI Service é independente do envio ao GitHub.
