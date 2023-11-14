import sys
import os
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit, QLabel, QPushButton, QListWidget, QFileDialog, QListWidgetItem, QCheckBox
from PyQt5.QtGui import QPixmap, QIcon


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Student Database')
        self.setGeometry(100, 100, 400, 300)

        self.student_name_box = QLineEdit(self)
        self.student_name_box.setGeometry(20, 20, 200, 30)
        self.student_name_label = QLabel('Student Name:', self)
        self.student_name_label.setGeometry(20, 60, 200, 30)

        self.course_name_box = QLineEdit(self)
        self.course_name_box.setGeometry(20, 100, 200, 30)
        self.course_name_label = QLabel('Password:', self)
        self.course_name_label.setGeometry(20, 140, 200, 30)

        self.role_label = QLabel('Role:', self)
        self.role_label.setGeometry(20, 180, 200, 30)
        self.role_checkbox_teacher = QCheckBox('teacher', self)
        self.role_checkbox_teacher.setGeometry(20, 220, 100, 30)
        self.role_checkbox_student = QCheckBox('student', self)
        self.role_checkbox_student.setGeometry(130, 220, 100, 30)
        self.role_checkbox_admin = QCheckBox('admin', self)
        self.role_checkbox_admin.setGeometry(240, 220, 100, 30)

        self.picture_label = QLabel('Picture:', self)
        self.picture_label.setGeometry(20, 260, 200, 30)
        self.picture_box = QLineEdit(self)
        self.picture_box.setGeometry(80, 260, 140, 30)
        self.picture_button = QPushButton('Select', self)
        self.picture_button.setGeometry(230, 260, 90, 30)
        self.picture_button.clicked.connect(self.select_picture)

        self.list_widget = QListWidget(self)
        self.list_widget.setGeometry(20, 300, 320, 120)
        self.list_widget.itemSelectionChanged.connect(self.enable_delete_button)
        self.create_button = QPushButton('Create', self)
        self.create_button.setGeometry(20, 440, 100, 30)
        self.create_button.clicked.connect(self.create_student)

        self.update_button = QPushButton('Update', self)
        self.update_button.setGeometry(130, 440, 100, 30)
        self.update_button.clicked.connect(self.update_student)

        self.delete_button = QPushButton('Delete', self)
        self.delete_button.setGeometry(240, 440, 100, 30)
        self.delete_button.clicked.connect(self.delete_student)

        self.redirect_button = QPushButton('quiz database', self)
        self.redirect_button.setGeometry(130, 480, 150, 30)
        self.redirect_button.clicked.connect(self.redirect_to_quiadatabase)


        self.redirect_button = QPushButton('video_analyzer', self)
        self.redirect_button.setGeometry(130, 520, 200, 30)
        self.redirect_button.clicked.connect(self.redirect_to_video)

        self.load_students()

        self.show()

    def select_picture(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Select Picture', '', 'Image Files (*.png *.jpg *.bmp)')
        if file_path:
            self.picture_box.setText(file_path)

    def create_student(self):
        student_name = self.student_name_box.text().strip()
        password = self.course_name_box.text().strip()
        role = ''
        if self.role_checkbox_teacher.isChecked():
            role = 'teacher'
        elif self.role_checkbox_student.isChecked():
            role = 'student'
        elif self.role_checkbox_admin.isChecked():
            role = 'admin'
        picture_path = self.picture_box.text().strip()
        if not picture_path:
            picture_data = None
        else:
            with open(picture_path, 'rb') as f:
                picture_data = f.read()

        if not student_name or not password or not role:
            QMessageBox.warning(
                self, 'Error', 'Please enter all data.')
            return

        connection = sqlite3.connect('students.db')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO students (student_name, password, role, picture, warnings_number, attendance_number, student_score) VALUES (?, ?, ?, ?, 0, 0, 0)',
                       (student_name, password, role, picture_data))
        connection.commit()
        connection.close()

        self.student_name_box.clear()
        self.course_name_box.clear()
        self.role_checkbox_teacher.setChecked(False)
        self.role_checkbox_student.setChecked(False)
        self.role_checkbox_admin.setChecked(False)

        self.load_students()

    def update_student(self):
        selected_item = self.list_widget.currentItem()
        if not selected_item:
            QMessageBox.warning(
                self, 'Error', 'Please select a student record to update.')
            return

        student_id = int(selected_item.text().split(':')[0])
        student_name = self.student_name_box.text().strip()
        password = self.course_name_box.text().strip()
        role = ''
        if self.role_checkbox_teacher.isChecked():
            role = 'teacher'
        elif self.role_checkbox_student.isChecked():
            role = 'student'
        elif self.role_checkbox_admin.isChecked():
            role = 'admin'

        if not student_name or not password or not role:
            QMessageBox.warning(
                self, 'Error', 'Please enter a student name, password, and select a role.')
            return

        connection = sqlite3.connect('students.db')
        cursor = connection.cursor()
        cursor.execute('UPDATE students SET student_name=?, password=?, role=? WHERE id=?',
                       (student_name, password, role, student_id))
        connection.commit()
        connection.close()

        self.student_name_box.clear()
        self.course_name_box.clear()
        self.role_checkbox_teacher.setChecked(False)
        self.role_checkbox_student.setChecked(False)
        self.role_checkbox_admin.setChecked(False)

        self.load_students()

    def enable_delete_button(self):
        if len(self.list_widget.selectedItems()) > 0:
            self.delete_button.setEnabled(True)
        else:
            self.delete_button.setEnabled(False)

    def delete_student(self):
        selected_item = self.list_widget.currentItem()
        if not selected_item:
            QMessageBox.warning(
                self, 'Error', 'Please select a student to delete.')
            return
        selected_text = selected_item.text()
        student_id = selected_text.split(':')[0]

        confirm = QMessageBox.question(self, 'Confirm', f"Are you sure you want to delete the student record for ID {student_id}?",
                                       QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            connection = sqlite3.connect('students.db')
            cursor = connection.cursor()
            cursor.execute('DELETE FROM students WHERE id=?', (student_id,))
            connection.commit()
            connection.close()

            self.load_students()

    def load_students(self):
        self.list_widget.clear()

        connection = sqlite3.connect('students.db')
        cursor = connection.cursor()
        cursor.execute('SELECT id, student_name, password, role, picture, warnings_number, attendance_number, student_score FROM students')
        students = cursor.fetchall()

        for student in students:
            student_id, student_name, password, role, picture_data, warnings_number, attendance_number, student_score = student
            item_text = f'{student_id}: {student_name} (password: {password}) (Role: {role}) (Warnings:{warnings_number}) (attendance: {attendance_number}) (score: {student_score})'
            item = QListWidgetItem(item_text, self.list_widget)

            if picture_data:
                pixmap = QPixmap()
                pixmap.loadFromData(picture_data)
                item.setIcon(QIcon(pixmap))

        connection.close()

 
    def redirect_to_quiadatabase(self):
        os.system('python quizdatabase.py')  # Change the command based on your Python execution method
        self.hide()


    def redirect_to_video(self):
        os.system('python videogui.py')  # Change the command based on your Python execution method
        self.hide()

if __name__ == '__main__':
    connection = sqlite3.connect('students.db')
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY, student_name TEXT NOT NULL, password TEXT NOT NULL, role TEXT NOT NULL, picture BLOB, warnings_number INTEGER, attendance_number INTEGER, student_score INTEGER)')
    connection.commit()
    connection.close()

    app = QApplication(sys.argv)

    window = MainWindow()

    sys.exit(app.exec_())
