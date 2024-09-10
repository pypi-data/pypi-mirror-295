# Bare (Backup Reminder) 🐻

![GitHub Actions Status](https://github.com/groovytron/bare/actions/workflows/ci.yaml/badge.svg?branch=main)

A simple CLI tool that can be used as a backup reminder for your laptop backups.

**This CLI does not perform any backup for you. It is just a CLI that
can be used to check the last time a backup was done and remind you if
a new backup is needed.**

You can use one of the following tools to perform backups for instance:

- [Back In Time](https://github.com/bit-team/backintime) (for your HOME folder for instance)
- [Timeshift](https://github.com/linuxmint/timeshift) (for system backups)
- [Restic](https://restic.net/) (combined with [Autorestic](https://autorestic.vercel.app/))

## Installation

### With pipx

```bash
pipx install backup-reminder
```

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
A system notification is displayed if a new backup is needed.

If a backup is needed, perform your backup and then run `bare commit` to
commit your backup.

### Perform check on login

You can for instance make your session manager run `bare check` after login.
By doing it this way, a check is performed on every login and you get notified
if a new backup is needed.

#### XFCE and GNOME

Simply create a file in the path `~/.config/autostart/Backup Reminder.desktop` with the following content:

```config
[Desktop Entry]
Encoding=UTF-8
Version=0.9.4
Type=Application
Name=Backup Reminder
Comment=Checks if a backup is needed
Exec=<path-to-the-bare-binary> check
OnlyShowIn=XFCE;
RunHook=0
StartupNotify=false
Terminal=false
Hidden=false
```

**Update `<path-to-the-bare-binary>` following your configuration.**

## Attribution

The logo is the result of the transformation of the following original image
designed by: Christie L. Ward, CC BY-SA 3.0
<https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons
