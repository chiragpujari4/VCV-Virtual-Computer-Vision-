#Jay Shree Ganeshaya Namah
#Jay Mata Di

import cv2
import mediapipe as mp
import pyautogui


cap=cv2.VideoCapture(0) #[To open the camera and capture the video with the fastest source.]
cap.set(3,1280)
cap.set(4,720)
hand_detector=mp.solutions.hands.Hands() #[Inbuilt function of mediapipe.]
drawing_utils=mp.solutions.drawing_utils #[importing drawing utilities to draw landmarks.]
screen_width, screen_height = pyautogui.size() #[To get the screen size.]
index_y=0
#thumb_y=0
while True:
    _,frame=cap.read() #[To read the video content and "_" to allocate video tab space.]
    frame=cv2.flip(frame, 1) #[To flip at y axis.]
    frame_height, frame_width, _ = frame.shape
    rgb_frame=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #[Convert BGR to RGB.]
    output= hand_detector.process(rgb_frame)
    hands=output.multi_hand_landmarks #[hands=landmarks.]
    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand) #[To draw landmarks.]
            landmarks=hand.landmark
            for id, landmark in enumerate(landmarks): #[For using the point numbers.]
                x=int(landmark.x*frame_width)
                y=int(landmark.y*frame_height)
                #print(x,y)
                if id==8: #[Index finger point id.]
                    cv2.circle(img=frame, center=(x,y), radius=10, color=(0,255,255)) #[To draw circle.]
                    index_x=(screen_width/frame_width)*x
                    index_y=(screen_height/frame_height)*y
                    
                    pyautogui.moveTo(index_x,index_y) #[To move the cursor.]
                if id==4: #[Thumb finger point id.]
                    cv2.circle(img=frame, center=(x,y), radius=10, color=(0,255,255)) #[To draw circle.]
                    thumb_x=(screen_width/frame_width)*x
                    thumb_y=(screen_height/frame_height)*y    
                    if abs((thumb_y-index_y)<30): #[To calculate absolute distance difference between thumb and index finger for the click event.]
                        pyautogui.click()
                        pyautogui.sleep(1)
                        #print(thumb_y-index_y)
    cv2.imshow('Virtual Mouse', frame) #[To show the frame.]
    cv2.waitKey(1)
    