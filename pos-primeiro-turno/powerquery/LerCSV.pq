// Criar uma consulta em branco chamada LerCSV e colar esta função.
// Exemplo: LerCSV("D:\eleicoes-2026-powerbi\pos-primeiro-turno\dados\resultados_abrangencia.csv")
// IDs permanecem texto. Definir manualmente inteiros e decimais depois de importar.
(Caminho as text) as table =>
let
    Fonte = Csv.Document(File.Contents(Caminho), [Delimiter=";", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Cabecalhos = Table.PromoteHeaders(Fonte, [PromoteAllScalars=true])
in
    Cabecalhos
