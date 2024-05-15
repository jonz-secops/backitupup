# simplebu

`simplebu` is a straightforward utility designed for performing basic local backups. It enables users to easily backup and synchronize directories, ensuring that important files are duplicated and up-to-date in the backup location.

`simplebu.trilian` is setup specifically to backup the awesome notebook app 'Trilium' <https://github.com/zadam/trilium> which automatically creates a local DB backup, but it would be smart to copy that to a seperate drive.

## Features

- **Simple Backup:** Perform basic directory backups with minimal configuration.
- **Easy Scheduled Job Integration:** Because time based directories are utilized as well as the process name for folder name, it's easier to adopt this to recurring backup jobs.
- **Ease of Use:** User-friendly command-line interface for straightforward operations.

## Installation

### Requirements

```json
{
  "Language": ["Python3"],
  "Libraries": ["os", "shutil", "sys", "time"],
  "Shell": "Bash compatible"
}

Preferences

json

{
  "OS": "Linux",
  "Kernel": ">=6.5",
  "Distro": ["Fedora", "Ubuntu", "Debian"]
}

To use simplebu, you need to have Python 3 installed. You can clone the repository and navigate to the simplebu directory.

```sh
git clone https://github.com/jonz-secops/backitupup.git
cd backitupup/simplebu
```

## Usage

### Command Line

You can use the simplebu.py script from the command line. Here’s how to run it:

```sh
python3 simplebu.py
```

### Script Options

#### Define Source and Backup Directories:

For testing:
```python
SOURCE_DIR = "/home/user/source"
BACKUP_DIR = "/mnt/backup"
```

For production:

```python
SOURCE_DIR = "/home/user/source"
BACKUP_DIR = "/mnt/backup"
```

### Example

Here's an example of using simplebu to backup a directory:

```sh
python3 simplebu.py
```

## Functions

### backup_directory(source, backup)

Copies files from the source directory to the backup directory, ensuring that the backup directory is synchronized with the source.

### synchronize_directories(source, backup)

Synchronizes the contents of the source and backup directories, copying new and updated files while removing files that no longer exist in the source.

## Output

The script will output the backup and synchronization results directly to the console, including any files copied, updated, or removed.

## Security

Defined by repo.

## License

Defined by repo.
