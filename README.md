## labelme_opencv
Simple image label tool using python and opencv.

##Usage:

### Step 0
Prepare data. Copy **.JPG into ./image folder

### Step 1
python splitData.py [number]

number is {0,1,2,3}

### Step 2

python labelme.py

1. Select rectangle using mouse.
2. Keyboard: "Space" ->  finish one rectangle
3. Keyboard: "d"     ->  delete rectangles
4. Keyboard: "Enter" ->  finish one image, write annotation into txt, and next.
5. Keyboard: "Esc"   ->  exit

### Step 3

python checkLabel.py
