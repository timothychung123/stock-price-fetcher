"""
QQQM Daily Close Fetcher
========================
Pulls QQQM's most recent daily closing price via yfinance and appends it to
market_data.json. This script is meant to run once per day via the GitHub
Actions workflow in .github/workflows/fetch_price.yml, safely after the US
market close.

market_data.json contains ONLY a date and a closing price per entry --
nothing else. This repo is public, so no personal, account, or position data
of any kind belongs here or in this script.
"""

import json
import os
import sys

import yfinance as yf

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(HERE, "market_data.json")
TICKER = "QQQM"


def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def main():
    data = load_data()
    existing_dates = {row["date"] for row in data}

    df = yf.download(TICKER, period="5d", auto_adjust=True, progress=False)
    if df.empty:
        print("No data returned from yfinance -- nothing to do.")
        return

    if hasattr(df.columns, "get_level_values"):
        df.columns = df.columns.get_level_values(0)

    added = 0
    for idx, row in df.iterrows():
        date_str = idx.strftime("%Y-%m-%d")
        if date_str in existing_dates:
            continue
        close = round(float(row["Close"]), 4)
        data.append({"date": date_str, "close": close})
        existing_dates.add(date_str)
        added += 1

    if added == 0:
        print("No new trading days to add -- market_data.json is already up to date.")
        return

    data.sort(key=lambda r: r["date"])
    save_data(data)
    print(f"Added {added} new day(s). market_data.json now has {len(data)} entries "
          f"(latest: {data[-1]['date']} = {data[-1]['close']}).")


if __name__ == "__main__":
    main()
