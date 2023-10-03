import unittest
import os
import csv
from data_loader import CsvWriter, DbWriter
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import BASE_DIR, Base
from models import Metric


class TestCsvWriter(unittest.TestCase):
    def setUp(self):
        # Create a sample data to be written to the CSV
        self.sample_data = [
            {"Name": "John", "Age": 30},
            {"Name": "Jane", "Age": 25},
        ]
        self.file_name = "test.csv"

    def tearDown(self):
        # Clean up any generated CSV files
        if os.path.exists(self.file_name):
            os.remove(self.file_name)

    def test_write_to_csv(self):
        # Create an instance of CsvWriter and write sample data to CSV
        CsvWriter(self.sample_data, self.file_name)

        # Verify that the CSV file has been created

        self.assertTrue(os.path.exists(self.file_name))

        # Verify the contents of the CSV file
        with open(self.file_name, "r") as f:
            reader = csv.reader(f)
            header = next(reader)  # Read the header
            self.assertEqual(header, ["Name", "Age"])
            data = list(reader)
            self.assertEqual(data, [["John", "30"], ["Jane", "25"]])


class TestDbWriter(unittest.TestCase):
    def setUp(self):
        # Create a sample data to be written to the database
        self.sample_data = [
            {"variable": "Temperature", "units": "Celsius", "value": 25.5},
            {"variable": "Pressure", "units": "Bar", "value": 3.0},
        ]
        self.db_name = "test_metric.db"
        # Define the database URL for testing
        self.database_url = f"sqlite:///{self.db_name}"

    def tearDown(self):
        # Clean up any generated test database files

        if os.path.exists(self.db_name):
            os.remove(self.db_name)

    def test_write_to_db(self):
        # Create an instance of DbWriter and write sample data to the test database
        DbWriter(self.sample_data, self.db_name)

        # Verify that the test database file has been created
        self.assertTrue(os.path.exists(self.db_name))

        # Verify the contents of the test database
        engine = create_engine(self.database_url)
        session = sessionmaker(autocommit=False, autoflush=False, bind=engine)()

        metrics = session.query(Metric).all()
        self.assertEqual(len(metrics), len(self.sample_data))


if __name__ == "__main__":
    unittest.main()
