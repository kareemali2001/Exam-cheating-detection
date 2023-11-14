import tkinter as tk
from tkinter import messagebox as mBox
from tkinter import ttk
from tkinter import filedialog
import sqlite3

class RegApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SIGN UP")
        self.resizable(0, 0)
        self.configure(bg="gray")
        self.geometry("347x360+10+60")

        admuname = tk.StringVar()
        admupass = tk.StringVar()
        admurole = tk.StringVar()
        self.picture_path = None

        self.MFrame = tk.LabelFrame(self, width=320, height=320, font=('arial', 15, 'bold'), bg='lightblue', bd=15,
                                    relief='ridge')
        self.MFrame.grid(row=0, column=0, padx=20, pady=10)
        self.EFrame = tk.LabelFrame(self, width=200, height=100, font=('arial', 10, 'bold'), bg='lightblue',
                                    relief='ridge', bd=13)
        self.EFrame.grid(row=3, column=0, pady=10)

        self.Lsyslogin = tk.Label(self.MFrame, text='SIGN UP:', font=('arial', 10, 'bold'), bg='lightblue')
        self.Lsyslogin.grid(row=1, column=0, sticky=tk.W, padx=20)
        self.LUsername = tk.Label(self.MFrame, text='Username:', font=('arial', 10, 'bold'), bg='lightblue')
        self.LUsername.grid(row=2, column=0, sticky=tk.W, padx=20)
        self.Lupass = tk.Label(self.MFrame, text='Password:', font=('arial', 10, 'bold'), bg='lightblue')
        self.Lupass.grid(row=3, column=0, sticky=tk.W, padx=20)
        self.Lurole = tk.Label(self.MFrame, text='Role:', font=('arial', 10, 'bold'), bg='lightblue')
        self.Lurole.grid(row=4, column=0, sticky=tk.W, padx=20)
        self.picture_label = tk.Label(self.MFrame, text='Picture:', font=('arial', 10, 'bold'), bg='lightblue')
        self.picture_label.grid(row=5, column=0, sticky=tk.W, padx=20)

        self.TxtUsername = tk.Entry(self.MFrame, font=('arial', 10, 'bold'), textvariable=admuname)
        self.TxtUsername.grid(row=2, column=1, padx=10, pady=5)
        self.Txtupass = tk.Entry(self.MFrame, font=('arial', 10, 'bold'), show="*", textvariable=admupass)
        self.Txtupass.grid(row=3, column=1, padx=10, pady=5)
        self.Cmburole = ttk.Combobox(self.MFrame, values=["student", "teacher", "admin"], textvariable=admurole)
        self.Cmburole.grid(row=4, column=1, padx=10, pady=5)
        self.picture_button = tk.Button(self.MFrame, text='Select', font=('arial', 10, 'bold'), command=self.select_picture)
        self.picture_button.grid(row=5, column=1, padx=10, pady=5)

        self.btnlogin = tk.Button(self.EFrame, text='SIGN UP', font=('arial', 10, 'bold'), width=9, command=self.savst)
        self.btnlogin.grid(row=0, column=0, padx=10, pady=5)
        self.btnreset = tk.Button(self.EFrame, text='RESET', font=('arial', 10, 'bold'), width=9, command=self.reset)
        self.btnreset.grid(row=0, column=1, padx=10, pady=5)
        self.btnexit = tk.Button(self.EFrame, text='EXIT', font=('arial', 10, 'bold'), width=9, command=self.exit)
        self.btnexit.grid(row=0, column=2, padx=10, pady=5)

    def select_picture(self):
        picture_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.bmp")])
        if picture_path:
            self.picture_path = picture_path
            self.picture_label.config(text="Picture:Selected" )

    def savst(self):
        student_name = self.TxtUsername.get()
        password = self.Txtupass.get()
        role = self.Cmburole.get()

        if student_name == "" or password == "" or role == "":
            mBox.showerror('Error', 'No blanks allowed')
        else:
            try:
                conn = sqlite3.connect("students.db")
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM students WHERE student_name=?", (student_name,))
                result = cursor.fetchone()
                if result:
                    mBox.showinfo('Information', "Username already used")
                else:
                    # Read picture data from the selected file
                    picture_data = None
                    if self.picture_path:
                        with open(self.picture_path, 'rb') as file:
                            picture_data = file.read()

                    cursor.execute(
                        "INSERT INTO students (student_name, password, role, picture, warnings_number, attendance_number) VALUES (?, ?, ?, ?, 0, 0)",
                        (student_name, password, role, picture_data)
                    )
                    conn.commit()
                    if cursor.rowcount > 0:
                        mBox.showinfo("Done", "Successfully Registered, Login")
                        self.destroy()
                    else:
                        mBox.showerror("Error", "Unable to Register")
                    cursor.close()
                    conn.close()
            except Exception as es:
                print('Error', f"due to: {str(es)}")

    def reset(self):
        self.TxtUsername.delete(0, 'end')
        self.Txtupass.delete(0, 'end')
        self.Cmburole.set('')
        self.picture_path = None
        self.picture_label.config(text='Picture:')

    def exit(self):
        result = mBox.askquestion('Exit Application', 'Are you sure you want to exit the application?', icon='warning')
        if result == 'yes':
            self.destroy()

if __name__ == '__main__':
    regapp = RegApp()
    regapp.mainloop()
