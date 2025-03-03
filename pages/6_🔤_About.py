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
# ----------------------------------------------------------------------

about_intro = """
    <p>
    I've always been a fan of track and field—hell, I even used to run myself! 😅 The Boys and Girls Championships have fascinated me for as long as I can remember, and I've been watching and following them closely over the years. As a data enthusiast, I've always wanted to dive deep into Champs data to answer the many questions that have been on my mind. This app is my attempt to uncover those answers.
    </p>

    <ul>
        <li>Who are the top athletes in terms of total medals over the years?</li>
        <li>Who are the top athletes based on total points accumulated?</li>
        <li>What would the rankings look like if medals, rather than points, determined the winners?</li>
        <li>How have performances progressed over the years in terms of times and distances?</li>
        <li>How are points distributed across different events?</li>
        <li></li>
    </u>
"""
st.markdown(about_intro, unsafe_allow_html=True)

how_method = """

"""


st.markdown(
    """
    who i am , what is this and why im doing this
    how i did this
        getting data
        cleaning data
        presenting data
    what i hope to achive
    
    """
)
