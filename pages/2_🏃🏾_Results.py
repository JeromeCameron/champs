import streamlit as st
import pandas as pd
import numpy as np


# -------------------- Settings -------------------------------#

primary_color: str = "#182536"
secondary_color: str = "#1874d0"
primary_text: str = "#fafbfd"
secondary_text: str = ""

st.header("Boys and Girls Champs Results 🏃🏾")
st.caption("2012 ➡️ Present")
st.html("<br>")

with open("css/style.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

# ----------------------------------------------------------------

df = pd.read_csv("./working_files/champs_results.csv")
df["note"] = df["note"].apply(
    lambda x: "" if pd.isna(x) else x
)  # Replace NaN values with an empty string
df["points"] = df["points"].fillna(0)
df["mark"] = df["mark"].str.rstrip("x")
df["position"] = pd.to_numeric(df["position"], errors="coerce").astype(
    "Int64"
)  # convert position to int ignoring nan values

records = pd.read_csv("./working_files/champs_records.csv")
records["mark"] = records["mark"].str.rstrip("x")


# Get Filters
st.text("Filter Results")
with st.container(border=True):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        year_series = df["year"].unique()
        year_series = np.sort(year_series)[::-1]
        year_series = year_series[year_series != 13]
        year = st.selectbox("Year", year_series)
    with col2:
        gender = st.selectbox("Gender", ("Boys", "Girls"))
    with col3:
        clas_series = df[["gender", "clas_s"]].copy()
        clas_series = clas_series[clas_series["gender"] == gender]
        clas_series = clas_series["clas_s"].unique()
        clas_series = np.sort(clas_series)
        clas_s = st.selectbox("Class", clas_series)
    with col4:
        events_df = df[
            (df["gender"] == gender) & (df["clas_s"] == clas_s) * (df["year"] == year)
        ]
        events = events_df["event"].unique()
        events = np.sort(events)
        discipline = st.selectbox("Discipline", events)

# Fiter results based on user input
results = df[
    (df["year"] == int(year))
    & (df["gender"] == gender)
    & (df["clas_s"] == clas_s)
    & (df["event"] == discipline).copy()
]

results = results.sort_values(by="position").copy()  # sort by position finished

try:
    wind = results["wind"].iloc[0]  # grap wind data
except IndexError:
    wind = "nil"

record = records[
    (records["event"] == discipline)
    & (records["gender"] == gender)
    & (records["clas_s"] == clas_s)
]

st.html("<br>")

# Results Header Row
result_header = f"""
<div style='display: inline-block;'>
    <h3 style='color: #5b5859; border-collapse: collapse; border-top: 4px solid {secondary_color}; padding-top: 2px;'>Results</h3>
</div>
<div style="background-color: {primary_color}; padding: 6px; padding-left: 15px;">
    <div style="display: flex; align-items: center; justify-content: space-between; padding-bottom: 0;">
        <h4 style='color: {primary_text}; display: inline-block; padding-bottom: 0;'>{discipline.upper()} {gender.upper()} CLASS {clas_s} | 20{year}</h4>
        <h4 style='color: {primary_text}; display: inline-block; padding-bottom: 0;'>WIND: {wind} 🍃</h4>
    </div>
    <div style="margin-top: 0; padding-top: 1px;">
        <h6 style='color: {primary_text}; margin-top:0; padding-top: 1px'>Record: <span style="font-weight: bold; color: white;">{record["mark"].iloc[0] }</span> by {record["athlete"].iloc[0] } of {record["school"].iloc[0] } | Set in {record["year"].iloc[0] }</h6>
    </div>
</div>
"""
st.markdown(result_header, unsafe_allow_html=True)

# Create HTML table with results
table_rows = "".join(
    f"<tr><td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'>{row['position']}</td>"
    f"<td style='border: none; padding: 8px; color: #5b5b5b;'>{row['school']}</td>"
    f"<td style='border: none; padding: 8px; color: #5b5b5b;'><strong>{row['athlete']}</strong></td>"
    f"<td style='border: none; padding: 8px; color: {primary_text}; text-align: center; background-color: {secondary_color};'><strong>{row['mark']}</strong></td>"
    f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'>{row['points']}</td>"
    f"<td style='border: none; padding: 8px; color: #5b5b5b;'>{row['note']}</td></tr>"
    for _, row in results.iterrows()
)

table_html = f"""
<table style="width:100%; border: none; border-collapse: collapse;">
  <tr style="background-color: {primary_color}; text-align: center; color: {primary_text};">
    <th style="padding: 8px;">POSITION</th>
    <th style="padding: 8px; text-align: left;">SCHOOL</th>
    <th style="padding: 8px; text-align: left;">ATHLETE</th>
    <th style="padding: 8px;">MARK</th>
    <th style="padding: 8px;">POINTS</th>
    <th style="padding: 8px;">NOTE</th>
  </tr>
  {table_rows}
</table>
"""

st.markdown(table_html, unsafe_allow_html=True)
