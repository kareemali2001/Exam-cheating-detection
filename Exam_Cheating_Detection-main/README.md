Exam Cheating Detection System


Description

The Exam Cheating Detection System is a Python-based application designed to enhance the integrity of online exams. It employs face recognition technology to verify the identity of students and monitors their behavior during the exam to detect potential cheating attempts.


Features

Login: Students are required to log in to the system using their credentials.

Face Recognition: The system uses face recognition to match the student's face with their database picture for identity verification.

Exam Start: Once the student's identity is confirmed, the exam begins.

Gaze Detection: The system monitors the student's gaze and alerts if they look away for an extended period (e.g., 3 seconds or more).

Warning System: If a student receives three warnings for suspicious behavior (e.g., looking away excessively), the exam is terminated.

Emotion Analysis: The system analyzes the student's facial expressions to determine emotions (happy, sad, afraid) during the exam.

Configuration

Configure system settings in config.py.
Update the student database in student_database.csv.
Contributing
Contributions are welcome! If you find any issues or want to add new features, please open an issue or submit a pull request.

Credits

[ZiadElbadawi]

License

This project is licensed under the MIT License.
