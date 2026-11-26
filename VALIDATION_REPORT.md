# Validation report — v1.1

## Evidence — 2026-11-26

GitHub Actions workflow Tests #7 displayed a successful result in the repository owner's screenshot for commit [c0b6d05](https://github.com/DgAlkan/decision-intelligence-plataform/commit/c0b6d055549b49719cf49c1e95963fcdd0473287). The workflow executes pytest, including Python, DuckDB integration and Streamlit AppTest checks. The earlier AppTest relative-path failure was corrected using an absolute path derived from the test file.

Evidence source: owner-provided screenshot of the Actions overview; detailed final test logs were not independently retrieved. This confirms the workflow result, not exhaustive coverage.

## Remaining checks

Manual visual and interaction review, performance benchmarks, publication review and deployment remain pending. Synthetic data only.

## Reproduce

```bash
pip install -r requirements.txt
python -m pytest -v
```

[Actions history](https://github.com/DgAlkan/decision-intelligence-plataform/actions)
