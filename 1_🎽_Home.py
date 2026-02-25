import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -------------------------- SETTINGS -------------------------------#

primary_color: str = "#182536"
secondary_color: str = "#1874d0"
primary_text: str = "#fafbfd"
secondary_text: str = "#536878"

header = f"""
    <div style='display: flex; align-items: baseline; flex-direction: column; width: 100%;'>
        <h1 style='color: {primary_color}; font-size: 2rem; margin-bottom: 0; padding-bottom: 0;'>Faster, Higher, Stronger:</h1>
        <h3 style='color: {secondary_text}; font-size: 1.4rem; padding-top: 6px;'>Analyzing the Athletes and Stats Behind Champs Glory</h3>
    </div>
"""
st.set_page_config(layout="wide")
# st.logo("assets/logo.jpeg", size="small")
st.markdown(header, unsafe_allow_html=True)
"---"

with open("css/style.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

# -------------------------------------------------------------------

# Data
points_system: pd.DataFrame = pd.read_csv("working_files/champs_points.csv")
champs_results: pd.DataFrame = pd.read_csv("working_files/champs_results.csv")
historical_winners: pd.DataFrame = pd.read_csv("working_files/historical_winners.csv")

# -------------------------------------------------------------------

intro: str = """
    <p>
    The <strong>Boys' and Girls' Championships</strong> is an annual track and field event in Jamaica, organized by the Inter-Secondary Schools Sports Association (ISSA). Over five days in March, high schools from across the country compete in a wide range of disciplines spanning multiple age groups. The winning schools are determined by a points system, with points awarded based on final placements in each event.
    </p>
    <p>
    Champs is the largest high school track and field competition in the world and is widely regarded as the breeding ground for many of Jamaica’s greatest athletes. Legendary sprinters such as Usain Bolt, Shelly-Ann Fraser-Pryce, Veronica Campbell-Brown, Michael Frater, and Melaine Walker all honed their talents on this stage.
    </p>
    <p>
    As a track and field fan and data enthusiast, I’ve always wanted to undertake a project focused on Champs. The purpose of this app is to dive deep into Champs data, examining schools and athlete performances, and sharing my insights. You can find more details about this project on the About page.
    </p>
    <p><Strong>Just a heads-up: the data currently runs from 2012 to 2024. 2013 is missing because I haven’t sourced that dataset yet, and there was no Champs in 2020 due to COVID-19.</Strong>
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
    f"<tr style='font-size: 0.8rem;'><td style='border: none; padding: 8px; color: #5b5b5b; text-align: left;'>{row['type']}</td>"
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
    <br>
    <h4 style='color: {primary_color};'>💯 Points System</h4>
    Athletes are awarded 9 points for winning an individual event, 7 points for finishing second, and 6 points for finishing third.
    For relays and combined events, winners are awarded 12 points, while second and third place earn 10 and 8 points, respectively.
    See table below for full points system.
    <p></p>
    <table style="width:70%; border: none; border-collapse: collapse;">
    <tr style="background-color: {primary_color}; text-align: center; color: {primary_text}; font-size: 0.8rem;">
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

    <p> A total of <strong>{calc_total_points("boys"):,}</strong> points is up for grabs for the males and <strong>{calc_total_points("girls"):,}</strong> for the females across <strong>{no_events}</strong> events each. The opportunities for points are spread across several classes and age groups, with the older student-athletes doing most of the heavy lifting. See graph 1 below. </p>
    <p>Each school is allowed to enter two athletes per individual event. The maximum possible points across all events and age categories are <strong>{max_points("boys")}</strong> for boys and <strong>{max_points("girls")}</strong> for girls. This assumes a school finishes first and second in individual events and secures first place in team events such as relays.</p>
    <p>On average, the winning team in the Girls Champs scores <strong>{get_avg_winning_point("Girls"):.2f}</strong> points for victory, while the boys average <strong>{get_avg_winning_point("Boys"):.2f}</strong> points to claim the Boys Champs title.</p> 
"""
st.markdown(points_system_txt, unsafe_allow_html=True)


# get total points possible for each age category
def age_group_points():
    points = (
        points_system.groupby(["gender", "class"])[
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


colors = ["#1249a1", "#1657c1", "#1863da", "#2871e7", "#4282ea"]

fig = px.bar(
    age_group_points(),
    y="total_points",
    x="gender",
    color="class",
    text_auto=True,
    title="      Possbile Points from Each Class",
    width=600,
    height=400,
)
# fig.update_traces(marker=dict(color=colors))
st.plotly_chart(
    fig, use_container_width=False, config={"staticPlot": True, "displayModeBar": False}
)

# ---------------------------------- How to Win ----------------------------------------

how_to_win = """
    <br>
    <h4 style='color: {primary_color};'>🏆 How to Win</h4>
    <p>The ultimate winner of the championship is determined by several key factors:</p>
    <ul>
        <li><strong>Active Recruiting:</strong> Top-performing schools actively recruit student-athletes from smaller, less traditional schools, other Caribbean nations, and even as far as African countries like Kenya. This approach helps them secure top-tier talent across multiple disciplines."</li>
        <li><strong>Numbers:</strong> Champs, at its core, is a numbers game. Winning schools must have a large pool of athletes competing in various events to maximize points. For smaller schools, this can be a major challenge, as depth across multiple disciplines is crucial for overall success.</li>
        <li><strong>Diversity Across Diciplines:</strong> A strong pipeline of athletes across all event types is essential. Sprint dominance alone is not enough—winning requires strength in middle and long-distance races, throws, jumps, and niche events like the pole vault. However, access to specialized equipment, such as pole vault gear and javelins, remains a significant barrier for non-traditional schools.</li>
        <li><strong>Financial Support:</strong> Any successful track and field program requires a steady influx of funding to cover essential expenses such as coaching salaries, gear and equipment, meal plans, and transportation to development meets. Without a significant and reliable source of funds, securing a Champs victory becomes nearly impossible. Schools that consistently perform well often have strong financial backing, whether through sponsorships, alumni support, allowing them to invest in athlete development and long-term success.</li>
        <li><strong>Elite Coaching & Training Facilities: </strong> Having experienced coaches who can refine technique, develop race strategies, and maximize athlete potential is crucial. Schools with access to high-quality training facilities, including modern gyms, recovery centers, and synthetic tracks, often have a competitive edge over those with limited resources.</li>
        <li><strong>Athlete Development & Injury Management:</strong>Longevity in the sport requires proper athlete development and injury prevention strategies. Schools with dedicated physiotherapists, nutritionists, and structured training programs can better maintain their athletes' peak performance throughout the season, reducing the risk of injuries that could derail their Champs campaign.</li>
    </ul>

    <p>Along with a solid strategy, the factors listed above cover most of what is required to win the Boys' or Girls' Championship. Until more of these hurdles—such as financial constraints, access to specialized equipment, and recruiting limitations—are overcome, the Champs titles will likely remain in the hands of the traditional powerhouse schools.</p>
"""

st.markdown(how_to_win, unsafe_allow_html=True)

# ---------------------------------- Past Winners ---------------------------------------


def get_most_wins(gender: str):
    most_wins = historical_winners[historical_winners["gender"] == gender]

    most_wins = (
        most_wins.groupby("school")
        .agg(wins=("year", "count"), years_won=("year", list))
        .reset_index()
    )
    most_wins.sort_values(by="wins", ascending=False, inplace=True)
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
hist_winners: str = f"""
    <br>
    <h4 style='color: {primary_color};'>📜 Past Winners</h4>
    <p>Historically, only <strong>{winners_boys}</strong> schools have ever won the Boys' Championship, with <strong>{get_most_wins("Boys").head(1)["school"].values[0]}</strong> holding the most titles. On the girls' side, <strong>{winners_girls}</strong> schools have won the coveted title, with <strong>{get_most_wins("Girls").head(1)["school"].values[0]}</strong> leading the count for the most wins.</p>
"""
st.markdown(hist_winners, unsafe_allow_html=True)


def create_table(df, gender):
    # Create HTML table with results
    table_rows = "".join(
        f"<tr style='font-size: 0.8rem;'><td style='border: none; padding: 8px; color: #5b5b5b; text-align: left;'>{row['school']}</td>"
        f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'><strong>{row['wins']}</strong></td>"
        f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'>{row['years_won']}</td></tr>"
        for _, row in df.iterrows()
    )

    past_winners_txt: str = f"""
        <h6 style='color: {secondary_text}; padding-bottom: 0;'> Schools with Champs Victories | {gender} Champs</h6>
        <p></p>
        <table style="width:100%; border: none; border-collapse: collapse;">
        <tr style="background-color: {primary_color}; text-align: center; color: {primary_text}; font-size: 0.8rem;">
            <th style="padding: 8px; text-align: left;">SCHOOL</th>
            <th style="padding: 8px; text-align: center;"># OF TITLES</th>
            <th style="padding: 8px; text-align: center;">YEARS</th>
        </tr>
        {table_rows}
        </table>
    """
    return past_winners_txt


col3, col4 = st.columns(2)

with st.container():
    with col3:
        st.markdown(create_table(boys_wins, "Boys"), unsafe_allow_html=True)
    with col4:
        st.markdown(create_table(girls_wins, "Girls"), unsafe_allow_html=True)

# -----------------------------------------------------------------------------------------
