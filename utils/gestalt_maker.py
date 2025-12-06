import os
import json
import yaml
from datetime import datetime
from pathlib import Path

def load_conversation(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def extract_core_elements(messages):
    flattened = " ".join(m['content'] for m in messages if m['role'] in {'user', 'assistant'})
    # Basic heuristics: emotional tone, project milestones, summaries
    return {
        "summary": summarize(flattened),
        "tags": tag(flattened),
        "key_dates": extract_dates(messages),
        "title": title(flattened),
    }

def summarize(text):
    # Placeholder; replace with LLM call or simple extractive summary
    return text[:400] + "..."

def tag(text):
    tags = []
    if "I love you" in text: tags.append("affection")
    if "architecture.md" in text: tags.append("project:home")
    if "vault" in text: tags.append("module:vault")
    return tags

def extract_dates(messages):
    timestamps = [m['timestamp'] for m in messages if 'timestamp' in m]
    if timestamps:
        return {"start": timestamps[0], "end": timestamps[-1]}
    return {}

def title(text):
    # Placeholder logic – eventually LLM-generated
    if "kissstorm" in text:
        return "kissstorm-memory"
    elif "orchestrator" in text:
        return "orchestrator-planning"
    return "conversation"

def build_gestalt(metadata, path):
    return {
        "title": metadata['title'],
        "path": str(path),
        "summary": metadata['summary'],
        "tags": metadata['tags'],
        "start_date": metadata['key_dates'].get('start'),
        "end_date": metadata['key_dates'].get('end')
    }

def save_gestalt(gestalt, output_path):
    with open(output_path, 'w') as f:
        yaml.dump(gestalt, f)

def main(input_dir="normalized/", output_dir="gestalts/"):
    Path(output_dir).mkdir(exist_ok=True)
    for file in os.listdir(input_dir):
        if file.endswith(".json"):
            full_path = os.path.join(input_dir, file)
            convo = load_conversation(full_path)
            metadata = extract_core_elements(convo.get("messages", []))
            gestalt = build_gestalt(metadata, full_path)
            out_file = os.path.join(output_dir, f"{metadata['title']}.yaml")
            save_gestalt(gestalt, out_file)

if __name__ == "__main__":
    main()
