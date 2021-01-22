import hashlib
import os
import requests
import exifread
from pathlib import PurePath
from datetime import datetime

url = 'http://192.168.0.114:8880/photos/'

sourceDir = 'BookLive/Public/Shared Pictures/Scan'
destDir   = '/volume1/photo'

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
        
def getDir(filename, dateTaken):
    """This function takes the filename and date taken 
    create a dir name dest folder will be YYYY/MM/DD/filename
    If EXIF is unavailable, then the folder should be 
    destFolder/filename"""
    
    if dateTaken is None or tags is None:
        return PurePath(destDir, PurePath(filename).parent.name, PurePath(filename).name)	
    return  PurePath(destDir, dateTaken[:4], dateTaken[5:7], dateTaken[8:10], PurePath(filename).name)
print(sourceDir)
for root, dirs, files in os.walk(sourceDir, topdown=False):
    print(root)
    if "@eaDir" in root:
        continue
    print(root)
    hashes = {}
    for name in files:
        # Iterate through the all files, calculate MD5 hash of each file
        # Check the hash in DB, if the hash already there, we have duplicate
        # If not, create the new record and copy the file
        # Destination dir is determined from EXIF: if EXIF data exist
        # the destination directory will be YYYY/MM/DD
        # If the EXIF doesn't exist, the destination directory will 
        # be the same as source dir
        hashcode = hash_file(os.path.join(root, name))
        result   = requests.get(url + hashcode)
        if result.status_code == 200:
            print(os.path.join(root, name) + ' already present')
            continue
        #So, hash is unique, lets figure the destination dir
        with open(os.path.join(root, name), 'rb') as f:
            tags = exifread.process_file(f, details=False)
            dateTaken = None
            if tags and 'EXIF DateTimeOriginal' in tags:
                dateTaken =  str(tags['EXIF DateTimeOriginal'])[:10].replace(":", "-") + 'T' + str(tags['EXIF DateTimeOriginal'])[11:]
        destFileName = getDir(name, dateTaken) 
        if dateTaken is None:
            dateTaken = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        print(destFileName)
        #result = requests.post(url, json = {"name": name, "path": root, "hash": hashcode, "dateTaken": dateTaken})
        #shutil.move(root / name, destFileName)
