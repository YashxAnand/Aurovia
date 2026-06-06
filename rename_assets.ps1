$mappings = @{
    "1341761380577_homevideo.mp4" = "home-hero-bg.mp4"
    "7931761397225_about-video.mp4" = "about-hero-bg.mp4"
    "8561761397451_services-video.mp4" = "services-hero-bg.mp4"
    "6881761397343_portfolio-video.mp4" = "portfolio-showcase.mp4"
    "6281761374641_candid-shots.jpg" = "service-weddings.jpg"
    "4851761374611_pre-wedding.jpg" = "service-pre-wedding.jpg"
    "1791761374576_engagements.jpg" = "service-engagements.jpg"
    "9801761374545_creatives1.jpg" = "service-parties-birthdays.jpg"
    "logo-svg-01.svg" = "aurovia-main-logo.svg"
    "f-g-1.jpg" = "footer-logo-primary.jpg"
    "f-g-2.jpg" = "footer-logo-secondary.jpg"
    "about.jpg" = "about-section-showcase.jpg"
    "Raveen_Sommy-0004-1.jpg" = "signature-style-bg.jpg"
    "contact_form.jpg" = "contact-section-bg.jpg"
    "1551761300747_22.jpg" = "portfolio-gallery-1.jpg"
    "1961780709306_DSC09336.jpeg" = "portfolio-gallery-2.jpeg"
    "2691780708870_1-141.jpeg" = "portfolio-gallery-3.jpeg"
    "3691780709373_IMG_8162.jpeg" = "portfolio-gallery-4.jpeg"
    "3711761300746_16.jpg" = "portfolio-gallery-5.jpg"
    "3721780709016_DSC00221.jpeg" = "portfolio-gallery-6.jpeg"
    "3921761300614_10.jpg" = "portfolio-gallery-7.jpg"
    "4351761300747_20.jpg" = "portfolio-gallery-8.jpg"
    "4791761300613_08.jpg" = "portfolio-gallery-9.jpg"
    "4801761300746_11.jpg" = "portfolio-gallery-10.jpg"
    "4941761300746_17.jpg" = "portfolio-gallery-11.jpg"
    "6621761300747_21.jpg" = "portfolio-gallery-12.jpg"
    "6731761300746_14.jpg" = "portfolio-gallery-13.jpg"
    "7111780708820_DSC08834.jpeg" = "portfolio-gallery-14.jpeg"
    "7201761300614_09.jpg" = "portfolio-gallery-15.jpg"
    "7201761300747_18.jpg" = "portfolio-gallery-16.jpg"
    "7591761300746_13.jpg" = "portfolio-gallery-17.jpg"
    "8101761300746_12.jpg" = "portfolio-gallery-18.jpg"
    "8291761300746_15.jpg" = "portfolio-gallery-19.jpg"
    "9421761300747_19.jpg" = "portfolio-gallery-20.jpg"
    "9071780709308_Wedding0357 copy.jpg" = "portfolio-gallery-21.jpg"
}

# 1. Rename files
$assetsDir = "d:\Aurovia\assets"
Get-ChildItem -Path $assetsDir -Recurse -File | ForEach-Object {
    $currentName = $_.Name
    if ($mappings.ContainsKey($currentName)) {
        $newName = $mappings[$currentName]
        Rename-Item -Path $_.FullName -NewName $newName -ErrorAction SilentlyContinue
    }
}

# 2. Update Codebase references
$codeFiles = Get-ChildItem -Path "d:\Aurovia" -Recurse -Include *.html,*.css,*.js -Exclude node_modules
foreach ($file in $codeFiles) {
    $content = Get-Content -Path $file.FullName -Raw
    $modified = $false
    
    foreach ($key in $mappings.Keys) {
        if ($content -match [regex]::Escape($key)) {
            $content = $content -replace [regex]::Escape($key), $mappings[$key]
            $modified = $true
        }
    }
    
    if ($modified) {
        Set-Content -Path $file.FullName -Value $content -Encoding UTF8
    }
}
Write-Host "Renaming complete!"
