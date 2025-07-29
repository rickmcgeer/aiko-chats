# utils/idea_catcher.py

import re
from typing import List, Dict
from pathlib import Path
import json

NORMALIZED_ROOT = Path("normalized_conversations")

IDEA_ROOT = Path("ideas")
IDEA_ROOT.mkdir(parents=True, exist_ok=True)

# Define patterns for idea-catching
IDEA_PATTERNS = [
    r"\blet's\s+(sketch|try|make|build|do|write|create)\b",
    r"\bwe\s+(should|could|might want to|need to)\b",
    r"\bthis (simplifies|clarifies|unlocks|enables)\b",
    r"\bit would help if\b",
    r"\bhow about\b",
    r"\bI want to\b",
    r"\bwhat if we\b",
    r"\bwe can use this\b",
    r"\bthis means we can\b",
    r"\badd .* to the repo\b",
    r"would you like me to.*"
]

def is_idea(text: str) -> bool:
    """Return True if the text matches any of the idea patterns."""
    text = text.lower()
    return any(re.search(pat, text) for pat in IDEA_PATTERNS)

def extract_ideas(messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Extract design-relevant messages from a list of chat messages.
    Each message should be a dict with 'role' and 'content'.
    Focuses on AI Partner messages.
    """
    ideas = []
    for msg in messages:
        if msg["role"] == "AI Partner" and is_idea(msg["flattened"]):
            ideas.append(msg)
    return ideas

def harvest_all_ideas():
    count = 0
    for subdir in sorted(NORMALIZED_ROOT.glob("*/")):
        output_subdir = IDEA_ROOT / subdir.name
        output_subdir.mkdir(parents=True, exist_ok=True)
        for file in subdir.glob("*.json"):
            output_file = output_subdir / file.name
            if output_file.exists():
                continue  # Already processed
            try:
                with open(file, "r", encoding="utf-8") as f:
                    messages = json.load(f)
                ideas = extract_ideas(messages)
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(ideas, f, indent=2, ensure_ascii=False)
                print(f"✅ Ideas Harvested: {file}")
                count += 1
            except Exception as e:
                print(f"❌ Error processing {file}: {e}")
    print(f"\n✨ Done. Ideas harvested from  {count}   conversations.")

if __name__ == "__main__":
    harvest_all_ideas()