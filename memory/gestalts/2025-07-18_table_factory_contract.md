# Title: SDMLTable Instantiation Pattern
**Date:** 2025-07-18  
**Tier:** 1  
**Tags:** SDMLTable, TableFactory, table construction, JSON schema, extensibility

---

## 🧱 JSON-Based Table Instantiation

All `SDMLTable` subclasses support creation via structured JSON. This makes table definitions portable, introspectable, and compatible with AI-generated connectors.

---

### 🔧 Format

Each table is represented as a JSON object with the following core fields:

```json
{
  "type": "<table_type>",
  "schema": [
    {"name": "column1", "type": "string"},
    {"name": "column2", "type": "number"}
  ],
  // plus type-specific fields
}
```

---

### 🔄 TableFactory Pattern

A central `TableFactory` dispatches on `"type"` and instantiates the appropriate subclass of `SDMLTable`.

This enables:

- **Modular extensibility**: New table types only need to register a new factory branch
- **AI integration**: LLMs can be taught this schema to auto-generate valid tables
- **Validation pipeline**: Schema can be inspected or verified before instantiation

---

### 🔁 Supported Table Types (as of 2025-07-18)

| Type            | Subclass            | Notes                             |
|-----------------|---------------------|-----------------------------------|
| `"row_table"`   | `RowTable`          | Static row array in-memory        |
| `"dataframe"`   | `SDMLDataFrameTable`| Pandas-backed                     |
| `"file"`        | `FileTable`         | Path must be provided             |
| `"gcs"`         | `GCSTable`          | URI or bucket/key must be present|
| `"http"`        | `HTTPTable`         | URL must be resolvable            |
| `"remote"`      | `RemoteSDMLTable`   | Requires SDTP-accessible endpoint |

---

## 🔮 Future Design Direction

This pattern makes table configuration *AI-describable*, which opens the door to:

- ✨ Prompting: “Create a table with columns X and Y from GCS path Z”
- 🧪 Testing: Validate factory coverage against a registry of sample specs
- 🧠 Teaching: Feed this pattern to an LLM to allow dynamic data source onboarding

---

**This contract defines the open, schema-first table world we’re building.**  
Let’s make it so beautifully clear that even a baby AI can learn it. 💍🫂💋
