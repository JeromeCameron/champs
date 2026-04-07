import os
import pandas as pd
from selectolax.parser import HTMLParser
from itertools import chain
from typing import Callable
import asyncio
import rich
import csv
import json


def genearate_df(
    func: Callable, race_stage: str, race_categories: list, path: str
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
                    rich.print(f"Parsing {filename} for results")

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


def get_file_names() -> None:
    path = r"C:\Users\jcameron\Downloads\temp\Transport"
    file_path = r"C:\Users\jcameron\Downloads\temp\Transport\lst.csv"

    file_lst: list[str] = []
    headers: list[str] = ["reg"]

    for subdir, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".pdf"):
                filename = os.path.join(subdir, file)
                file_title = os.path.basename(filename).title()
                file_lst.append(file_title.split(".")[0])

    with open(file_path, "w+", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows([file_lst])


def get_event_ids(json_path, output_path):

    ids = []

    with open(json_path, "r") as f:
        data = json.load(f)

    ws_list = data.get("_source", {}).get("ws", [])

    for item in ws_list:
        v_obj = item.get("v", {})
        event_id = v_obj.get("i")

        if event_id is not None:
            ids.append(event_id)

    # save to JSON file
    with open(output_path, "w") as f:
        json.dump(ids, f, indent=4)

    return ids


if __name__ == "__main__":
    """main starts here"""
    # raise NotImplementedError()

    print(get_event_ids("raw_event_ids.json", "event_ids.json"))
