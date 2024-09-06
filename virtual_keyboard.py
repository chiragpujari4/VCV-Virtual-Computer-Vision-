#Jay Shree Ganeshaya Namah
#Jay Mata Di

import cv2
import mediapipe as mp
import pyautogui
from time import sleep
import cvzone
from pynput.keyboard import Controller


cap=cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
hand_detector=mp.solutions.hands.Hands() #[Inbuilt function of mediapipe.]
drawing_utils=mp.solutions.drawing_utils #[importing drawing utilities to draw landmarks.]
screen_width, screen_height = pyautogui.size() #[To get the screen size.]
index_y=0

keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]
finalText=""

def drawALL(img,buttonList):
    for button in buttonList:
        x,y=button.pos
        w,h=button.size
        cv2.rectangle(img, button.pos,(x+w,y+h),(255,0,255),cv2.FILLED)
        cv2.putText(img,button.text, (x+20,y+65), cv2.FONT_HERSHEY_PLAIN,4, (255,255,255), 4)
    return img    

class Button:
    def __init__(self, pos, text, size=[85,85]):
        self.pos=pos
        self.size=size
        self.text=text
        
       # return img
    
buttonList=[]
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100*j+50,100*i+50], key))


while True:
    success,img=cap.read()
    img=cv2.flip(img, 1) #[To flip at y axis.]
    img_height, img_width, _ = img.shape
    rgb_frame=cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #[Convert BGR to RGB.]
    output= hand_detector.process(rgb_frame)
    hands=output.multi_hand_landmarks #[hands=landmarks.]
    if hands:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size
        for hand in hands:
            drawing_utils.draw_landmarks(img, hand) #[To draw landmarks.]
            landmarks=hand.landmark
            for id, landmark in enumerate(landmarks): #[For using the point numbers.]
                x=int(landmark.x*img_width)
                y=int(landmark.y*img_height)

                if id==8: #[Index finger point id.]
                    cv2.circle(img=img, center=(x,y), radius=10, color=(0,255,255)) #[To draw circle.]
                    index_x=(screen_width/img_width)*x
                    index_y=(screen_height/img_height)*y
                    
                    pyautogui.moveTo(index_x,index_y) #[To move the cursor.]
                if id==12: #[Thumb finger point id.]
                    cv2.circle(img=img, center=(x,y), radius=10, color=(0,255,255)) #[To draw circle.]
                    thumb_x=(screen_width/img_width)*x
                    thumb_y=(screen_height/img_height)*y
                    if abs((thumb_y-index_y)<30):
                        pyautogui.press(button.text)
                        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 20, y + 65),cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                        finalText += button.text
                        
    cv2.rectangle(img,(50,350),(700,450),(175,0,175),cv2.FILLED)
    cv2.putText(img,finalText, (60,425), cv2.FONT_HERSHEY_PLAIN,5, (255,255,255), 5)                  
    
    img=drawALL(img,buttonList)
    
    cv2.imshow("Image", img)
    cv2.waitKey(1)
