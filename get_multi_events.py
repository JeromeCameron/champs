from models import MultiEvent
import rich


# ---------------------------------------------------------------------
def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


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


def main(data, event_details, year):
    """Parse decathlon and heptathlon events - Finals"""

    lst: list = []  # will contian all results details

    # Split original data into manageble chunks
    parshal = data.partition("Finals                          ")[2]
    results = parshal.partition("=======")[0].splitlines()

    for i in range(0, len(results)):

        line = list(filter(None, results[i].split("    ")))
        other_details = [ele for ele in line if ele.strip()]

        if other_details != []:
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

            try:
                if len(mark) > 7:
                    mark = other_details[-1].split(" ")
                    mark = [ele for ele in mark if ele.strip()][0]
            except IndexError:
                continue

            # create pydantic dataclass
            result = MultiEvent(
                event=event_details[0],
                gender=event_details[1],
                clas_s=event_details[2],
                typ=event_details[4],
                wind="",
                name=athlete_name,
                year=year,
                position=str(position),
                school=school,
                mark=str(mark),
                points=str(points),
            )
            lst.append(result)

    return lst


# -----------------------------------------------------------------------
def parse_multi_event(data, event, year):
    """Main Starts Here"""
    # Get event details
    event_details: list = get_event_details(event)
    results: list = []

    results = main(data, event_details, year)

    return results
