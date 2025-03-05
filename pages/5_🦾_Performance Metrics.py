import streamlit as st
import pandas as pd
import numpy as np
import re
import plotly_express as px

# ---------------- Settings ------------------------------------

primary_color: str = "#182536"
secondary_color: str = "#1874d0"
primary_text: str = "#fafbfd"
secondary_text: str = ""

header = f"""
    <div style='display: flex; align-items: baseline;'>
        <h1 style='color: {primary_color}; font-size: 2rem;'>Faster, Higher, Stronger: Performance Over the Years 📈</h1>
    </div>
"""
st.set_page_config(layout="wide")
st.logo("assets/logo.jpeg", size="large")
st.markdown(header, unsafe_allow_html=True)
st.caption("2012 ➡️ Present")
"---"

with open("css/style.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)


# Functions ----------------------------------------------------------------------
def time_to_seconds(time_str):
    """Converts a time string (H:MM:SS.mmm or MM:SS.mmm or SS.mmm) to seconds."""

    parts = re.split(r":|\.", time_str)  # Split by ":" and "."

    if len(parts) >= 3:  # H:MM:SS.mmm or MM:SS.mmm
        if len(parts[0]) > 1:  # H:MM:SS.mmm
            hours = int(parts[0])
            minutes = int(parts[1])
            seconds = float(parts[2] + "." + parts[3])
            total_seconds = hours * 3600 + minutes * 60 + seconds
        else:  # MM:SS.mmm
            minutes = int(parts[0])
            seconds = float(parts[1] + "." + parts[2])
            total_seconds = minutes * 60 + seconds

    elif len(parts) == 2:  # SS.mmm
        seconds = float(parts[0] + "." + parts[1])  # join back the split seconds
        total_seconds = seconds
    else:
        raise ValueError("Invalid time format.  Use H:MM:SS.mmm, MM:SS.mmm, or SS.mmm")

    return total_seconds


# ------------------------------------------------------------------------------------

# Import data
df = pd.read_csv("./working_files/champs_results.csv")
df["note"] = df["note"].apply(
    lambda x: "" if pd.isna(x) else x
)  # Replace NaN values with an empty string

df["mark"] = df["mark"].str.rstrip("x R X m M")  # Strip str from mark
df["position"] = pd.to_numeric(df["position"], errors="coerce").astype(
    "Int64"
)  # convert position to int ignoring nan values


# ------------------------------------------------------------------------------------

# Get DF Filters from user
st.text("Filter Results")
with st.container(border=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        gender = st.selectbox("Gender", ("Boys", "Girls"))
    with col2:
        clas_series = df[["gender", "clas_s"]].copy()
        clas_series = clas_series[clas_series["gender"] == gender]
        clas_series = clas_series["clas_s"].unique()
        clas_series = np.sort(clas_series)
        clas_s = st.selectbox("Class", clas_series)
    with col3:
        events_df = df[(df["gender"] == gender) & (df["clas_s"] == clas_s)]
        events = events_df["event"].unique()
        events = np.sort(events)
        discipline = st.selectbox("Discipline", events)

# Fiter results based on user input
track_events = df[
    (df["gender"] == gender)
    & (df["clas_s"] == clas_s)
    & (df["event"] == discipline)
    & (df["category"] == "Track Event")
    & (df["mark"].notna())
].copy()
track_events["mark"] = track_events["mark"].astype(str)

field_events = df[
    (df["gender"] == gender)
    & (df["clas_s"] == clas_s)
    & (df["event"] == discipline)
    & (df["category"] == "Field Event")
    & (df["mark"].notna())
].copy()
field_events["mark"] = field_events["mark"].astype(str)

# -------------------------------------------------------------------------------------

# Top 10 best performances in a finals over the years from 2012
track_events["time_seconds"] = track_events["mark"].apply(time_to_seconds)
track_events.sort_values(by="time_seconds", inplace=True)  # sort by time
field_events.sort_values(
    by="mark", inplace=True, ascending=False
)  # sort by distance or height
all_events = pd.concat([track_events, field_events])


st.html("<br>")

# Results Header Row
result_header = f"""
<div style='display: inline-block;'>
    <h3 style='color: #5b5859; border-collapse: collapse; border-top: 4px solid {secondary_color}; padding-top: 2px;'>Top Perfomances</h3>
</div>
<div style="background-color: {primary_color}; padding: 6px; padding-left: 15px;">
    <div style="display: flex; align-items: center; justify-content: space-between; padding-bottom: 0;">
        <h4 style='color: {primary_text}; display: inline-block; padding-bottom: 0;'> Top 10 Perfomaces in CLASS {clas_s} {gender.upper()} {discipline.upper()} Finals since 2012*</h4>
    </div>
    <div>
        <p style='color: white;'>*2013 data is missing, and there was no championship in 2020 due to COVID</p>
        </div>
</div>
"""
st.markdown(result_header, unsafe_allow_html=True)

# Create HTML table with results
table_rows = "".join(
    f"<tr style='font-size: 0.8rem;'><td style='border: none; padding: 8px; color: #5b5b5b; text-align: left;'><strong>{row['athlete']}</strong></td>"
    f"<td style='border: none; padding: 8px; color: #5b5b5b;'>{row['school']}</td>"
    f"<td style='border: none; padding: 8px; color: {primary_text}; text-align: center; background-color: {secondary_color};'><strong>{row['mark']}</strong></td>"
    f"<td style='border: none; padding: 8px; color: #030303; text-align: center;'>{row['year']}</td>"
    f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'>{row['wind']}</td></tr>"
    for _, row in all_events.head(10).iterrows()
)

table_html = f"""
<table style="width:100%; border: none; border-collapse: collapse;">
  <tr style="background-color: {secondary_color}; text-align: left; color: {primary_text}; font-size: 0.8rem;">
    <th style="padding: 8px;">ATHLETE</th>
    <th style="padding: 8px; text-align: left;">SCHOOL</th>
    <th style="padding: 8px; text-align: center;">MARK</th>
    <th style="padding: 8px; text-align: center;">YEAR</th>
    <th style="padding: 8px; text-align: center;">WIND</th>
  </tr>
  {table_rows}
</table>
"""

st.markdown(table_html, unsafe_allow_html=True)

# ----------------------------------------------------------------------------------------------


"---"
st.subheader("Performance Progression")
st.write(
    "How have athlete performances changed over the years? Are athletes, on average, performing better than in previous years?"
)
number = st.number_input(
    "Select the top # of finishers to calculate averages. The top 5 is recommended to exclude athletes who may not be competing competitively and are participating just for points.",
    value=5,
    max_value=8,
    min_value=1,
)

# Fiter results based on user input
tr_events = df[
    (df["gender"] == gender)
    & (df["event"] == discipline)
    & (df["category"] == "Track Event")
    & (df["mark"].notna())
].copy()
tr_events["mark"] = tr_events["mark"].astype(str)

tr_events["time_seconds"] = tr_events["mark"].apply(time_to_seconds)
tr_events.sort_values(by="time_seconds", inplace=True)  # sort by time

# avg performance
avg_performance_track = tr_events[tr_events["position"] <= number].copy()
avg_performance_track = (
    avg_performance_track.groupby(["year", "clas_s"])["time_seconds"]
    .agg(["mean", "min"])
    .reset_index()
)

avg_performance_track = avg_performance_track.reset_index()
avg_performance_track["clas_s"] = avg_performance_track["clas_s"].astype(str)

options = ["1", "2", "3", "4"]
selection = st.segmented_control(
    "Compare Classes", options, selection_mode="multi", default=["1", "2"]
)

avg_performance_track = avg_performance_track[
    avg_performance_track["clas_s"].isin(selection)
]


fig = px.line(
    avg_performance_track,
    x="year",
    y="mean",
    title="Avg. Performances",
    markers=True,
    template="seaborn",
    color=avg_performance_track["clas_s"].astype(str),
)

st.plotly_chart(fig)
