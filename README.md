# Amazon SKU Automation

A small FastAPI service for checking inventory files against a master Amazon SKU list. Upload an Amazon export plus up to three other spreadsheets, and it tells you which SKUs in each file don't show up in the Amazon file.

## How it works

- `POST /upload/` takes four files: `amazon` (the master file) and `file1`/`file2`/`file3` (the files to check).
- Each file is merged against the Amazon file on a `SKU` column.
- Rows that don't find a match are written out as `<original filename>_missing.xlsx` in `outputs/`.

`index.html` is a minimal upload form (Tailwind via CDN, no build step) that posts to the API and links to the generated files.

## Running it

```bash
pip install fastapi uvicorn pandas openpyxl python-multipart
uvicorn app:app --reload
```

Then open `index.html` directly in a browser, or serve it from wherever you're hosting the frontend — CORS is wide open (`allow_origins=["*"]`) for local development.

## Notes

- The match key is hardcoded to a column named `SKU` (see `KEY` in `app.py`) — rename that if your files use something else.
- `uploads/` and `outputs/` are created automatically and are gitignored; nothing you upload gets committed.
