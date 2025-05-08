#!/usr/bin/env python3

import hashlib
import os
from pathlib import Path

def calculate_checksum(file_path):
    """Calculate SHA-256 checksum of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def get_all_files_with_checksums(directory):
    """Get all files and their checksums in a directory recursively."""
    file_hashes = {}
    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = Path(root) / filename
            checksum = calculate_checksum(filepath)
            file_hashes[checksum] = str(filepath)
    return file_hashes

def compare_directories(candidate_dir, baseline_dir):
    """Compare directories using checksums."""
    # Get all files from both directories
    files_a = get_all_files_with_checksums(candidate_dir)
    files_b = get_all_files_with_checksums(baseline_dir)

    # Find files that exist in candidate_dir but not in baseline_dir
    unique_files = {
        checksum: filepath 
        for checksum, filepath in files_a.items() 
        if checksum not in files_b
    }

    return unique_files

def main():
    import sys

    if len(sys.argv) != 3:
        print("Usage: python script.py <candidate_dir> <baseline_dir>")
        sys.exit(1)

    candidate_dir, baseline_dir = sys.argv[1], sys.argv[2]

    if not os.path.isdir(candidate_dir) or not os.path.isdir(baseline_dir):
        print("Error: Both arguments must be valid directories")
        sys.exit(1)

    unique_files = compare_directories(candidate_dir, baseline_dir)

    print(f"\nFiles found in {candidate_dir} but not in {baseline_dir}:")
    if unique_files:
        for checksum, filepath in unique_files.items():
            print(f"- {filepath}")
    else:
        print("No unique files found.")

if __name__ == "__main__":
    main()
