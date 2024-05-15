# bucheck

`bucheck` is a utility for comparing directories and verifying backups. It provides functionality to compute hashes of files, compare directory structures and files, and ensure that the backup process has been executed correctly. It will identify differences in file content as well as missing or unique files in either the source or backup destination directory.

## Features

- **Hash Files:** Compute MD5 hashes of files to ensure data integrity.
- **Compare Directories:** Compare directory structures and files to identify differences.
- **Detailed Reporting:** Generate detailed reports of any discrepancies found during the comparison.

### Two Utilities

`backup.verbose.py` is meant to be more reliable, but isn't too slow. I verified a diverse source and destination directory of ~240G in ~`29`s. Also, thanks to the use of hashing, it's meant to be very accurate in detecting file differences.

`backup.fastest.py` is meant to be the fastest way to perform this kind of check, that I'm aware of. Again, that same ~240G took ~`3.7`s with this utility. I feel that without hashing, this version is almost _assuming_ rather than verifying, though it hasn't failed to function as intended as of yet.

## Installation

### Requirements

```json
{
  "Language": ["Python3"],
  "Libraries": ["os", "hashlib", "sys", "from filecmp import dircmp", "from tqdm import tqdm", "time"],
  "Shell": "Bash compatible"
}
```

### Preferences

```json
{
  "OS": "Linux",
  "Kernel": ">=6.5",
  "Distro": ["Fedora", "Ubuntu", "Debian"]
}
```

To use `bucheck`, you need to have Python 3 installed. You can clone the repository and navigate to the `bucheck` directory.

```sh
git clone https://github.com/jonz-secops/backitupup.git
cd backitupup/bucheck
```

## Usage

### Command Line

You can use the bucheck.verbose.py script from the command line. Here’s how to run it:

```sh
python3 bucheck.verbose.py
```

#### Script Options

Define Directories to Compare:

For testing:

```python
TESTSDIR = "/home/user/test/dir"
TESTDDIR = "/mnt/storageb/_bu/rsync/dir"
# DIR1 = TESTSDIR
# DIR2 = TESTDDIR
```

For production:

```python
DIR1 = "/home/user/test/dir"
DIR2 = "/mnt/storageb/_bu/rsync/dir"
```

## Example

Here's an example of using bucheck to compare two directories:

```sh
python3 bucheck.verbose.py
```

## Functions

### compute_md5(file_path)

Computes the MD5 hash of the given file.

### compare_directories(dir1, dir2)

Compares the directory structures and files of dir1 and dir2. It prints out any differences found and performs hash comparisons for common files.

### print_diff_files(dir_comparison, dir1, dir2)

Prints the differences between the directories.

## Output

The script will output the comparison results directly to the console, including any differences found in the directory structure and the results of the hash comparisons.

## Security

Defined by repo.

## License

Defined by repo.
