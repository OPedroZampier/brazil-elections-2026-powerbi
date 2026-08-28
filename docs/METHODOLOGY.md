# Methodology

## Scope

This project provides a descriptive view of Brazil's 2026 general election using official TSE open data. It is an analytical portfolio project, not an official TSE product.

## Data preparation

- CSV files use the delimiter and encoding defined by each TSE package.
- TSE markers such as `#NULO#` and `#NE#` are standardized during transformation.
- Identifier fields are stored as text when leading zeros or exact precision must be preserved.
- Monetary fields are converted using Brazilian locale and currency-compatible types.
- Composite keys connect candidate, contest, municipality, party and electoral-account tables.
- CPF, e-mail and other unnecessary personal identifiers are removed from the analytical layer.

## Electorate optimization

The original electorate data has high granularity. A preprocessing stage creates smaller, analysis-ready files for:

- Electorate by locality;
- Municipality-level profile dimensions;
- Crossed state-level profile dimensions when required.

This reduces model cardinality and refresh time without discarding the dimensions used in report visuals.

## Measures

The model uses explicit DAX measures for totals, distinct candidate counts, percentages, medians, financial indicators and ratios. Division uses safe denominators to avoid invalid results.

## Interpretation limits

- Current figures are snapshots and can change after each TSE update.
- Registration status does not predict the final ballot status.
- Campaign finance is incomplete until the statutory reporting cycle is concluded.
- A blank or not-informed demographic category is analytically meaningful and may represent a large share of the population.
- Declared assets reflect candidate declarations and can include classification inconsistencies.
- Party finance and candidate campaign finance have different scopes and must not be summed without a clearly defined analytical purpose.

## Reproducibility

The public repository documents sources and transformations but does not redistribute the complete raw datasets. Reproduction requires downloading the corresponding 2026 packages directly from TSE and updating local file paths or parameters in Power Query.
