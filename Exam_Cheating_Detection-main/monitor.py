import mediapipe as mp
import cv2
import gaze
import time
from imutils import face_utils
import dlib
import math
import datetime
import sqlite3
import easygui

mp_face_mesh = mp.solutions.face_mesh  
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

cap = cv2.VideoCapture(0) 
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_filename = 'video.avi'
output_path = 'C:/Users/HP_OS 11/hci project/videos/'
output_file = output_path + output_filename
out = cv2.VideoWriter(output_file, fourcc, 20.0, (640, 480)) 
UPPER_LIP_INNER_START = 51
UPPER_LIP_INNER_END = 52
LOWER_LIP_INNER_START = 60
LOWER_LIP_INNER_END = 62
LIP_MOVEMENT_THRESHOLD = 7


left_warning_displayed = False
right_warning_displayed = False
center_warning_displayed = False

warning_display_time = 3  
last_warning_time = time.time()  
conn = sqlite3.connect('students.db')
cursor = conn.cursor()

def update_warning_numbers(student_id):
    cursor.execute("UPDATE students SET warnings_number = warnings_number + 1 WHERE id = ?", (student_id,))
    conn.commit()

enteredid= easygui.integerbox("Enter ID number:")

with mp_face_mesh.FaceMesh(
        max_num_faces=1,  
        refine_landmarks=True,  
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as face_mesh:

    while cap.isOpened():
        success, image = cap.read()
        if not success: 
            print("Ignoring empty camera frame.")
            continue
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        rects = detector(gray, 0)
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  
        results = face_mesh.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  
        for (i, rect) in enumerate(rects):
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)
            if results.multi_face_landmarks:
                gaze.gaze(image, results.multi_face_landmarks[0])  # gaze estimation
                upper_lip_inner_distance = math.sqrt((shape[UPPER_LIP_INNER_END][0] - shape[UPPER_LIP_INNER_START][0]) ** 2 + (shape[UPPER_LIP_INNER_END][1] - shape[UPPER_LIP_INNER_START][1]) ** 2)
                lower_lip_inner_distance = math.sqrt((shape[LOWER_LIP_INNER_END][0] - shape[LOWER_LIP_INNER_START][0]) ** 2 + (shape[LOWER_LIP_INNER_END][1] - shape[LOWER_LIP_INNER_START][1]) ** 2)

                for (x, y) in shape:
                    cv2.circle(image, (x, y), 2, (0, 255, 0), -1)

                if upper_lip_inner_distance > LIP_MOVEMENT_THRESHOLD and lower_lip_inner_distance > LIP_MOVEMENT_THRESHOLD:
                    cv2.putText(image, "WARNING: STOP TALKING OR YOU WILL BE CONSIDERED CHEATING", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                # Get the gaze direction from the gaze module
                gaze_direction = gaze.prev_gaze

                # Get the center of the frame
                frame_center = (image.shape[1] // 2, image.shape[0] // 2)

                # Check if the gaze line goes to the left side of the frame
                if gaze_direction[0] < frame_center[0]:
                    left_warning_displayed = True
                    right_warning_displayed = False
                    center_warning_displayed = False
                else:
                    left_warning_displayed = False

                # Check if the gaze line goes to the right side of the frame
                if gaze_direction[0] > frame_center[0]:
                    left_warning_displayed = False
                    right_warning_displayed = True
                    center_warning_displayed = False
                else:
                    right_warning_displayed = False

                # Check if the gaze line goes towards the center of the frame
                if frame_center[0] - 50 < gaze_direction[0] < frame_center[0] + 50 and \
                        frame_center[1] - 50 < gaze_direction[1] < frame_center[1] + 50:
                    left_warning_displayed = False
                    right_warning_displayed = False
                    center_warning_displayed = True

                # Display warning messages based on conditions
                if center_warning_displayed:
                    cv2.putText(image, 'Looking at Center', (10, 60), cv2.FONT_HERSHEY_SIMPLEX,
                                0.7, (0, 255, 0), 2)
                elif left_warning_displayed and time.time() - last_warning_time >= warning_display_time:
                    cv2.putText(image, 'WARNING: Gaze to the Left!', (10, 60), cv2.FONT_HERSHEY_SIMPLEX,
                                0.7, (0, 0, 255), 2)
                    last_warning_time = time.time()
                    update_warning_numbers(enteredid) 

                elif right_warning_displayed and time.time() - last_warning_time >= warning_display_time:
                    cv2.putText(image, 'WARNING: Gaze to the Right!', (10, 60), cv2.FONT_HERSHEY_SIMPLEX,
                                 0.7, (0, 0, 255), 2)
                    last_warning_time = time.time()
                    update_warning_numbers(enteredid) 

        cv2.imshow('output window', image)
        out.write(image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release() 
cv2.destroyAllWindows()
