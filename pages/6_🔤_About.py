import streamlit as st


# ------------------------ Settings -------------------------------------

primary_color: str = "#182536"
secondary_color: str = "#1874d0"
primary_text: str = "#fafbfd"
secondary_text: str = ""


header = f"""
    <div>
        <h1 style='color: {primary_color}; font-size: 2rem;'>What is this all about and how did i do it...? 🤔</h1>
    </div>
"""
st.set_page_config(layout="wide")
st.logo("assets/logo.jpeg", size="large")
st.markdown(header, unsafe_allow_html=True)
"---"

with open("css/style.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

# ----------------------------------------------------------------------

about_intro = """
    <p>
    I've always been a fan of track and field—hell, I even used to run competively a the junior level myself 🤫😅! The Boys and Girls Championships have fascinated me for as long as I can remember, and I've been watching and following them closely over the years. As a data enthusiast, I've always wanted to dive deep into Champs data to answer the many questions that have been on my mind. This app is my attempt to uncover those answers.
    </p>
    <ul>
        <li>Who are the top athletes in terms of total medals over the years?</li>
        <li>Who are the top athletes based on total points accumulated?</li>
        <li>What would the rankings look like if medals, rather than points, determined the winners?</li>
        <li>How have performances progressed over the years in terms of times and distances?</li>
        <li>How are points distributed across different events?</li>
        <li>Among others.</li>
    </u>
    <p>I also wanted to present this data in a format that is easy to digest, searchable, and accessible all in one place.</p>
"""
st.markdown(about_intro, unsafe_allow_html=True)

how_method = f"""
    <div>
        <h4 style='color: {primary_color};'>The How Behind It All</h4>
        <p>This project has gone through multiple phases to reach its current state. Below, I break down each stage:</p>
        <br>
        <h5 style='color: #879596;'>Data Gathering</h5>
        <p>
        With the idea embedded in my head, the next step was gathering the data needed to bring this project to life. I scoured the internet for websites hosting Champs data but kept running into poorly formatted PDFs that I was unwilling to parse. So, I started asking around and was finally pointed in the right direction. I was told I could find this information at <a href='https://issasports.com/results/'>https://issasports.com/results</a> and so it began...
        </p>
        <p>
        I started by writing a Python script to download the results for each event across multiple years. This allowed me to continuously test various parsing methods without needing to access the site each time or bombard their servers with a stream of requests. Instead, I could simply work with the files locally.
        </p>
    </div>
"""
st.markdown(how_method, unsafe_allow_html=True)
get_pages = """
    async def main() -> None:

    async with httpx.AsyncClient(verify=False) as client:
        # get data
        year = 0  # Set at run

        while year <= 24:
            links = await get_links(year=str(year), client=client)

            if links:
                for key, value in links.items():
                    rich.print(f"Getting {value}")
                    await get_pages(link=key, year=str(year), name=value, client=client)

            year += 1

if __name__ == "__main__":
 
    asyncio.run(main())
"""
st.caption("Sample Code - Called functions missing")
st.code(get_pages, language="python", wrap_lines=True)

how_method_part2 = """
    <p>Getting the data was the easy part; parsing the information was tedious because the way the data was presented across events and years lacked consistency. Writing a one-size-fits-all script wasn't going to work, but writing a script for each year would be inefficient. So, I had to identify all the commonalities and write the most versatile script I could, incorporating conditionals to extract the data I needed and saved it to a CSV file. An simple example of this inconsistency is that in 2023, the athlete numbers were included, but in 2024, they were not. Additionally, the names of athletes and schools were sometimes shortened or had parts completely missing. See the images below:</P>
"""
st.markdown(how_method_part2, unsafe_allow_html=True)

col1, col2 = st.columns(2)

with st.container():
    with col1:
        st.image(
            "assets/2023_example.png",
            caption="2023 Class 1 Boys 100M Finals",
            use_container_width=True,
        )
    with col2:
        st.image(
            "assets/2024_example.png",
            caption="2024 Class 1 Boys 100M Finals",
            use_container_width=True,
        )

with st.expander("See the code snippet used to parse athlete names below:"):
    code_sample_2 = """
    def get_athlete_name(result: list) -> str:
    '''Returns athlete name'''

    athlete_name = ""

    lst: list = list(filter(None, result.split("   ")))
    lst = [ele for ele in lst if ele.strip()]

    try:
        if lst != []:  # ignore empty lists
            if len(lst[0]) > 6:
                athlete_name = lst[0].rsplit(" ")

            else:
                athlete_name = lst[1].rsplit(" ")

            athlete_name = athlete_name[-2:][0] + " " + athlete_name[-2:][1]

            # if len(athlete_name) >= 5:
            #     athlete_name = " ".join(athlete_name[3:])
            # else:
            #     athlete_name = " ".join(athlete_name[1:])
    except IndexError:
        athlete_name = "nil"

    return athlete_name


    def parse_race_event(data, event, year):
    '''Parse details for race events [100m to 1500m events] - Finals'''

    lst: list = []  # will contian all results details
    other_details = []

    # Split original data into manageble trunks
    parshal = data.partition("Finals                          ")[2]
    results = parshal.partition("=======")[0].splitlines()

    # Get event details
    event_details: list = get_event_details(event)

    for line in results:
        # Loop through results and parse details

        athlete: str = get_athlete_name(line)
        school: str = get_school(line, event, year)
        other_details = list(filter(None, line.split(" ")))

        # Get other race details
        if other_details != []:
            if "#" in other_details:
                other_details.remove("#")
                other_details.pop(1)

            if "--" in other_details:
                other_details.append("")

            position = other_details[0] if other_details[0].isdigit() else 0

            # ----------points------------------
            if int(position) > 8 or int(position) == 0:
                points = "0"
            else:
                points = other_details[-1]

            # ----------mark------------------
            try:
                if int(event[4]) > 200 and len(points) < 3:
                    mark = other_details[-2]
                elif int(event[4]) > 4 and len(points) > 3:
                    mark = other_details[-4]
                else:
                    mark = other_details[-3]
            except ValueError:
                mark = other_details[-2]

            if int(position) > 8:
                # gets mark if athlete is out of the top 8 finishers
                mark = other_details[-1]
            # ----------------------------
            if len(points) > 3:
                points = other_details[-2]
                wind = other_details[-3]
            else:
                wind = other_details[-2]

            try:
                if int(event[4]) > 200:
                    wind = None
                else:
                    wind = wind
            except ValueError:
                wind = None

            # ----------------------------
            # create pydantic dataclass
            result = TrackEvents(
                event=event_details[0],
                gender=event_details[1],
                clas_s=event_details[2],
                heat=event_details[3],
                typ=event_details[4],
                wind=wind,
                name=athlete,
                year=year,
                position=other_details[0],
                school=school,
                mark=mark + "x",
                points=points,
            )

            lst.append(result)

    return lst
"""
    st.code(code_sample_2, language="python")
st.markdown(
    "<p>All of this made the next step—data cleaning—very time-consuming.</p>",
    unsafe_allow_html=True,
)

data_cleaning = """
    <h5 style='color: #879596;'>Data Cleaning</h5>
    <p></p>
"""
st.markdown(data_cleaning, unsafe_allow_html=True)


st.markdown(
    """
        presenting data  
    """
)
