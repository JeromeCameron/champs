import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Page header
st.header("Boy and Girls Champs Records 🐐")
st.html("<br>")

# Read csv file into dataframe
records_df = pd.read_csv("./working_files/champs_records.csv")
results_df = pd.read_csv("./working_files/champs_results.csv")

records_df["mark"] = records_df["mark"].str.strip("x")  # strip x from mark
records_df["record_age"] = (
    datetime.now().year - records_df["year"]
)  # add col for record age

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "Records",
        "Schools with Most Records",
        "Athletes with Most Records",
        "Oldest Records",
        "Top Performers",
    ]
)

with tab1:
    # Get Filters
    st.text("Filter Results")
    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            gender = st.selectbox("Gender", ("Boys", "Girls"))
        with col2:
            class_df = records_df[(records_df["gender"] == gender)]
            classes = class_df["clas_s"].unique()
            classes = np.sort(classes)
            clas_s = st.selectbox("Class", classes)

    # Fiter results based on user input
    records = records_df[
        (records_df["gender"] == gender) & (records_df["clas_s"] == clas_s)
    ]

    st.html("<br>")

    # Results Header Row
    result_header = f"""
    <div style='display: inline-block;'>
        <h3 style='color: #5b5859; border-collapse: collapse; border-top: 4px solid #029568; padding-top: 2px;'>Records</h3>
    </div>
    <div style="background-color: #029568; padding: 6px; padding-left: 15px; display: flex; align-items: center; justify-content: space-between;">
        <h4 style='color: white; display: inline-block;'>{gender.upper()} CLASS {clas_s} RECORDS </h4>
    </div>
    """
    st.markdown(result_header, unsafe_allow_html=True)

    # Create HTML table with results
    table_rows = "".join(
        f"<tr><td style='border: none; padding: 8px; color: #5b5b5b; text-align: left;'>{row['event']}</td>"
        f"<td style='border: none; padding: 8px; color: #030303; text-align: center; background-color: #eaeaea;'>{row['mark']}</td>"
        f"<td style='border: none; padding: 8px; color: #5b5b5b;'><strong>{row['athlete']}</strong></td>"
        f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'>{row['year']}</td>"
        f"<td style='border: none; padding: 8px; color: #5b5b5b;'>{row['school']}</td>"
        f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'>{row['record_age']}</td></tr>"
        for _, row in records.iterrows()
    )

    table_html = f"""
    <table style="width:100%; border: none; border-collapse: collapse;">
    <tr style="background-color: #403f40; text-align: center; color: white;">
        <th style="padding: 8px;">EVENT</th>
        <th style="padding: 8px;">PERFORMANCE</th>
        <th style="padding: 8px; text-align: left;">ATHLETE</th>
        <th style="padding: 8px;">YEAR</th>
        <th style="padding: 8px; text-align: left;">SCHOOL</th>
        <th style="padding: 8px; text-align: center;">RECORD AGE</th>
    </tr>
    {table_rows}
    </table>
    """
    # Show html table
    st.markdown(table_html, unsafe_allow_html=True)

with tab2:
    # Schools with the most records
    st.html("<br>")

    # Results Header Row
    result_header = """
    <div style='display: inline-block;'>
        <h3 style='color: #5b5859; border-collapse: collapse; border-top: 4px solid #029568; padding-top: 2px;'>Most Records</h3>
    </div>
    <div style="background-color: #029568; padding: 6px; padding-left: 15px; display: flex; align-items: center; justify-content: space-between;">
        <h4 style='color: white; display: inline-block;'>Top 10 schools with the most records </h4>
    </div>
    """

    st.markdown(result_header, unsafe_allow_html=True)

    most_records = records_df.groupby("school")["event"].count()
    most_records = most_records.sort_values(ascending=False)
    most_records = most_records.reset_index()
    top_ten = most_records.head(10)

    # Create HTML table with results
    table_rows = "".join(
        f"<tr><td style='border: none; padding: 8px; color: #5b5b5b; text-align: left;'>{row['school']}</td>"
        f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'>{row['event']}</td></tr>"
        for _, row in top_ten.iterrows()
    )

    table_html = f"""
    <table style="width:100%; border: none; border-collapse: collapse;">
    <tr style="background-color: #403f40; text-align: center; color: white;">
        <th style="padding: 8px; text-align: left;">SCHOOL</th>
        <th style="padding: 8px;">TOTAL RECORDS</th>
    </tr>
    {table_rows}
    </table>
    """
    # Show html table
    st.markdown(table_html, unsafe_allow_html=True)

    with tab4:
        # Oldest Records (Top 10)
        st.html("<br>")

        # Results Header Row
        result_header = """
        <div style='display: inline-block;'>
            <h3 style='color: #5b5859; border-collapse: collapse; border-top: 4px solid #029568; padding-top: 2px;'>Oldest Records</h3>
        </div>
        <div style="background-color: #029568; padding: 6px; padding-left: 15px; display: flex; align-items: center; justify-content: space-between;">
            <h4 style='color: white; display: inline-block;'>Top 15 oldest records </h4>
        </div>
        """
        st.markdown(result_header, unsafe_allow_html=True)

        oldest_records = records_df.sort_values("record_age", ascending=False)
        oldest_records = oldest_records.head(15)

        # Create HTML table with results
        table_rows = "".join(
            f"<tr><td style='border: none; padding: 8px; color: #5b5b5b; text-align: left;'>{row['event']}</td>"
            f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'>{row['clas_s']}</td>"
            f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'>{row['gender']}</td>"
            f"<td style='border: none; padding: 8px; color: #030303; text-align: center; background-color: #eaeaea;'>{row['mark']}</td>"
            f"<td style='border: none; padding: 8px; color: #5b5b5b;'><strong>{row['athlete']}</strong></td>"
            f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'>{row['year']}</td>"
            f"<td style='border: none; padding: 8px; color: #5b5b5b;'>{row['school']}</td>"
            f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'>{row['record_age']}</td></tr>"
            for _, row in oldest_records.iterrows()
        )

        table_html = f"""
        <table style="width:100%; border: none; border-collapse: collapse;">
        <tr style="background-color: #403f40; text-align: center; color: white;">
            <th style="padding: 8px; text-align: left;">EVENT</th>
            <th style="padding: 8px;">CLASS</th>
            <th style="padding: 8px;">GENDER</th>
            <th style="padding: 8px;">PERFORMANCE</th>
            <th style="padding: 8px; text-align: left;">ATHLETE</th>
            <th style="padding: 8px;">YEAR</th>
            <th style="padding: 8px; text-align: left;">SCHOOL</th>
            <th style="padding: 8px; text-align: center;">RECORD AGE</th>
        </tr>
        {table_rows}
        </table>
        """
        # Show html table
        st.markdown(table_html, unsafe_allow_html=True)

with tab3:
    # Athletes with Most Records
    st.html("<br>")

    # Results Header Row
    result_header = """
        <div style='display: inline-block;'>
            <h3 style='color: #5b5859; border-collapse: collapse; border-top: 4px solid #029568; padding-top: 2px;'>Athlete Records</h3>
        </div>
        <div style="background-color: #029568; padding: 6px; padding-left: 15px; display: flex; align-items: center; justify-content: space-between;">
            <h4 style='color: white; display: inline-block;'>Athlete with most records</h4>
        </div>
        """
    st.markdown(result_header, unsafe_allow_html=True)

    schools = records_df["school"].unique()

    athlete_records = records_df.groupby("athlete")["event"].count()
    athlete_records = athlete_records.sort_values(ascending=False)
    athlete_records = athlete_records.reset_index()
    athlete_records = athlete_records[athlete_records["event"] > 1]
    athlete_records = athlete_records[~athlete_records["athlete"].isin(schools)]

    athlete_records = athlete_records.head(15)

    # Create HTML table with results
    table_rows = "".join(
        f"<tr><td style='border: none; padding: 8px; color: #5b5b5b; text-align: left;'>{row['athlete']}</td>"
        f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'>{row['event']}</td></tr>"
        for _, row in athlete_records.iterrows()
    )

    table_html = f"""
        <table style="width:100%; border: none; border-collapse: collapse;">
        <tr style="background-color: #403f40; text-align: center; color: white;">
            <th style="padding: 8px; text-align: left;">ATHLETE</th>
            <th style="padding: 8px; text-align: center;"># OF RECORDS</th>
        </tr>
        {table_rows}
        </table>
        """
    # Show html table
    st.markdown(table_html, unsafe_allow_html=True)

    # Best Year for records
    # ----------------------------------------------------------------------------------------------------------------------
    with tab5:
        col1, col2 = st.columns(2)
        with col1:
            st.html("<br>")
            sort_by = st.selectbox(
                "Sort by",
                ["Total Points Earned", "Quality of Medals Won"],
                key="sort",
            )
        with col2:
            st.html("<br>")
            filter_by = st.selectbox(
                "Filter by",
                ["Boys", "Girls"],
                key="filter",
            )

        def show_data() -> None:

            # Fiter results based on user input
            results = results_df[results_df["gender"] == filter_by].copy()
            schools = results_df["school"].unique()

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
            medalTable = results[
                ["athlete", "school", "gold", "silver", "bronze", "points"]
            ]
            medalTable = medalTable.pivot_table(
                index=["athlete", "school"],
                aggfunc=pd.Series.sum,
                values=["gold", "silver", "bronze", "points"],
            )

            if sort_by == "Total Points Earned":
                medalTable = medalTable.sort_values(by="points", ascending=False)
                medalTable = medalTable.reindex(
                    ["gold", "silver", "bronze", "points"], axis=1
                ).reset_index()
                medalTable = medalTable[medalTable["points"] > 0]
                medalTable = medalTable[~medalTable["athlete"].isin(schools)]
                medalTable = medalTable.reset_index()
            else:
                medalTable = medalTable.sort_values(
                    by=["gold", "silver", "bronze"], ascending=[False, False, False]
                )
                medalTable = medalTable.reindex(
                    ["gold", "silver", "bronze", "points"], axis=1
                ).reset_index()
                medalTable = medalTable[medalTable["points"] > 0]
                medalTable = medalTable[~medalTable["athlete"].isin(schools)]
                medalTable = medalTable.reset_index()

            # ---------------------------------------------------------------------------------------------------------

            # Header Row
            result_header = f"""
            <div style="background-color: #3856b2; padding: 6px; padding-left: 15px;">
                <h4 style='color: white; padding-bottom: 0; margin-bottom:0;'>Top Athlete Performers🏆</h4>
                <h6 style='color: #e0e1e1; padding-top: 0; margin-top: 0;'>by {sort_by}</h6>
            </div>
            """
            st.markdown(result_header, unsafe_allow_html=True)

            # Create HTML table with results
            table_rows = "".join(
                f"<tr><td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'>{_ + 1}</td>"
                f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: left;'>{row['athlete']}</td>"
                f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: left;'>{row['school']}</td>"
                f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'>{row['gold']}</td>"
                f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'>{row['silver']}</td>"
                f"<td style='border: none; padding: 8px; color: #030303; text-align: center;'>{row['bronze']}</td>"
                f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: center; background-color: #eaeaea; font-weight: bold;'>{row['points']}</td></tr>"
                for _, row in medalTable.head(10).iterrows()
            )

            table_html = f"""
            <table style="width:100%; border: none; border-collapse: collapse;">
            <tr style="background-color: #403f40; text-align: center; color: white;">
                <th style="padding: 8px; text-align: center;">#</th>
                <th style="padding: 8px; text-align: left;">ATHLETE</th>
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

        show_data()  # display table data
