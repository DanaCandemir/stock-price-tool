import oracledb
from sqlalchemy import URL, Column, Integer, String, create_engine, text, MetaData, insert, Table
from sqlalchemy.orm import declarative_base
from sqlalchemy.engine import URL

metadata = MetaData()

Base = declarative_base()

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

# TO DO: insert test obj into 'daily' table
