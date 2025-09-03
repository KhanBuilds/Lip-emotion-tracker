#importing all the libraries
import cv2
import mediapipe as mp
import serial
import math

webcam = cv2.VideoCapture(0)  #webcam is an object of video capture
mp_face = mp.solutions.face_mesh  #loads facemesh from the mediapipe
mp_drawing= mp.solutions.drawing_utils  #loads facial landmarks drawing utilities
ardiuno = serial.Serial('com3',9600)  #this sets the communication with the arduino
with mp_face.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.52) as face_mesh:  #this creates a facemesh object and setting detection, tracking confidence
    while True:
        control, frame= webcam.read()  #control is boolean it checks if the frame has been captured
        if control== False:  #incase its not it breaks the loop
            break
        rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)  #cv2 returns image in  BGR this converts it to RGB because mediapipe accepts images in RGB
        result = face_mesh.process(rgb)  #loads that rgb image into facemesh and the result contains all the facial landmarks
        height,width,channels = frame.shape  # gets the dimensions of the frame/image
        if result.multi_face_landmarks:  #this checks if the mediapipe actually found a face the result.multietc contains the facial landmarks
            for face_landmarks in result.multi_face_landmarks: #this loops and creates a face_landmarks for the landmarks of every face detected
                point1= face_landmarks.landmark[306]  # this is some basic indexing for points on the face you will get this if you search up the media pipe face mesh
                x1= int(point1.x * width)
                y1 = int(point1.y * height)
                cv2.circle(frame, (x1,y1), 2, (0,0,255), 3)
                point2 = face_landmarks.landmark[61]
                x2 = int(point2.x * width)
                y2 = int(point2.y * height)
                cv2.circle(frame, (x2, y2), 2, (0, 0, 255), 3)
                distance = math.sqrt(math.pow(x2-x1,2)+math.pow(y2-y1,2))
                print(distance)
                #some conditioning that helps the arduino output different results based on what letter is sent
                if distance > 45:
                    ardiuno.write(b'A')
                if distance<42 :
                    ardiuno.write(b'B')
                if distance > 42 and distance <45:
                    ardiuno.write(b'N')

        cv2.imshow("final", frame) # this shows the video feed with the points on the desired indexes
        if cv2.waitKey(10) == 27:  # this breaks the loop and stops the program if you press escape '27' is ACII for escape key
            break

