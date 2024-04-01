from models import Record
import rich

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


def parse_records(data, event, year):
    """Parse decathlon and heptathlon events - Finals"""

    lst: list = []  # will contian all results details
    event_details: list = get_event_details(event)

    # Split original data into manageble chunks
    parshal = data.partition("Meet Record:")[2]
    results = parshal.partition("=======")[0].splitlines()

    for i in range(0, len(results)):
        line = list(filter(None, results[i].split("  ")))

        if "R" in line[0]:
            record_line = line[0].split(" ")
            record_line = [ele for ele in record_line if ele.strip()]

            if "R" in record_line[0] and len(record_line) > 1:
                mark = record_line[1]
                other_info = [ele for ele in line if ele.strip()]
                yr = other_info[-2][-4:]
                other_info = other_info[-1].split(",")
                school = other_info[1]
                athlete = other_info[0]

                # create pydantic dataclass
                record = Record(
                    event=event_details[0],
                    gender=event_details[1],
                    clas_s=event_details[2],
                    mark=mark + "x",
                    athlete=athlete,
                    year=yr,
                    school=school,
                )

                lst.append(record)
    return lst


# -----------------------------------------------------------------------
