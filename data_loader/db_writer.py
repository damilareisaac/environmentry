from functools import partial
from config import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from logs import get_logger
from .utils import provision_back_up
from models import Metric
from schema import MetricSchema


class DbWriter:
    logger = partial(get_logger, __name__)

    def __init__(self, data, db_name="metric.db") -> None:
        self.write_to_db(data, db_name)

    def write_to_db(self, data, db_name):
        self.logger(to_console=True).info("Start Writing to DB")
        database_url = f"sqlite:///{db_name}"
        engine = create_engine(database_url)

        session = sessionmaker(bind=engine)()

        provision_back_up(db_name, type="db")

        Base.metadata.create_all(engine)

        data = [row for row in data if row]
        data = MetricSchema(many=True).load(data)
        for item in data:
            metric = Metric(**item)
            session.add(metric)
        session.commit()

        self.logger(to_console=True).info("Writing to DB complete")
