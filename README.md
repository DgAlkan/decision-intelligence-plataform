# Decision Intelligence Platform

[Live demo](https://dgalkan-decision-intelligence.streamlit.app)

Independent portfolio project by Rodrigo Alcantara.

Operational analytics, KPI segmentation and hypothetical decision scenarios using synthetic appointments.

## Run locally

```bash
pip install -r requirements.txt
python generate_data.py
python -m pytest -q
streamlit run app.py
```

Run SQL with DuckDB from the repository root after generating the CSV. See [methodology](docs/methodology.md) for definitions and limitations.

## Structure

- engine.py: deterministic generator and analytical functions
- app.py: interactive dashboard and CSV export
- sql/analysis.sql: analytical SQL
- tests/: automated checks
- .github/workflows/: CI configuration

