import os
import sys
from filecmp import dircmp, cmpfiles
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

# [! Compare Directories and Files !]
def compare_directories(dir1, dir2):
    dir_comparison = dircmp(dir1, dir2)
    differences_found = print_diff_files(dir_comparison, dir1, dir2)

    # Recursively check subdirectories
    for sub_dir in dir_comparison.common_dirs:
        sub_dir1 = os.path.join(dir1, sub_dir)
        sub_dir2 = os.path.join(dir2, sub_dir)
        if not compare_directories(sub_dir1, sub_dir2):
            differences_found = True

    # Check for mismatched or errored files in common directories
    match, mismatch, errors = cmpfiles(dir1, dir2, dir_comparison.common_files)
    if mismatch or errors:
        print(f"Mismatched files: {mismatch}")
        print(f"Errored files: {errors}")
        differences_found = True

    return not differences_found

# [! Print Differences !]
def print_diff_files(dir_comparison, dir1, dir2):
    differences_found = False
    if dir_comparison.left_only:
        print(f"Only in {dir1}: {dir_comparison.left_only}")
        differences_found = True
    if dir_comparison.right_only:
        print(f"Only in {dir2}: {dir_comparison.right_only}")
        differences_found = True
    if dir_comparison.diff_files:
        print(f"Differing files in {dir1} and {dir2}: {dir_comparison.diff_files}")
        differences_found = True
    if dir_comparison.funny_files:
        print(f"Problematic files in {dir1} and {dir2}: {dir_comparison.funny_files}")
        differences_found = True
    return differences_found

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
