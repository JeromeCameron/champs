import streamlit as st


# ------------------------ Settings -------------------------------------

primary_color: str = "#182536"
secondary_color: str = "#1874d0"
primary_text: str = "#fafbfd"
secondary_text: str = ""

with open("css/style.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

st.header("About")
"---"

st.markdown(
    """Boys and Girls Championship in annual track and field event in Jamaica.
    Here high schools across the country come together in march and compete in an array of events.
    The winning schools are determind by a points system where points awareded for position finished in the finals of each event.

    Questions i want to answer:

    Number of schools that participate each year.
    Who are the top athletes interms of medals over the period?
    Who are the top athlets based on total points over the period?
    What would the top five schools look like if medals were used to determine the winners"""
)
