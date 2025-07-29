import os
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

"""
Run this from the parent directory of conversations and normalized_conversations
"""

CONVERSATIONS_ROOT = Path("conversations")
NORMALIZED_ROOT = Path("normalized_conversations")
NORMALIZED_ROOT.mkdir(parents=True, exist_ok=True)

def is_message(value):
    if not isinstance(value, dict):
        return False
    message = value.get("message")
    if not isinstance(message, dict):
        return False
    author = message.get("author")
    content = message.get("content")
    if not (isinstance(author, dict) and "role" in author):
        return False
    if not (isinstance(content, dict) and isinstance(content.get("parts"), list) and content["parts"]):
        return False
    return True

def normalize_role(input_role: str) -> str:
    ROLE_MAP = {
        "user": "User",
        "assistant": "AI Partner",
        "system": "System"
    }
    if input_role is None:
        return input_role
    return ROLE_MAP.get(input_role, input_role)

def format_timestamp(ts: float) -> str:
    try:
        return datetime.utcfromtimestamp(ts).isoformat() + "Z"
    except Exception:
        return ""

def convert_conversation_to_messages(conversation: Dict[str, Any]) -> List[Dict[str, Any]]:
    mapping = conversation.get("mapping", {})
    title = conversation.get("title", "")
    nodes = [
        node for node in mapping.values()
        if isinstance(node, dict) and is_message(node)
    ]
    nodes.sort(key=lambda node: node["message"].get("create_time") or 0)

    messages = []
    for node in nodes:
        message = node["message"]
        content_parts = message["content"].get("parts", [])
        create_time = message.get("create_time", 0.0)
        role = normalize_role(message["author"]["role"])

        # Build flattened with intelligent treatment of non-strings
        stringified_parts = []
        processed_parts = []
        for part in content_parts:
            if isinstance(part, str):
                stringified_parts.append(part)
                processed_parts.append(part)

            elif isinstance(part, dict) and part.get("content_type") == "image_asset_pointer":
                width = part.get("width", "?")
                height = part.get("height", "?")
                size = part.get("size_bytes", 0)
                size_kb = f"{round(size / 1024)} KB" if size else "?"
                processed_parts.append(f"[Image: {width}×{height}, {size_kb}]")
            else:
                processed_parts.append("[Unsupported content]")  # fallback

        result = {
            "role": role,
            "parts": processed_parts,
            "flattened": "\n".join(stringified_parts).strip(),
            "id": message["id"],
            "create_time": create_time,
            "timestamp": format_timestamp(create_time)
        }

        messages.append(result)

        # Log any unexpected non-string parts
        if len(stringified_parts) < len(content_parts):
            print(f"⚠️  Non-string part found in message {message['id']}, conversation {title}")

    return messages


def normalize_all_conversations():
    count = 0
    for subdir in sorted(CONVERSATIONS_ROOT.glob("*/")):
        output_subdir = NORMALIZED_ROOT / subdir.name
        output_subdir.mkdir(parents=True, exist_ok=True)
        for file in subdir.glob("*.json"):
            output_file = output_subdir / file.name
            if output_file.exists():
                continue  # Already processed
            try:
                with open(file, "r", encoding="utf-8") as f:
                    conversation = json.load(f)
                messages = convert_conversation_to_messages(conversation)
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(messages, f, indent=2, ensure_ascii=False)
                print(f"✅ Normalized: {file}")
                count += 1
            except Exception as e:
                print(f"❌ Error processing {file}: {e}")
    print(f"\n✨ Done. {count} new files normalized.")

if __name__ == "__main__":
    normalize_all_conversations()
