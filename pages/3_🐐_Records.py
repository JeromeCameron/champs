import streamlit as st
import pandas as pd

st.header("Champs Records 🐐")

df = pd.read_csv("./working_files/champs_records.csv")
df["mark"] = df["mark"].str.strip("x")
df.rename(
    columns={
        "event": "Event",
        "clas_s": "Class",
        "mark": "Perf",
        "athlete": "Athlete",
        "year": "Year",
        "school": "School",
    },
    inplace=True,
)


tab1, tab2 = st.tabs(["👦🏾 Boys", "👧🏾 Girls"])

with tab1:
    st.subheader("Boys Records")
    boys_records = df[df["gender"] == "Boys"]
    boys_records = boys_records.drop(columns=["gender"])
    boys_records = boys_records.reset_index(drop=True)
    st.table(boys_records)

with tab2:
    st.subheader("Girls Records")
    st.table(df[df["gender"] == "Girls"])
