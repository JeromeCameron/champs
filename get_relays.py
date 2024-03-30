from models import TrackEvents


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

    event_name = event[4] + " " + event[5] + " " + event[6]
    gender = event[2]

    if "Open" in event:
        clas_s = "Open"
    else:
        clas_s = event[event.index("Class") + 1]

    if "Finals.Html" in event:
        heat = None
    else:
        heat = ""  # add heat details

    typ = event[-1][:-5]
    event_details.extend([event_name, gender, clas_s, heat, typ])

    return event_details


# ---------------------------------------------------------------------


def get_school(result: list, event: list) -> str:
    """Returns School Name"""

    school = ""

    lst: list = list(filter(None, result.split("   ")))

    if " " in lst:  # remove empty strings
        lst.remove(" ")

    if " JURY REINSTATE" in lst:  # remove empty strings
        lst.pop(lst.index(" JURY REINSTATE"))

    if lst != []:  # ignore empty lists
        school = lst[0].rsplit(" ")
        if school[-1] == "'A'":
            school.pop(-1)
        school = [i for i in school if i]

        try:
            if int(school[0]):
                school = " ".join(school[1:])
        except:
            school = " ".join(school[0:])
        school = school.replace("--", "")

    school = "".join([i for i in school if not i.isdigit()])
    return school


# ---------------------------------------------------------------------


def parse_relay_event(data, event, year):
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
        school: str = get_school(line, event)
        other_details = list(filter(None, line.split("  ")))

        # Get other race details
        if (
            other_details != []
            and len(other_details) > 1
            and ")" not in other_details[0]
        ):
            if "#" in other_details:
                other_details.remove("#")

            if "'A'" in other_details:
                other_details.remove("'A'")

            if " " in other_details:
                other_details.remove(" ")

            # if "--" in other_details:
            #     other_details.append("")
            mark = other_details[1]

            if len(other_details) > 2:
                points = other_details[-1]
            else:
                points = 0
            # ----------------------------
            # create pydantic dataclass
            result = TrackEvents(
                event=event_details[0],
                gender=event_details[1],
                clas_s=event_details[2],
                heat=event_details[3],
                typ=event_details[4],
                wind=None,
                name=None,
                year=year,
                position=other_details[0][0],
                school=school,
                mark=mark,
                points=points,
            )

            lst.append(result)

    return lst
