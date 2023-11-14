import sqlite3
import tkinter as tk
from tkinter import messagebox

# Connect to the database
conn = sqlite3.connect('quiz1.db')
cursor = conn.cursor()

# Function to add a new question and answers to the database
def add_question():
    question = entry_question.get()
    answer1 = entry_answer1.get()
    answer2 = entry_answer2.get()
    answer3 = entry_answer3.get()
    answer4 = entry_answer4.get()
    correct_answer = int(entry_correct_answer.get())

    try:
        cursor.execute('INSERT INTO quiz (question, answer1, answer2, answer3, answer4, correct_answer) VALUES (?, ?, ?, ?, ?, ?)',
                       (question, answer1, answer2, answer3, answer4, correct_answer))
        conn.commit()
        messagebox.showinfo("Success", "Question added successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to delete a question from the database
def delete_question():
    question_id = entry_question_id.get()

    try:
        cursor.execute('DELETE FROM quiz WHERE id=?', (question_id,))
        conn.commit()
        messagebox.showinfo("Success", "Question deleted successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to update a question in the database
def update_question():
    question_id = entry_question_id.get()
    question = entry_question.get()
    answer1 = entry_answer1.get()
    answer2 = entry_answer2.get()
    answer3 = entry_answer3.get()
    answer4 = entry_answer4.get()
    correct_answer = int(entry_correct_answer.get())

    try:
        cursor.execute('UPDATE quiz SET question=?, answer1=?, answer2=?, answer3=?, answer4=?, correct_answer=? WHERE id=?',
                       (question, answer1, answer2, answer3, answer4, correct_answer, question_id))
        conn.commit()
        messagebox.showinfo("Success", "Question updated successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to display questions and answers from the database
def display_questions():
    try:
        cursor.execute('SELECT * FROM quiz')
        questions = cursor.fetchall()
        for question in questions:
            print(f"ID: {question[0]}")
            print(f"Question: {question[1]}")
            print(f"Answer 1: {question[2]}")
            print(f"Answer 2: {question[3]}")
            print(f"Answer 3: {question[4]}")
            print(f"Answer 4: {question[5]}")
            print(f"Correct Answer: {question[6]}")
            print("------------------------")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create the main window
window = tk.Tk()
window.title("Quiz Database Interface")

# Create labels and entry fields for adding a new question
label_question = tk.Label(window, text="Question:")
label_question.grid(row=0, column=0, padx=5, pady=5)
entry_question = tk.Entry(window)
entry_question.grid(row=0, column=1, padx=5, pady=5)

label_answer1 = tk.Label(window, text="Answer 1:")
label_answer1.grid(row=1, column=0, padx=5, pady=5)
entry_answer1 = tk.Entry(window)
entry_answer1.grid(row=1, column=1, padx=5, pady=5)

label_answer2 = tk.Label(window, text="Answer 2:")
label_answer2.grid(row=2, column=0, padx=5, pady=5)
entry_answer2 = tk.Entry(window)
entry_answer2.grid(row=2, column=1, padx=5, pady=5)

label_answer3 = tk.Label(window, text="Answer 3:")
label_answer3.grid(row=3, column=0, padx=5, pady=5)
entry_answer3 = tk.Entry(window)
entry_answer3.grid(row=3, column=1, padx=5, pady=5)

label_answer4 = tk.Label(window, text="Answer 4:")
label_answer4.grid(row=4, column=0, padx=5, pady=5)
entry_answer4 = tk.Entry(window)
entry_answer4.grid(row=4, column=1, padx=5, pady=5)

label_correct_answer = tk.Label(window, text="Correct Answer (Enter the index):")
label_correct_answer.grid(row=5, column=0, padx=5, pady=5)
entry_correct_answer = tk.Entry(window)
entry_correct_answer.grid(row=5, column=1, padx=5, pady=5)

button_add_question = tk.Button(window, text="Add Question", command=add_question)
button_add_question.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

# Create labels and entry fields for deleting and updating a question
label_question_id = tk.Label(window, text="Question ID:")
label_question_id.grid(row=7, column=0, padx=5, pady=5)
entry_question_id = tk.Entry(window)
entry_question_id.grid(row=7, column=1, padx=5, pady=5)

button_delete_question = tk.Button(window, text="Delete Question", command=delete_question)
button_delete_question.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

button_update_question = tk.Button(window, text="Update Question", command=update_question)
button_update_question.grid(row=9, column=0, columnspan=2, padx=5, pady=5)

# Create a button to display questions and answers
button_display_questions = tk.Button(window, text="Display Questions", command=display_questions)
button_display_questions.grid(row=10, column=0, columnspan=2, padx=5, pady=5)

# Start the GUI main loop
window.mainloop()

# Close the connection to the database
conn.close()
