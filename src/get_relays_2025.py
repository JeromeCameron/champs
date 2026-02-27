import pandas as pd


def parse_relays(json_path) -> pd.DataFrame:

    results = []

    for item in json_path:
        source = item.get("_source", {})

        event_name = source.get("n")
        gender = source.get("gl")
        clas_s = source.get("eo")

        wind = (
            source.get("hew", {}).get("1")
            if isinstance(source.get("hew"), dict)
            else None
        )

        for result in source.get("rts", []):
            results.append(
                {
                    "event": event_name,
                    "gender": gender,
                    "clas_s": clas_s,
                    "wind": wind,
                    "athlete": result.get("t", {}).get("n"),
                    "year": 25,
                    "position": result.get("p"),
                    "school": result.get("t", {}).get("f"),
                    "mark": result.get("m"),
                    "points": result.get("pt"),
                }
            )

    df = pd.DataFrame(results)
    return df


if __name__ == "__main__":
    raise NotImplementedError("Nothing to see here")
