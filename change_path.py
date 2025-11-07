#!/usr/bin/env python3
import os
import re
import shutil

# Root content folder
CONTENT_DIR = "content"
BACKUP_DIR = "content_backup"

# Regex to match src="/workshops/..."
# It handles any figure shortcode line containing src="..."
pattern = re.compile(r'src="(/workshops/(esp-idf-(basic|advanced)/[^\"]+))"')

def replacement(match):
    src_path = match.group(1)
    return f'src="{{{{ "{src_path}" | absURL }}}}"'

def backup_file(file_path):
    backup_path = os.path.join(BACKUP_DIR, os.path.relpath(file_path, CONTENT_DIR))
    os.makedirs(os.path.dirname(backup_path), exist_ok=True)
    shutil.copy2(file_path, backup_path)

def convert_file(file_path):
    print(f"Checking: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content, count = pattern.subn(replacement, content)
    if count > 0:
        backup_file(file_path)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  Updated {count} figure src(s)")

def walk_content():
    for root, _, files in os.walk(CONTENT_DIR):
        for file in files:
            if file.endswith(".md"):
                convert_file(os.path.join(root, file))

if __name__ == "__main__":
    os.makedirs(BACKUP_DIR, exist_ok=True)
    walk_content()
    print("Done! Originals backed up in 'content_backup/'.")
