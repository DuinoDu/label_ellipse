
'''
================
Label image tool
================
Usage:
1. Select rectangle using mouse.
2. Keyboard: "Space" ->  finish one rectangle
3. Keyboard: "d"     ->  delete rectangles
4. Keyboard: "g" ->  finish one image, write annotation into txt, and next.
5. Keyboard: "Esc"   ->  exit
'''


import numpy as np
import cv2
import os

IMG = "./image_segment"
DST = "annotation"


def onmouse(event,x,y,flags,param):
    global im, x1, y1, x2, y2, state

    img = im.copy()
    # Draw Rectangle
    if event == cv2.EVENT_LBUTTONDOWN:
        if state is 0 or state is 2:
            state = 1
            x1, y1 = x,y

    elif event == cv2.EVENT_MOUSEMOVE:
        if state is 1 :
            cv2.rectangle(img,(x1,y1),(x,y), (255,255,0),2)
        elif state is 2:
            cv2.rectangle(img,(x1,y1),(x2,y2), (255,0,0),2)

    elif event == cv2.EVENT_LBUTTONUP:
        if state is 1:
            state = 2
            x2, y2 = x,y
            cv2.rectangle(img,(x1, y1),(x2,y2), (255,255,0),2)
            #label.append((x1*scale, y1*scale, x2*scale, y2*scale))

    cv2.imshow('image', img)

state =  0
scale = 0.5
im = np.zeros((100,100)) #cv2.imread('start.jpg')
x1,y1, x2,y2 = 0,0,0,0
label = []



def writeFile(filename):
    f = open(filename, 'w')
    imgNumber = os.path.splitext(os.path.split(filename)[1])[0]
    f.write(imgNumber + "\n")
    f.write(str(len(label)) + "\n")
    for e in label:
        f.write(str(e)+"\n")
    f.close()


def drawText(im):
    def draw_str(dst, target, s):
        x, y = target
        cv2.putText(dst, s, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 255), lineType=cv2.LINE_AA)
    
    draw_str(im, (5,15), "d : delete rectangle")
    draw_str(im, (5,30), "space : finish rectangle")
    draw_str(im, (5,45), "g : next image")
    draw_str(im, (5,60), "a : previous image")


def main():
    global im
    global label
    global x1, y1, x2, y2

    cv2.namedWindow('image')
    cv2.setMouseCallback('image',onmouse)
    
    imgfiles = os.listdir( IMG )
    imgfiles = sorted(imgfiles)
    i = 0

    while True:
        if i < 0:
            i = 0
        if i >= len(imgfiles):
            i = len(imgfiles)-1
        
        imgfile = imgfiles[i]
        if '.JPG' in imgfile:
            print imgfile
            im = cv2.imread( IMG + "/" + imgfile)
            drawText(im)
            im = cv2.resize(im, (int(im.shape[1]/scale), int(im.shape[0]/scale)))
            cv2.imshow('image', im)
      
            ch = 0
            while True:
                ch = 0xFF & cv2.waitKey(0)
                if ch == 27:
                    break
                elif ch == ord('g'): # finish one image  [enter]
                    (filename,ext) = os.path.splitext(imgfile)
                    writeFile(DST + "/"+ filename +".txt")
                    state = 0
                    i = i + 1
                    label = []
                    x1,y1, x2,y2 = 0,0,0,0
                    break
                elif ch == ord('a'):
                    i -= 1
                    state = 0
                    label = []
                    x1,y1, x2,y2 = 0,0,0,0
                    break
                elif ch == 32: # finish rectangle [space]
                    label.append((x1*scale, y1*scale, x2*scale, y2*scale))
                    cv2.rectangle(im, (x1, y1), (x2,y2), (255,0,0),2)
                    cv2.imshow('image', im)
                elif ch == ord('d'): # clear current rectangle
                    state = 0
                    label = []
                    x1,y1, x2,y2 = 0,0,0,0
                    break
            if ch == 27: 
                break
        else:
            i += 1

if __name__ == '__main__':
    print(__doc__)
    main()

