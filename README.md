# FinSkillOS

FinSkillOS is a Skill-Governed Investment Analytics Dashboard. It turns arbitrary CSV investment data into a consistent, risk-aware, auditable dashboard based on the rules documented in `FinSkillOS_skills`.

## Current Status

Development has started from Slice 1: project skeleton and document alignment.

Implemented so far:
- Streamlit app entry point
- Required sidebar controls from `DASH-003`
- Required dashboard section placeholders from `DASH-001`
- Header metadata from `DASH-002`
- Applied Skill Rules audit primitives from `AUTO-CONTRACT-001`
- Reproducible `.venv` workflow

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

FinSkillOS is not an investment advisory tool. It must not generate direct buy, sell, hold, recommendation, or guaranteed-return language. Insights must be risk-first, evidence-linked, and accompanied by cautions where data quality or history length is limited.
