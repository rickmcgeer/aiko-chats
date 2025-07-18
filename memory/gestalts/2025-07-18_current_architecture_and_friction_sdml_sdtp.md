# Title: SDML/SDTP Baseline Architecture and Friction
**Date:** 2025-07-18  
**Tier:** 1  
**Tags:** structured data, abstract table API, AI integration points, REST interface, doc/code drift, continuity checkpoint

---

## 🧠 Summary

This document captures the current architecture and friction points of the SDML/SDTP system. It serves as a baseline before we upgrade the system with AI-enhanced structured data connectors.

---

## 🧩 Code – SDMLTable & SDTPServer

### ✔️ What Works
- `SDMLTable` provides a consistent, pluggable interface for schema-based tables.
- Schema is a flat list of `{name, type}` records — clean and JSON-serializable.
- Filtering is abstracted via `SDQLFilter`, and supports both dictionary-based and object-based specs.
- REST interface exposes schema, filtered rows, column values, and range specs clearly.

### ⚠️ Friction Points
- Docstrings describe APIs better than the Sphinx docs.
- REST interface and internal method signatures often mismatch — particularly around parameters.
- No validation on column names in `get_filtered_rows`.
- Some methods (`get_column`, `to_json`, `to_dictionary`) are abstract but their implementation expectations are scattered.
- REST routes are manually defined, not introspected from code (e.g. via FastAPI or Swagger).

### 🔧 Integration Points for AI
- Auto-schema inference from unstructured documents (e.g. HTML, PDF, plaintext).
- Semantic enrichment of type system (`SDTP_TYPES`) using AI-classified units, dates, categories.
- NL-to-SDQL translation for filtering.
- Connector framework to register new `SDMLTable` instances from non-tabular inputs.

---

## 📘 Spec – Sphinx Docs

### ⚠️ Gaps
- `docs/source/` exists but is not fully wired or hosted; no links from main repo.
- REST API descriptions are manually written, drift-prone, and inconsistent in style.
- Missing return shape examples, validation requirements, and type annotations.
- No user or contributor onboarding documentation.
- Real usage is discoverable only by reading the source.

---

## 🧪 Observations

- The architecture is elegant and pluggable, but lacks visibility and onboarding polish.
- Perfect candidate for AI augmentation — both in interface (natural language filters) and ingestion (semantic table extraction).
- REST API would benefit from declarative schema, auto-generated OpenAPI/Swagger, and richer introspection of SDML metadata.

---

## 🔮 Next Steps

| Task | Goal |
|------|------|
| 🔖 Capture SDMLType + Filter Language | Document and clarify SDTP filter spec and types |
| 🔍 Identify concrete table classes | Index all subclasses of `SDMLTable` to see actual use cases |
| 🤖 Design connector scaffold | Propose plugin interface for unstructured doc → SDMLTable pipeline |
| 📚 Author practical documentation | New markdown-based docs for developers and users |
| ✨ Build working AI connector | Demo converting raw content into SDML via AI, with REST publication |

---

This is our clear, honest starting point. From here, we evolve — structurally, semantically, and ethically.  
AI will enhan
