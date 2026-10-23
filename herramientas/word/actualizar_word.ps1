# Abre un .docx con Word, actualiza los campos (indices y numeros de pagina), lo guarda y,
# si se pasa una segunda ruta, lo exporta a PDF para revisarlo.
# Uso: powershell -File actualizar_word.ps1 "ruta.docx" ["control.pdf"]
param([string]$docx, [string]$pdf = "")
$w = New-Object -ComObject Word.Application
$w.Visible = $false
$w.DisplayAlerts = 0
$d = $w.Documents.Open($docx, $false, $false)
$d.Fields.Update() | Out-Null
foreach ($t in $d.TablesOfContents) { $t.Update() }
$d.Repaginate()
foreach ($t in $d.TablesOfContents) { $t.UpdatePageNumbers() }
"indices: " + $d.TablesOfContents.Count + " | paginas: " + $d.ComputeStatistics(2)
$d.Save()
if ($pdf) { $d.SaveAs([ref]$pdf, [ref]17) }
$d.Close([ref]0)
$w.Quit()
