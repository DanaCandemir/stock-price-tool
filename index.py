import oracledb
import requests
import json
from datetime import date
from sqlalchemy import URL, Column, Integer, String, create_engine, text, MetaData, insert, Table
from sqlalchemy.orm import declarative_base
from sqlalchemy.engine import URL

metadata = MetaData()

Base = declarative_base()
today = date.today()

daily = Table('daily', metadata,
              Column('id', Integer, primary_key=True),
              Column('open', String(50)),
              Column('high', String(50)),
              Column('low', String(50)),
              Column('close', String(50)),
              Column('volume', String(50)),
              Column('date', String(50)))


class Test123(Base):
    __tablename__ = "test123"
    id = Column(Integer, primary_key=True)
    open = Column(String(50))
    high = Column(String(50))
    low = Column(String(50))
    close = Column(String(50))
    volume = Column(String(50))
    date = Column(String(50))


def get_engine():
    username = "SYS"
    password = "ReallyLongPW@1!"  # Consider using environment variables later
    host = "localhost"
    port = "1521"
    service_name = "freepdb1"

    connection_url = URL.create(
        "oracle+oracledb",
        username=username,
        password=password,
        host=host,
        port=port,
        query={"service_name": service_name}
    )

    return create_engine(connection_url, connect_args={"mode": oracledb.AUTH_MODE_SYSDBA}, echo=True)


engine = get_engine()
connection = engine.connect()
metadata.create_all(engine)

test_obj = {
    'open': '123',
    'high': '234',
    'low': '345',
    'close': '456',
    'volume': '567',
    'date': '12/23/1999'
}

# insert_stmt = insert()


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
        close_prc.append(float(day["4. close"]))

    return (sum(close_prc)/len(close_prc))


def low_high(time_series):
    '''Prints and returns the low and high for the time series
    '''
    lows = []
    highs = []

    for day in time_series:
        highs.append(float(day["2. high"]))
        lows.append(float(day["3. low"]))

    print(f"52-week low: {min(lows)}\n52-week high: {max(highs)}")
    return (min(lows), max(highs))


# slice_52 = slice_52_wk()
# print(slice_52[0])

# avg = get_avg(slice_52)
# print(f"52 week average: {avg}")

# low_high_52_wk = low_high(slice_52)
# engine = get_engine()
# metadata.create_all(engine)
# insert_stmt = insert()
# # Base.metadata.create_all(engine)
# with engine.connect() as conn:
#     result = conn.execute(text("SELECT * FROM ALERT_QT"))
#     for row in result:
#         print("row: ", row)
