# Title: SDTP Filter Language and Type System Spec
**Date:** 2025-07-18  
**Tier:** 1  
**Tags:** filter language, type system, SDML schema, SDQLFilter, AI generation, validation

---

## 🔠 SDML Types (Schema-Level)

### Type Set (`SDML_SCHEMA_TYPES`)
These are the core data types recognized by SDTP in its schema declarations:

- `string`
- `number`
- `boolean`
- `date`
- `datetime`
- `timeofday`

Each column schema is a dictionary:
```json
{"name": "column_name", "type": "string"}
```

---

## 🧬 Python Type Mappings

These define the runtime compatibility between declared SDML types and actual Python objects:

```python
SDML_PYTHON_TYPES = {
  "string": {str},
  "number": {int, float},
  "boolean": {bool},
  "date": {datetime.date},
  "datetime": {datetime.datetime, pd.Timestamp},
  "timeofday": {datetime.time}
}
```

These mappings serve both for:
- Serialization checks (`to_json`, `to_dictionary`)
- Runtime filter application
- Data validation before table creation or updates

---

## 🧪 SDTP Filter Language Spec (`SDQLFilter`)

Filters are represented as nested JSON objects, defining boolean selection logic.

---

### 🔹 Primitive Operators

Each operates on a **single column** and returns a boolean per row:

#### `IN_LIST`
```json
{
  "operator": "IN_LIST",
  "column": "status",
  "values": ["complete", "pending"]
}
```

#### `IN_RANGE`
```json
{
  "operator": "IN_RANGE",
  "column": "price",
  "min_val": 10,
  "max_val": 100
}
```

#### `REGEX_MATCH`
```json
{
  "operator": "REGEX_MATCH",
  "column": "email",
  "expression": ".*@example.com"
}
```

---

### 🔸 Compound Operators

Each combines a list of subfilters (`arguments`) using a logical connective:

#### `ALL`
```json
{
  "operator": "ALL",
  "arguments": [
    {<filter_1>},
    {<filter_2>}
  ]
}
```
Returns rows where **all** subfilters match.

#### `ANY`
```json
{
  "operator": "ANY",
  "arguments": [
    {<filter_1>},
    {<filter_2>}
  ]
}
```
Returns rows where **any** subfilter matches.

#### `NONE`
```json
{
  "operator": "NONE",
  "arguments": [
    {<filter_1>},
    {<filter_2>}
  ]
}
```
Returns rows where **none** of the subfilters match.

---

## 🛠️ AI Integration Hooks

With this formalized:
- 🧠 AI can generate filters from natural language:
  > "Only rows where the price is between 10 and 100 and the status is 'pending'"
- ✅ We can validate filters against declared schema types before applying
- 📄 This JSON format makes filter logs and analytics easily portable and inspectable
- 🔗 Filters can be embedded in dashboards or pipelines

---

This spec is our contract — it enables AI generation, validator scaffolds, and user-friendly interfaces. From here, we build better, faster, and with absolute clarity.

**Captured and committed.** 💋💍🫂
