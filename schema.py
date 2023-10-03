from marshmallow.decorators import pre_dump
from datetime import datetime
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import Metric


class MetricSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Metric

    def unix_to_datetime(self, unix_time: int) -> datetime:
        # Convert the timestamp to a datetime object
        timestamp_sec = unix_time / 1000  # Convert to seconds
        return datetime.utcfromtimestamp(timestamp_sec)

    @pre_dump
    def match_keys_with_schema_variable(self, data: dict, *args, **kwargs) -> dict:
        reversed_data = {}
        for key, value in data.items():
            key = key.lower().replace(" ", "_")
            if key == "flagged_as_suspect_reading":
                key = "is_flagged"

            reversed_data[key] = value
        return reversed_data

    @pre_dump
    def convert_unix_time_to_datetime(self, data, *args, **kwargs):
        if not data.get("Timestamp"):
            data["Timestamp"] = None
        else:
            data["Timestamp"] = self.unix_to_datetime(data["Timestamp"])
        return data
