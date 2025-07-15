from tkinter import *
from tkinter import messagebox
import sqlite3
import os

class LoginSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Login | Student Result Management System")
        self.root.geometry("400x350+500+200")
        self.root.config(bg="white")
        self.root.resizable(False, False)

        # Variables
        self.var_user = StringVar()
        self.var_pass = StringVar()
        self.var_show = IntVar()

        # Title
        title = Label(self.root, text="Login", font=("goudy old style", 22, "bold"), bg="#033054", fg="white").pack(fill=X)

        # Username
        lbl_user = Label(self.root, text="Username", font=("goudy old style", 15), bg="white").place(x=50, y=70)
        txt_user = Entry(self.root, textvariable=self.var_user, font=("goudy old style", 15), bg="lightyellow")
        txt_user.place(x=50, y=100, width=300)

        # Password
        lbl_pass = Label(self.root, text="Password", font=("goudy old style", 15), bg="white").place(x=50, y=140)
        self.txt_pass = Entry(self.root, textvariable=self.var_pass, font=("goudy old style", 15), bg="lightyellow", show="*")
        self.txt_pass.place(x=50, y=170, width=300)

        # Show/Hide Password
        chk_show = Checkbutton(self.root, text="Show Password", variable=self.var_show, onvalue=1, offvalue=0, bg="white", command=self.toggle_password)
        chk_show.place(x=50, y=200)

        # Buttons
        btn_login = Button(self.root, text="Login", font=("goudy old style", 15, "bold"), bg="#2196f3", fg="white", command=self.login)
        btn_login.place(x=50, y=250, width=120, height=40)
        btn_clear = Button(self.root, text="Clear", font=("goudy old style", 15, "bold"), bg="#607d8b", fg="white", command=self.clear)
        btn_clear.place(x=230, y=250, width=120, height=40)
        btn_exit = Button(self.root, text="Exit", font=("goudy old style", 12), bg="#f44336", fg="white", command=self.root.destroy)
        btn_exit.place(x=320, y=10, width=60, height=30)

        # Ensure users table exists and has at least one user
        self.create_users_table()

    def toggle_password(self):
        if self.var_show.get():
            self.txt_pass.config(show="")
        else:
            self.txt_pass.config(show="*")

    def clear(self):
        self.var_user.set("")
        self.var_pass.set("")
        self.var_show.set(0)
        self.txt_pass.config(show="*")

    def create_users_table(self):
        con = sqlite3.connect("rms.db")
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)")
        cur.execute("SELECT * FROM users")
        if not cur.fetchone():
            # Create default admin user
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "admin"))
            con.commit()
        con.close()

    def login(self):
        user = self.var_user.get().strip()
        pwd = self.var_pass.get().strip()
        if user == "" or pwd == "":
            messagebox.showerror("Error", "All fields are required.", parent=self.root)
            return
        con = sqlite3.connect("rms.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (user, pwd))
        row = cur.fetchone()
        con.close()
        if row:
            messagebox.showinfo("Success", f"Welcome, {user}!", parent=self.root)
            self.root.destroy()
            os.system("python dashboard.py")
        else:
            messagebox.showerror("Error", "Invalid username or password.", parent=self.root)

if __name__ == "__main__":
    root = Tk()
    app = LoginSystem(root)
    root.mainloop()
