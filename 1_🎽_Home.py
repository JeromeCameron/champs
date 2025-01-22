import streamlit as st
import pandas as pd
import numpy as np

# ---------------------- SETTINGS -----------------------------------#
page_title = "Boys and Girls Champs"
page_icon = "🏃🏾"
st.set_page_config(page_title=page_title, page_icon=page_icon)
st.title(page_title + " " + page_icon)
"---"


df = pd.read_csv("./working_files/track_events.csv")

# Adding medals column
conditions = [(df["position"] == "1"), (df["position"] == "2"), (df["position"] == "3")]
medals = ["Gold", "Silver", "Bronze"]

df["medals"] = np.select(conditions, medals, "na")
df["gold"] = np.where(df["medals"] == "Gold", 1, 0)
df["silver"] = np.where(df["medals"] == "Silver", 1, 0)
df["bronze"] = np.where(df["medals"] == "Bronze", 1, 0)

# Based on total points
df["points"] = df["points"].astype(float)
pointsTable = df[["school", "year", "gender", "points"]]
pointsTable = pointsTable[
    (pointsTable["year"] == 24) & (pointsTable["gender"] == "Boys")
]


pointsTable = (
    pointsTable.pivot_table(index="school", aggfunc=pd.Series.sum, values="points")
    .sort_values("points", ascending=False)
    .reset_index()
)


# Based on total quality of medals won
medalTable = df[["school", "year", "gender", "gold", "silver", "bronze", "points"]]
medalTable = medalTable[(medalTable["year"] == 24) & (medalTable["gender"] == "Boys")]
medalTable = medalTable.pivot_table(
    index="school", aggfunc=pd.Series.sum, values=["gold", "silver", "bronze", "points"]
)
medalTable = medalTable.sort_values(["gold", "silver", "bronze"], ascending=False)
medalTable = medalTable.reindex(
    ["gold", "silver", "bronze", "points"], axis=1
).reset_index()

st.table(medalTable)
