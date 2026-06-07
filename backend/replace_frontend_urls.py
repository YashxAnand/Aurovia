import os
import re

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to match src="assets/.../filename.ext" or url('assets/.../filename.ext')
    # capturing the filename
    # We will match .jpg, .jpeg, .png (case insensitive)
    
    # Match any path like assets/.../filename.jpg
    # Look for a quote, then assets/
    pattern_path = re.compile(r'(assets/(?:[a-zA-Z0-9_\-/]+)/([a-zA-Z0-9_\-]+\.(?:jpg|jpeg|png)))', re.IGNORECASE)
    
    # We want to replace the whole match with https://media.auroviaweddings.com/filename
    # match.group(1) is the full path, match.group(2) is the filename
    def replace_match(match):
        filename = match.group(2)
        return f"https://media.auroviaweddings.com/{filename}"
        
    content = pattern_path.sub(replace_match, content)

    # Note: SVGs and other formats won't be replaced, just .jpg/.png/.jpeg as requested

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def migrate_codebase():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    templates_dir = os.path.join(base_dir, "backend", "templates")
    admin_dir = os.path.join(base_dir, "admin")
    
    for d in [templates_dir, admin_dir]:
        for root, dirs, files in os.walk(d):
            for file in files:
                if file.endswith(".html") or file.endswith(".css") or file.endswith(".js"):
                    process_file(os.path.join(root, file))
                
    print("Codebase URLs updated.")

if __name__ == "__main__":
    migrate_codebase()
