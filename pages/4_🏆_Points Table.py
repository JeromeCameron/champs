import streamlit as st
import pandas as pd
import numpy as np
import warnings
import plotly.express as px

warnings.filterwarnings("ignore")

# ------------------------ Settings -------------------------------------

primary_color: str = "#182536"
secondary_color: str = "#1874d0"
primary_text: str = "#fafbfd"
secondary_text: str = ""

with open("css/style.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

st.header("Boys and Girls Champs Point Table | Historical 🏃🏾")
st.caption("2012 ➡️ Present")
st.html("<br>")
"---"
# ----------------------------------------------------------------------

df = pd.read_csv("./working_files/champs_results.csv")


# Get Filters
st.text("Filter Results")
with st.container(border=True):
    col1, col2 = st.columns(2)
    with col1:
        year_series = df["year"].unique()
        year_series = np.sort(year_series)[::-1]
        year_series = year_series[year_series != 13]
        year = st.selectbox("Year", year_series)
    with col2:
        gender = st.selectbox("Gender", ("Boys", "Girls"))

tab1, tab2 = st.tabs(["Points Table", "Points Breakdown - Top 15 Schools"])

# ---------------------- Winners based and points or quality of medals ---------------------
with tab1:
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

        # ---------------------------------------------------------------------------------------------------------

        # Header Row
        result_header = f"""
        <div style="background-color: {primary_color}; padding: 6px; padding-left: 15px;">
            <h4 style='color: white; padding-bottom: 0; margin-bottom:0;'>{gender} Championship Winners 20{year} 🏆</h4>
            <h6 style='color: {primary_text}; padding-top: 0; margin-top: 0;'>by {sort_by}</h6>
        </div>
        """
        st.markdown(result_header, unsafe_allow_html=True)

        # Create HTML table with results
        table_rows = "".join(
            f"<tr><td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'>{_ + 1}</td>"
            f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: left;'>{row['school']}</td>"
            f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'>{row['gold']}</td>"
            f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'><strong>{row['silver']}</strong></td>"
            f"<td style='border: none; padding: 8px; color: #030303; text-align: center;'>{row['bronze']}</td>"
            f"<td style='border: none; padding: 8px; color: {primary_text}; text-align: center; background-color: {secondary_color};'><strong>{row['points']}</strong></td></tr>"
            for _, row in medalTable.iterrows()
        )

        table_html = f"""
        <table style="width:100%; border: none; border-collapse: collapse;">
        <tr style="background-color: {secondary_color}; text-align: center; color: {primary_text};">
            <th style="padding: 8px; text-align: center;">#</th>
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

# --------------------------------------------------- Tab | Points Breakdown -------------------------------------------------------

with tab2:
    with st.container():
        # ---------------------------- Breakdown of points. Where are the winning teams scoring their points --------------------

        # Fiter results based on user input
        df_points = df[(df["year"] == int(year)) & (df["gender"] == gender)]

        points_df = (
            df_points.groupby(["school", "sub_category"])["points"]
            .sum()
            .unstack(fill_value=0)
            .reset_index()
        )

        if "Long Distance" not in points_df.columns:
            points_df["Long Distance"] = 0

        points_df["total_points"] = points_df[
            [
                "Combined Events",
                "Hurdles",
                "Jumps",
                "Long Distance",
                "Middle Distance",
                "Relay",
                "Sprints",
                "Throws",
            ]
        ].sum(axis=1)

        points_df = points_df.sort_values(by="total_points", ascending=False)
        points_df = points_df[points_df["total_points"] > 0]
        points_df = points_df.reset_index()

        # Header Row
        result_header = f"""
        <div style="background-color: {primary_color}; padding: 6px; padding-left: 15px;">
            <h4 style='color: white; padding-bottom: 0; margin-bottom:0;'>{gender} Championship Winners 20{year} 🏆</h4>
            <h6 style='color: {primary_text}; padding-top: 0; margin-top: 0;'>by {sort_by}</h6>
        </div>
        """
        st.markdown(result_header, unsafe_allow_html=True)

        # Create HTML table with results
        table_rows = "".join(
            f"<tr><td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'>{_ + 1}</td>"
            f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: left;'>{row['school']}</td>"
            f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'>{row['Sprints']}</td>"
            f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'>{row['Hurdles']}</td>"
            f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'>{row['Middle Distance']}</td>"
            f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'>{row['Long Distance']}</td>"
            f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'>{row['Relay']}</td>"
            f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'>{row['Jumps']}</td>"
            f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'>{row['Throws']}</td>"
            f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'>{row['Combined Events']}</td>"
            f"<td style='border: none; padding: 8px; color: {primary_text}; text-align: center; background-color: {secondary_color};'><strong>{row['total_points']}</strong</td></tr>"
            for _, row in points_df.head(15).iterrows()
        )

        table_html = f"""
        <table style="width:100%; border: none; border-collapse: collapse;">
        <tr style="background-color: {secondary_color}; text-align: center; color: {primary_text};">
            <th style="padding: 8px; text-align: center;">#</th>
            <th style="padding: 8px; text-align: left;">SCHOOL</th>
            <th style="padding: 8px;">SPRINTS</th>
            <th style="padding: 8px;">HURDLES</th>
            <th style="padding: 8px;">MIDDLE DISTANCE</th>
            <th style="padding: 8px;">LONG DISTANCE</th>
            <th style="padding: 8px;">RELAY</th>
            <th style="padding: 8px;">JUMPS</th>
            <th style="padding: 8px;">THROWS</th>
            <th style="padding: 8px;">COMBINED EVENTS</th>
            <th style="padding: 8px;">TOTAL POINTS</th>
        </tr>
        {table_rows}
        </table>
        """

        st.markdown(table_html, unsafe_allow_html=True)
        "---"
        # Charts to show the distribution of points
        st.html("<br>")
        # Get Filters
        st.text("Compare School Points Distributions")
        with st.container(border=True):

            school_series = points_df["school"].unique()
            school_series = "" + np.sort(school_series)
            school_l_col, school_2_col = st.columns(2)

            with school_l_col:
                school_1 = st.selectbox(
                    "School 1", school_series, placeholder="Choose a school to compare"
                )
            with school_2_col:
                school_2 = st.selectbox(
                    "School 2", school_series, placeholder="Choose a school to compare"
                )

            chart_df = df_points.fillna(0)
            chart_df = chart_df[["sub_category", "points", "category"]]

            # Chart 1
            chart_df_1 = chart_df[(df_points["school"] == school_1)].copy()

            # Chart 2
            chart_df_2 = df_points[(df_points["school"] == school_2)].copy()

        col3, col4 = st.columns(2)

        # Create the plot
        def draw_plot(category, title, d_frame) -> None:

            if not d_frame.empty and (d_frame["points"] > 0).any():
                fig = px.pie(
                    d_frame,
                    values="points",
                    names=category,
                    title=title,
                    color_discrete_sequence=px.colors.qualitative.Pastel,
                    hole=0.3,
                )

                # Update layout for better appearance
                fig.update_layout(
                    title_x=0.2,  # Center the title
                    title_font_size=16,
                    showlegend=True,
                    height=400,  # Control height
                    width=400,  # Control width
                    margin=dict(t=40, b=0, l=0, r=0),  # Adjust margins
                )

                return fig
            else:
                st.write("No data to plot or all values are zero")

        # First school for comparison
        with col3:
            st.html("<br>")
            fig2 = draw_plot(
                "category",
                "Distribution of Points Track Events VS Field Events",
                chart_df_1,
            )
            st.plotly_chart(fig2, use_container_width=True, key=1)

            st.html("<br>")
            fig1 = draw_plot(
                "sub_category", "Distribution of Points Event Type", chart_df_1
            )
            st.plotly_chart(fig1, use_container_width=True, key=2)

        # Second school for comparison
        with col4:
            st.html("<br>")
            fig2 = draw_plot(
                "category",
                "Distribution of Points Track Events VS Field Events",
                chart_df_2,
            )
            st.plotly_chart(fig2, use_container_width=True, key=3)

            st.html("<br>")
            fig1 = draw_plot(
                "sub_category", "Distribution of Points Event Type", chart_df_2
            )
            st.plotly_chart(fig1, use_container_width=True, key=4)


# Total potential points based on number of athletes that got into the finals
# Points lost
## make graph colours standard across events in charts
