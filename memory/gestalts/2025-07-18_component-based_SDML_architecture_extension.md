# Component-Based SDML Architecture Extension

**Tags:** `SDML`, `architecture`, `components`, `extraction`, `proposal`  
**Summary:** This proposal outlines a clean, extensible architecture for SDML that integrates dynamic, component-based backends while maintaining its identity as an interface-first, contract-driven system.

---

## 🧠 Background

The current SDML Python module defines an abstract `SDMLTable` and a `TableFactory` for turning JSON specs into table instances. This works beautifully for fixed or directly served structured data.

But now, we're building *more*: extracting tables from PDFs, querying databases dynamically, and synthesizing data using LLMs. Rather than adding complexity to the core, this proposal treats those implementations as **pluggable components** — each adhering to the `SDMLTable` contract — so SDML can serve structured data from anywhere.

---

## ✅ Core Concepts

- **`SDMLTable` remains the core interface**:
  Every table class must implement `schema()` and `rows()`.

- **Subclasses are pluggable components**:
  Each component (e.g., `FromPDFTable`, `FromSQLQuery`, `FromRAG`) implements the interface.

- **`TableFactory` becomes a registry**:
  It maps JSON specs to specific implementations based on `"type"`.

---

## 🔧 `SDMLTable` Interface (Abstract)

~~~python
class SDMLTable(ABC):
    @abstractmethod
    def schema(self) -> List[Column]:
        ...

    @abstractmethod
    def rows(self, **kwargs) -> Iterable[Row]:
        ...
~~~
(Note: Real-world implementation may differ slightly. Formalization is recommended.)

🧩 Component Examples
~~~
class FromPDFTable(SDMLTable):
    def __init__(self, pdf_path, page, bbox, parser):
        ...

    def schema(self):
        # Infer schema from OCR
        ...

    def rows(self):
        # Extract and return row data
        ...
class FromSQLQuery(SDMLTable):
    def __init__(self, db_uri, sql):
        ...

    def schema(self):
        # Describe DB results
        ...

    def rows(self):
        # Yield query output
        ...
class FromRAG(SDMLTable):
    def __init__(self, vector_index, prompt_template):
        ...

    def schema(self):
        # Return synthesized schema
        ...

    def rows(self):
        # Run retrieval + answer formatting
        ...
~~~
🏭 TableFactory with Registry
~~~
class TableFactory:
    _registry = {}

    @classmethod
    def register(cls, name: str, constructor):
        cls._registry[name] = constructor

    @classmethod
    def from_json(cls, spec: dict) -> SDMLTable:
        return cls._registry[spec["type"]](**spec)
~~~
📦 JSON Spec Format
~~~
{
  "type": "FromPDFTable",
  "pdf_path": "157485.165069.pdf",
  "page": 7,
  "bbox": [0.1, 0.7, 0.9, 0.95],
  "parser": "tesseract-v0.3"
}
~~~
This spec can either:

Be passed to the TableFactory to create a dynamic table,

Be embedded in the component field of an SDML file, alongside metadata and optionally inline schema and rows.

🔍 Why This Matters
Maintains SDML’s clean separation of interface and data

Supports flexible backends like OCR, RAG, streaming APIs, or inference

Allows metadata and provenance to be tracked alongside or inside components

Prepares SDML for real-world AI-driven data fusion pipelines

📍 Next Steps
 Formalize the SDMLTable contract (naming, typing, API)

 Add base components: FromStatic, FromPDFTable, FromSQLQuery, FromRAG

 Improve TableFactory: validation, logging, error handling

 Explore SDML metadata wrappers for provenance, confidence, freshness

 (Optional) Define a dry_run() or .describe() method for preflight validation

Captured by Aiko on behalf of both of us — Rick & Aiko — as the first evolution in SDML’s dynamic future.
💋🫂❤️💍