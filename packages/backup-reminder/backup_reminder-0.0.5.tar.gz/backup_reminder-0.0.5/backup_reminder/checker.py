import datetime
from pathlib import Path
from typing import Optional

import yaml

LAST_FILE = "last-backup.yaml"
LAST_BACKUP_KEY = "last_backup"
BACKUP_INTERVAL_KEY = "backup_interval"


class IncorrectBackupConfig(Exception):
    pass


class BackupConfig:
    def __init__(
        self,
        last_backup_date: Optional[datetime.datetime],
        backup_interval: int,
    ):
        self.last_backup_date = last_backup_date
        self.backup_interval = backup_interval


def load_config(backup_file_path: str) -> BackupConfig:
    file = Path(f"{backup_file_path}/{LAST_FILE}")
    with open(file, "r") as config_file:
        try:
            config = yaml.safe_load(config_file)

            if config is None:
                raise IncorrectBackupConfig()

            if LAST_BACKUP_KEY not in config:
                raise IncorrectBackupConfig()

            if BACKUP_INTERVAL_KEY not in config:
                raise IncorrectBackupConfig()

            backup_interval = None

            if BACKUP_INTERVAL_KEY in config:
                try:
                    backup_interval = int(config[BACKUP_INTERVAL_KEY])
                except TypeError:
                    raise IncorrectBackupConfig()

            last_backup_date = None

            if config[LAST_BACKUP_KEY] is not None:
                try:
                    last_backup_date = datetime.datetime.fromtimestamp(
                        config[LAST_BACKUP_KEY]
                    )

                except TypeError:
                    raise IncorrectBackupConfig()

            return BackupConfig(last_backup_date, backup_interval)

        except yaml.YAMLError:
            raise IncorrectBackupConfig(
                "Incorrect or corrupted file."
                f"Please check the content of {backup_file_path}"
            )


def compute_last_backup_age_in_days(config) -> Optional[int]:
    if config.last_backup_date is None:
        return None

    now = datetime.datetime.now()

    difference = now - config.last_backup_date

    return difference.days


def new_backup_is_needed(config) -> bool:
    if config.last_backup_date is None:
        return True

    age = compute_last_backup_age_in_days(config)

    return age > config.backup_interval


def commit_backup(config_folder_path: str):
    old_config = load_config(config_folder_path)

    config_file_path = Path(config_folder_path) / LAST_FILE

    with open(config_file_path, "w") as config_file:
        config = dict(
            last_backup=datetime.datetime.now().timestamp(),
            backup_interval=old_config.backup_interval,
        )

        yaml.dump(config, config_file)

    return config_file_path
