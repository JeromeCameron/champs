import streamlit as st
import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings("ignore")

st.header("Boys and Girls Champs Winners 🏃🏾")
st.caption("2012 ➡️ Present")
st.html("<br>")

df = pd.read_csv("./working_files/champs_results.csv")

# Get Filters
st.text("Filter Results")
with st.container(border=True):
    col1, col2 = st.columns(2)
    with col1:
        year_series = df["year"].unique()
        year_series = np.sort(year_series)[::-1]
        year = st.selectbox("Year", year_series)
    with col2:
        gender = st.selectbox("Gender", ("Boys", "Girls"))


with st.container(border=False):
    col1, col2 = st.columns(2)
    with col1:
        sort_by = st.selectbox(
            "Sort by",
            ["Total Points", "Quality of Medals"],
            key="sort",
        )


def show_data() -> None:

    # Fiter results based on user input
    results = df[(df["year"] == int(year)) & (df["gender"] == gender)]

    # Adding medals column
    conditions = [
        (results["position"] == "1"),
        (results["position"] == "2"),
        (results["position"] == "3"),
    ]
    medals = ["Gold", "Silver", "Bronze"]

    results["medals"] = np.select(conditions, medals, "na")
    results["gold"] = np.where(results["medals"] == "Gold", 1, 0)
    results["silver"] = np.where(results["medals"] == "Silver", 1, 0)
    results["bronze"] = np.where(results["medals"] == "Bronze", 1, 0)

    # Based on total quality of medals won
    medalTable = results[["school", "gold", "silver", "bronze", "points"]]
    medalTable = medalTable.pivot_table(
        index="school",
        aggfunc=pd.Series.sum,
        values=["gold", "silver", "bronze", "points"],
    )

    if sort_by == "Total Points":
        medalTable = medalTable.sort_values(by="points", ascending=False)
        medalTable = medalTable.reindex(
            ["gold", "silver", "bronze", "points"], axis=1
        ).reset_index()
        medalTable = medalTable[medalTable["points"] > 0]
    else:
        medalTable = medalTable.sort_values(
            by=["gold", "silver", "bronze"], ascending=[False, False, False]
        )
        medalTable = medalTable.reindex(
            ["gold", "silver", "bronze", "points"], axis=1
        ).reset_index()
        medalTable = medalTable[medalTable["points"] > 0]

    # ------------------------------------------------------------------------------------------------------------------------------------------------

    # Header Row
    result_header = f"""
    <div style="background-color: #3856b2; padding: 6px; padding-left: 15px;">
        <h4 style='color: white; padding-bottom: 0; margin-bottom:0;'>{gender} Championship Winners 20{year} 🏆</h4>
        <h6 style='color: #e0e1e1; padding-top: 0; margin-top: 0;'>by {sort_by}</h6>
    </div>
    """
    st.markdown(result_header, unsafe_allow_html=True)

    # Create HTML table with results
    table_rows = "".join(
        f"<tr><td style='border: none; padding: 8px; color: #5b5b5b; text-align: left;'>{row['school']}</td>"
        f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'>{row['gold']}</td>"
        f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'><strong>{row['silver']}</strong></td>"
        f"<td style='border: none; padding: 8px; color: #030303; text-align: center;'>{row['bronze']}</td>"
        f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: center; background-color: #eaeaea; font-weight: bold;'>{row['points']}</td></tr>"
        for _, row in medalTable.iterrows()
    )

    table_html = f"""
    <table style="width:100%; border: none; border-collapse: collapse;">
    <tr style="background-color: #403f40; text-align: center; color: white;">
        <th style="padding: 8px; text-align: left;">SCHOOL</th>
        <th style="padding: 8px;">GOLD 🥇</th>
        <th style="padding: 8px;">SILVER 🥈</th>
        <th style="padding: 8px; ">BRONZE 🥉</th>
        <th style="padding: 8px;">TOTAL POINTS</th>
    </tr>
    {table_rows}
    </table>
    """

    st.markdown(table_html, unsafe_allow_html=True)


show_data()

# Breakdown of points. Where are the winning teams scoring their points
