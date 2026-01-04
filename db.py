from sqlalchemy import URL, Column, Integer, Identity, String, create_engine, text, MetaData, insert, Table
from sqlalchemy.orm import declarative_base
from sqlalchemy.engine import URL
from time_series_stats import slice_52_wk

metadata = MetaData()

Base = declarative_base()

# Table definition
daily = Table('daily', metadata,
              Column('id', Integer, Identity(start=1),
                     primary_key=True),
              Column('open', String(50)),
              Column('high', String(50)),
              Column('low', String(50)),
              Column('close', String(50)),
              Column('volume', String(50)),
              Column('date', String(50)))


def get_engine():
    username = "dana"
    password = "MyStrongPW1!"  # Consider using environment variables later
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

    return create_engine(connection_url, echo=True)


engine = get_engine()
connection = engine.connect()

# Create table if it doesn't exist
metadata.create_all(engine)

# test data for database instantiation
test_obj = {
    'open': '123',
    'high': '234',
    'low': '345',
    'close': '456',
    'volume': '567',
    'date': '12/23/1999'
}


def read_db():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM daily"))
        for row in result.mappings():
            print(row)


# seed_data to be a list of dictionary entries
# as oracle refuses to insert multiple records at once
def seed_db(seed_data):
    with engine.connect() as conn:
        for row in seed_data:
            conn.execute(insert(daily).values(row))
            conn.commit()


def restore_daily():
    daily.drop(engine, checkfirst=True)
    metadata.create_all(engine)
    sliced_data = slice_52_wk()
    seed_db(sliced_data)
