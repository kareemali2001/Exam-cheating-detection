import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import messagebox as mBox
from tkinter import messagebox

import sqlite3
from subprocess import call
import os

class LoginApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LOGIN SYSTEM")
        self.resizable(0, 0)
        self.configure(bg="gray")
       
        SLeft = (self.winfo_screenwidth() - 380) / 2
        STop = (self.winfo_screenheight() - 310) / 2
        self.geometry("%dx%d+%d+%d" % (380, 310, SLeft, STop))

       
        self.admuname = tk.StringVar()
        self.admupass = tk.StringVar()
        self.admurole = tk.StringVar()

       
        self.MFrame = LabelFrame(self, width=320, height=290, font=('arial', 15, 'bold'), bg='lightblue', bd=15,
                                 relief='ridge')
        self.MFrame.grid(row=0, column=0, padx=20, pady=10)
        self.EFrame = LabelFrame(self, width=200, height=100, font=('arial', 10, 'bold'), bg='lightblue',
                                 relief='ridge', bd=13)
        self.EFrame.grid(row=2, column=0, pady=10)

        self.Lsyslogin = Label(self.MFrame, text='SYSTEM LOGIN:', font=('arial', 10, 'bold'), bg='lightblue')
        self.Lsyslogin.grid(row=1, column=0, sticky=W, padx=20)
        self.LUsername = Label(self.MFrame, text='Username:', font=('arial', 10, 'bold'), bg='lightblue')
        self.LUsername.grid(row=2, column=0, sticky=W, padx=20)
        self.Lupass = Label(self.MFrame, text='Password:', font=('arial', 10, 'bold'), bg='lightblue')
        self.Lupass.grid(row=3, column=0, sticky=W, padx=20)
        self.Lurole = Label(self.MFrame, text='Role:', font=('arial', 10, 'bold'), bg='lightblue')
        self.Lurole.grid(row=4, column=0, sticky=W, padx=20)


        self.TxtUsername = Entry(self.MFrame, font=('arial', 10, 'bold'), textvariable=self.admuname)
        self.TxtUsername.grid(row=2, column=1, padx=10, pady=5)
        self.Txtupass = Entry(self.MFrame, font=('arial', 10, 'bold'), show="*", textvariable=self.admupass)
        self.Txtupass.grid(row=3, column=1, padx=10, pady=5)
        self.Cmburole = ttk.Combobox(self.MFrame, font=('arial', 10, 'bold'), textvariable=self.admurole)
        self.Cmburole['values'] = ('teacher', 'student', 'admin')
        self.Cmburole.grid(row=4, column=1, padx=10, pady=5)

        self.btnlogin = Button(self.EFrame, text='LOGIN', font=('arial', 10, 'bold'), width=9, command=self.adlogn)
        self.btnlogin.grid(row=0, column=0, padx=10, pady=10)
        self.btnExit = Button(self.EFrame, text='EXIT', font=('arial', 10, 'bold'), width=9, command=self.exitt)
        self.btnExit.grid(row=0, column=1, padx=10, pady=10)

        self.btnReg = Button(self.EFrame, text='REGISTER', font=('arial', 10, 'bold'), width=9, command=self.clickreg)
        self.btnReg.grid(row=1, column=1, padx=10, pady=10)

    def exitt(self):
        result = mBox.askquestion('Exit', 'Are you sure you want to exit?', icon="warning")
        if result == 'yes':
            self.destroy()

    def clickreg(self):
        self.withdraw()  
        call(["python", "Register.py"])

    def adlogn(self):
        student_name = self.admuname.get()
        password = self.admupass.get()
        role = self.admurole.get()
        if student_name == "" or password == "" or role == "":
            mBox.showerror('Error', 'Enter username & password')
        else:
            try:
                conn = sqlite3.connect("students.db")
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM students WHERE student_name=? AND password=? AND role=?",
                               (student_name, password, role))
                result = cursor.fetchone()
                if result:
                    mBox.showinfo('Information', "Login Successfully")
                    self.destroy()
                  



                    if role == 'admin':
                        root = tk.Tk()
                        root.withdraw()    

                        choice = messagebox.askquestion("Admin Menu", "Which page would you like to open?\n\nClick 'Yes' for admin_control\n\nClick 'No' for questoin_control")
                        if choice == 'yes':
                            os.system('python admin_control.py')
                        elif choice == 'no':
                            os.system('python quizdatabase.py')

                    elif role == 'student':
                        os.system('python student_main.py')
                    elif role == 'teacher':  
                        os.system('python quizdatabase.py')
                else:
                    mBox.showinfo('Information', "Login failed, Invalid Username or Password. Try again!!!")
                cursor.close()
                conn.close()
            except Exception as es:
                print('Error', f"Due to: {str(es)}")


LoginApp().mainloop()
