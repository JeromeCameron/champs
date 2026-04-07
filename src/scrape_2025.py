import httpx
from get_events_2025 import parse_results
import json

from get_relays_2025 import parse_relays
import pandas as pd
import os
import time


def scrape_event_details(url) -> pd.DataFrame:

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://live.athletic.net",
        "Referer": "https://live.athletic.net/",
    }

    with httpx.Client(http2=True) as client:
        response = client.get(url, headers=headers)

    data = []
    data.append(response.json())

    results = parse_relays(data)
    return results


if __name__ == "__main__":

    with open("event_ids.json", "r") as f:
        event_ids = json.load(f)

    results = []
    file_path = "csv_files/champs_2026__relay_results.csv"

    for event_id in event_ids:
        print(f"Getting results for event # {event_id}")
        results = scrape_event_details(
            f"https://athleticlive.blob.core.windows.net/$web/rel_res_list/_doc/{event_id}"
        )
        file_exists = os.path.isfile(file_path)
        results.to_csv(file_path, mode="a", header=not file_exists, index=False)

        time.sleep(2)

    print("Done!")

    # relays - https://athleticlive.blob.core.windows.net/$web/rel_res_list/_doc/
    # individual - https://athleticlive.blob.core.windows.net/$web/ind_res_list/_doc/1700923
