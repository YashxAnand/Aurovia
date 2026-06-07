import os
import re

directory = r"d:\Aurovia"

html_files = [
    "index.html",
    "about-us.html",
    "portfolio.html",
    "services.html",
    "blogs.html",
    "get-in-touch.html",
    "404.html"
]

def update_links(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace specific file links with root relative paths without .html
    content = content.replace('href="index.html"', 'href="/"')
    content = content.replace('href="about-us.html"', 'href="/about-us"')
    content = content.replace('href="portfolio.html"', 'href="/portfolio"')
    content = content.replace('href="services.html"', 'href="/services"')
    content = content.replace('href="blogs.html"', 'href="/blogs"')
    content = content.replace('href="get-in-touch.html"', 'href="/get-in-touch"')
    
    # Also replace any other hrefs that might match exactly
    # But be careful with admin/login.html if they exist
    # If the file has href="admin/login.html", we might want it to be href="/admin/login"
    content = content.replace('href="admin/login.html"', 'href="/admin/login"')
    content = content.replace('href="login.html"', 'href="/login"')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith('.html'):
            update_links(os.path.join(root, file))

print("Updated HTML links.")
