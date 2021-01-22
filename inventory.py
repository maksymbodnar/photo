import hashlib
import os
import requests
import exifread

url = 'http://192.168.0.114:8880/photos/'

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
        
for root, dirs, files in os.walk("/var/services/photo", topdown=False):
    if "@eaDir" in root:
        continue
    print(root)
    hashes = {}
    for name in files:
        hashcode = hash_file(os.path.join(root, name))
        result   = requests.get(url + hashcode)
        if result.status_code == 200:
            print(hashcode + ' ' + os.path.join(root, name) + ' already present for ' + result.text)
            continue
        dateTaken = None 
        with open(os.path.join(root, name), 'rb') as f:
            tags = exifread.process_file(f, details=False)
            if tags and 'EXIF DateTimeOriginal' in tags:
                dateTaken =  str(tags['EXIF DateTimeOriginal'])[:10].replace(":", "-") + 'T' + str(tags['EXIF DateTimeOriginal'])[11:]
        if dateTaken is None:
            dateTaken = '2021-01-01T00:00:00'
        result = requests.post(url, json = {"name": name, "path": root, "hash": hashcode, "dateTaken": dateTaken})
