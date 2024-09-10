# Bare (Backup Reminder)

![GitHub Actions Status](https://github.com/groovytron/bare/actions/workflows/ci.yaml/badge.svg?branch=main)

A simple CLI tool that can be used as a backup reminder for your laptop backups.

**This CLI does not perform any backup for you. It is just a CLI that
can be used to check the last time a backup was done and remind you if
a new backup is needed.**

## Usage

### Initialization

After installing, run `bare init` to generate the configuration file.

This generates a configuration file named `last-backup.yaml` in
your HOME directory.

You can change the `backup_interval` value (how many days between two backups)
in the configuration file following your needs. By default the value is 5
(backup every 5 days).

### Check if a backup is needed

Simply run `bare check` to know if a new backup is needed.

If a backup is needed, perform your backup and then run `bare commit` to
commit your backup.
