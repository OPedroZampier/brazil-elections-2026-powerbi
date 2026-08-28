# Eleições 2026 — Power BI

[English](README.md) | **Português (Brasil)**

> **Um dos primeiros projetos publicamente documentados em Power BI a integrar os dados abertos do TSE para as Eleições de 2026 no Brasil.**

Este projeto interativo transforma dados abertos oficiais do Tribunal Superior Eleitoral (TSE) em seis visões analíticas conectadas sobre candidaturas, eleitorado, patrimônio declarado, partidos e financiamento eleitoral.

![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?logo=powerbi&logoColor=black)
![Fonte dos dados](https://img.shields.io/badge/Dados-TSE%20Dados%20Abertos-20c997)
![Status](https://img.shields.io/badge/Status-Em%20desenvolvimento-0b2239)
![Idioma](https://img.shields.io/badge/Dashboard-Português-38bdf8)

## Visão geral

O projeto transforma diferentes bases do TSE em um único modelo analítico, desenvolvido para responder perguntas como:

- Quantas candidaturas estão registradas por cargo e UF?
- Qual é o perfil demográfico do eleitorado e das candidaturas?
- Como as candidaturas se distribuem por gênero, raça/cor, escolaridade e ocupação?
- Quanto foi declarado em bens pelas candidaturas?
- Quanto os partidos receberam e gastaram?
- De onde vêm os recursos de campanha e em que são utilizados?

Os dados são provisórios e mudam conforme o TSE processa registros e prestações de contas. Os números exibidos nas capturas representam uma extração específica e podem ser diferentes dos totais oficiais mais recentes.

## Páginas do dashboard

### 1. Panorama Nacional

Principais indicadores da eleição, candidaturas por cargo e situação dos registros.

![Panorama Nacional](assets/screenshots/01-national-overview.png)

### 2. Perfil do Eleitorado

Eleitorado, cobertura biométrica, pessoas com deficiência, uso de nome social e distribuições demográficas por UF e município.

![Perfil do Eleitorado](assets/screenshots/02-electorate-profile.png)

### 3. Perfil das Candidaturas

Composição das candidaturas por gênero, raça/cor e escolaridade, além de idade, ocupação, presença digital e consulta individual.

![Perfil das Candidaturas](assets/screenshots/03-candidate-profile.png)

### 4. Patrimônio e Campanha

Patrimônio declarado, mediana patrimonial, candidaturas com bens, ranking patrimonial e resumo inicial do financiamento de campanha.

![Patrimônio e Campanha](assets/screenshots/04-assets-and-campaign.png)

### 5. Partidos e Recursos

Receitas e despesas partidárias, ranking financeiro, origem dos recursos, destino dos gastos e composição dos recursos eleitorais.

![Partidos e Recursos](assets/screenshots/05-parties-and-resources.png)

### 6. Financiamento Eleitoral

Receitas de campanha, receita média por candidatura, doadores e fornecedores únicos, origem dos recursos e destino das despesas.

![Financiamento Eleitoral](assets/screenshots/06-electoral-financing.png)

## Fontes de dados

Todos os dados eleitorais são provenientes do [Portal de Dados Abertos do TSE](https://dadosabertos.tse.jus.br/), incluindo:

- Candidaturas e informações complementares;
- Bens declarados pelas candidaturas;
- Coligações, federações e vagas disponíveis;
- Redes sociais das candidaturas;
- Perfil e localidade do eleitorado;
- Receitas e despesas anuais dos partidos;
- Receitas de campanha e despesas contratadas e pagas.

Consulte [docs/DATA_SOURCES.md](docs/DATA_SOURCES.md) para conhecer o mapeamento das bases e as observações sobre atualização.

## Fluxo dos dados

```text
Dados Abertos do TSE (ZIP/CSV)
              ↓
Download e extração automatizados
              ↓
Pré-processamento em Python das bases volumosas do eleitorado
              ↓
Limpeza e padronização no Power Query
              ↓
Modelo semântico, relacionamentos e medidas DAX no Power BI
              ↓
Relatório interativo
```

A base do eleitorado foi pré-agregada em arquivos CSV preparados para análise. Isso reduz o tamanho do modelo sem eliminar as dimensões utilizadas no relatório. Identificadores técnicos são empregados nos relacionamentos; campos sensíveis, como CPF e e-mail, não fazem parte do modelo analítico nem deste repositório.

## Principais tecnologias

- Microsoft Power BI Desktop;
- Power Query (M);
- DAX;
- Python e pandas para pré-processamento;
- PowerShell e Python para automação das atualizações;
- Dados abertos do TSE em formato CSV.

## Estrutura do repositório

```text
eleicoes-2026-powerbi/
├── assets/
│   └── screenshots/
├── docs/
│   ├── DATA_SOURCES.md
│   └── METHODOLOGY.md
├── .gitignore
├── LICENSE
├── README.md
└── README.pt-BR.md
```

Os arquivos brutos do TSE e o arquivo `.pbix` não são versionados por causa do tamanho, da frequência de atualização e da organização do repositório. Um link para o relatório público ou uma versão para download poderá ser adicionado após a publicação.

## Observações metodológicas

- Os dados de candidaturas são provisórios e podem mudar após julgamentos, recursos, renúncias e substituições.
- As prestações de contas eleitorais são parciais durante a campanha e se tornam mais completas ao longo do calendário eleitoral.
- A categoria “Não informado” é preservada quando sua remoção pode distorcer a interpretação dos dados demográficos.
- Os valores patrimoniais são declarados pelas próprias candidaturas e não representam patrimônio líquido auditado de forma independente.
- Contas partidárias e contas eleitorais de campanha são conjuntos diferentes e não são tratados como equivalentes.
- Os indicadores monetários são apresentados em reais (BRL).

Mais detalhes estão disponíveis em [docs/METHODOLOGY.md](docs/METHODOLOGY.md).

## Autor

Desenvolvido por **Pedro Zampier** como projeto de portfólio em análise de dados e Power BI.

Fonte dos dados: [Tribunal Superior Eleitoral — Portal de Dados Abertos](https://dadosabertos.tse.jus.br/).

## Licença

A documentação e os materiais originais do projeto estão disponíveis sob a [Licença MIT](LICENSE). Os dados do TSE permanecem sujeitos às condições oficiais e à legislação brasileira aplicável.
