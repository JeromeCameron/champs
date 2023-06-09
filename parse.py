from selectolax.parser import HTMLParser
import rich
import pandas as pd
from datetime import date
import os
from get_races import parse_race_event

PATH = "pages/"
SPRINT = ["100", "200", "400"]
HURDLE = ["60", "80", "100", "110", "400"]
MIDDLE_DISTANCE = ["800", "1500"]
LONG_DISTANCE = ["3000", "500"]
RELAY = ["4x100", "4x400", "1600"]
JUMP = ["Long", "Triple", "High", "Pole"]
THROWS = ["Shot", "Discuss", "Javeline"]


if __name__ == "__main__":
    """main starts here"""

file_path = "pages/23/Event 6 Boys 16-19 110 Meter Hurdles CLASS 1 BOYS Finals.html"

with open(file_path) as file:
    page = file.read()
    html = HTMLParser(page)
    data = html.text()
    filename = os.path.basename(file_path).title()
    event = filename.split(" ")

    r = parse_race_event(data, event, "23")
    print(r)
