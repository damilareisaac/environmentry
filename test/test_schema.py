import unittest
from datetime import datetime
from schema import MetricSchema  # Import your schema module


class TestMetricSchema(unittest.TestCase):
    def setUp(self):
        self.schema = MetricSchema()

    def test_unix_to_datetime(self):
        unix_time = 1633110000000
        expected_datetime = datetime.utcfromtimestamp(unix_time / 1000)
        result = self.schema.unix_to_datetime(unix_time)
        self.assertEqual(result, expected_datetime)

    def test_match_keys_with_schema_variable(self):
        data = {
            "Value": 42,
            "Timestamp": 1633110000000,
            "Flagged as Suspect Reading": True,
        }
        expected_data = {"value": 42, "timestamp": 1633110000000, "is_flagged": True}
        result = self.schema.match_keys_with_schema_variable(data)
        self.assertEqual(result, expected_data)


if __name__ == "__main__":
    unittest.main()
