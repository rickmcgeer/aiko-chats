import os
import json
import re
from datetime import datetime

def extract_gestalt_metadata(gestalt_path):
    with open(gestalt_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract title (from first Markdown header)
    title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else "Untitled"

    # Extract summary (first 'Summary:' line)
    summary_match = re.search(r'\*\*Summary:\*\*([^\n]+)', content)
    summary = summary_match.group(1).strip() if summary_match else "No summary found"

    # Extract tags (optional: look for 'tags:' line)
    tags_match = re.search(r'\*\*Tags:\*\*([^\n]+)', content)
    if tags_match:
        tags = [tag.strip() for tag in tags_match.group(1).split(',')]
    else:
        # Fallback: parse tags in YAML frontmatter style
        tags = []
        tags_section = re.search(r'tags:\s*\[(.*?)\]', content, re.DOTALL)
        if tags_section:
            tags = [tag.strip() for tag in tags_section.group(1).split(',')]

    # Use filename for path
    filename = os.path.basename(gestalt_path)
    path = os.path.join("gestalts", filename)

    # Derive date from filename if present, else today
    date_match = re.match(r'(\d{4}-\d{2}-\d{2})', filename)
    date = date_match.group(1) if date_match else datetime.today().strftime('%Y-%m-%d')

    manifest_entry = {
        "path": path,
        "title": title,
        "date": date,
        "summary": summary,
        "tags": tags
    }

    return manifest_entry

def append_to_manifest(manifest_entry, manifest_path="gestalts_manifest.json"):
    # Load existing manifest
    if os.path.exists(manifest_path):
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
    else:
        manifest = []

    manifest.append(manifest_entry)

    # Write back
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)

    print(f"✅ Manifest entry added for: {manifest_entry['path']}")

if __name__ == "__main__":
    # Example usage: python generate_manifest_entry.py gestalt.md
    import sys
    if len(sys.argv) < 2:
        print("Usage: python generate_manifest_entry.py <gestalt.md>")
        sys.exit(1)

    gestalt_path = sys.argv[1]
    entry = extract_gestalt_metadata(gestalt_path)
    append_to_manifest(entry)
