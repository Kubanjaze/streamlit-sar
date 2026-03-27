"""Phase 90 — Streamlit SAR Dashboard: Interactive compound explorer."""
import sys
import os

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

import pandas as pd

FAMILY_COLORS = {
    "benz": "#4C72B0", "naph": "#DD8452", "ind": "#55A868",
    "quin": "#C44E52", "pyr": "#8172B2", "bzim": "#937860",
    "other": "#808080",
}

DATA_PATH = "data/compounds.csv"


def load_data(path: str) -> pd.DataFrame:
    """Load compounds CSV and add scaffold family column."""
    df = pd.read_csv(path)
    df["family"] = df["compound_name"].apply(lambda x: x.split("_")[0])
    return df


def run_test():
    """Validate data loading without launching Streamlit."""
    print("Running data validation tests...")

    assert os.path.exists(DATA_PATH), f"Data file not found: {DATA_PATH}"
    df = load_data(DATA_PATH)

    assert "compound_name" in df.columns, "Missing compound_name column"
    assert "smiles" in df.columns, "Missing smiles column"
    assert "pic50" in df.columns, "Missing pic50 column"
    print(f"  Loaded {len(df)} compounds")

    assert "family" in df.columns, "Family column not created"
    families = df["family"].unique()
    print(f"  Families: {sorted(families)}")
    assert len(families) == 6, f"Expected 6 families, got {len(families)}"

    assert len(df) == 45, f"Expected 45 compounds, got {len(df)}"
    assert df["pic50"].min() > 0, "pIC50 values should be positive"

    print(f"  pIC50 range: {df['pic50'].min():.2f} - {df['pic50'].max():.2f}")
    print("\nAll validation tests passed!")


def run_dashboard():
    """Launch Streamlit dashboard."""
    import streamlit as st

    st.set_page_config(page_title="SAR Dashboard", layout="wide")
    st.title("SAR Compound Dashboard")

    df = load_data(DATA_PATH)

    # Sidebar filters
    st.sidebar.header("Filters")
    families = st.sidebar.multiselect(
        "Scaffold Family",
        options=sorted(df["family"].unique()),
        default=sorted(df["family"].unique()),
    )
    pic50_range = st.sidebar.slider(
        "pIC50 Range",
        float(df["pic50"].min()),
        float(df["pic50"].max()),
        (float(df["pic50"].min()), float(df["pic50"].max())),
    )

    # Filter data
    mask = df["family"].isin(families) & df["pic50"].between(*pic50_range)
    filtered = df[mask]

    # Metrics row
    col1, col2, col3 = st.columns(3)
    col1.metric("Compounds", len(filtered))
    col2.metric("Avg pIC50", f"{filtered['pic50'].mean():.2f}" if len(filtered) > 0 else "N/A")
    col3.metric("Families", filtered["family"].nunique())

    # Data table
    st.subheader(f"Compounds ({len(filtered)})")
    st.dataframe(
        filtered[["compound_name", "family", "smiles", "pic50"]].sort_values("pic50", ascending=False),
        use_container_width=True,
    )

    # Bar chart: avg pIC50 by family
    if len(filtered) > 0:
        st.subheader("Average pIC50 by Scaffold Family")
        family_stats = filtered.groupby("family")["pic50"].agg(["mean", "count", "std"]).round(2)
        family_stats = family_stats.sort_values("mean", ascending=False)
        st.bar_chart(family_stats["mean"])

        # Top compounds table
        st.subheader("Top 10 Most Potent")
        top10 = filtered.nlargest(10, "pic50")[["compound_name", "family", "pic50"]]
        st.table(top10)


# Handle --test flag before Streamlit takes over argv
if __name__ == "__main__":
    if "--test" in sys.argv:
        run_test()
    elif "--help" in sys.argv or "-h" in sys.argv:
        print("Usage:")
        print("  python main.py --test           Validate data loading")
        print("  streamlit run main.py           Launch dashboard")
        print("  python main.py --help           Show this help")
    else:
        # When run via `streamlit run main.py`, __name__ is "__main__"
        run_dashboard()

# Also run dashboard when imported by Streamlit
if "streamlit" in sys.modules and "__main__" not in sys.argv[0]:
    run_dashboard()
