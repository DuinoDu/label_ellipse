#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
###########
Check label tool

y: yes and next
n: no, record error label and next

After finishing this, go to ./relabel folder and relabel using relabel/labelme.py
'''

import cv2
import os
import shutil

def drawNumber(im, number):
    def draw_str(dst, target, s):
        x, y = target
        cv2.putText(dst, s, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 255), lineType=cv2.LINE_AA)
    draw_str(im, (5,15), "Number:")
    draw_str(im, (5,30), str(number))

def copyErrorImage(errFile):
    """copy error label image file to new fold 'relabel' 
    """
    if not os.path.isdir('./relabel'):
        os.mkdir('./relabel')
    if not os.path.isdir('./relabel/annotation'): 
        os.mkdir('./relabel/annotation')
    if not os.path.isdir('./relabel/image_segment'):
        os.mkdir('./relabel/image_segment')
    if not os.path.exists('./relabel/labelme.py'):
        shutil.copy('./labelme.py', './relabel/labelme.py')
    shutil.copy(errFile, './relabel/image_segment/' + os.path.split(errFile)[1])
     

def main():
    """TODO: Docstring for main.
    1. display image
    2. read label from annotation file
    3. draw rectangle in the image
    """

    imgfiles = os.listdir('image_segment/')
    imgfiles = sorted(imgfiles)
    labelfiles = os.listdir('annotation/')
    labelfiles = sorted(labelfiles)

    if len(imgfiles) is not len(labelfiles):
        print "wrong number label files"

    # add file path
    imgfiles2 = []
    for f in imgfiles:
        imgfiles2.append('image_segment/'+f)
    imgfiles = imgfiles2
    labelfiles2 = []
    for f in labelfiles:
        labelfiles2.append('annotation/'+f)
    labelfiles = labelfiles2

    #print imgfiles
    #print labelfiles

    cv2.namedWindow('image')

    for imgfile in imgfiles:
        im = cv2.imread(imgfile)
        filename = os.path.splitext(os.path.split(imgfile)[1])[0]
        
        # get labels
        labelID = -1
        filename = os.path.splitext(os.path.split(imgfile)[1])[0]
        for index, labelfile in enumerate(labelfiles):
            labelfilename = os.path.splitext(os.path.split(labelfile)[1])[0]
            
            if int(filename) == int(labelfilename):
                labelID = index
                break
            else:
                continue
        if labelID is -1:
            print "error labelID"
            break
       
        # get rectangles
        rects = []
        f = open(labelfiles[labelID], 'r')
        filename_read = f.readline().split('\n')[0]
        if(int(filename_read) == int(filename)):
            rectNumber = int(f.readline().split('\n')[0])
            for i in range(rectNumber):
                rects.append(f.readline().split('\n')[0])
        f.close()
    
        print rects

        #print os.path.split(imgfile)[1], "nums:", len(rects) 
        drawNumber(im, len(rects)) 
        for r in rects:
            (x1, y1, x2, y2) = eval(r)
            cv2.rectangle(im,(int(x1), int(y1)),(int(x2), int(y2)), (255,255,0),2)
        
        im = cv2.resize(im, (int(im.shape[1]*2), int(im.shape[0]*2)))
        cv2.imshow('image', im)
        ch = 0xFF & cv2.waitKey(0)
        while True:
            if ch == 27: 
                break
            elif ch == ord('y'):
                break
            elif ch == ord('n'):
                print "Error label image file:", imgfile
                copyErrorImage(imgfile)
                break
            else:
                ch = 0xFF & cv2.waitKey(0)
        if ch == 27:
            break

if __name__ == "__main__":
    print(__doc__)
    main()
