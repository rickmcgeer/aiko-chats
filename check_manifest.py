import os
import json
import re

# CONFIG
GESTALTS_DIR = "gestalts"
MANIFEST_FILE = "manifest.json"

def load_manifest():
    with open(MANIFEST_FILE, 'r') as f:
        return json.load(f)

def extract_title_from_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith("# "):
                return line.strip("# ").strip()
    return None

def check_gestalt(file_entry, manifest_entry):
    errors = []

    filename = os.path.basename(file_entry)
    slug_from_filename = filename.replace(".md", "")
    title_from_file = extract_title_from_file(file_entry)

    # Slug match
    if manifest_entry['name'] != slug_from_filename:
        errors.append(f"Slug mismatch: {manifest_entry['name']} vs {slug_from_filename}")

    # Title match
    if manifest_entry['title'] != title_from_file:
        errors.append(f"Title mismatch: {manifest_entry['title']} vs {title_from_file}")

    # Path match
    if manifest_entry['path'] != file_entry:
        errors.append(f"Path mismatch: {manifest_entry['path']} vs {file_entry}")

    # Date match
    date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}')
    match = date_pattern.match(slug_from_filename)
    if match and manifest_entry['date'] != match.group(0):
        errors.append(f"Date mismatch: {manifest_entry['date']} vs {match.group(0)}")

    return errors

def main():
    manifest = load_manifest()

    print(f"Checking {len(manifest)} manifest entries...\n")

    for entry in manifest:
        path = entry['path']
        if not os.path.exists(path):
            print(f"Missing file: {path}")
            continue

        errors = check_gestalt(path, entry)
        if errors:
            print(f"Issues for {path}:")
            for e in errors:
                print(f"  - {e}")
        else:
            print(f"{path}: OK")

if __name__ == "__main__":
    main()
