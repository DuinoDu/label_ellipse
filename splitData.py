#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''

'''

import os, sys
import shutil

src = "./image"
dst = "./image_segment"

def getJPG(path):
    f = []
    for root, dirs, files in os.walk(path):
        for file in files:
            f.append(root + "/" + file)
    return f

def copy(files, dst):
    for index, f in enumerate(files):
        #index = '{0:0=4}'.format(index)
        #filename = dst + "/" + index + ".JPG" 
        filename = dst + '/' + os.path.split(f)[1]
        print 'copy ', f, filename
        shutil.copy(f, filename)


if __name__ == '__main__':

    print(__doc__)

    files = getJPG(src)
    sorted(files)
    if sys.argv[1] is None:
        print 'Set segmentation number first.'
        os._exit(0)
   
    number = int(sys.argv[1])
    step = len(files)/4
    if number is 0 or number is 1 or number is 2:
        files = files[number*step : (number+1)*step]
    elif number is 3:
        files = files[number*step:]
    else:
        print 'Error number'
        os._exit(0)

    copy(files, dst)
