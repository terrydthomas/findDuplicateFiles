#!/usr/bin/env python2
__doc__ = """
findDuplicateFiles - finds duplicate files in a directory tree.

This script walks through a directory to find duplicate files,
it first eliminates by file size, then uses hashes as a
descriptor for duplicate files.

After using file size, it eliminates further by comparing
the first 'chunk' of a file (set to 1024 bytes by default),
then finally displays groups of duplicate file paths of files
with the same full hash.

"""
__author__ = "Terry Thomas"
__email__ = "terrydthomasuk@gmail.com"
__date__ = "09/02/2018"
__usage__ = "findDuplicates <directory path>"

import os
import sys
import hashlib
from collections import defaultdict
from scandir import walk

def parseArgs(args):

    help = "Please provide a valid directory"

    try:
        dirPath = args[1]
    except IndexError:
        print help
        exit(0)

    if not os.path.exists(dirPath):
        print "Directory does not exist... {0}".format(help)
        exit(0)

    return dirPath


def findDuplicateSizes(dirPath):
    # walks through directory to find files and sizes

    fileSizes = defaultdict(list)

    for root, _, fileNames in walk(dirPath):
        for fileName in fileNames:
            filePath = os.path.join(root, fileName)

            try:
                fileSize = os.stat(filePath).st_size
            except OSError as e:
                print "Could not access file {0} \
                       continuing...".format(filePath)
                print e
                # file not accessible - move on
                continue

            # use file size as dictionary key to group files by size
            fileSizes[fileSize].append(filePath)

    return fileSizes


def readChunks(fileObj, chunkSize):
    # Generator function to read a file in chunks
    while True:
        chunk = fileObj.read(chunkSize)
        if not chunk:
            return
        else:
            yield chunk


def hashFile(filePath, firstRun, hasher=hashlib.sha1, chunkSize=1024):
    # returns the hash of a file by updating in chunks, if firstRun is True
    # it will only read the first chunk

    # TO DO (?): compare actual speeds and hash sizes

    hashObj = hasher()

    with open(filePath, 'rb') as fileObj:
        if firstRun:
            hashObj.update(fileObj.read(chunkSize))
        else:
            for chunk in readChunks(fileObj, chunkSize):
                hashObj.update(chunk)

    return hashObj.hexdigest()


def findDuplicateHashes(fileDict, firstRun=False):
    hashDuplicates = defaultdict(list)

    for _, filePaths in fileDict.items():
        # only check duplicates (sizes with more than one file)
        if len(filePaths) < 2:
            continue

        for filePath in filePaths:
            fileHash = hashFile(filePath, firstRun)

            # use hash as a dictionary key to group files by hash
            hashDuplicates[fileHash].append(filePath)

    return hashDuplicates


def printDuplicates(filePaths):
    # function to format printing duplicate files

    # correct grammar for multiple duplicates
    if len(filePaths) > 2:
        plural = 's'
    else:
        plural = ''

    print "\nDuplicate{0} found!".format(plural)
    for filePath in filePaths:
        print filePath


def main():
    dirPath = parseArgs(sys.argv)

    print "Scanning {0} for duplicate files...".format(dirPath)

    fileSizes = findDuplicateSizes(dirPath)

    firstHashDuplicates = findDuplicateHashes(fileSizes, firstRun=True)
    fullHashDuplicates = findDuplicateHashes(firstHashDuplicates, firstRun=False)

    foundDuplicates = False

    for _, filePaths in fullHashDuplicates.items():
        # only show duplicates (hashes with more than one file)
        if len(filePaths) < 2:
            continue
        foundDuplicates = True

        printDuplicates(filePaths)

    if not foundDuplicates:
        print "No duplicates found"


if __name__ == '__main__':
    sys.exit(main())
