import os
import hashlib
import sys
from filecmp import dircmp
from tqdm import tqdm
import time

# [! Define directories to compare !]
# for testing 
TESTSDIR = '/home/user/test/dir'
TESTDDIR = '/mnt/storageb/_bu/rsync/dir'
#DIR1 = TESTSDIR
#DIR2 = TESTDDIR

# for production
DIR1 = '/home/user/test/dir'
DIR2 = '/mnt/storageb/_bu/rsync/dir'

# [! Define functions !]

# [! Hash Files !]
def compute_md5(file_path):
    md5_hash = hashlib.md5()
    try:
        with open(file_path, 'rb') as file:
            while chunk := file.read(4096):
                md5_hash.update(chunk)
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None
    return md5_hash.hexdigest()

# [! Compare Directories and Files !]
def compare_directories(dir1, dir2):
    start_time = time.time()
    try:
        # Compare the directories
        dir_comparison = dircmp(dir1, dir2)

        # Print results
        print_diff_files(dir_comparison, dir1, dir2)

        # Check for any differences
        if dir_comparison.left_only or dir_comparison.right_only or dir_comparison.diff_files or dir_comparison.funny_files:
            print("Differences found in directory structure.")
            return False

        # Check files in both directories
        common_files = dir_comparison.common_files
        if common_files:
            print("\nStarting hash comparisons for common files...\n")
            for file_name in tqdm(common_files, desc="Checking file hashes", unit="file"):
                file1 = os.path.join(dir1, file_name)
                file2 = os.path.join(dir2, file_name)
                hash1 = compute_md5(file1)
                hash2 = compute_md5(file2)
                if hash1 != hash2:
                    print(f"Hash mismatch: {file1} (MD5: {hash1}) != {file2} (MD5: {hash2})")
                    return False
                else:
                    print(f"Hashes match: {file1} (MD5: {hash1}) == {file2} (MD5: {hash2})")
            print("\nHash comparisons completed.\n")

        # Recursively check subdirectories
        for sub_dir in dir_comparison.common_dirs:
            if not compare_directories(os.path.join(dir1, sub_dir), os.path.join(dir2, sub_dir)):
                return False

        end_time = time.time()
        print(f"Directory comparison completed in {end_time - start_time:.2f} seconds.")
        return True
    except Exception as e:
        print(f"Error comparing directories {dir1} and {dir2}: {e}")
        return False

# [! Print Differences !]
def print_diff_files(dir_comparison, dir1, dir2):
    if dir_comparison.left_only:
        print(f"Files only in {dir1}: {dir_comparison.left_only}")
    if dir_comparison.right_only:
        print(f"Files only in {dir2}: {dir_comparison.right_only}")
    if dir_comparison.diff_files:
        print(f"Files different in {dir1} and {dir2}: {dir_comparison.diff_files}")
    if dir_comparison.funny_files:
        print(f"Files that could not be compared in {dir1} and {dir2}: {dir_comparison.funny_files}")

# [! Main !]
def main():
    start_time = time.time()
    # Check if directories exist
    if not os.path.exists(DIR1):
        print(f"Error: Directory {DIR1} does not exist.")
        sys.exit(1)
    if not os.path.exists(DIR2):
        print(f"Error: Directory {DIR2} does not exist.")
        sys.exit(1)

    print(f"Comparing directories {DIR1} and {DIR2}...\n")

    # Perform the comparison
    are_identical = compare_directories(DIR1, DIR2)

    if are_identical:
        print(f"\nThe directories {DIR1} and {DIR2} are identical.")
    else:
        print(f"\nThe directories {DIR1} and {DIR2} are different.")

    end_time = time.time()
    print(f"Total execution time: {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    main()
