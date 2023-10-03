from sqlalchemy.ext.declarative import declarative_base
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SENSORS_CSV_URL = "https://newcastle.urbanobservatory.ac.uk/api/v1.1/sensors/csv/"
BASE_URL = "http://uoweb3.ncl.ac.uk/api/v1.1"
START_DATE = "20220601"
END_DATE = "20231230"


# SQL Alchemy extension
Base = declarative_base()
