import csv
from functools import partial

from logs import get_logger
from .utils import provision_back_up


class CsvWriter:
    logger = partial(get_logger, __name__)

    def __init__(self, data, file_name="metrics.csv") -> None:
        self.write_to_csv(data, file_name)

    def write_to_csv(self, data, file_name):
        self.logger(to_console=True).info("Start Writing to CSV")
        data = [row for row in data if row]
        if not data:
            return
        header = list(data[0].keys())
        provision_back_up(file_name)
        with open(file_name, "w") as f:
            writer = csv.DictWriter(f, header)
            writer.writeheader()
            writer.writerows(data)
        self.logger(to_console=True).info("Writing to CSV complete")
