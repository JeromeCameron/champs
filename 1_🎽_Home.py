import streamlit as st
import pandas as pd
import numpy as np

# ---------------------- SETTINGS -----------------------------------#

primary_color: str = "#182536"
secondary_color: str = "#1874d0"
primary_text: str = "#fafbfd"
secondary_text: str = "#536878"

header = f"""
    <div style='display: flex; align-items: baseline;'>
        <h1 style='color: {primary_color};'>Faster, Higher, Stronger:</h1>
        <h3 style='color: {secondary_text};'>Analyzing the Athletes and Stats Behind Champs Glory</h3>
    </div>
"""
st.set_page_config(layout="wide")
st.markdown(header, unsafe_allow_html=True)
"---"

with open("css/style.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

# -------------------------------------------------------------------

# Data
points_system = pd.read_csv("working_files/points_system.csv")
total_points = pd.read_csv("working_files/total_points.csv")

# ------------------------------------------------------------------

intro: str = """
    <p>
    Boys and Girls Championship is an annual track and field event in Jamaica. Here high schools 
    across the country come together in march and compete in an array of disciplines spanning across several age groups. The winning schools are determind 
    by a points system where points awareded for position finished in the finals of each event.
    </p> 
"""
st.markdown(intro, unsafe_allow_html=True)

# ------------------- Calculate total points up for grabs ------------------
# Boys
total_points_boys = (
    total_points.loc[total_points["gender"] == "Boys", ["one", "two", "three", "open"]]
    .sum()
    .sum()
)

# Girls
total_points_girls = (
    total_points.loc[
        total_points["gender"] == "Girls", ["one", "two", "three", "four", "open"]
    ]
    .sum()
    .sum()
)
no_events = total_points["event"].nunique()  # number of events competed in at champs


# ----------------------------- Get max points for boys -------------------------------


def max_points(gender: str) -> int:
    individual_points = (
        points_system.loc[
            points_system["event_type"] == "Individual Events", ["first", "second"]
        ]
        .sum()
        .sum()
    )

    other_points = (
        points_system.loc[points_system["event_type"] != "Individual Events", ["first"]]
        .sum()
        .sum()
    )

    events = total_points[
        (total_points["gender"] == gender)
        & (total_points["event_type"] != "relay")
        & (total_points["event_type"] != "combine events")
    ]
    events = events["event"].nunique()
    points = (individual_points + other_points) * events

    return points


# ----------------------------------------------------------------------------------------------

# Create HTML table with results
table_rows = "".join(
    f"<tr><td style='border: none; padding: 8px; color: #5b5b5b; text-align: left;'>{row['event_type']}</td>"
    f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'>{row['first']}</td>"
    f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'>{row['second']}</td>"
    f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'>{row['third']}</td>"
    f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'>{row['fourth']}</td>"
    f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'>{row['fifth']}</td>"
    f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'>{row['sixth']}</td>"
    f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'>{row['seventh']}</td>"
    f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'>{row['eighth']}</td></tr>"
    for _, row in points_system.iterrows()
)

points_system_txt: str = f"""
    <h4 style='color: {secondary_text};'>Points System</h4>
    Athletes are awarded 9 points for winning an individual event, 7 points for finishing second, and 6 points for finishing third.
    For relays and combined events, winners are awarded 12 points, while second and third place earn 10 and 8 points, respectively.
    See table below for full points system.
    <p></p>
    <table style="width:50%; border: none; border-collapse: collapse;">
    <tr style="background-color: {primary_color}; text-align: center; color: {primary_text};">
        <th style="padding: 8px; text-align: left;">EVENT TYPE</th>
        <th style="padding: 8px; text-align: center;">FIRST</th>
        <th style="padding: 8px; text-align: center;">SECOND</th>
        <th style="padding: 8px; text-align: center;">THIRD</th>
        <th style="padding: 8px; text-align: center;">FOURTH</th>
        <th style="padding: 8px; text-align: center;">FIFTH</th>
        <th style="padding: 8px; text-align: center;">SIXTH</th>
        <th style="padding: 8px; text-align: center;">SEVENTH</th>
        <th style="padding: 8px; text-align: center;">EIGHTH</th>
    </tr>
    {table_rows}
    </table>

    <p> A total of <strong>{total_points_boys:,}</strong> points is up for grabs for the males and <strong>{total_points_girls:,}</strong> for the females across <strong>{no_events}</strong> events.</p>
"""
st.markdown(points_system_txt, unsafe_allow_html=True)
st.write(max_points("Girls"))

# intro -- what is champs
# some champs stats
# of events
# Top times / distances
# division of points among top school
# total possible points
# points lost
# % of athletes in finals from schools
# of schools that make finals
# are athletes running faster today

# Insights into the athletes and stats behind Champs victories.
# A deep dive into the history and performances of Boys and Girls Champs.
