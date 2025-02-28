import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

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
points_system = pd.read_csv("working_files/champs_points.csv")
champs_results = pd.read_csv("working_files/champs_results.csv")

# ------------------------------------------------------------------

intro: str = """
    <p>
    The <strong>Boys and Girls Championship</strong> is an annual track and field event in Jamaica held by Jamaica's Inter-Secondary Schools Sports Association. Here, over five days high schools 
    across the country come together in march and compete in an array of disciplines spanning across several age groups. The winning schools are determind 
    by a points system where points awareded for position finished in the finals of each event. These championships are the biggest track and field event involving high school students anywhere in the world.
    </p>
"""
st.markdown(intro, unsafe_allow_html=True)

points_columns = [
    "first",
    "second",
    "third",
    "fourth",
    "fifth",
    "sixth",
    "seventh",
    "eighth",
]
points_distribution = points_system.groupby("type", as_index=False)[
    points_columns
].mean()

# ------------------- Calculate total points up for grabs ------------------


def calc_total_points(gender: str) -> int:
    points = (
        points_system.loc[
            points_system["gender"] == gender,
            [
                "first",
                "second",
                "third",
                "fourth",
                "fifth",
                "sixth",
                "seventh",
                "eighth",
            ],
        ]
        .sum()
        .sum()
    )
    return points


no_events = points_system[points_system["gender"] == "boys"]
no_events = no_events["event"].nunique()  # number of events competed in at champs

# ----------------------------- Get max points -------------------------------


def max_points(gender: str) -> int:
    individual_points = (
        points_system.loc[
            (points_system["type"] != "relay") & (points_system["gender"] == gender),
            ["first", "second"],
        ]
        .sum()
        .sum()
    )
    relay_points = (
        points_system.loc[
            (points_system["type"] == "relay") & (points_system["gender"] == gender),
            ["first"],
        ]
        .sum()
        .sum()
    )

    return individual_points + relay_points


# ----------------------------- Get average points for winners -------------------------------

avg_winner_points = champs_results[champs_results["year"] != 13]
avg_winner_points = (
    avg_winner_points.groupby(["school", "year", "gender"])["points"]
    .sum()
    .reset_index()
)
avg_winner_points = (
    avg_winner_points.groupby(["year", "gender"])["points"].agg(["max"]).reset_index()
)
avg_winner_points.sort_values(by="max", inplace=True, ascending=False)


def get_avg_winning_point(gender: str):
    avg_winning_points = avg_winner_points[avg_winner_points["gender"] == gender][
        "max"
    ].mean()
    return avg_winning_points


# ----------------------------------------------------------------------------------------------


# Create HTML table with results
table_rows = "".join(
    f"<tr><td style='border: none; padding: 8px; color: #5b5b5b; text-align: left;'>{row['type']}</td>"
    f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'>{row['first']}</td>"
    f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'>{row['second']}</td>"
    f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'>{row['third']}</td>"
    f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'>{row['fourth']}</td>"
    f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'>{row['fifth']}</td>"
    f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'>{row['sixth']}</td>"
    f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'>{row['seventh']}</td>"
    f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'>{row['eighth']}</td></tr>"
    for _, row in points_distribution.iterrows()
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

    <p> A total of <strong>{calc_total_points("boys"):,}</strong> points is up for grabs for the males and <strong>{calc_total_points("girls"):,}</strong> for the females across <strong>{no_events}</strong> events each.</p>
    <p>Each school is allowed to enter two athletes per individual event. The maximum possible points across all events and age categories are <strong>{max_points("boys")}</strong> for boys and <strong>{max_points("girls")}</strong> for girls. This assumes a school finishes first and second in individual events and secures first place in team events such as relays.</p>
    <p>On average, the winning team for Girls Champs averages <strong>{get_avg_winning_point("Girls"):.2f}</strong> points for victory, and the boys tend to average <strong>{get_avg_winning_point("Boys"):.2f}</strong> to claim the Boys Champs title.</p> 
"""
st.markdown(points_system_txt, unsafe_allow_html=True)


# get total points possible for each age category
def age_group_points(gender: str):
    points = (
        points_system[points_system["gender"] == gender]
        .groupby(["gender", "class"])[
            [
                "first",
                "second",
                "third",
                "fourth",
                "fifth",
                "sixth",
                "seventh",
                "eighth",
            ]
        ]
        .sum()
        .reset_index()
    )

    points["total_points"] = points[
        ["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth"]
    ].sum(axis=1)

    return points


# st.write(age_group_points("girls"))

# ---------------------------------- Historical Winners ---------------------------------------
# Data
historical_winners = pd.read_csv("working_files/historical_winners.csv")


def get_most_wins(gender: str):
    most_wins = (
        historical_winners[historical_winners["gender"] == gender]
        .groupby("school")["year"]
        .count()
        .reset_index()
    )
    most_wins.sort_values(by="year", ascending=False, inplace=True)
    return most_wins


# No of schools to have won boys champs
winners_boys = historical_winners[historical_winners["gender"] == "Boys"][
    "school"
].nunique()

# No of schools to have won girls champs
winners_girls = historical_winners[historical_winners["gender"] == "Girls"][
    "school"
].nunique()

boys_wins = get_most_wins("Boys")
girls_wins = get_most_wins("Girls")

# Paragraph historical winners of boys and girls champs
historical_winners: str = f"""
    <h4 style='color: {secondary_text};'>Historical Winners</h4>
    <p>Historically, only <strong>{winners_boys}</strong> schools have ever won the Boys Championship, with <strong>{get_most_wins("Boys").head(1)["school"].values[0]}</strong> having the most titles. On the girls' side, <strong>{winners_girls}</strong> schools have won the coveted title, with <strong>{get_most_wins("Girls").head(1)["school"].values[0]}</strong> having the most wins.</p>
"""
st.markdown(historical_winners, unsafe_allow_html=True)

col3, col4 = st.columns(2)


def create_table(df, gender):
    # Create HTML table with results
    table_rows = "".join(
        f"<tr><td style='border: none; padding: 8px; color: #5b5b5b; text-align: left;'>{row['school']}</td>"
        f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'>{row['year']}</td></tr>"
        for _, row in df.head(5).iterrows()
    )

    past_winners_txt: str = f"""
        <h6 style='color: {secondary_text};'>Top 5 schools with most winners | {gender} Champs</h6>
        <p></p>
        <table style="width:50%; border: none; border-collapse: collapse;">
        <tr style="background-color: {primary_color}; text-align: center; color: {primary_text};">
            <th style="padding: 8px; text-align: left;">SCHOOL</th>
            <th style="padding: 8px; text-align: center;"># OF TITLES</th>
        </tr>
        {table_rows}
        </table>
    """
    return past_winners_txt


with st.container():
    with col3:
        st.markdown(create_table(boys_wins, "Boys"), unsafe_allow_html=True)
    with col4:
        st.markdown(create_table(girls_wins, "Girls"), unsafe_allow_html=True)

# -----------------------------------------------------------------------------------------


# Create the plot
# def draw_plot(category, title, d_frame):

#     if not d_frame.empty and (d_frame["total_points"] > 0).any():
#         fig = px.pie(
#             d_frame,
#             values="total_points",
#             names=category,
#             title=title,
#             color_discrete_sequence=px.colors.qualitative.Pastel,
#             hole=0.3,
#         )

#         # Update layout for better appearance
#         fig.update_layout(
#             title_x=0.2,  # Center the title
#             title_font_size=16,
#             showlegend=True,
#             height=400,  # Control height
#             width=400,  # Control width
#             margin=dict(t=40, b=0, l=0, r=0),  # Adjust margins
#         )

#         return fig
#     else:
#         st.write("No data to plot or all values are zero")

#     # First school for comparison
#     with col3:
#         st.html("<br>")
#         fig2 = draw_plot(
#             "category",
#             "Distribution of Points Track Events VS Field Events",
#             chart_df_1,
#         )
#         st.plotly_chart(fig2, use_container_width=True, key=1)

#         st.html("<br>")
#         fig1 = draw_plot(
#             "sub_category", "Distribution of Points Event Type", chart_df_1
#         )
#         st.plotly_chart(fig1, use_container_width=True, key=2)

#     # Second school for comparison
#     with col4:
#         st.html("<br>")
#         fig2 = draw_plot(
#             "category",
#             "Distribution of Points Track Events VS Field Events",
#             chart_df_2,
#         )
#         st.plotly_chart(fig2, use_container_width=True, key=3)

#         st.html("<br>")
#         fig1 = draw_plot(
#             "sub_category", "Distribution of Points Event Type", chart_df_2
#         )
#         st.plotly_chart(fig1, use_container_width=True, key=4)


# intro -- what is champs
# some champs stats
# of events

# division of points among top school

# points lost
# % of athletes in finals from schools
# of schools that make finals
# are athletes running faster today

# Insights into the athletes and stats behind Champs victories.
# A deep dive into the history and performances of Boys and Girls Champs.
# % of how each class is performing of total possible points
