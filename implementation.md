# Phase 90 — Streamlit SAR Dashboard (v1.0)

## Goal
Build a Streamlit dashboard for exploring SAR data from compounds.csv. --test flag validates data loading without launching server.

## CLI
```bash
PYTHONUTF8=1 python main.py --test           # Validate data loading
PYTHONUTF8=1 streamlit run main.py           # Launch dashboard
```

## Outputs
- Interactive Streamlit dashboard (normal mode)
- Console validation results (--test mode)

## Logic
1. Load compounds.csv, parse scaffold family
2. Dashboard: sidebar filters (family, pIC50 range), data table, bar chart of avg pIC50 by family
3. --test: validate CSV loading, column checks, family extraction

## Key Concepts
- Streamlit interactive dashboard
- SAR data filtering and visualization
- Self-test pattern for dashboard apps

## Verification Checklist
- [ ] `--help` works
- [ ] --test validates data loading
- [ ] Dashboard renders (manual check)

## Risks
- Streamlit requires browser for full testing
