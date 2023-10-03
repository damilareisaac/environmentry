import asyncio
from functools import partial
from itertools import chain
from multiprocessing import get_logger
from config import BASE_URL, END_DATE, SENSORS_CSV_URL, START_DATE
from schema import MetricSchema
from .utils import http_get_async
import pandas as pd


class FetchFromApi:
    logger = partial(get_logger, __name__)

    async def fetch_sensor_data_async(self, sensor_id):
        self.logger(to_console=True).info(f"Fetching data for sensor {sensor_id}")
        url = f"{BASE_URL}/sensors/{sensor_id}/data/json/?starttime={START_DATE}&endtime={END_DATE}"
        response = await http_get_async(url)
        if not response:
            self.logger(to_console=True).info(
                "No response found for sensor {sensor_id}"
            )
            return

        sensor_information = response.get("sensors")[0]
        data = sensor_information.get("data")
        if not data:
            self.logger(to_console=True).info("No data found for sensor {sensor_id}")
            return {}

        data = list(chain.from_iterable(data.values()))
        sensor_schema = MetricSchema(many=True)
        data_dump = sensor_schema.dump(data)
        return data_dump

    async def get_all_details_from_sensors(self, sensors_ids):
        tasks = [self.fetch_sensor_data_async(sensor_id) for sensor_id in sensors_ids]
        return await asyncio.gather(*tasks)

    def get_sensors_id(self):
        try:
            sensors_df = pd.read_csv(SENSORS_CSV_URL)
            if "Raw ID" in sensors_df:
                sensors_df.set_index("Raw ID", inplace=True)
            return list(set(sensors_df["Sensor Name"].values))
        except Exception as e:
            self.logger(to_console=True).exception(str(e))
            return None
