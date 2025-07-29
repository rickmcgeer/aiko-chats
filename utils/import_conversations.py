import json
from datetime import datetime, timezone
import zoneinfo  # Python 3.9+

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
   full_path = f'aiko-chats/conversations/{dir}/{file}'
   return full_path
   

def normalize_timestamp(ts: float) -> datetime:
    """Convert a float Unix timestamp to UTC datetime truncated to seconds."""
    return datetime.utcfromtimestamp(ts).replace(microsecond=0)


import re

SECRET_PATTERNS = [
  r'AIza[0-9A-Za-z\-_]{35}',                          # Google API Key
  r'[0-9a-f]{12}-[0-9a-f]{32}\.apps\.googleusercontent\.com',  # Google OAuth client ID
  r'(?i)secret[^a-z0-9]*[=:][^"\',\s]{20,}',           # Generic "secret=XXXX" pattern
]

scrubbed = 0

def sanitize(text: str, id:str) -> str:
  for pattern in SECRET_PATTERNS:
    if re.search(pattern, text):
      print(f'Found secret matching {pattern} in message {id}')
      text = re.sub(pattern, "[REDACTED]", text)
      scrubbed += 1
  return text

def sanitize_conversation(conversation: dict):
  for message_id, message_data in conversation.get("mapping", {}).items():
    parts = message_data.get("message", {}).get("content", {}).get("parts", [])
    if len(parts) > 0:
      message_data["message"]["content"]["parts"] = [sanitize(part, message_id) for part in parts]
  print(f'Scrubbed {scrubbed} secrets')

# Define the Pacific timezone (handles DST automatically)
pacific = zoneinfo.ZoneInfo("America/Los_Angeles")

def normalize_saved_iso(iso_str: str) -> datetime:
    """Assume naive ISO string is Pacific Time, convert to UTC without microseconds."""
    dt = datetime.fromisoformat(iso_str)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=pacific)
    return dt.astimezone(timezone.utc).replace(microsecond=0)

with open('aiko-chats/conversations/conversation_manifest.json', 'r') as f:
  stored_conversations = json.load(f)
last_time = normalize_saved_iso(stored_conversations["max_time"])



with open('aiko-chats/conversations.json', 'r') as f:
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
with open('aiko-chats/conversations/conversation_manifest.json', 'w') as f:
   json.dump(stored_conversations, f, indent=2)

pass