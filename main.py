import rich
import pandas as pd
from get_races import parse_race_event
from get_field_events import parse_field_event
from get_multi_events import parse_multi_event
from get_relays import parse_relay_event
from get_records import parse_records
from utils import genearate_df
import asyncio

PATH: str = "pages/"

# Race Types
TRACK_EVENTS: list = [
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
]
FIELD_EVENTS: list = [
    "Long Jump",
    "Triple Jump",
    "Shot Put",
    "Discus Throw",
    "Javelin Throw",
    "High Jump",
    "Pole Vault",
]
RELAYS: list = ["4x100 Meter Relay", "4x400 Meter Relay", "1600 Sprint Medley"]
MULTI_EVENTS: list = ["Decathlon", "Heptathlon"]
# -----
RACE_STAGES: list = ["Finals", "Semis", "Prelims"]
ACTIONS: list = ["get_finals", "get_semis", "get_prelims", "get_records"]

# ---------------------------------------------------------------------------------

if __name__ == "__main__":
    """main starts here"""

    task: str = "get_records"

    if task == ACTIONS[0]:

        ALL_CATEGORIES: list = [TRACK_EVENTS, RELAYS, FIELD_EVENTS, MULTI_EVENTS]
        records: list[pd.DataFrame] = []
        # Get records
        for event_cat in range(len(ALL_CATEGORIES)):
            df: pd.DataFrame = genearate_df(
                func=parse_records,
                race_stage=RACE_STAGES[0],
                race_categories=ALL_CATEGORIES[event_cat],
                path=PATH,
            )
            # Combine all records df into one
            records.append(df)
        records_df: pd.DataFrame = pd.concat(records)
        records_df.to_csv("csv_files/champs_records.csv", index=False)
        rich.print(records_df)

    else:
        # Get data for individual track events
        individual_track_events_df: pd.DataFrame = genearate_df(
            func=parse_race_event,
            race_stage=RACE_STAGES[0],
            race_categories=TRACK_EVENTS,
            path=PATH,
        )
        # Get data for relays
        relays_df: pd.DataFrame = genearate_df(
            func=parse_relay_event,
            race_stage=RACE_STAGES[0],
            race_categories=RELAYS,
            path=PATH,
        )
        # Get data for individual field events
        field_events_df: pd.DataFrame = genearate_df(
            func=parse_field_event,
            race_stage=RACE_STAGES[0],
            race_categories=FIELD_EVENTS,
            path=PATH,
        )
        # Get data for multi events
        multi_events_df: pd.DataFrame = genearate_df(
            func=parse_multi_event,
            race_stage=RACE_STAGES[0],
            race_categories=MULTI_EVENTS,
            path=PATH,
        )

        frame: list = [individual_track_events_df, relays_df]

        # Combine all tarck dat into one df
        all_track_events_df: pd.DataFrame = pd.concat(frame)

        # Sample of data | Track Events
        rich.print(all_track_events_df.shape)
        rich.print(all_track_events_df.head(5))

        # Sample of data | Field Events
        rich.print(field_events_df.shape)
        rich.print(field_events_df.head(4))

        # Sample of data | Multi Events
        rich.print(multi_events_df.shape)
        rich.print(multi_events_df.head(5))

        # Export parsed data to CSV
        all_track_events_df.to_csv("csv_files/track_events2.csv", index=False)
        field_events_df.to_csv("csv_files/field_events.csv", index=False)
        multi_events_df.to_csv("csv_files/multi_events.csv", index=False)


# TODO: Select event to scrape ✅
# TODO: Loop through folders for that event ✅
# TODO: Scrape event info and save to df ✅
# TODO: Write df data to csv File ✅
# TODO: Function to read long distance info ✅
# TODO: Function to read hurdles info ✅
# TODO: Function to read relays info ✅
# TODO: Add 2024 check in field events function ✅
# TODO: What to do if no series data ✅
# TODO: Function to read field events info ✅
# TODO: Function to parse multi events pages ✅
# TODO Check class 1 boys 2022 results
