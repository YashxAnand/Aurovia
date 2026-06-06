$files = Get-ChildItem -Path "d:\Aurovia" -Filter *.html
foreach ($file in $files) {
    $content = Get-Content -Path $file.FullName -Raw

    # Update css link
    $content = $content -replace 'href="css/style\.css"', 'href="css/style.min.css"'

    # Add loading="lazy" to imgs that lack it
    $content = [regex]::Replace($content, '(?i)<img(?![^>]*loading=)([^>]+)>', '<img loading="lazy"$1>')

    # Add preload for index.html
    if ($file.Name -eq 'index.html' -and -not $content.Contains('<link rel="preload" as="video"')) {
        $content = $content -replace '</head>', "    <link rel=`"preload`" as=`"video`" href=`"assets/uploads/home-page/1341761380577_homevideo.mp4`" type=`"video/mp4`">`n</head>"
    }
    
    # Add preload for about-us.html
    if ($file.Name -eq 'about-us.html' -and -not $content.Contains('<link rel="preload" as="video"')) {
        $content = $content -replace '</head>', "    <link rel=`"preload`" as=`"video`" href=`"assets/uploads/about-page/7931761397225_about-video.mp4`" type=`"video/mp4`">`n</head>"
    }
    
    # Add preload for services.html
    if ($file.Name -eq 'services.html' -and -not $content.Contains('<link rel="preload" as="video"')) {
        $content = $content -replace '</head>', "    <link rel=`"preload`" as=`"video`" href=`"assets/uploads/service-video/8561761397451_services-video.mp4`" type=`"video/mp4`">`n</head>"
    }

    Set-Content -Path $file.FullName -Value $content -Encoding UTF8
}
