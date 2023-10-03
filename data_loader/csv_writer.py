import csv

from logs import get_logger
from .utils import provision_back_up

logger = get_logger(__name__)


class CsvWriter:
    def __init__(self, data, file_name="metrics.csv") -> None:
        self.write_to_csv(data, file_name)

    def write_to_csv(self, data, file_name):
        logger.info("Start Writing to CSV")
        data = [row for row in data if row]
        if not data:
            return
        header = list(data[0].keys())
        provision_back_up(file_name)
        with open(file_name, "w") as f:
            writer = csv.DictWriter(f, header)
            writer.writeheader()
            writer.writerows(data)
        logger.info("Writing to CSV complete")
