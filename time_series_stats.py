import requests
import json
from datetime import date

today = date.today()


def fetch_data():
    api_key = "ZAWB70NZ1KPQXI4O"
    interval = "Daily"
    symbol = "IBM"
    function = "TIME_SERIES_DAILY"
    output_size = "full"
    url = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&interval={interval}&outputsize={output_size}&apikey={api_key}'

    r = requests.get(url)
    data = r.json()

    # saving json locally to get around throttling by API while testing
    filename = "output.json"
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def slice_52_wk():
    '''
    Slice the most recent 52 dates from the dict 
    '''
    from datetime import date

    sliced_dates = []

    # Change today's date to last year's
    new_date = date.today()
    today = str(new_date).split("-")
    today[0] = str(int(today[0]) - 1)
    last_year = "-".join(today)

    # refactored this piece of code to utilize output.json instead of storing the response in memory to call API less.
    filename = "output.json"
    with open(filename, "r") as f:
        data = json.load(f)

        for day, daily_prices in data["Time Series (Daily)"].items():
            if day >= last_year:
                daily_copy = {}
                daily_copy["open"] = daily_prices["1. open"]
                daily_copy["high"] = daily_prices["2. high"]
                daily_copy["low"] = daily_prices["3. low"]
                daily_copy["close"] = daily_prices["4. close"]
                daily_copy["volume"] = daily_prices["5. volume"]
                daily_copy["date"] = day
                sliced_dates.append(daily_copy)

        return sliced_dates


def get_avg(time_series):
    '''
    Collects all closing prices in the time series data and returns the average
    '''

    close_prc = []

    for day in time_series:
        close_prc.append(float(day["close"]))

    return (sum(close_prc)/len(close_prc))


def low_high(time_series):
    '''Prints and returns the low and high for the time series
    '''
    lows = []
    highs = []

    for day in time_series:
        highs.append(float(day["high"]))
        lows.append(float(day["low"]))

    print(f"52-week low: {min(lows)}\n52-week high: {max(highs)}")
    return (min(lows), max(highs))
