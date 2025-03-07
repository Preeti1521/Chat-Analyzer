import re
import pandas as pd


def preprocess(data):
    # Define the regex pattern for extracting messages and dates
    pattern = r"\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s"
    # Split the chat data into messages and capture dates
    messages = re.split(pattern, data)[1:]  # First element is empty due to the split
    dates = [
        date.replace(" - ", "").replace(",", "") for date in re.findall(pattern, data)
    ]

    # Create a DataFrame with messages and dates
    df = pd.DataFrame({"user_message": messages, "date": pd.to_datetime(dates)})

    # Ensure the user_message column is string type
    df["user_message"] = (
        df["user_message"].astype(str).fillna("")
    )  # Fill NaN with empty strings

    # Extract user and message using regex
    # This regex captures the user and the message, allowing for cases where there is no user (e.g., group notifications)
    df[["user", "message"]] = df["user_message"].str.extract(
        r"([\w\s\.-]+?):\s(.*)", expand=True
    )

    # Handle messages without a user (like system messages)
    df["user"].fillna("group_notification", inplace=True)
    df.drop(columns=["user_message"], inplace=True)

    # Extract additional time-related features
    df["only_date"] = df["date"].dt.date
    df["day_name"] = df["date"].dt.day_name()
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month_name()
    df["day"] = df["date"].dt.day
    df["hour"] = df["date"].dt.hour
    df["minute"] = df["date"].dt.minute

    # Create a period column based on the hour
    df["period"] = df["hour"].apply(lambda h: f"{h}-00" if h == 23 else f"{h}-{h + 1}")
    return df
