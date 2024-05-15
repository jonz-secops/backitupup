#!/bin/bash

# Ensure script is executable: chmod +x /path/to/your/script.sh
# or run it with 'bash /path/to/your/backup/script.sh'

# Exit immediately if a command exits with a non-zero status
set -e

# Function to handle errors
error_exit() {
  echo "Error: $1" | tee -a "$LOG_FILE"
  exit 1
}

# Path to the rsync command
RSYNC=$(which rsync)

# Verify the path to rsync
if [ ! -x "${RSYNC}" ]; then
  error_exit "rsync not found at ${RSYNC}"
fi

# Home directory
HOME=$(eval echo ~$USER)

# Process to look for and kill before backup
PROCTK="/app/trilium/trilium"

# [! Definition of backup source and destination directories and files to back up !]

# Define your source directories and files
# [! Testing directory !]
# testdir='/home/user/test/dir'
# BACKUP_THIS=("$testdir") # Add additional directories or files to this array

# [! Production directories !]
# this is setup for trillium local-backup backup
dir1='/home/user/.local/share/trilium-data/backup/*.db'
# dir2='/path/to/another/directory'
# file1='/path/to/some/file'
# file2='/path/to/another/file'
BACKUP_THIS=("$dir1") # Add additional directories or files to this array

# [! Path to the backup destination directory !]
# this is customized to the process you are backing up
# in this case, it is the Trilium note-taking app
BACKUP_TO="$HOME/_bu/rsync/${PROCTK##*/}" # parameter expansion to get the process name and not whole path string

# some cool options using parameter expansion
# echo "${PROCTK##*/}" # trilium
# echo "${PROCTK%/*}" # /app/trilium
# echo "${PROCTK//\//}" # apptrilium

# Ensure the backup directory exists
mkdir -p "$BACKUP_TO" || error_exit "Failed to create backup directory: $BACKUP_TO"

# Create a timestamp for the backup
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")

# Create a new backup directory with the timestamp
BACKUP_DIR="$BACKUP_TO/${PROCTK##*/}_$TIMESTAMP"

# rsync command options
RSYNC_OPTS="-avz --delete --progress"

# Log file for backup operations
LOG_FILE="$BACKUP_TO/backup_log_${TIMESTAMP}.txt"

# Check if the process is running, kill it if found
PID=$(ps -ef | grep -i -P "$PROCTK" | awk '!length($9) {print $2}') # pgrep doesn't handle edge cases as well as this
if [ -n "$PID" ]; then
  echo "Killing process $PROCTK with PID $PID..." | tee -a "$LOG_FILE"
  kill -9 "$PID" || error_exit "Failed to kill process: $PROCTK with PID $PID"
fi

# Start backup using rsync
echo "Starting backup..." | tee -a "$LOG_FILE"

# Ensure the backup directory exists
mkdir -p "$BACKUP_DIR" || error_exit "Failed to create backup directory: $BACKUP_DIR"

# Perform the backup and log the output
for SOURCE in "${BACKUP_THIS[@]}"; do
  # Expand wildcard characters in the source path
  for file in $SOURCE; do
    if [ -e "$file" ]; then
      $RSYNC $RSYNC_OPTS "$file" "$BACKUP_DIR" | tee -a "$LOG_FILE" || error_exit "rsync failed for $file"
    else
      echo "Warning: Source $file does not exist" | tee -a "$LOG_FILE"
    fi
  done
done

echo "Backup completed successfully at $TIMESTAMP" | tee -a "$LOG_FILE"

# Optionally, delete old backups older than a certain number of days
# For example, delete backups older than 30 days
find "$BACKUP_TO" -name "${PROCTK##*/}_*" -type d -mtime +30 -exec rm -rf {} \; || error_exit "Failed to delete old backups"

echo "Old backups cleanup completed" | tee -a "$LOG_FILE"
