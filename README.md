# FinSkillOS

FinSkillOS is a Skill-Governed Investment Analytics Dashboard. It turns arbitrary CSV investment data into a consistent, risk-aware, auditable dashboard based on the rules documented in `FinSkillOS_skills`.

## Current Status

Slices 1-11 are implemented for the MVP submission package.

Implemented:
- CSV upload and bundled sample dataset analysis
- Data profiling, schema inference, metric calculation, chart planning, and risk-first insights
- Mixed schema mapping for fields such as `trade_dt`, `ticker_name`, `nav_value`, and `trading_amount`
- Multi-asset cumulative return, risk-return, correlation, drawdown, and metric table outputs
- Applied Skill Rules audit table and downloadable CSV/JSON audit logs
- Downloadable HTML analysis report
- Local acceptance checks for `AUTO-TEST-001` through `AUTO-TEST-005`

## Local Setup

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/streamlit run app.py
```

After `.venv` is ready, you can use the helper script:

```bash
./run_app.sh
```

If the system Python does not include `ensurepip`, bootstrap pip inside `.venv` first, then install `requirements.txt`.

## Reproducible Demo

Run the app and select one of the bundled datasets in the sidebar.

```bash
./run_app.sh
```

Suggested validation path:

1. Select `single_asset_price.csv` and confirm the app detects a single asset price schema.
2. Select `mixed_schema_assets.csv` and confirm `trade_dt`, `ticker_name`, `nav_value`, and `trading_amount` map to date, asset, price, and volume.
3. Select `multi_asset_portfolio.csv` and confirm cumulative return, risk-return scatter, correlation heatmap, drawdown, and asset metric table outputs appear.
4. Open `Applied Skill Rules` and confirm rule IDs from DATA, SCHEMA, METRIC, VIS, INSIGHT, SAFE, AUTO, and DASH categories are visible.
5. Use `Download HTML Report` to export the reproducible analysis report.

## Validation

Compile the app and engine modules:

```bash
.venv/bin/python -m compileall app.py engine
```

Run the local acceptance test pack:

```bash
.venv/bin/python -m unittest discover -s tests
```

The tests cover:
- `AUTO-TEST-001`: valid CSV analysis completes through the pipeline
- `AUTO-TEST-002`: mixed schema detection maps standard fields
- `AUTO-TEST-003`: multi-asset chart planning includes required outputs
- `AUTO-TEST-004`: direct investment-action language is rewritten or absent from generated outputs
- `AUTO-TEST-005`: applied rules expose at least five rule records and required categories

## Skill Documents

The implementation is governed by:
- `FinSkillOS_skills/Skills.md`
- `FinSkillOS_skills/skills/01_data_understanding.md`
- `FinSkillOS_skills/skills/02_financial_metrics.md`
- `FinSkillOS_skills/skills/03_visualization_dashboard.md`
- `FinSkillOS_skills/skills/04_insight_guardrails.md`
- `FinSkillOS_skills/skills/05_vibecoding_automation.md`
- `FinSkillOS_skills/skills/06_extension_ideas.md`

## Development Slices

High-level slices are tracked in:
- `.devmd/FinSkillOS_high_level_work_slices.md`

Daily implementation slices for 2026-04-30 are tracked in:
- `.devmd/2026-04-30/`

## Financial Safety

FinSkillOS is not an investment advisory tool. It must not generate direct transaction instructions, position instructions, recommendation language, or promised-return language. Insights must be risk-first, evidence-linked, and accompanied by cautions where data quality or history length is limited.

## Submission Contents

Core files for review:
- `app.py`
- `engine/`
- `FinSkillOS_skills/`
- `sample_data/`
- `reports/sample_report.html`
- `tests/test_acceptance.py`
- `requirements.txt`
- `README.md`
