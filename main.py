import cv2
import numpy as np
import cvzone
import pickle

with open('carParkPos','rb') as f:
    poslist = pickle.load(f)

width, height = (508-400), (235-189)

def checkParkingSpace(vidProc):
    spaceCounter = 0
    for pos in poslist:
        x, y = pos
        vidCrop = vidProc[y:y+height,x:x+width]
        count = cv2.countNonZero(vidCrop)
        if count < 500:
            spaceCounter +=1
            color = (0,255,0)
            thickness = 3
        else:
            color = (0,0,255)
            thickness=1
        cvzone.putTextRect(vid, str(count),(x,y+height-2),scale=1,thickness=1,offset=0,
                           colorR=color)
        cv2.rectangle(vid, pos, (pos[0]+width,pos[1]+height),color,thickness)
        cvzone.putTextRect(vid, f'Free Space {spaceCounter}/{len(poslist)}',(450,50),
                           scale=2,thickness=3,offset=20,colorR=(255,200,0))



cap = cv2.VideoCapture('carPark.mp4')

while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)  #this if statement is used to loop the video
   
    success, vid = cap.read()

    vidGray = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)

    #video is made blurred to remove unnecessary edges(or noise)
    vidBlur = cv2.GaussianBlur(vidGray, (3,3),1)

    #the following statement is used to get edges of blurred video
    vidThreshold = cv2.adaptiveThreshold(vidBlur, 255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                          cv2.THRESH_BINARY_INV,25, 16)
    
    #remove remaining noise
    vidMedian = cv2.medianBlur(vidThreshold,5)

    #to broaden the edges 
    kernel = np.zeros((3,3),np.uint8)
    vidDilate = cv2.dilate(vidMedian,kernel, iterations=1)

    checkParkingSpace(vidDilate)


    cv2.imshow('carParking',vid)
    # cv2.imshow()
    cv2.waitKey(1)