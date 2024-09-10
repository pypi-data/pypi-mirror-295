from pathlib import Path

from jinja2 import Environment, PackageLoader, select_autoescape

from backup_reminder.checker import LAST_FILE


def init_config(config_folder_path: str, backup_interval: int = 5) -> Path:
    config_file_path = Path(config_folder_path) / LAST_FILE

    with open(config_file_path, "w") as config_file:
        env = Environment(
            loader=PackageLoader("backup_reminder.generator"),
            autoescape=select_autoescape(),
            keep_trailing_newline=True,
        )

        template = env.get_template("last-backup.yaml.jinja")

        config_file.write(template.render(backup_interval=backup_interval))

    return config_file_path
