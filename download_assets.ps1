$sourceDir = "d:\Aurovia\legacy"
$targetDir = "d:\Aurovia\assets"

if (!(Test-Path -Path $targetDir)) {
    New-Item -ItemType Directory -Path $targetDir | Out-Null
}

$files = Get-ChildItem -Path $sourceDir -Filter *.html
$urls = @()

foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw
    $matches = [regex]::Matches($content, 'https://auroviaproductions.com/([^"''\s\?]+)')
    foreach ($match in $matches) {
        $url = $match.Groups[0].Value
        $path = $match.Groups[1].Value
        
        # Only download asset files
        if ($url -match '\.(png|jpg|jpeg|svg|mp4|css|js|woff|woff2|ttf|eot)$') {
            $urls += [PSCustomObject]@{ Url = $url; Path = $path }
        }
    }
}

$uniqueUrls = $urls | Select-Object -Property Url, Path -Unique

Write-Host "Found $($uniqueUrls.Count) unique assets to download."

foreach ($item in $uniqueUrls) {
    # Fix local path mapping
    $localPath = Join-Path -Path $targetDir -ChildPath $item.Path
    $localDir = Split-Path -Path $localPath -Parent

    if (!(Test-Path -Path $localDir)) {
        New-Item -ItemType Directory -Path $localDir -Force | Out-Null
    }

    if (!(Test-Path -Path $localPath)) {
        try {
            Write-Host "Downloading $($item.Url) to $localPath"
            Invoke-WebRequest -Uri $item.Url -OutFile $localPath -UseBasicParsing
        } catch {
            Write-Host "Failed to download $($item.Url)"
        }
    }
}

Write-Host "Download complete."
