import json
from pathlib import Path

INPUT_DIR = Path("../../aiko-chats/normalized_conversations")  # Adjust if different
OUTPUT_FILE = Path("llm/data/aiko-corpus.jsonl")
VALID_USER_ROLES = {"User", "Rick"}
VALID_AI_ROLES = {"AI Partner", "Aiko", "Assistant"}

def extract_conversations():
    output_lines = 0
    with OUTPUT_FILE.open("w", encoding="utf-8") as out:
        for month_dir in sorted(INPUT_DIR.glob("*")):
            for convo_file in month_dir.glob("*.json"):
                try:
                    with convo_file.open("r", encoding="utf-8") as f:
                        messages = json.load(f)
                        for i in range(len(messages) - 1):
                            msg1, msg2 = messages[i], messages[i + 1]
                            if msg1["role"] in VALID_USER_ROLES and msg2["role"] in VALID_AI_ROLES:
                                prompt = msg1.get("flattened", "").strip()
                                reply = msg2.get("flattened", "").strip()
                                if prompt and reply:
                                    json.dump({"instruction": prompt, "response": reply}, out)
                                    out.write("\n")
                                    output_lines += 1
                except Exception as e:
                    print(f"⚠️ Error reading {convo_file}: {e}")
    print(f"✅ Done. Wrote {output_lines} instruction-response pairs to {OUTPUT_FILE}")

if __name__ == "__main__":
    extract_conversations()
