import os
import sys
from os.path import join, exists
import exifread
import shutil
import time
import datetime

basedir  = '../../photo/ImportIPhone/iCloud Photos/'
destBase = '/var/services/video/imports'

excludeDirs = set(['@eaDir'])
filesMoved  = 0

for folder, subs, files in os.walk(basedir, topdown=True):
    subs[:] = [d for d in subs if d not in excludeDirs ]
    for filename in files:
        if filename.endswith(('avi', 'AVI', 'mp3', 'MP3', 'mov', 'MOV')):
            destDir = join(destBase, datetime.date.fromtimestamp(os.path.getmtime(join(folder, filename))).strftime('%Y-%m-%d'))
            if not exists(destDir):
                os.makedirs(destDir)
            #shutil.move(join(folder, filename), join(destDir, filename))
            if not exists(join(destDir, filename)):
                shutil.copy(join(folder, filename), join(destDir, filename))
                filesMoved += 1
print('Moved ' + str(filesMoved) + ' files')
