import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from utils import time_to_seconds, seconds_to_minutes

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
# st.logo("assets/logo.jpeg", size="small")
st.markdown(header, unsafe_allow_html=True)
st.caption("2012 ➡️ Present (excluding 2013 and 2020)")
"---"

with open("css/style.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

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

        events = sorted(events_df["event"].unique())

        if "discipline_2" not in st.session_state:
            st.session_state.discipline_2 = None

        # If no events available
        if len(events) == 0:
            discipline = None
            st.selectbox("Discipline", ["No events"], disabled=True)
        else:
            # If previous discipline not valid, reset
            if st.session_state.discipline_2 not in events:
                st.session_state.discipline_2 = events[0]

            current_index = events.index(st.session_state.discipline_2)

            discipline = st.selectbox("Discipline", events, index=current_index)

            st.session_state.discipline_2 = discipline


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
    | (df["category"] == "Combined Events") & (df["mark"].notna())
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
    <h3 style='color: #5b5859; border-collapse: collapse; border-top: 4px solid {secondary_color}; padding-top: 2px;'>Top Performances</h3>
</div>
<div style="background-color: {primary_color}; padding: 6px; padding-left: 15px;">
    <div style="display: flex; align-items: center; justify-content: space-between; padding-bottom: 0;">
        <h4 style='color: {primary_text}; display: inline-block; padding-bottom: 0;'> Top 10 Performances in CLASS {clas_s} {gender.upper()} {discipline.upper()} Finals since 2012*</h4>
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

# ---------------- Track Events -----------------------------------------
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
    avg_performance_track.groupby(["year", "clas_s", "category"])["time_seconds"]
    .agg(["mean", "min"])
    .reset_index()
)

avg_performance_track = avg_performance_track.reset_index()
avg_performance_track["clas_s"] = avg_performance_track["clas_s"].astype(str)
avg_performance_track["avg_mark"] = avg_performance_track["mean"].apply(
    seconds_to_minutes
)

# ---------------------- Field Events --------------------------------------
fi_events = df[
    (df["gender"] == gender)
    & (df["event"] == discipline)
    & ((df["category"] == "Field Event") | (df["category"] == "Combined Events"))
    & (df["mark"].notna())
].copy()

fi_events["mark"] = pd.to_numeric(fi_events["mark"], errors="coerce")
fi_events.sort_values(by="mark", inplace=True)  # sort by distance

# avg performance
avg_performance_field = fi_events[fi_events["position"] <= number].copy()
avg_performance_field = (
    avg_performance_field.groupby(["year", "clas_s", "category"])["mark"]
    .agg(["mean", "min"])
    .reset_index()
)

avg_performance_field = avg_performance_field.reset_index()
avg_performance_field["clas_s"] = avg_performance_field["clas_s"].astype(str)
avg_performance_field["avg_mark"] = avg_performance_field["mean"]

# --------------------------------------------------------------------------

avg_performances = pd.concat([avg_performance_track, avg_performance_field])

options = sorted(avg_performances["clas_s"].unique())
selection = st.segmented_control(
    "Compare Classes", options, selection_mode="multi", default=options[:1]
)

avg_performances = avg_performances[avg_performances["clas_s"].isin(selection)]

# Calculate buffers for the y-axis (from earlier)
ymin, ymax = avg_performances["mean"].min(), avg_performances["mean"].max()
padding = (ymax - ymin) * 0.2

avg_performances["formatted_mark"] = [
    (
        seconds_to_minutes(row["mean"])
        if row["category"] == "Track Event"
        else f"{row['mean']:.2f}"
    )
    for _, row in avg_performances.iterrows()
]

if not selection:
    st.warning("Please select at least one class!")
else:
    # 1. Create the base chart
    fig = px.line(
        avg_performances,
        x="year",
        y="mean",
        color=avg_performances["clas_s"].astype(str),
        markers=True,
        template="simple_white",
        labels={"color": "Class", "mean": "Performance", "year": "Year"},
        hover_data={
            "avg_mark": False,  # we'll control this manually
        },
    )

    # 2. Add dynamic flare: Smooth lines and donut markers
    fig.update_traces(
        line_shape="linear",
        line_width=4,
        marker=dict(size=12, line=dict(width=2, color="white")),
        cliponaxis=False,
        customdata=avg_performances[["formatted_mark"]].values,
        hovertemplate="<b>Year:</b> %{x}<br>"
        "<b>Avg. Performance:</b> %{customdata[0]}<br>"
        "<extra></extra>",
    )

    # 3. Dynamic Annotation: Auto-locate the overall best point
    if not avg_performance_track.empty:
        best_idx = avg_performances["mean"].idxmin()
        fig.update_yaxes(autorange="reversed")
        tick_vals = np.linspace(ymin, ymax, 6)  # 6 clean ticks
        tick_text = [seconds_to_minutes(val) for val in tick_vals]
        fig.update_yaxes(tickvals=tick_vals, ticktext=tick_text)
    else:
        best_idx = avg_performances["mean"].idxmax()
        fig.update_yaxes(tickformat=".2f")

    best_val = avg_performances.loc[best_idx]

    fig.update_xaxes(
        tickmode="linear",
        tick0=avg_performances["year"].min(),
        dtick=1,
        fixedrange=True,
        gridcolor="whitesmoke",
    )

    # 4. Cleanup and Spacing
    fig.update_layout(
        title={
            "text": f"<b>Performance Analysis: {discipline}</b>",
            "x": 0.05,
            "y": 0.95,
        },
        margin=dict(l=20, r=20, t=100, b=100),
        yaxis=dict(range=[ymin - padding, ymax + padding], fixedrange=True),
        xaxis=dict(fixedrange=True),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    # Adds a subtle fill under the lines

    fig.update_layout(legend_title_text="Class")

    st.plotly_chart(fig, config={"displayModeBar": False})
