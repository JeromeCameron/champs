import pandas as pd


def time_to_seconds(time_str):
    """Converts H:MM:SS.mmm, MM:SS.mmm, or SS.mmm to seconds safely."""

    if pd.isna(time_str):
        return None

    time_str = str(time_str).strip()

    # Remove non-time entries
    if time_str in ["DNF", "DNS", "DQ", "NT", "", "-"]:
        return None

    try:
        colon_count = time_str.count(":")

        if colon_count == 2:  # H:MM:SS.mmm
            hours, minutes, seconds = time_str.split(":")
            return int(hours) * 3600 + int(minutes) * 60 + float(seconds)

        elif colon_count == 1:  # MM:SS.mmm
            minutes, seconds = time_str.split(":")
            return int(minutes) * 60 + float(seconds)

        else:  # SS.mmm
            return float(time_str)

    except Exception:
        return None


def seconds_to_minutes(time_in_seconds: float):
    if time_in_seconds >= 60:
        minutes = int(time_in_seconds // 60)
        seconds = time_in_seconds - (minutes * 60)  # time_in_seconds % 60
        return f"{minutes}:{seconds:05.2f}"
    else:
        return f"{time_in_seconds:.2f}"


if __name__ == "__main__":
    user_input = input("Enter string time... ")

    tm = seconds_to_minutes(float(user_input))
    print(type(tm))
