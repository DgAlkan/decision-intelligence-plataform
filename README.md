# Decision Intelligence Platform

Independent portfolio project by Rodrigo Alcantara (DgAlkan), developed with AI assistance. Version 1.0 initial implementation.

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

No employer data or proprietary code. Synthetic demonstration only. No hosted deployment or production performance claims. Test execution must be verified before release.

## Original introduction

# decision-intelligence-plataform
An interactive analytics platform for business perfomance, KPI monitoring and decision scenario simulation.
