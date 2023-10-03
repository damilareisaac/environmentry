import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Metric  # Import your Metric model class
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from config import Base

# Define a sample SQLite in-memory database for testing
DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class TestMetricModel(unittest.TestCase):
    def setUp(self):
        self.session = SessionLocal()
        Base.metadata.create_all(bind=engine)
        self.session = SessionLocal()

    def tearDown(self):
        self.session.close()

    def test_create_metric(self):
        # Create a sample Metric object
        metric = Metric(
            variable="Temperature",
            units="Celsius",
            sensor_name="Sensor1",
            value=25.5,
            is_flagged=False,
            timestamp=datetime(2023, 4, 4, 10, 21, 0),
        )

        # Add and commit the Metric object to the database

        self.session.add(metric)
        self.session.commit()

        # Retrieve the Metric object from the database
        retrieved_metric = self.session.query(Metric).filter_by(id=metric.id).first()

        # Assert that the retrieved Metric matches the created Metric
        self.assertEqual(retrieved_metric.variable, "Temperature")
        self.assertEqual(retrieved_metric.units, "Celsius")
        self.assertEqual(retrieved_metric.sensor_name, "Sensor1")
        self.assertEqual(retrieved_metric.value, 25.5)
        self.assertFalse(retrieved_metric.is_flagged)
        self.assertEqual(retrieved_metric.timestamp, datetime(2023, 4, 4, 10, 21, 0))


if __name__ == "__main__":
    unittest.main()
