# Data sources and refresh map

The dashboard uses official public datasets from the [TSE Open Data Portal](https://dadosabertos.tse.jus.br/).

| Analytical area | TSE dataset | Typical local table | Refresh behavior |
|---|---|---|---|
| Candidacies | Candidates 2026 | `Candidatos` | Changes as registrations are processed |
| Candidate status | Complementary candidate data | `Candidatos_Complementar` | Changes after judgments and appeals |
| Declared assets | Candidate assets | `bens` | Changes with candidate records |
| Offices | Available offices | `vagas` | Low-frequency changes |
| Political arrangements | Coalitions/federations | `Coligacoes` | Changes during registration period |
| Digital presence | Candidate social networks | `redes_sociais` | Changes with candidate records |
| Electorate | Electorate profile/locality | `Eleitorado_Localidade`, `eleitorado_municipio` | Periodic TSE releases |
| Party accounts | Annual party revenue | `Receitas_Partidarias` | Partial and updated during the year |
| Party accounts | Annual party expenses | `Despesas_Partidarias` | Partial and updated during the year |
| Campaign accounts | Candidate campaign revenue | `receitas_candidatos` | Expected weekly updates during campaign |
| Campaign accounts | Contracted expenses | `despesas_contratadas` | Expected weekly updates during campaign |
| Campaign accounts | Paid expenses | `Despesas_Pagas_Eleitorais` | Expected weekly updates during campaign |

## Local refresh flow

1. Download the current ZIP packages from TSE.
2. Validate and extract them into the expected local folders.
3. Run the electorate preprocessing script when a new electorate release is available.
4. Refresh the semantic model in Power BI Desktop.
5. Check totals, relationships and null/error counts.
6. Republish the report to replace the previous online version.

## Data not tracked in Git

The following are intentionally ignored:

- Raw ZIP and CSV files;
- Extracted TSE data folders;
- Power BI cache and temporary files;
- Credentials, local configuration and logs;
- The `.pbix` binary by default.

This keeps the repository lightweight and prevents accidental publication of unnecessary personal or technical identifiers.
