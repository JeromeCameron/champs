import streamlit as st
import pandas as pd

st.header("Champs Results 🏃🏾")
"---"

df = pd.read_csv("./working_files/track_events.csv")

st.text("Filter Results")
with st.container(border=True):
    col1, col2 = st.columns(2)
    with col1:
        year = st.text_input("Year", value=2024, max_chars=4)
        gender = st.selectbox("Gender", ("Boys", "Girls"))

    with col2:
        clas_s = st.selectbox("Class", (1, 2, 3, "Open"))
        discipline = st.selectbox(
            "Discipline",
            (
                "100 Meter Dash",
                "200 Meter Dash",
                "400 Meter Dash",
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
df = df[df["year"] == 24]
st.table(df)
