import cv2
import pickle

width, height = (508-400), (235-189)

try:
    with open('carParkPos','rb') as f:
        poslist = pickle.load(f)
except:
    poslist = []

def mouseclick(events, x,y,flags,params):
    if events==cv2.EVENT_LBUTTONDOWN:
        poslist.append((x,y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i,pos in enumerate(poslist):
            x1,y1=pos
            if x1<x<(x1+width) and y1<y<(y1+height):
                poslist.pop(i)
    with open('carParkPos', 'wb') as f:
        pickle.dump(poslist,f)

while True:
    img = cv2.imread('carPark.png')
    cv2.rectangle(img,(400,189),(508,235),(255,0,255),2)

    for pos in poslist:
        cv2.rectangle(img, pos,(pos[0]+width,pos[1]+height),(255,0,255),2)
    
    cv2.imshow('parking',img)
    cv2.setMouseCallback('parking',mouseclick)

    cv2.waitKey(1)