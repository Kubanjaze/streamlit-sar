# Phase 90 — Streamlit SAR Dashboard (v1.1)

## Goal
Build a Streamlit dashboard for exploring SAR data from compounds.csv. --test flag validates data loading without launching server.

## CLI
```bash
PYTHONUTF8=1 python main.py --test           # Validate data loading
PYTHONUTF8=1 streamlit run main.py           # Launch dashboard
```

## Outputs
- Interactive Streamlit dashboard with sidebar filters, data table, bar chart, top 10 table
- Console validation results (--test mode)

## Logic
1. Load compounds.csv, parse scaffold family
2. Sidebar: family multiselect, pIC50 range slider
3. Main: metrics row, filterable data table, avg pIC50 bar chart, top 10 table
4. --test: validate CSV loading, column checks, 45 compounds, 6 families

## Key Concepts
- Streamlit interactive dashboard (st.sidebar, st.dataframe, st.bar_chart)
- Self-test pattern for UI apps

## Verification Checklist
- [x] `--help` works
- [x] --test validates: 45 compounds, 6 families, pIC50 range 5.75-8.55
- [x] Dashboard code structured (manual browser test needed for full validation)

## Results
- 45 compounds loaded, 6 scaffold families
- pIC50 range: 5.75 - 8.55
- Dashboard provides filtering by family and pIC50 range

## Deviations
- None

## Risks
- Streamlit requires browser for full UI testing
