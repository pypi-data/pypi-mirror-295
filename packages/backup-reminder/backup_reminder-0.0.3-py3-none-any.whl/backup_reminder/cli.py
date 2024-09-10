import tomllib
from pathlib import Path

import click
from notifypy import Notify

from backup_reminder.checker import (
    IncorrectBackupConfig,
    commit_backup,
    compute_last_backup_age_in_days,
    load_config,
    new_backup_is_needed,
)
from backup_reminder.generator import init_config

notification = Notify(
    default_notification_title="Backups status",
    default_application_name="Backup Checker",
    default_notification_icon=str(
        Path(__file__).parent.resolve() / "assets/logo.svg"
    ),
)

BACKUP_NEVER_PERFORMED_MESSAGE = (
    "You have never performed a backup. "
    "Please make one as soon as possible."
)

NO_BACKUP_NEEDED_MESSAGE = "No backup needed you're all good and safe."

NO_CONFIG_MESSAGE = (
    "No configuration file found. " "Please create one with the init command."
)

CONFIG_ERROR_MESSAGE = (
    "An error occured during configuration loading. "
    "Please check and fix your configuration file."
)

COMMIT_MESSAGE = "Your backup has been committed."


@click.group()
def cli():
    pass


@cli.command(help="Initialize the backup checker configuration.")
@click.option(
    "--backup-interval",
    default=5,
    help="""Amount of days between backups. A notification will be sent after
    this amount of days passed without any backup.""",
)
def init(backup_interval):
    click.echo("Generating configuration...")
    config_file = init_config(Path.home(), backup_interval)
    click.echo(f"Configuration generated in {config_file}")


@cli.command(help="Check if a new backup is necessary.")
def check():
    try:
        config = load_config(Path.home())
        backup_is_needed = new_backup_is_needed(config)

        if backup_is_needed:
            age = compute_last_backup_age_in_days(config)

            if age is None:
                message = BACKUP_NEVER_PERFORMED_MESSAGE
                click.echo(message)

                notification.message = message
                notification.title = "You need a new backup"
                notification.send()

                return

            message = (
                f"Your last backup was done {age} days ago. "
                "Please make a new one as soon as possible."
            )
            click.echo(message)

            notification.message = message
            notification.title = "You need a new backup"
            notification.send()

            return

        click.echo(NO_BACKUP_NEEDED_MESSAGE)
    except IncorrectBackupConfig:
        click.echo(CONFIG_ERROR_MESSAGE)
        exit(1)
    except FileNotFoundError:
        click.echo(NO_CONFIG_MESSAGE)
        exit(1)


@cli.command(help="Commit your backup.")
def commit():
    try:
        config = load_config(Path.home())

        if new_backup_is_needed(config):
            commit_backup(Path.home())
            click.echo(COMMIT_MESSAGE)
    except IncorrectBackupConfig:
        click.echo(CONFIG_ERROR_MESSAGE)
        exit(1)
    except FileNotFoundError:
        click.echo(NO_CONFIG_MESSAGE)
        exit(1)


@cli.command(help="Show bare CLI current version")
def version():
    with open(
        (Path(__file__).parent.resolve() / "../pyproject.toml"), "rb"
    ) as f:
        data = tomllib.load(f)
        click.echo(f"bare version {data["tool"]["poetry"]["version"]}")


if __name__ == "__main__":
    cli()
