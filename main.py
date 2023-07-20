from selectolax.parser import HTMLParser
import rich
import pandas as pd
from datetime import date
import os
from get_races import parse_race_event
from get_field_events import parse_field_event
from get_relays import parse_relay_event

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

    # pages/18/Event 19 Boys 14-15 110 Meter Hurdles CLASS 2 BOYS Finals.html
    # pages\18\Event 7 Boys 16-19 400 Meter Hurdles CLASS 1 BOYS Finals.html
    # pages\23\Event 1 Boys 16-19 100 Meter Dash CLASS 1 BOYS Finals.html
    # pages\23\Event 82 Girls 13-19 400 Meter Hurdles OPEN Finals.html
    # pages\23\Event 59 Girls 15-16 100 Meter Hurdles CLASS 2 Finals.html
    # pages\19\Event 32 Boys 10-13 100 Meter Hurdles CLASS 3 BOYS Finals.html
    # pages\21\Event 6 Boys 16-19 110 Meter Hurdles CLASS 1 BOYS Finals.html
    # pages\23\Event 9 Boys 16-19 High Jump CLASS 1 BOYS Finals.html
    # pages\23\Event 8 Boys 16-19 4x100 Meter Relay CLASS 1 BOYS Finals.html


file_path = r"pages/23/Event 8 Boys 16-19 4x100 Meter Relay CLASS 1 BOYS Finals.html"

with open(file_path) as file:
    page = file.read()
    html = HTMLParser(page)
    data = html.text()
    filename = os.path.basename(file_path).title()
    event = filename.split(" ")
    year = file_path.split("/")[1]

    r = parse_relay_event(data, event, year)
    # for result in r:
    #     rich.print(result)
