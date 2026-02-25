import pandas as pd


def parse_results(json_path) -> pd.DataFrame:

    results = []

    for item in json_path:
        source = item.get("_source", {})

        event_name = source.get("sn")
        # wind = source.get("hew", {}).get("1")
        wind = (
            source.get("hew", {}).get("1")
            if isinstance(source.get("hew"), dict)
            else None
        )

        for athlete in source.get("r", []):
            results.append(
                {
                    "event_name": event_name,
                    "wind": wind,
                    "position": athlete.get("p"),
                    "mark": athlete.get("m"),
                    "points": athlete.get("pt"),
                    "athlete_name": athlete.get("a", {}).get("n"),
                    "school": athlete.get("a", {}).get("t", {}).get("f"),
                }
            )

    df = pd.DataFrame(results)
    return df


if __name__ == "__main__":
    raise NotImplementedError("Nothing to see here")
