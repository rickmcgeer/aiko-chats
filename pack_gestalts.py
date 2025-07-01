import os
def concatenate_gestalts(memory_dir, output_file):
    """
    Concatenate gestalt_manifest.md + all gestalts in memory/gestalts into one Markdown file.
    """
    gestalt_dir = os.path.join(memory_dir, "gestalts")
    manifest_path = os.path.join(gestalt_dir, "gestalt_manifest.md")

    files = []
    for root, _, filenames in os.walk(gestalt_dir):
        for filename in filenames:
            if filename.endswith('.md') and filename != "gestalt_manifest.md":
                files.append(os.path.join(root, filename))

    files.sort()

    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write("# Aiko Gestalt Archive\n")
        outfile.write("_Concatenated narrative summaries for rehydration._\n\n")

        if os.path.exists(manifest_path):
            outfile.write("## Gestalt Manifest\n\n")
            with open(manifest_path, 'r', encoding='utf-8') as mf:
                outfile.write(mf.read().strip())
                outfile.write("\n\n---\n\n")

        for file in files:
            rel_path = os.path.relpath(file, gestalt_dir)
            outfile.write(f"<!-- {rel_path} -->\n\n")

            with open(file, 'r', encoding='utf-8') as infile:
                content = infile.read().strip()
                outfile.write(content)
                outfile.write("\n\n---\n\n")

    print(f"✅ Gestalt archive created: {output_file}")

if __name__ == "__main__":
    concatenate_gestalts(
        memory_dir="./memory",
        output_file="./memory/aiko-gestalts.md"
    )
