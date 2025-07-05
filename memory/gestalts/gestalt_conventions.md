# Gestalt Conventions

**Purpose:**  
This document defines the naming, linking, and cross-checking pattern for *our* gestalts.  
It guarantees that our narrative spine is consistent, canonical, and trustable across:
- Raw files in `gestalts/`
- `gestalt_manifest.md` (human-readable index)
- `manifest.json` (machine-checkable manifest)

---

## 🗝️ Canonical Rules

✅ **1️⃣ One Title is the Source of Truth**

- Each gestalt has a single canonical title.
- It must appear as the `# Title` in the file’s first line or frontmatter.
- The exact same title must appear:
  - In `gestalt_manifest.md`
  - In `manifest.json` → `"title"`

---

✅ **2️⃣ File Naming**

- Filenames always start with the canonical date.
- Then a slugified version of the title:
  - Spaces become underscores.
  - Lowercase for consistency.

**Example:**  
Title: `BearBorg Static Page Build`  
Filename: `2025-06-18_bearborg_static_page_build.md`

---

✅ **3️⃣ Manifest Path**

- `manifest.json` uses the exact filename as `path`.
- Example:
  ```json
  {
    "date": "2025-06-18",
    "title": "BearBorg Static Page Build",
    "path": "gestalts/2025-06-18_bearborg_static_page_build.md",
    ...
  }
