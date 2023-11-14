import numpy as np
import cv2
from deepface import DeepFace
from collections import deque
from datetime import datetime
import time
import sqlite3 
import easygui

# Define blue color range
Lower_blue = np.array([90, 100, 100])
Upper_blue = np.array([130, 255, 255])

# Initialize webcam
cap = cv2.VideoCapture(0)

# Track pointer position
pointer_center = None

# Initialize deque for pointer trail
pts = deque(maxlen=64)

# Connect to the database
conn = sqlite3.connect('quiz1.db')
cursor = conn.cursor()

conn2 = sqlite3.connect('students.db')
cursor2 = conn2.cursor()


# Create the "quiz" table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS quiz (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question TEXT,
                    answer1 TEXT,
                    answer2 TEXT,
                    answer3 TEXT,
                    answer4 TEXT,
                    correct_answer INTEGER,
                    selected_answer INTEGER
                )''')

# Add sample questions and answers to the database

# Fetch quiz questions and answers from the database
cursor.execute('SELECT question, answer1, answer2, answer3, answer4, correct_answer FROM quiz')
quiz_questions = cursor.fetchall()

# Quiz control variables
current_question = 0
show_result = False
start_time = time.time()  
finished_quiz = False


expression_timer = time.time()
img = 0


def on_mouse_click(event, x, y, flags, param):
    global current_question, show_result, start_time, finished_quiz

    if event == cv2.EVENT_LBUTTONDOWN:
        # Check if retry button is clicked
        if img.shape[1] - 100 <= x <= img.shape[1] and img.shape[0] - 50 <= y <= img.shape[0]:
            if finished_quiz:
                # Reset quiz variables
                current_question = 0
                show_result = False
                start_time = time.time()  # Reset start_time
                finished_quiz = False
                cursor.execute('UPDATE quiz SET selected_answer=NULL')
                conn.commit()

cv2.namedWindow('Facial Recognition')
cv2.setMouseCallback('Facial Recognition', on_mouse_click)

def start_quiz():
    global current_question, show_result, start_time, finished_quiz, expression_timer

    # Ask the user for ID number using a message box
    idelstudent = easygui.integerbox(msg='Enter your ID number:', title='ID Entry')

    


    while True:
        ret, img = cap.read()

       
        if time.time() - expression_timer >= 10.0:
            # Perform facial recognition on the captured frame
            result = DeepFace.analyze(img, actions=['emotion', 'gender'], enforce_detection=False)

            # Reset the timer
            expression_timer = time.time()

            # Check if a face is detected in the frame
            if len(result) > 0:
                # Get the dominant emotion and gender
                emotions = result[0]['emotion']
                dominant_emotion = max(emotions, key=emotions.get)
                gender = result[0]['gender']
                dominant_gender = max(gender, key=gender.get)

                # Store the facial expression information in a text file
                with open('facial_expression_log.txt', 'a') as log_file:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    log_file.write(f"{timestamp} - Emotion: {dominant_emotion}, Gender: {dominant_gender}\n")

                # Draw bounding box and display dominant emotion on the frame
                cv2.putText(
                    img,
                    dominant_emotion,
                    (img.shape[1] - 200, img.shape[0] - 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    2,
                    cv2.LINE_AA
                )
                cv2.putText(
                    img,
                    dominant_gender,
                    (img.shape[1] - 200, img.shape[0] - 20),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    2,
                    cv2.LINE_AA
                )

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.inRange(hsv, Lower_blue, Upper_blue)
        mask = cv2.erode(mask, kernel, iterations=2)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.dilate(mask, kernel, iterations=1)
        res = cv2.bitwise_and(img, img, mask=mask)
        cnts, heir = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2:]
        center = None

        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            if radius > 5:
                cv2.circle(img, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                cv2.circle(img, center, 5, (0, 0, 255), -1)

        # Update pointer position and append to deque
        pointer_center = center
        pts.appendleft(pointer_center)

        # Draw pointer trail
        for i in range(1, len(pts)):
            if pts[i - 1] is None or pts[i] is None:
                continue
            thickness = int(np.sqrt(len(pts) / float(i + 1)) * 2.5)
            cv2.line(img, pts[i - 1], pts[i], (0, 0, 225), thickness)

       
        if pointer_center is not None and current_question < len(quiz_questions) and not finished_quiz:
            selected_answer = None
            for i, _ in enumerate(quiz_questions[current_question][1:5]):
                x_pos = 50
                y_pos = 100 + (i * 30)
                width = 200
                height = 20
                if x_pos <= pointer_center[0] <= x_pos + width and y_pos <= pointer_center[1] <= y_pos + height:
                    selected_answer = i

            # Display question
            question = quiz_questions[current_question][0]
            cv2.putText(img, question, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

            # Process selected answer
            if selected_answer is not None:
                if start_time is None:
                    start_time = time.time()
                else:
                    elapsed_time = time.time() - start_time
                    if elapsed_time >= 2:
                        cursor.execute('UPDATE quiz SET selected_answer=? WHERE id=?', (selected_answer, current_question + 1))
                        conn.commit()
                        show_result = True
                        start_time = None

            if show_result:
                correct_answer = quiz_questions[current_question][5]
                result_text = "Correct!" if selected_answer == correct_answer else "Incorrect!"
                cv2.putText(img, result_text, (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                show_result = False
                current_question += 1

                if current_question >= len(quiz_questions):
                    finished_quiz = True

        # Draw answer options
        if current_question < len(quiz_questions) and not finished_quiz:
            for i, answer in enumerate(quiz_questions[current_question][1:5]):
                x_pos = 50
                y_pos = 100 + (i * 30)
                cv2.putText(img, answer, (x_pos, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        if finished_quiz:
            cv2.rectangle(img, (img.shape[1] - 100, img.shape[0] - 50), (img.shape[1], img.shape[0]), (0, 0, 255), -1)
            cv2.putText(img, "Retry", (img.shape[1] - 90, img.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            # Calculate and display the score
            cursor.execute('SELECT selected_answer, correct_answer FROM quiz')
            answers = cursor.fetchall()
            score = sum(answer[0] == answer[1] for answer in answers)
            cv2.putText(img, f"Score: {score}/{len(quiz_questions)}", (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            cursor2.execute('UPDATE students SET student_score = ? WHERE id = ?', (score, idelstudent))
            conn2.commit()
        cv2.imshow("Facial Recognition", img)

        if cv2.waitKey(30) & 0xFF == 32:
            break


    cap.release()
    cv2.destroyAllWindows()


def check_student_id(student_id):
    cursor2.execute('SELECT id FROM students WHERE id = ?', (student_id,))
    result = cursor2.fetchone()
    if result is None:
        return False
    return True


idelstudent = easygui.integerbox(msg='Enter your ID number:', title='ID Entry')

if check_student_id(idelstudent):
    start_quiz()
else:
    easygui.msgbox('Invalid ID number. Please try again.')


# Call the modified function to start the quiz
start_quiz()
