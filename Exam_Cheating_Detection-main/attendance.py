import cv2
import sqlite3
import face_recognition
import numpy as np
from tkinter import messagebox
import time
import subprocess
import os
import sys
import easygui

# Connect to the database
connection = sqlite3.connect('students.db')
cursor = connection.cursor()

known_faces = []
known_names = []
known_ids = []

for row in cursor.execute('SELECT picture, student_name, id FROM students'):
    picture_data, student_name, student_id = row
    if picture_data is not None:
        picture_array = np.frombuffer(picture_data, dtype=np.uint8)
        picture = cv2.imdecode(picture_array, cv2.IMREAD_COLOR)
        face_locations = face_recognition.face_locations(picture)
        if len(face_locations) > 0:
            face_encodings = face_recognition.face_encodings(picture, face_locations)
            known_faces.append(face_encodings[0])
            known_names.append(student_name)
            known_ids.append(student_id)

video_capture = cv2.VideoCapture(0)

while True:
    _, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)
    message_box_shown = False

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_faces, face_encoding)
        name = "Unknown"
        if True in matches:
            idelstudent = easygui.integerbox("Please enter your ID number:")
            match_index = matches.index(True)
            name = known_names[match_index]
            student_id = known_ids[match_index]
            if student_id == idelstudent:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                cursor.execute("UPDATE students SET attendance_number = attendance_number + 1 WHERE id = ?", (student_id,))
                if not message_box_shown:
                    messagebox.showinfo("Attendance Recorded", "Your attendance is recorded successfully.")
                connection.commit()
                sys.exit(0)
            else:
                messagebox.showerror("Invalid ID", "The entered ID number is invalid.")
            

    cv2.imshow("Video", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
