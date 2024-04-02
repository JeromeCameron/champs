from models import FieldEvents
import rich
import pandas as pd

# ---------------------------------------------------------------------


def get_event_details(event: list) -> list:
    """Return event deatils"""
    event_details: list = []

    event_name = event[4] + " " + event[5]
    gender = event[2]
    try:
        clas_s = event[event.index("Class") + 1]
    except ValueError:
        clas_s = "Open"

    if "Finals.Html" in event:
        heat = None
    else:
        heat = ""  # add heat details

    typ = event[-1][:-5]
    event_details.extend([event_name, gender, clas_s, heat, typ])

    return event_details


# ---------------------------------------------------------------------


def parse_jumps_throws(data: str, event_details: list, year: str) -> list[pd.DataFrame]:
    """Parse details for field events [horizontal jumps anf throws] - Finals"""

    lst: list = []  # will contian all results details

    # Split original data into manageble chunks
    parshal = data.partition("Finals                          ")[2]
    results = parshal.partition("=======")[0].splitlines()

    if int(year) == 16 or int(year) > 17:
        for i in range(0, len(results)):

            if i % 2 != 0:
                line = list(filter(None, results[i].split("    ")))
                other_details = [ele for ele in line if ele.strip()]

                position_names = other_details[0].split(" ")
                position_names = [ele for ele in position_names if ele.strip()]
                position = position_names[0] if position_names[0] != "--" else ""
                athlete_name = position_names[-2] + " " + position_names[-1]
                athlete_name = "".join(
                    [i for i in athlete_name if not i.isdigit()]
                ).strip()
                points = other_details[-1].split(" ")

                if position != "":
                    if int(position) <= 8:
                        # gets points if athlete is in the top 8 finishers
                        points = [ele for ele in points if ele.strip()][-1]
                    else:
                        points = 0

                wind = other_details[-1].split(" ")

                if event_details[0] == "Long Jump" or event_details[0] == "Triple Jump":
                    wind = [ele for ele in wind if ele.strip()][0]
                else:
                    wind = ""

                school = other_details[1].strip()
                school = "".join([i for i in school if not i.isdigit()])
                mark = other_details[2].strip().replace("Q", "")

                try:
                    if len(mark) > 7:
                        mark = other_details[-1].split(" ")
                        wind = [ele for ele in mark if ele.strip()][1]
                        mark = [ele for ele in mark if ele.strip()][0]
                except IndexError:
                    wind = "n/a"

                if year == "24":
                    mark = other_details[-2].strip().replace("Q", "")

                try:
                    if int(year) > 18:
                        series_line = list(filter(None, results[i + 1].split(" ")))
                        series_details = [ele for ele in series_line if ele.strip()]
                        if series_details != []:
                            series = series_details
                    else:
                        series = []
                except IndexError:
                    series = []

                # create pydantic dataclass
                result = FieldEvents(
                    event=event_details[0],
                    gender=event_details[1],
                    clas_s=event_details[2],
                    typ=event_details[4],
                    wind=str(wind),
                    name=athlete_name,
                    year=year,
                    position=str(position),
                    school=school,
                    series=series,
                    mark=str(mark),
                    points=str(points),
                )
                lst.append(result)
    else:
        for i in range(0, len(results)):

            line = list(filter(None, results[i].split("    ")))
            other_details = [ele for ele in line if ele.strip()]

            if other_details != []:
                position_names = other_details[0].split(" ")
                position_names = [ele for ele in position_names if ele.strip()]
                position = position_names[0] if position_names[0] != "--" else ""
                athlete_name = position_names[-2] + " " + position_names[-1]
                athlete_name = "".join(
                    [i for i in athlete_name if not i.isdigit()]
                ).strip()
                points = other_details[-1].split(" ")

                if position != "":
                    if int(position) <= 8:
                        # gets points if athlete is in the top 8 finishers
                        points = [ele for ele in points if ele.strip()][-1]
                    else:
                        points = 0

                wind = other_details[-1].split(" ")

                if event_details[0] == "Long Jump" or event_details[0] == "Triple Jump":
                    wind = [ele for ele in wind if ele.strip()][0]
                else:
                    wind = ""

                school = other_details[1].strip()
                school = "".join([i for i in school if not i.isdigit()])

                try:
                    mark = other_details[2].strip().replace("Q", "")
                except IndexError:
                    mark = other_details[-1].strip().replace("Q", "")

                try:
                    if len(mark) > 7:
                        mark = other_details[-1].split(" ")
                        wind = [ele for ele in mark if ele.strip()][1]
                        mark = [ele for ele in mark if ele.strip()][0]
                except IndexError:
                    wind = "n/a"

                if year == "24":
                    mark = other_details[-2].strip().replace("Q", "")

                series = []

                # create pydantic dataclass
                result = FieldEvents(
                    event=event_details[0],
                    gender=event_details[1],
                    clas_s=event_details[2],
                    typ=event_details[4],
                    wind=str(wind),
                    name=athlete_name,
                    year=year,
                    position=str(position),
                    school=school,
                    series=series,
                    mark=str(mark),
                    points=str(points),
                )

                lst.append(result)
    return lst


# -----------------------------------------------------------------------
def parse_vertical_jumps(
    data: str, event_details: list, year: str
) -> list[pd.DataFrame]:
    """Parse details for field events [vertical jumps] - Finals"""

    lst: list = []  # will contian all results details

    # Split original data into manageble chunks
    parshal = data.partition("Finals                          ")[2]
    results = parshal.partition("=======")[0].splitlines()

    if int(year) == 16 or int(year) > 17:
        for i in range(1, len(results), 3):
            line = list(filter(None, results[i].split("    ")))
            other_details = [ele for ele in line if ele.strip()]

            position_names = other_details[0].split(" ")
            position_names = [ele for ele in position_names if ele.strip()]
            position = position_names[0] if position_names[0] != "--" else ""
            athlete_name = position_names[-2] + " " + position_names[-1]
            athlete_name = "".join([i for i in athlete_name if not i.isdigit()]).strip()
            points = other_details[-1].split(" ")

            if position != "":
                if int(position) <= 8:
                    # gets points if athlete is in the top 8 finishers
                    points = [ele for ele in points if ele.strip()][-1]
                else:
                    points = 0

            school = other_details[1].strip()
            school = "".join([i for i in school if not i.isdigit()])
            mark = other_details[2].strip().replace("Q", "")

            if year == "24":
                mark = other_details[-2].strip().replace("Q", "")

            try:
                series_line_1 = list(filter(None, results[i + 1].split(" ")))
                series_line_2 = list(filter(None, results[i + 2].split(" ")))
                series_details_1 = [ele for ele in series_line_1 if ele.strip()]
                series_details_2 = [ele for ele in series_line_2 if ele.strip()]

                if series_details_1 != []:
                    series = [series_details_1, series_details_2]

            except IndexError:
                series = [[], []]

            # create pydantic dataclass
            result = FieldEvents(
                event=event_details[0],
                gender=event_details[1],
                clas_s=event_details[2],
                typ=event_details[4],
                wind="",
                name=athlete_name,
                year=year,
                position=str(position),
                school=school,
                series=series,
                mark=str(mark),
                points=str(points),
            )

            lst.append(result)
    else:
        for i in range(1, len(results)):
            line = list(filter(None, results[i].split("    ")))
            other_details = [ele for ele in line if ele.strip()]

            position_names = other_details[0].split(" ")
            position_names = [ele for ele in position_names if ele.strip()]
            position = position_names[0] if position_names[0] != "--" else ""
            athlete_name = position_names[-2] + " " + position_names[-1]
            athlete_name = "".join([i for i in athlete_name if not i.isdigit()]).strip()
            points = other_details[-1].split(" ")

            if position != "":
                if int(position) <= 8:
                    # gets points if athlete is in the top 8 finishers
                    points = [ele for ele in points if ele.strip()][-1]
                else:
                    points = 0

            school = other_details[1].strip()
            school = "".join([i for i in school if not i.isdigit()])
            mark = other_details[2].strip().replace("Q", "")

            if year == "24":
                mark = other_details[-2].strip().replace("Q", "")

            series = [[], []]

            # create pydantic dataclass
            result = FieldEvents(
                event=event_details[0],
                gender=event_details[1],
                clas_s=event_details[2],
                typ=event_details[4],
                wind="",
                name=athlete_name,
                year=year,
                position=str(position),
                school=school,
                series=series,
                mark=str(mark),
                points=str(points),
            )

            lst.append(result)

    return lst


# -----------------------------------------------------------------------
def parse_field_event(data: str, event: list[str], year: str) -> list[pd.DataFrame]:
    """Main Starts Here"""
    # Get event details
    event_details: list[str] = get_event_details(event)
    results: list[pd.DataFrame] = []

    if event_details[0] in ["High Jump", "Pole Vault"]:
        results = parse_vertical_jumps(data, event_details, year)
    else:
        results = parse_jumps_throws(data, event_details, year)

    return results
