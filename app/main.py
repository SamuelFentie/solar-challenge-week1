import streamlit as st
import pandas as pd
import os
import altair as alt  # Import Altair for visualization

COUNTRIES = ["Benin", "Togo", "Sierraleone"]
FILE_MAP = {
    "Benin": "data/benin_clean.csv",
    "Togo": "data/togo_clean.csv",
    "Sierraleone": "data/sierraleone_clean.csv"
}

# Sidebar
st.sidebar.title("Dashboard Filters")
selected_countries = st.sidebar.multiselect("Select Countries", COUNTRIES, default=COUNTRIES)
selected_metric = st.sidebar.selectbox("Select Metric", ["GHI", "DNI", "DHI"])

# Load data
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

df_all = pd.concat(dfs)

# Boxplot using Altair
st.title(f"{selected_metric} Distribution by Country")

boxplot = alt.Chart(df_all).mark_boxplot().encode(
    x='Country:N',
    y=alt.Y(f'{selected_metric}:Q', title=selected_metric)
).properties(
    width=600,
    height=400
)

st.altair_chart(boxplot, use_container_width=True)

# Top Regions Table (e.g., top 5 rows by GHI)
st.subheader("Top Regions by GHI")
top_regions = df_all.sort_values(by="GHI", ascending=False).head(5)
st.dataframe(top_regions[["Country", "GHI", "DNI", "DHI"]])
