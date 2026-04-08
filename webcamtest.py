#IMPORT IMPORTANT LIBS
import cv2
import mediapipe as mp
import numpy as np

mpHands=mp.solutions.hands
mpDraw=mp.solutions.drawing_utils

#HAND OBJECT
hands=mpHands.Hands(
    max_num_hands=1,
    min_detection_confidence=.5,
    min_tracking_confidence=.5
)

#VIDEO CAPTURE
cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

#CREATING OUR CANVAS TO DRAW AT
canvas=np.zeros((700,800,3), dtype=np.uint8)
drawColor=(236,80,78)
drawThickness=3
pause=False
x_prev, y_prev=None, None

#FUNCTION TO CHECH IF ALL FINGERS IS UP (USED FOR CLEARING)
def isOpenHand(hand):
    fingers=0

    if hand.landmark[4].x < hand.landmark[3].x  :
        fingers+=1
    if hand.landmark[8].y < hand.landmark[7].y  :
        fingers+=1
    if hand.landmark[12].y < hand.landmark[11].y:
        fingers+=1
    if hand.landmark[16].y < hand.landmark[15].y:
        fingers+=1
    if hand.landmark[20].y < hand.landmark[19].y:
        fingers+=1
    return fingers == 5

#FUNCTION TO CHECK IF THUMB IS UP (USED FOR TEMP STOPING)
def isThumbUp(hand):
    return hand.landmark[4].x < hand.landmark[3].x


while True:
    ret,frame=cap.read()
    if not ret:
        print("camera not detected! ")
        break

    frame=cv2.resize(frame, (800,700))
    frame=cv2.flip(frame,1)
    rgb=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result=hands.process(rgb)

    x_index, y_index =None, None

    #MANAGING HAND MOVEMENT
    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            mpDraw.draw_landmarks(frame, hand, mpHands.HAND_CONNECTIONS)

            h, w, c = frame.shape
            indexTip=hand.landmark[8]
            x_index=int(indexTip.x * w)
            y_index=int(indexTip.y * h)

            cv2.circle(frame, (x_index, y_index), 7, (254,58,90), -1)

            if isOpenHand(hand):
                canvas=np.zeros((700,800,3), dtype=np.uint8)
                cv2.putText(frame, "HAND OPENED - CLEAR ", (10,600), cv2.FONT_HERSHEY_COMPLEX, 0.9, (88,90,76), 3 )
            if isThumbUp(hand):
                 pause=True
                 cv2.putText(frame, "Thumb's up - stopped drawing", (10,500), cv2.FONT_HERSHEY_COMPLEX, 0.9,(88,90,76),3 )
            else:
                pause=False
    

    #CHOOSING DRAWING COLOR
    cv2.putText(frame, 'COLORS: green=g | blue=b | red=r | yellow=y | magenta=m |cyan=c| white=w', (20,50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.9, (255, 8, 76), 1)
    key=cv2.waitKey(1) & 0xFF
    if key == ord("g"):
        drawColor=(0,255,0)
    elif key == ord("b"):
        drawColor=(255,0,0)
    elif key == ord("r"):
        drawColor=(0,0,255)
    elif key == ord("y"):
        drawColor=(0,255,255)
    elif key == ord("m"):
        drawColor=(255,0,255)
    elif key == ord('c'):
        drawColor=(255, 255, 0)
    elif key == ord("w"):
        drawColor=(255,255,255)

    #MANAGE THE ACTUAL DRAWING
    if not pause and x_index is not None and y_index is not None:
        if x_prev is None and y_prev is None:
            x_prev, y_prev = x_index, y_index
        else:
            cv2.line(canvas, (x_prev, y_prev), (x_index, y_index), drawColor, drawThickness)
            x_prev, y_prev = x_index, y_index
    else:
        x_prev,y_prev=None, None
    
    #PUT CANVAS ABOVE FRAME
    canvasAndFrame=cv2.addWeighted(frame, 1, canvas, 1, 0)
    cv2.putText(frame, 'Hi draw with your index finger', (10,30), cv2.FONT_HERSHEY_COMPLEX, 0.9, (99,45,78), 2)
    cv2.putText(frame, 'open hand to clear  |  thumb up to stop drawing', (10,100), cv2.FONT_HERSHEY_COMPLEX, 0.9, (99,45,78), 2)

    #DISPLAYING THE CAMERA
    cv2.imshow('FULL frame with canvas',canvasAndFrame)
    cv2.imshow('canvas only', canvas)

    key=0
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#DESTROY
cap.release()
cv2.destroyAllWindows()


