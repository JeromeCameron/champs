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
    lst = [x.strip() for x in lst]
    lst = [x for x in lst if x != ""]

    if lst != []:  # ignore empty lists
        athlete_name = lst[0].rsplit(" ")

        athlete_name = [x for x in athlete_name if x != ""]
        athlete_name = [x for x in athlete_name if x != "#"]

        if len(athlete_name) > 2 and len(athlete_name) < 5:
            athlete_name = athlete_name[-2:]

            if not isfloat(athlete_name[0]):
                athlete_name = athlete_name = " ".join(athlete_name[0:])

                return athlete_name


# ---------------------------------------------------------------------


def get_event_details(event: list) -> list:
    """Return event deatils"""
    event_details: list = []

    event_name = event[4] + " " + event[5] + " " + event[6]
    gender = event[2]
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
    lst = [x.strip() for x in lst]
    lst = [x for x in lst if x != ""]

    if " JURY REINSTATE" in lst:  # remove empty strings
        lst.pop(lst.index(" JURY REINSTATE"))

    if lst != [] and len(lst) > 2:  # ignore empty lists
        school = lst[1]
        if len(school) > 2:
            school = school
            return school


# ---------------------------------------------------------------------


def parse_field_event(data, event, year):
    """Parse details for field events [jumps anf throws] - Finals"""

    lst: list = []  # will contian all results details
    other_details = []

    # Split original data into manageble trunks
    parshal = data.partition("Finals                          ")[2]
    results = parshal.partition("=======")[0].splitlines()

    # Get event details
    event_details: list = get_event_details(event)

    for line in results:
        # athlete: str = get_athlete_name(line)
        # if athlete is not None:
        #     athlete = athlete
        school: str = get_school(line, event)
        print(school)
        # other_details = list(filter(None, line.split(" ")))
