$files = Get-ChildItem -Path . -Filter *.html -File
foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw
    $original = $content
    
    $content = $content.Replace('â€œ', '“')
    $content = $content.Replace('â€”', '—')
    $content = $content.Replace('â€™', '’')
    $content = $content.Replace('â€˜', '‘')
    $content = $content.Replace('â€', '”')
    
    if ($original -ne $content) {
        Set-Content -Path $file.FullName -Value $content -Encoding UTF8
    }
}
