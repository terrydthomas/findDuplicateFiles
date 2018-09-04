# findDuplicateFiles
This script walks through a directory to find duplicate files, it first eliminates by file size, then uses hashes as a descriptor for duplicate files.  After using file size, it eliminates further by comparing the first 'chunk' of a file (set to 1024 bytes by default), then finally displays groups of duplicate file paths of files with the same full hash.
