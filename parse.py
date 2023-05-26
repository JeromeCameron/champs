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


def parse_race_event(data, event, year):
    """Parse details for race events - Finals"""

    lst = []
    parshal = data.partition("Finals                          ")[2]
    results = parshal.partition("=======")[0].splitlines()

    for line in results:
        row = list(filter(None, line.split(" ")))

        if "#" in row:
            row.remove("#")
            row.pop(1)
            # print(row)

        try:
            result = Result(
                event=event[3] + " " + event[4] + " " + event[5],
                gender=event[1],
                clas_s=event[event.index("Class") + 1],
                heat=None,
                typ=event[-1][:-5],
                wind=None if int(event[3]) > 200 else row[-2],
                name=row[1] + " " + row[2],
                year=year,
                position=row[0],
                school=row[3] + " " + row[4],
                mark=row[-2] if int(event[3]) > 200 else row[-3],
                points=row[-1],
            )

        except IndexError:
            continue

        lst.append(result)
    return lst


if __name__ == "__main__":
    """main starts here"""

file_path = "pages/18/#1 Boys 16-19 100 Meter Dash CLASS 1 BOYS Finals.html"
with open(file_path) as file:
    page = file.read()
    html = HTMLParser(page)
    data = html.text()
    filename = os.path.basename(file_path).title()
    event = filename.split(" ")

    r = parse_race_event(data, event, "23")
    print(r)
