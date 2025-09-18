# AI-driven Unified Data Platform — Django Prototype

This is a minimal prototype scaffold for the "Unified Data Platform for Oceanographic, Fisheries & Biodiversity Insights".
It's intended for local development and demonstration only (uses SQLite by default).

## Quick start

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Upload CSVs via the Upload page and try the prediction page (stubbed models).
