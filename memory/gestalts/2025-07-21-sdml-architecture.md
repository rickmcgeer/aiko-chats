# Gestalt: SDML Table & Auth Architecture Refactor
**Date**: 2025-07-21  
We refactored the table and authentication architecture for SDML/SDTP.  
- Introduced clean separation for `RemoteSDMLTable` with secure `auth` hooks.  
- Unified handling of FileTable, GCSTable, and HTTPTable under a common access pattern.  
- Left hooks in place for pluggable table architectures.