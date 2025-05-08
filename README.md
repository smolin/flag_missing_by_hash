# flag_missing_by_hash

Walk two directory trees, computing hashes for all files. Emit a list of files
in one that are not found in the other. Intended to be useful when you have
multiple copies of a large directory tree (like btrfs snapshots, for instance),
where files may have been renamed and reorganized, and you want to know if
removing one of the copies will result in the loss of irreplacable files.



# Usage

    Usage: flag_missing_by_hash <candidate_dir> <baseline_dir>



# Example

    % flag_missing_by_hash possibly_obsolete/ currently_configured/
