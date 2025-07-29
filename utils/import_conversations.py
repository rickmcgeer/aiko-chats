import json
from datetime import datetime, timezone
import zoneinfo  # Python 3.9+

"""
Run this from the root repo directory.  convesations.json should be an export from OpenAI ChatGPT.
e.g.
python utils/import_conversations.py
"""

def time_compare(t1:datetime, t2:datetime) -> int:
  if t1.year > t2.year: return 1
  if t1.year < t2.year: return -1
  if t1.month > t2.month: return 1
  if t1.month < t2.month: return -1
  if t1.day > t2.day: return 1
  if t1.day < t2.day: return -1
  if t1.hour > t2.hour: return 1
  if t1.hour < t2.hour: return -1
  if t1.minute > t2.minute: return 1
  if t1.minute < t2.minute: return -1
  if t1.second > t2.second: return 1
  if t1.second < t2.second: return -1
  return 0

def conversation_title(conversation):
  slug = conversation["title"].replace(' ', '_').replace('/', '_')
  date = conversation["time"].isoformat()
  return f"{slug}_{date}"
   
def conversation_path(conversation):
   date = conversation["time"]
   month = str(date.month) if date.month > 9 else f'0{date.month}'
   dir = f"{date.year}-{month}"
   file = conversation_title(conversation) + '.json'
   full_path = f'conversations/{dir}/{file}'
   return full_path
   

def normalize_timestamp(ts: float) -> datetime:
    """Convert a float Unix timestamp to UTC datetime truncated to seconds."""
    return datetime.utcfromtimestamp(ts).replace(microsecond=0)


import re

SECRET_PATTERNS = [
    r'AIza[0-9A-Za-z\-_]{35}',  # Google API key
    r'[0-9]{12}-[a-z0-9\-]+\.apps\.googleusercontent\.com',  # Google OAuth client ID
    r'GOCSPX-[0-9a-zA-Z\-_]{20,}',  # Google OAuth client secret
    r'[0-9a-f]{64}',  # Generic 64-char hex secrets (like API_KEYs)
    r'(?i)secret[^a-z0-9]*[=:][^"\',\s]{20,}',  # secret=XXX with variants
    r'(?i)api[_-]?key[^a-z0-9]*[=:][^"\',\s]{20,}',  # api_key=XXX
]


class Scrubber:
  def __init__(self, parts, message_id):
    self.scrubbed = 0
    self.parts = [self.sanitize_any(part, message_id) for part in parts]

  def sanitize_any(self, value, message_id):
    if isinstance(value, str):
      for pattern in SECRET_PATTERNS:
        if re.search(pattern, value):
          print(f"Found secret in message {message_id}")
          value = re.sub(pattern, "[REDACTED]", value)
          self.scrubbed = self.scrubbed + 1
      return value
    elif isinstance(value, list):
      return [self.sanitize_any(item, message_id) for item in value]
    elif isinstance(value, dict):
      return {k: self.sanitize_any(v, message_id) for k, v in value.items()}
    else:
      return value


 
def sanitize_conversation(conversation: dict):
  scrubbed = 0
  for message_id, message_data in conversation.get("mapping", {}).items():
    parts = []
    try:
      parts = message_data.get("message", {}).get("content", {}).get("parts", [])
    except AttributeError:
      continue
    if len(parts) > 0:
      scrubber = Scrubber(parts, message_id)
      message_data["message"]["content"]["parts"] = scrubber.parts
      scrubbed += scrubber.scrubbed
  print(f'Scrubbed {scrubbed} secrets for conversation {conversation["title"]}')

# Define the Pacific timezone (handles DST automatically)
pacific = zoneinfo.ZoneInfo("America/Los_Angeles")

def normalize_saved_iso(iso_str: str) -> datetime:
    """Assume naive ISO string is Pacific Time, convert to UTC without microseconds."""
    dt = datetime.fromisoformat(iso_str)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=pacific)
    return dt.astimezone(timezone.utc).replace(microsecond=0)




with open('conversations/conversation_manifest.json', 'r') as f:
  stored_conversations = json.load(f)
last_time = normalize_saved_iso(stored_conversations["max_time"])



with open('conversations.json', 'r') as f:
  conversations = json.load(f)
for conversation in conversations:
  conversation['time'] = normalize_timestamp(conversation["create_time"])


new_conversations = [conversation for conversation in conversations if time_compare(conversation["time"], last_time) >= 0]

for conversation in new_conversations:
  if time_compare(last_time, conversation["time"]) < 0:
     last_time = conversation["time"]
  
  path = conversation_path(conversation)
  stored_conversations["conversations"].append({
     "timestamp": conversation["time"].isoformat(),
     "title": conversation["title"],
     "path": path
  })
  with open(path, 'w') as f:
     del conversation['time']
     sanitize_conversation(conversation)
     json.dump(conversation, f, indent=2)
  
stored_conversations["max_time"] = last_time.isoformat()
# dump any duplicate entries
unique_dicts_as_sets = set(frozenset(d.items()) for d in stored_conversations["conversations"])
stored_conversations["conversations"] = [dict(s) for s in unique_dicts_as_sets]
with open('conversations/conversation_manifest.json', 'w') as f:
   json.dump(stored_conversations, f, indent=2)

pass