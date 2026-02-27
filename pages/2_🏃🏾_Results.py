import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from utils import seconds_to_minutes, time_to_seconds

# -------------------- Settings -------------------------------#

primary_color: str = "#182536"
secondary_color: str = "#1874d0"
primary_text: str = "#fafbfd"
secondary_text: str = ""

header = f"""
    <div style='display: flex; align-items: baseline;'>
        <h1 style='color: {primary_color}; font-size: 2rem;'>Results Over The Years</h1>
    </div>
"""
st.set_page_config(layout="wide")
# st.logo("assets/logo.jpeg", size="small")
st.markdown(header, unsafe_allow_html=True)
st.caption("2012 ➡️ Present (excluding 2013 and 2020)")


with open("css/style.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

# ----------------------------------------------------------------

df = pd.read_csv("./working_files/champs_results.csv")
df["note"] = df["note"].apply(
    lambda x: "" if pd.isna(x) else x
)  # Replace NaN values with an empty string
df["points"] = df["points"].fillna(0)
df["mark"] = df["mark"].str.rstrip("x R X m M")
df["position"] = pd.to_numeric(df["position"], errors="coerce").astype(
    "Int64"
)  # convert position to int ignoring nan values

records = pd.read_csv("./working_files/champs_records.csv")
records["mark"] = records["mark"].str.rstrip("x R X m M")

tab1, tab2 = st.tabs(["Filter By Event", "Filter by Athlete"])

with tab1:
    # Get Filters
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
                (df["gender"] == gender)
                & (df["clas_s"] == clas_s)
                & (df["year"] == year)
            ]

            events = sorted(events_df["event"].unique())

            if "discipline" not in st.session_state:
                st.session_state.discipline = None

            # If no events available
            if len(events) == 0:
                discipline = None
                st.selectbox("Discipline", ["No events"], disabled=True)
            else:
                # If previous discipline not valid, reset
                if st.session_state.discipline not in events:
                    st.session_state.discipline = events[0]

                current_index = events.index(st.session_state.discipline)

                discipline = st.selectbox("Discipline", events, index=current_index)

                st.session_state.discipline = discipline

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
        f"<tr style='font-size: 0.8rem;'><td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'>{row['position']}</td>"
        f"<td style='border: none; padding: 8px; color: #5b5b5b;'>{row['school']}</td>"
        f"<td style='border: none; padding: 8px; color: #5b5b5b;'><strong>{row['athlete']}</strong></td>"
        f"<td style='border: none; padding: 8px; color: {primary_text}; text-align: center; background-color: {secondary_color};'><strong>{row['mark']}</strong></td>"
        f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'>{row['points']}</td>"
        f"<td style='border: none; padding: 8px; color: #5b5b5b;'>{row['note']}</td></tr>"
        for _, row in results.iterrows()
    )

    table_html = f"""
    <table style="width:100%; border: none; border-collapse: collapse;">
    <tr style="background-color: {primary_color}; text-align: center; color: {primary_text}; font-size: 0.8rem;">
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

with tab2:
    # Get Filters
    with st.container(border=True):
        (
            col5,
            col6,
        ) = st.columns(2)

        with col5:
            gender = st.selectbox("Gender", ("Boys", "Girls"), key="athlete_box")
        with col6:
            athlete_series = df[["gender", "athlete"]].copy()
            athlete_series = athlete_series[athlete_series["gender"] == gender]
            schools = df["school"].unique()
            athlete_series = athlete_series[~athlete_series["athlete"].isin(schools)]
            athlete_series = athlete_series["athlete"].unique()
            athlete_series = np.sort(athlete_series)
            athlete = st.selectbox("Athlete", athlete_series)

    # Fiter results based on user input
    athlete_events = df[(df["gender"] == gender) & (df["athlete"] == athlete).copy()]

    athlete_events = athlete_events.sort_values(
        by=["event", "year"]
    ).copy()  # sort by event name and year

    event_df_series = athlete_events["event"].unique()
    event_list = event_df_series.tolist()
    event_list = ", ".join(event_list)

    # st.html("<br>")

    # Results Header Row
    result_header = f"""
        <div style="background-color: {primary_color}; padding: 6px; padding-left: 15px;">
            <div style="padding-bottom: 0;">
                <h4 style='color: {primary_text}; display: inline-block; padding-bottom: 0;'>{athlete.upper()}</h4>
                <p style='color: {primary_text}; font-size: 0.8rem;'>Events: {event_list}.</p> 
            </div>
        </div>
    """
    st.markdown(result_header, unsafe_allow_html=True)

    # Create HTML table with results
    table_rows = "".join(
        f"<tr style='font-size: 0.8rem;'><td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'>{row['year']}</td>"
        f"<td style='border: none; padding: 8px; color: #5b5b5b;'>{row['event']}</td>"
        f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'>{row['clas_s']}</td>"
        f"<td style='border: none; padding: 8px; color: #5b5b5b;'>{row['school']}</td>"
        f"<td style='border: none; padding: 8px; color: {primary_text}; text-align: center; background-color: {secondary_color};'><strong>{row['mark']}</strong></td>"
        f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'>{row['points']}</td>"
        f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'>{row['position']}</td>"
        f"<td style='border: none; padding: 8px; color: #5b5b5b;'>{row['note']}</td></tr>"
        for _, row in athlete_events.iterrows()
    )

    table_athlete_events = f"""
    <table style="width:100%; border: none; border-collapse: collapse;">
    <tr style="background-color: {primary_color}; text-align: center; color: {primary_text}; font-size: 0.8rem;">
        <th style="padding: 8px;">YEAR</th>
        <th style="padding: 8px; text-align: left;">EVENT</th>
        <th style="padding: 8px;">CLASS</th>
        <th style="padding: 8px; text-align: left;">SCHOOL</th>
        <th style="padding: 8px;">MARK</th>
        <th style="padding: 8px;">POINTS</th>
        <th style="padding: 8px;">POSITION</th>
        <th style="padding: 8px;">NOTE</th>
    </tr>
    {table_rows}
    </table>
    """
    st.markdown(table_athlete_events, unsafe_allow_html=True)

    # show  athlete progression with graph
    selected_event = st.selectbox("Event", athlete_events["event"].unique())
    athlete_sel_event = athlete_events[athlete_events["event"] == selected_event].copy()
    athlete_sel_event["year"] = athlete_sel_event["year"].astype(int)
    athlete_sel_event.sort_values(by="year", inplace=True)  # sort by year
    athlete_sel_event.sort_values(by="mark", inplace=True)

    athlete_sel_event["mark"] = athlete_sel_event["mark"].str.rstrip(
        "x R X m M"
    )  # Strip str from mark

    # ---------------- Track Events -----------------------------------------
    tr_events = athlete_sel_event[(df["category"] == "Track Event")].copy()

    tr_events["mark"] = tr_events["mark"].astype(str)

    tr_events["time_seconds"] = tr_events["mark"].apply(time_to_seconds)
    tr_events.sort_values(by="time_seconds", inplace=True)  # sort by time

    tr_events["mark"] = tr_events["time_seconds"]
    # tr_events["mark"] = tr_events["time_seconds"].apply(seconds_to_minutes)

    # ---------------------- Field Events --------------------------------------
    fi_events = athlete_sel_event[
        (df["category"] == "Field Event")
        | (df["category"] == "Combined Events") & (df["mark"].notna())
    ].copy()

    fi_events["mark"] = pd.to_numeric(fi_events["mark"], errors="coerce")
    fi_events.sort_values(by="mark", inplace=True)  # sort by distance

    # --------------------------------------------------------------------------

    performances = pd.concat([tr_events, fi_events])
    performances = performances.sort_values("year")
    performances["mark"] = pd.to_numeric(performances["mark"], errors="coerce")

    # Calculate buffers for the y-axis (from earlier)
    ymin, ymax = performances["mark"].min(), performances["mark"].max()
    padding = (ymax - ymin) * 0.1

    x = performances["year"]
    y = performances["mark"]

    performances["formatted_mark"] = [
        (
            seconds_to_minutes(row["mark"])
            if row["category"] == "Track Event"
            else f"{row['mark']:.2f}"
        )
        for _, row in performances.iterrows()
    ]

    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)

    trend_y = p(x)

    # 1. Create the base chart
    fig = px.line(
        performances,
        x="year",
        y="mark",
        # color=performances["clas_s"].astype(str),
        markers=True,
        template="simple_white",
        labels={"mark": "Performance", "year": "Year"},
        hover_data={
            "wind": True,
            "position": True,
            "school": True,
            "mark": False,  # we'll control this manually
        },
    )

    # 2. Add dynamic flare: Smooth lines and donut markers
    fig.update_traces(
        line_shape="linear",
        line_width=4,
        marker=dict(size=12, line=dict(width=2, color="white")),
        cliponaxis=False,
        customdata=performances[["wind", "position", "formatted_mark"]].values,
        hovertemplate="<b>Year:</b> %{x}<br>"
        "<b>Performance:</b> %{customdata[2]}<br>"
        "<b>Wind:</b> %{customdata[0]} m/s<br>"
        "<b>Position:</b> %{customdata[1]}<br>"
        "<extra></extra>",
    )

    # 3. Dynamic Annotation: Auto-locate the overall best point
    if not tr_events.empty:
        best_idx = performances["mark"].idxmin()
        fig.update_yaxes(autorange="reversed")
        tick_vals = np.linspace(ymin, ymax, 6)  # 6 clean ticks
        tick_text = [seconds_to_minutes(val) for val in tick_vals]
        fig.update_yaxes(tickvals=tick_vals, ticktext=tick_text)

    else:
        best_idx = performances["mark"].idxmax()
        fig.update_yaxes(tickformat=".2f")

    best_val = performances.loc[best_idx]

    if not tr_events.empty:
        best_display = seconds_to_minutes(best_val["mark"])
    else:
        best_display = f"{best_val['mark']:.2f}"

    best_label = f"<b>All-Time Best</b><br>{best_display}"

    fig.add_annotation(
        x=best_val["year"],
        y=best_val["mark"],
        text=best_label,
        showarrow=True,
        arrowhead=3,
        arrowsize=1.5,
        arrowwidth=2,
        ax=0,
        ay=-50,
        bgcolor="white",
        bordercolor="black",
        borderpad=4,
    )

    fig.update_xaxes(
        tickmode="linear",
        tick0=performances["year"].min(),
        dtick=1,
        fixedrange=True,
        gridcolor="whitesmoke",
    )

    # 4. Cleanup and Spacing
    fig.update_layout(
        title={
            "text": f"<b>Performance Analysis: {selected_event}</b>",
            "x": 0.05,
            "y": 0.95,
        },
        margin=dict(l=20, r=20, t=100, b=100),
        yaxis=dict(range=[ymin - padding, ymax + padding], fixedrange=True),
        xaxis=dict(fixedrange=True),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    fig.add_scatter(
        x=[best_val["year"]],
        y=[best_val["mark"]],
        mode="markers",
        marker=dict(size=20, symbol="circle", line=dict(width=4), color="orange"),
        showlegend=False,
    )

    fig.add_scatter(
        x=x,
        y=trend_y,
        mode="lines",
        line=dict(
            dash="dot",
            width=2,
        ),
        name="Trend",
        showlegend=False,
    )

    st.plotly_chart(fig, config={"displayModeBar": False})
