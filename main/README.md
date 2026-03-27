# Main Structure

`main/` is organized by the major project domains:

- `bronze/`: data ingestion to the Bronze zone
- `silver/`: cleaning and enrichment for the Silver zone
- `gold/`: analytics jobs that build Gold outputs
- `common/`: shared Spark, GCS, models, paths, and utilities
- `query/`: query-facing data access and schemas
- `backend/`: backend API and fake request generation
- `web/`: frontend application
- `config/`: environment configuration files
- `tests/`: tests grouped by domain

The active Bronze implementation currently lives in:

- `bronze/models.py`
- `bronze/ingest.py`
- `bronze/upload.py`
- `bronze/run.py`
- `common/spark.py`
