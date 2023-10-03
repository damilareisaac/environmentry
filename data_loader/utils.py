from datetime import datetime, timedelta
import os
import shutil

csv_dir = "files_csv"
db_dir = "files_db"


def get_back_up_timestamp_name():
    today = datetime.now()
    lag = timedelta(days=1)
    diff = today - lag
    return diff.strftime("%Y-%m-%dT%H:%M:%SZ")


def provision_back_up(data_source, type="csv") -> None:
    root_path = csv_dir if type == "csv" else db_dir
    file_path = os.path.join(root_path, data_source)
    file_name, extension = data_source.split(".")
    if os.path.exists(file_path):
        os.rename(
            file_path,
            f"{root_path}/{file_name}_bak_{get_back_up_timestamp_name()}.{extension}",
        )


def provision_clean_up():
    if not os.path.exists(csv_dir):
        os.mkdir(csv_dir)
    if not os.path.exists(db_dir):
        os.mkdir(db_dir)

    for file_name in os.listdir("."):
        if file_name.endswith(".csv") and not os.path.exists(f"{csv_dir}/{file_name}"):
            shutil.move(file_name, csv_dir)
        if file_name.endswith(".db") and not os.path.exists(f"{db_dir}/{file_name}"):
            shutil.move(file_name, db_dir)
