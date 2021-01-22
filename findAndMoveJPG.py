# This script searches all dirs and subdirs in basedir, finds JPG images, checks EXIF
# and moves file to directory basedir/DATE/filename, where DATE is derived from EXIF DateTimeOriginal tag

import os
import sys
from os.path import join, exists
import exifread
import shutil
import hashlib

basedir = 'BookLive/Shared Pictures/Copy/'
destBase = '/var/services/photo'

excludeDirs = set(['@eaDir'])
filesMoved  = 0

def hash_file(filename):
    """"This function returns the SHA-1 hash
    of the file passed into it"""
    # make a hash object
    h = hashlib.sha1()
    # open file for reading in binary mode
    with open(filename,'rb') as file:
        # loop till the end of the file
        chunk = 0
        while chunk != b'':
            # read only 1024 bytes at a time
            chunk = file.read(1024)
            h.update(chunk)
        # return the hex representation of digest
        return h.hexdigest()

for folder, subs, files in os.walk(basedir, topdown=True):
    subs[:] = [d for d in subs if d not in excludeDirs ]
    for filename in files:
        exists_already = False
        if filename.endswith(('jpg', 'JPG', 'tiff', 'TIFF')):
            with open(join(folder, filename), 'rb') as f:
                tags = exifread.process_file(f, details=False)
                if tags and 'EXIF DateTimeOriginal' in tags:
                    destDir = join(destBase, str(tags['EXIF DateTimeOriginal'])[:10].replace(':', '-'))
                    if folder != destDir:
                        if not exists(destDir):
                            os.makedirs(destDir)
                else:
                    destDir = join(destBase, 'no-date')
                hashsum = hash_file(join(folder, filename))
                for f in os.listdir(destDir):
                    if not os.path.isdir(os.path.join(destDir, f)) and hashsum == hash_file(join(destDir, f)):
                        print('The same file as ' + filename + ' already exists in ' + destDir)
                        exists_already = True
                        break
                fname = filename
                if  not exists_already:
                    if exists(join(destDir, filename)):
                        fname, ext = os.path.splitext(filename)
                        fname = fname + '_1' + ext
                        print('Rename the file to ' + fname)
                    shutil.move(join(folder, filename), join(destDir, fname))
                    filesMoved += 1
                else:
                    print('Removing ' + join(folder, filename))
                    os.remove(join(folder, filename))
print('Moved ' + str(filesMoved) + ' files')
