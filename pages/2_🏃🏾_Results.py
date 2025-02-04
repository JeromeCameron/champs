import streamlit as st
import pandas as pd

st.header("Champs Results 🏃🏾")
"---"

df = pd.read_csv("./working_files/track_events.csv")
df["note"] = df["note"].apply(
    lambda x: "" if pd.isna(x) else x
)  # Replace NaN values with an empty string
df["mark"] = df["mark"].str.rstrip("x")


st.text("Filter Results")
with st.container(border=True):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        year = st.text_input("Year", value=24, max_chars=2)
    with col2:
        gender = st.selectbox("Gender", ("Boys", "Girls"))
    with col3:
        clas_s = st.selectbox("Class", ("1", "2", "3", "4", "Open"))
    with col4:

        discipline = st.selectbox(
            "Discipline",
            (
                "100 Meter",
                "200 Meter",
                "400 Meter",
                "70 Meter Hurdles",
                "80 Meter Hurdles",
                "100 Meter Hurdles",
                "110 Meter Hurdles",
                "400 Meter Hurdles",
                "800 Meter Run",
                "1500 Meter Run",
                "2000 Meter Steeplechase",
                "3000 Meter Run",
                "5000 Meter Run",
                "Long Jump",
                "Triple Jump",
                "Shot Put",
                "Discus Throw",
                "Javelin Throw",
                "High Jump",
                "Pole Vault",
                "4x100 Meter Relay",
                "4x400 Meter Relay",
                "1600 Sprint Medley",
                "Decathlon",
                "Heptathlon",
            ),
        )


results = df[
    (df["year"] == int(year))
    & (df["gender"] == gender)
    & (df["clas_s"] == clas_s)
    & (df["event"] == discipline)
]

results.drop(["event", "gender", "clas_s", "heat", "typ", "year"], axis=1, inplace=True)
results.sort_values(by="position", inplace=True)
wind = results["wind"].iloc[0]

st.header("Final")
result_header = f"""
<div style="background-color: #633974; padding: 6px; padding-left: 15px;">
    <h4 style='color: white;'>{discipline.upper()} {gender.upper()} CLASS {clas_s} |   WIND: {wind}</h4>
</div>
"""
st.markdown(result_header, unsafe_allow_html=True)

# st.dataframe(
#     results,
#     hide_index=True,
#     column_order=("wind", "position", "name", "school", "mark", "points", "note"),
# )

# Generate table rows dynamically
table_rows = "".join(
    f"<tr><td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'>{row['position']}</td>"
    f"<td style='border: none; padding: 8px; color: #5b5b5b;'>{row['school']}</td>"
    f"<td style='border: none; padding: 8px; color: #5b5b5b;'>{row['name']}</td>"
    f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'>{row['mark']}</td>"
    f"<td style='border: none; padding: 8px; color: #5b5b5b; text-align: center;'>{row['points']}</td>"
    f"<td style='border: none; padding: 8px; color: #5b5b5b;'>{row['note']}</td></tr>"
    for _, row in results.iterrows()
)

table_html = f"""
<table style="width:100%; border: none; border-collapse: collapse;">
  <tr style="background-color: #273746; text-align: center; color: white;">
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
