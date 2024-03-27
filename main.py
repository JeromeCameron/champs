import rich
import pandas as pd
from get_races import parse_race_event
from get_field_events import parse_field_event
from get_relays import parse_relay_event
from utils import genearate_df

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

sprints_df: pd.DataFrame = genearate_df(
    func=parse_race_event, race_type="Finals", race_categories=SPRINTS, path=PATH
)

middle_distance_df: pd.DataFrame = genearate_df(
    func=parse_race_event,
    race_type="Finals",
    race_categories=MIDDLE_DISTANCES,
    path=PATH,
)

# long_distance_df: pd.DataFrame = genearate_df(
#     func=parse_race_event,
#     race_type="Finals",
#     race_categories=LONG_DISTANCES,
#     path=PATH,
# )

frames: list = [sprints_df, middle_distance_df]
race_events: pd.DataFrame = pd.concat(frames)

rich.print(race_events.shape)
rich.print(race_events.head())
rich.print(race_events.tail())
race_events.to_csv("csv_files/sprints.csv", index=False)

# TODO: Select event to scrape ✅
# TODO: Loop through folders for that event ✅
# TODO: Scrape event info and save to df ✅
# TODO: Write df data to csv File ✅
# TODO: Correct 2012 Class 1 girsl 200 meter event
