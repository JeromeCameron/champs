import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.header("Boy and Girls Champs Records 🐐")
st.html("<br>")

df = pd.read_csv("./working_files/champs_records.csv")
df["mark"] = df["mark"].str.strip("x")

df["record_age"] = datetime.now().year - df["year"]

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Records",
        "Schools with Most Records",
        "Athletes with Most Records",
        "Oldest Records",
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
            class_df = df[(df["gender"] == gender)]
            classes = class_df["clas_s"].unique()
            classes = np.sort(classes)
            clas_s = st.selectbox("Class", classes)

    # Fiter results based on user input
    records = df[(df["gender"] == gender) & (df["clas_s"] == clas_s)]

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

    most_records = df.groupby("school")["event"].count()
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

        oldest_records = df.sort_values("record_age", ascending=False)
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

    athlete_records = df.groupby("athlete")["event"].count()
    athlete_records = athlete_records.sort_values(ascending=False)
    athlete_records = athlete_records.reset_index()
    athlete_records = athlete_records[athlete_records["event"] > 1]
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
    st.markdown(table_html, unsafe_allow_html=True)

    # Best Year for records
