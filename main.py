import rich
import pandas as pd
from get_races import parse_race_event
from get_field_events import parse_field_event
from get_relays import parse_relay_event
from utils import genearate_df
import asyncio

PATH: str = "pages/"
TRACK_EVENTS: list = [
    "100 Meter Dash",
    "200 Meter Dash",
    "400 Meter Dash",
    "60 Meter Hurdles",
    "80 Meter Hurdles",
    "100 Meter Hurdles",
    "110 Meter Hurdles",
    "400 Meter Hurdles",
    "800 Meter Run",
    "1500 Meter Run",
    "2000 Meter Steeplechase",
    "3000 Meter Run",
    "5000 Meter Run",
]
RELAYS: list = ["4x100 Meter Relay", "4x400 Meter Relay", "1600 Sprint Medley"]
MULTI_EVENTS: list = ["Dec", "Hept"]
JUMPS: list = ["Long Jump", "Triple Jump", "High Jump", "Pole Vault"]
THROWS: list = ["Shot Put", "Discus Throw", "Javelin Throw"]
RACE_STAGES: list = ["Finals", "Prelims", "Semis"]


if __name__ == "__main__":
    """main starts here"""

    track_events_df: pd.DataFrame = genearate_df(
        func=parse_race_event,
        race_type="Finals",
        race_categories=TRACK_EVENTS,
        path=PATH,
    )

    relays_df: pd.DataFrame = genearate_df(
        func=parse_relay_event,
        race_type="Finals",
        race_categories=RELAYS,
        path=PATH,
    )

frames: list = [track_events_df, relays_df]
race_events: pd.DataFrame = pd.concat(frames)

rich.print(race_events.shape)
rich.print(race_events.head())
rich.print(race_events.tail())
race_events.to_csv("csv_files/race_events.csv", index=False)


# TODO: Select event to scrape ✅
# TODO: Loop through folders for that event ✅
# TODO: Scrape event info and save to df ✅
# TODO: Write df data to csv File ✅
# TODO: Function to read long distance info ✅
# TODO: Function to read hurdles info ✅
# TODO: Function to read relays info ✅
# TODO: Function to read field events info
# TODO: Correct 2012 Class 1 girls 200 meter event
