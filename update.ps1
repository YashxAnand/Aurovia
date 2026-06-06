$files = Get-ChildItem -Path . -Include *.html, *.js -Recurse
foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw
    $original = $content
    
    # Phone number replacement
    $content = $content -replace '7986288550', '9838358799'
    
    # Increase photo size
    $content = $content -replace 'max-width: 220px; height: 220px;', 'max-width: 300px; height: 300px;'
    
    # Reduce horizontal whitespaces
    $content = $content -replace 'gap: 2rem; align-items: center;', 'gap: 1rem; align-items: center;'
    
    if ($original -ne $content) {
        Set-Content -Path $file.FullName -Value $content -Encoding UTF8
    }
}
