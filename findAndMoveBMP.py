import os
import sys
from os.path import join, exists
import exifread
import shutil
import hashlib

basedir = 'BookLive/Shared Pictures/Copy/'
destBase = '/var/services/photo/bmp/'

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

hashes = {}


for folder, subs, files in os.walk(basedir, topdown=True):
    for filename in files:
        if filename.endswith(('bmp', 'BMP')):
            dirName = folder[folder.rfind('/') + 1:]
            print('Move ' + filename + ' to ' + join(destBase, dirName))        
            hash_sum = hash_file(join(folder, filename))
            if not hash_sum in hashes:
                hashes[hash_sum] = filename
                if not exists(join(destBase, dirName)):
                    os.makedirs(join(destBase, dirName))
                shutil.move(join(folder, filename), join(destBase, dirName, filename))
            else:
                print('There is a file ' + filename + ' in ' + join(destBase, dirName) + ', removing ')
                os.remove(join(folder, filename))

