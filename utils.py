import os
import pandas as pd
from selectolax.parser import HTMLParser
from itertools import chain
import asyncio
import rich


def genearate_df(
    func, race_stage: str, race_categories: list, path: str
) -> pd.DataFrame:

    results: list = []

    for subdir, dirs, files in os.walk(path):
        for event_cat in race_categories:
            for file in files:
                if (
                    file.endswith(".html")
                    and file.find(event_cat) >= 0
                    and file.find(race_stage) >= 0
                ):
                    filename = os.path.join(subdir, file)
                    # rich.print(f"Parsing {filename} for results")

                    with open(filename) as file:
                        page = file.read()
                        html = HTMLParser(page)
                        data = html.text()
                        file_title = os.path.basename(filename).title()
                        event = file_title.split(" ")
                        year = filename.split("/")[1].split("\\")[0]

                        res: list = func(data, event, year)
                        res_dict = [x.dict() for x in res]
                        results.append(res_dict)

    df = pd.DataFrame(list(chain.from_iterable(results)), dtype=str)
    return df


def edit_file_names() -> None:
    path = "../pages/24"

    for subdir, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".html") and file.find("#") >= 0:
                filename = os.path.join(subdir, file)
                os.rename(filename, filename.replace("#", "Event "))
                print(filename.replace("#", "Event"))


if __name__ == "__main__":
    """main starts here"""
    pass
