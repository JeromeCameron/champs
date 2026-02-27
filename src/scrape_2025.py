import httpx
from get_events_2025 import parse_results

# from get_relays_2025 import parse_relays
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

    results = parse_results(data)
    return results


if __name__ == "__main__":

    event_ids = [
        1700793,
        1700794,
        1700796,
        1700798,
        1700800,
        1700803,
        1700805,
        1700806,
        1700808,
        1700809,
        1700810,
        1700812,
        1700814,
        1700816,
        1700819,
        1700820,
        1700821,
        1700823,
        1700824,
        1700826,
        1700828,
        1700830,
        1700832,
        1700834,
        1700836,
        1700838,
        1700840,
        1700843,
        1700845,
        1700847,
        1700849,
        1700851,
        1700853,
        1700855,
        1700858,
        1700861,
        1700863,
        1700865,
        1700867,
        1700870,
        1700873,
        1700876,
        1700878,
        1700880,
        1700883,
        1700886,
        1700889,
        1700891,
        1700893,
        1700895,
        1700898,
        1700900,
        1700903,
        1700906,
        1700908,
        1700910,
        1700912,
        1700915,
        1700918,
        1700920,
        1700923,
        1700926,
        1700928,
        1700929,
        1700930,
        1700931,
        1700932,
        1700933,
        1700934,
        1700935,
        1700938,
        1700941,
        1700944,
        1700947,
        1700950,
        1700953,
        1700956,
        1700957,
        1700958,
        1700959,
        1700960,
        1700961,
        1700962,
        1700963,
        1700964,
        1700965,
        1700966,
        1700969,
        1700972,
        1700974,
        1700976,
        1700979,
    ]

    results_25 = []
    file_path = "csv_files/champs_2025_2_results.csv"

    for event_id in event_ids:
        print(f"Getting page {event_id}")
        results_25 = scrape_event_details(
            f"https://athleticlive.blob.core.windows.net/$web/ind_res_list/_doc/{event_id}"
        )
        file_exists = os.path.isfile(file_path)
        results_25.to_csv(file_path, mode="a", header=not file_exists, index=False)

        time.sleep(2)

    print("Done!")

    # relays - https://athleticlive.blob.core.windows.net/$web/rel_res_list/_doc/
    # individual - https://athleticlive.blob.core.windows.net/$web/ind_res_list/_doc/1700923
