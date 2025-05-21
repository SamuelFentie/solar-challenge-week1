import streamlit as st
import pandas as pd
import os
import altair as alt

# Constants
COUNTRIES = ["Benin", "Togo", "Sierraleone"]
FILE_MAP = {
    "Benin": "data/benin_clean.csv",
    "Togo": "data/togo_clean.csv",
    "Sierraleone": "data/sierraleone_clean.csv"
}
MAX_ROWS = 10000  # Safety limit for rendering

# Sidebar filters
st.sidebar.title("Dashboard Filters")
selected_countries = st.sidebar.multiselect("Select Countries", COUNTRIES, default=COUNTRIES)
selected_metric = st.sidebar.selectbox("Select Metric", ["GHI", "DNI", "DHI"])

# Load and combine data
dfs = []
for country in selected_countries:
    path = FILE_MAP[country]
    if os.path.exists(path):
        df = pd.read_csv(path)
        df["Country"] = country
        dfs.append(df)

if not dfs:
    st.warning("No data loaded. Please check your selections or CSV files.")
    st.stop()

df_all = pd.concat(dfs, ignore_index=True)

# Limit data to avoid exceeding Streamlit's message size limit
if len(df_all) > MAX_ROWS:
    df_viz = df_all.sample(MAX_ROWS, random_state=42)
    st.info(f"Data has been sampled to {MAX_ROWS} rows for performance.")
else:
    df_viz = df_all

# Altair Boxplot
st.title(f"{selected_metric} Distribution by Country")
boxplot = alt.Chart(df_viz).mark_boxplot().encode(
    x='Country:N',
    y=alt.Y(f'{selected_metric}:Q', title=selected_metric)
).properties(
    width=600,
    height=400
)
st.altair_chart(boxplot, use_container_width=True)

# Top Regions Table
st.subheader(f"Top Regions by {selected_metric}")
top_regions = df_all.sort_values(by=selected_metric, ascending=False).head(5)
st.dataframe(top_regions[["Country", "GHI", "DNI", "DHI"]])

# Optional: Download button for full data
csv_data = df_all.to_csv(index=False)
st.download_button("📥 Download Full Data as CSV", csv_data, file_name="full_data.csv", mime="text/csv")
