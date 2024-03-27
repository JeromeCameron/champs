from selectolax.parser import HTMLParser
import rich
import pandas as pd
from datetime import date
import os
from get_races import parse_race_event
from get_field_events import parse_field_event
from get_relays import parse_relay_event
from itertools import chain

PATH: str = "pages/"
SPRINTS: list = ["100 Meter Dash", "200 Meter Dash", "400 Meter Dash"]
HURDLES: list = [
    "60 Meter Hurdles",
    "80 Meter Hurdles",
    "100 Meter Hurdles",
    "110 Meter Hurdles",
    "400 Meter Hurdles",
]
MIDDLE_DISTANCES: list = ["800 Meter Run", "1500 Meter Run"]
LONG_DISTANCES: list = ["2000 Meter Steeplechase", "3000 Meter Run", "5000 Meter Run"]
RELAYS: list = ["4x100 Meter Relay", "4x400 Meter Relay", "1600 Sprint Medley"]
JUMPS: list = ["Long Jump", "Triple Jump", "High Jump", "Pole Vault"]
THROWS: list = ["Shot Put", "Discus Throw", "Javelin Throw"]
RACE_STAGES: list = ["Finals", "Prelims", "Semis"]


if __name__ == "__main__":
    """main starts here"""

race_type: str = RACE_STAGES[0]
results: list = []

for subdir, dirs, files in os.walk(PATH):
    for event_cat in MIDDLE_DISTANCES:
        for file in files:
            if (
                file.endswith(".html")
                and file.find(event_cat) >= 0
                and file.find(race_type) >= 0
            ):
                filename = os.path.join(subdir, file)

                with open(filename) as file:
                    page = file.read()
                    html = HTMLParser(page)
                    data = html.text()
                    file_title = os.path.basename(filename).title()
                    event = file_title.split(" ")
                    year = filename.split("/")[1].split("\\")[0]

                    res: list = parse_race_event(data, event, year)
                    res_dict = [x.dict() for x in res]
                    results.append(res_dict)

df = pd.DataFrame(list(chain.from_iterable(results)), dtype=str)
# rich.print(df[df["clas_s"] == "2"])
df.to_csv("csv_files/sprints.csv", index=False)

# TODO: Select event to scrape ✅
# TODO: Loop through folders for that event ✅
# TODO: Scrape event info and save to df ✅
# TODO: Write df data to csv File
# TODO: Correct 2012 Class 1 girsl 200 meter event
