import streamlit as st
import pandas as pd
import numpy as np

# ---------------------- SETTINGS -----------------------------------#

primary_color: str = "#182536"
secondary_color: str = "#1874d0"
primary_text: str = "#fafbfd"
secondary_text: str = ""

header = f"""
    <div style='display: flex; align-items: baseline;'>
        <h1 style='color: {primary_color};'>Faster, Higher, Stronger:</h1>
        <h3 style='color: #536878;'>Analyzing the Athletes and Stats Behind Champs Glory</h3>
    </div>
"""
st.set_page_config(layout="wide")
st.markdown(header, unsafe_allow_html=True)
"---"

with open("css/style.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

# -------------------------------------------------------------------

intro: str = """
    <p>
    Boys and Girls Championship in annual track and field event in Jamaica. Here high schools 
    across the country come together in march and compete in an array of events spanning across several age groups. The winning schools are determind 
    by a points system where points awareded for position finished in the finals of each event.
    </p>
"""

st.markdown(intro, unsafe_allow_html=True)
# st.write(
#     """Boys and Girls Championship in annual track and field event in Jamaica. Here high schools
#          across the country come together in march and compete in an array of events spanning across several age groups. The winning schools are determind
#          by a points system where points awareded for position finished in the finals of each event."""
# )


# intro -- what is champs
# some champs stats
# of events
# Top times / distances
# division of points among top school
# total possible points
# points lost
# % of athletes in finals from schools
# of schools that make finals
# are athletes running faster today

# Insights into the athletes and stats behind Champs victories.
# A deep dive into the history and performances of Boys and Girls Champs.
