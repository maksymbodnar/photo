import hashlib
import os

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
        if hashcode in hashes:
            print('In dir ' + root + ': ' + name + ' is the same as ' + hashes[hashcode])
            print('Removing ' + os.path.join(root, name))    
            os.remove(os.path.join(root, name))    
        hashes[hashcode] = name
