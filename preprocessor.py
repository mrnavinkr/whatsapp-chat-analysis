import re
import pandas as pd


def preprocessor(data):
    pattern = r'(\d{1,2}/\d{1,2}/\d{4},\s\d{1,2}:\d{2}\s?(?:am|pm)?)\s-\s'
    messages = re.split(pattern, data)[1:]

    dates = messages[::2]
    msgs = messages[1::2]

    users, texts = [], []
    for msg in msgs:
        entry = re.split(r'([^:]+):\s', msg, maxsplit=1)
        if len(entry) > 2:
            users.append(entry[1].strip())
            texts.append(entry[2].strip())
        else:
            users.append("Group Notification")
            texts.append(entry[0].strip())

    df = pd.DataFrame({"date": dates, "user": users, "message": texts})
    df["date"] = pd.to_datetime(df["date"], errors="coerce", format="%d/%m/%Y, %I:%M %p")
    return df
