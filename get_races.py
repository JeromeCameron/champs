from models import Result


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
    count = 0
    get_name = []

    parshal = data.partition("Finals                          ")[2]
    results = parshal.partition("=======")[0].splitlines()
    results2 = parshal.partition("=======")[0].splitlines()

    for line in results2:
        other_details = list(filter(None, line.split(" ")))

        athlete_name = ""

        get_name = list(filter(None, results[count].split("   ")))

        if " " in get_name:
            get_name.remove(" ")

        if get_name != [] and len(get_name) == 4:
            athlete_name = get_name[0].rsplit(" ")
            athlete_name = [i for i in athlete_name if i]

            if len(athlete_name) == 5:
                athlete_name = " ".join(athlete_name[3:])
            else:
                athlete_name = " ".join(athlete_name[1:])

        elif get_name != [] and len(get_name) == 5 and int(event[4]) > 200:
            athlete_name = get_name[1].rsplit(" ")
            athlete_name = [i for i in athlete_name if i]
            athlete_name = " ".join(athlete_name[1:])

        elif get_name != [] and len(get_name) == 5 and int(event[4]) <= 200:
            athlete_name = get_name[0].rsplit(" ")
            athlete_name = [i for i in athlete_name if i]
            athlete_name = (
                " ".join(athlete_name[3:])
                if len(athlete_name) > 3
                else " ".join(athlete_name[1:])
            )

        count += 1

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
                school=get_name[-3].strip()
                if int(event[4]) > 200
                else get_name[1].strip(),
                mark=other_details[-2] if int(event[4]) > 200 else other_details[-3],
                points="0" if int(other_details[0]) > 8 else other_details[-1],
            )
            if int(result.position) > 8:
                result.mark = other_details[-1]

        except (IndexError, ValueError):
            continue

        lst.append(result)

    return lst
