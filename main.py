import asyncio
from functools import partial
from data_ingestion import FetchFromApi
from data_loader.utils import provision_clean_up
from data_loader import DbWriter, CsvWriter
from logs import get_logger


async def main():
    logger = partial(get_logger, __name__)

    fetch_from_api = FetchFromApi()
    sensors_ids = fetch_from_api.get_sensors_id()
    if not sensors_ids:
        logger(to_console=True).info("No sensors found")
        return None
    sensors_ids = sensors_ids[:100]
    logger(to_console=True).info(f"Total sensors {len(sensors_ids)}")
    list_of_sensor_data_list = await fetch_from_api.get_all_details_from_sensors(
        sensors_ids
    )
    list_of_data = []
    for sensor_data in list_of_sensor_data_list:
        if sensor_data:
            list_of_data += sensor_data

    DbWriter(list_of_data)
    CsvWriter(list_of_data)
    provision_clean_up()


if __name__ == "__main__":
    asyncio.run(main())
