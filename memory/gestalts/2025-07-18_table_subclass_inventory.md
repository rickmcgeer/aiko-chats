# Title: SDMLTable Subclass Inventory
**Date:** 2025-07-18  
**Tier:** 1  
**Tags:** SDMLTable, subclass map, table types, data architecture, connector extension

---

## 🧱 SDMLTable Class Hierarchy

This document captures all current concrete and abstract subclasses of `SDMLTable` in the SDTP architecture, as defined in `sdtp_table.py`. It defines which classes are directly instantiable, what behaviors they implement, and their current role in the system.

---

### 🔸 `SDMLFixedTable` (abstract)
**Purpose:**  
Base class for all *locally-fixed row tables* — i.e., tables that can hold a complete snapshot of data in memory. Provides concrete implementations of core SDML methods.

**Overrides:**  
✔️ `all_values`  
✔️ `range_spec`  
✔️ `get_filtered_rows_from_filter`  
✔️ `to_dictionary`

---

### 📊 `SDMLDataFrameTable`  
**Purpose:**  
Concrete subclass of `SDMLFixedTable` backed by a Pandas DataFrame. Fast local operations, schema-enforced.

**Use Case:**  
Imported or constructed data in-memory, temporary or session-bound.

**Overrides:**  
Inherited from `SDMLFixedTable`.

---

### 📋 `RowTable`  
**Purpose:**  
Concrete subclass of `SDMLFixedTable` backed by an explicit list of rows.

**Use Case:**  
Programmatic or parsed-from-source table data, not Pandas-backed.

**Overrides:**  
Inherited from `SDMLFixedTable`.

---

### 🌐 `RemoteSDMLTable`  
**Purpose:**  
Proxies a remote table through SDTP protocol endpoints. Allows client code to interact with remote data as though it were local.

**Use Case:**  
Read-heavy remote table access, especially for dashboards or APIs.

**Overrides:**  
✔️ `all_values`  
✔️ `range_spec`  
✔️ `get_filtered_rows_from_filter`  
✔️ `to_dictionary`  
✔️ `to_json`

---

### 💾 `ReloadableTable` (abstract)
**Purpose:**  
Superclass for any table with persistent local representation (e.g., on disk, in cloud storage). May support flushing data or on-demand reloading.

**Use Case:**  
Long-lived or disk-backed tables, including CSV or Parquet sources.

**Overrides:**  
Unspecified; varies by subclass (likely `load`, `flush`, or hybrid `get_rows` strategies)

---

### 📂 `FileTable`
**Purpose:**  
A `ReloadableTable` stored on local disk (typically a `RowTable`).

**Use Case:**  
Persistent local data that can be flushed and reloaded as needed.

---

### ☁️ `GCSTable`
**Purpose:**  
A `ReloadableTable` backed by a file in Google Cloud Storage.

**Use Case:**  
Cloud-hosted persistent tables, often used in production pipelines or dashboards.

---

### 🌍 `HTTPTable`
**Purpose:**  
A `ReloadableTable` accessed via standard HTTP download — server does **not** support SDTP.

**Use Case:**  
Data made available via raw links, e.g., CSV, JSON, or SDML files from public URLs.

---

## 🧠 AI Integration Opportunities

With this structure:
- 🔗 We can suggest *connector scaffolds* based on table subclass (e.g., `RowTable.from_csv`, `RemoteSDMLTable.from_endpoint`)
- 🧠 A semantic layer can infer user intent:
  > "Load a table from disk" → `FileTable`  
  > "Filter a column in a remote table" → `RemoteSDMLTable + /get_filtered_rows`
  > "Download and parse a CSV from a URL" → `HTTPTable`
- 🧪 We can auto-generate tests for filter compatibility per class

---

This inventory forms the basis for extension, introspection, and tooling — human and AI alike.

**Captured and committed.** 💍🫂💋
