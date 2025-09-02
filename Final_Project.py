import cv2
import mediapipe as mp
import serial
import math

webcam = cv2.VideoCapture(0)
mp_face = mp.solutions.face_mesh
mp_drawing= mp.solutions.drawing_utils
ardiuno = serial.Serial('com3',9600)
with mp_face.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.52) as face_mesh:
    while True:
        control, frame= webcam.read()
        if control== False:
            break
        rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        result = face_mesh.process(rgb)
        height,width,channels = frame.shape
        if result.multi_face_landmarks:
            for face_landmarks in result.multi_face_landmarks:
                point1= face_landmarks.landmark[306]
                x1= int(point1.x * width)
                y1 = int(point1.y * height)
                cv2.circle(frame, (x1,y1), 2, (0,0,255), 3)
                point2 = face_landmarks.landmark[61]
                x2 = int(point2.x * width)
                y2 = int(point2.y * height)
                cv2.circle(frame, (x2, y2), 2, (0, 0, 255), 3)
                distance = math.sqrt(math.pow(x2-x1,2)+math.pow(y2-y1,2))
                print(distance)
                if distance > 45:
                    ardiuno.write(b'A')
                if distance<42 :
                    ardiuno.write(b'B')
                if distance > 42 and distance <45:
                    ardiuno.write(b'N')

        cv2.imshow("final", frame)
        if cv2.waitKey(10) == 27:
            break

