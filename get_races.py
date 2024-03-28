from models import Result


# ---------------------------------------------------------------------
def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


# ---------------------------------------------------------------------


def get_athlete_name(result: list) -> str:
    """Returns athlete name"""

    athlete_name = ""

    lst: list = list(filter(None, result.split("   ")))

    if " " in lst:  # remove empty strings
        lst.remove(" ")
    try:
        if lst != []:  # ignore empty lists
            athlete_name = lst[0].rsplit(" ")

            if len(athlete_name) < 5 and "--" not in athlete_name:
                athlete_name = lst[1].rsplit(" ")

            athlete_name = [i for i in athlete_name if i]

            if len(athlete_name) >= 5:
                athlete_name = " ".join(athlete_name[3:])
            else:
                athlete_name = " ".join(athlete_name[1:])
    except IndexError:
        athlete_name = "nil"

    return athlete_name


# ---------------------------------------------------------------------


def get_event_details(event: list) -> list:
    """Return event deatils"""
    event_details: list = []

    event_name = event[4] + " " + event[5] + " " + event[6]
    gender = event[2]
    try:
        clas_s = event[event.index("Class") + 1]
    except:
        clas_s = "Open"

    if "Finals.Html" in event:
        heat = None
    else:
        heat = ""  # add heat details

    typ = event[-1][:-5]
    event_details.extend([event_name, gender, clas_s, heat, typ])

    return event_details


# ---------------------------------------------------------------------


def get_school(result: list, event: list, year: int) -> str:
    """Returns School Name"""

    school = ""

    lst: list = list(filter(None, result.split("   ")))

    if " " in lst:  # remove empty strings
        lst.remove(" ")

    if " JURY REINSTATE" in lst:  # remove empty strings
        lst.pop(lst.index(" JURY REINSTATE"))
    try:
        if lst != []:  # ignore empty lists
            if int(event[4]) < 200:
                school = lst[1].rsplit(" ")
            elif int(year) == 24 and len(lst) > 4:
                school = lst[-4].rsplit(" ")
            else:
                school = lst[-3].rsplit(" ")

            school = [i for i in school if i]

            school = " ".join(school[0:])
    except IndexError:
        school = "nil"
    return school


# ---------------------------------------------------------------------


def parse_race_event(data, event, year):
    """Parse details for race events [100m to 1500m events] - Finals"""

    lst: list = []  # will contian all results details
    other_details = []

    # Split original data into manageble trunks
    parshal = data.partition("Finals                          ")[2]
    results = parshal.partition("=======")[0].splitlines()

    # Get event details
    event_details: list = get_event_details(event)

    for line in results:
        # Loop through results and parse details

        athlete: str = get_athlete_name(line)
        school: str = get_school(line, event, year)
        other_details = list(filter(None, line.split(" ")))

        # Get other race details
        if other_details != []:
            if "#" in other_details:
                other_details.remove("#")
                other_details.pop(1)

            if "--" in other_details:
                other_details.append("")

            position = other_details[0] if other_details[0].isdigit() else 0

            # ----------points------------------
            if int(position) > 8 or int(position) == 0:
                points = "0"
            else:
                points = other_details[-1]

            # ----------mark------------------
            if int(event[4]) > 200 and len(points) < 3:
                mark = other_details[-2]
            elif int(event[4]) > 4 and len(points) > 3:
                mark = other_details[-4]
            else:
                mark = other_details[-3]

            if int(position) > 8:
                # gets mark if athlete is out of the top 8 finishers
                mark = other_details[-1]
            # ----------------------------
            if len(points) > 3:
                points = other_details[-2]
                wind = other_details[-3]
            else:
                wind = other_details[-2]

            # ----------------------------
            # create pydantic dataclass
            result = Result(
                event=event_details[0],
                gender=event_details[1],
                clas_s=event_details[2],
                heat=event_details[3],
                typ=event_details[4],
                wind=None if int(event[4]) > 200 else wind,
                name=athlete,
                year=year,
                position=other_details[0],
                school=school,
                mark=mark,
                points=points,
            )

            lst.append(result)

    return lst
