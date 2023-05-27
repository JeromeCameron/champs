from selectolax.parser import HTMLParser
from pydantic import BaseModel
import rich
import pandas as pd
from datetime import date
import os

BASE_URL = "https://issasports.com/results/"
PATH = "pages/"
SPRINT = ["100", "200", "400"]
HURDLE = ["60", "80", "100", "110", "400"]
MIDDLE_DISTANCE = ["800", "1500"]
LONG_DISTANCE = ["3000", "500"]
RELAY = ["4x100", "4x400", "1600"]
JUMP = ["Long", "Triple", "High", "Pole"]
THROWS = ["Shot", "Discuss", "Javeline"]


class Result(BaseModel):
    # id: int
    event: str
    gender: str
    clas_s: str | None = None
    heat: str | None = None
    typ: str
    wind: str | None = None
    name: str | None = None
    year: str
    position: str
    school: str
    mark: str | None = None
    points: str | None = None


class Record(BaseModel):
    id: int
    mark: str
    athlete: str
    year: int


class Event(BaseModel):
    id: int
    name: str
    record: Record


class Athlete(BaseModel):
    id: int
    firstname: str
    lastname: str
    dob: date | None = None
    events: list[str] = []
    gender: str


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


def parse_race_event(data, event, year):
    """Parse details for race events - Finals"""

    lst = []
    other_details = []
    get_name = []
    athlete_name = ""

    parshal = data.partition("Finals                          ")[2]
    results = parshal.partition("=======")[0].splitlines()

    for line in results:
        other_details = list(filter(None, line.split(" ")))

    for line in results:
        get_name = list(filter(None, line.split("   ")))
        if get_name != []:
            athlete_name = get_name[0].rsplit(" ")
            print(get_name)
            athlete_name = [i for i in athlete_name if i]
            athlete_name = " ".join(athlete_name[3:])

        if "#" in other_details:
            other_details.remove("#")
            other_details.pop(1)

            if "--" in other_details:
                other_details.append("")

        try:
            result = Result(
                event=event[4] + " " + event[5] + " " + event[6],
                gender=event[2],
                clas_s=event[event.index("Class") + 1],
                heat=None,
                typ=event[-1][:-5],
                wind=None if int(event[4]) > 200 else other_details[-2],
                name=athlete_name,
                year=year,
                position=other_details[0],
                school=get_name[1].strip(),
                mark=other_details[-2] if int(event[4]) > 200 else other_details[-3],
                points=other_details[-1],
            )
            # print(len(other_details))

        except (IndexError, ValueError):
            continue

        lst.append(result)
    return lst


if __name__ == "__main__":
    """main starts here"""

file_path = "pages/18/Event 7 Boys 16-19 400 Meter Hurdles CLASS 1 BOYS Finals.html"
with open(file_path) as file:
    page = file.read()
    html = HTMLParser(page)
    data = html.text()
    filename = os.path.basename(file_path).title()
    event = filename.split(" ")

    r = parse_race_event(data, event, "23")
    # rich.print(r)
