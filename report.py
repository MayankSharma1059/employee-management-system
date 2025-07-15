from tkinter import*
from PIL import Image, ImageTk
from tkinter import ttk,messagebox
import sqlite3

class reportClass:
    def __init__(self,root):
        self.root=root
        self.root.title("Student Result Management System")
        self.root.geometry("1400x700+50+50")
        self.root.config(bg="white")
        self.root.focus_force()
        
        # Make window stay on top and modal
        self.root.transient(root.master)
        self.root.grab_set()
        
        # Initialize database
        self.create_db()
        
        #===title===
        title=Label(self.root,text="Add Student Results",font=("goudy old style",25,"bold"),bg="#033054",fg="white").place(x=10,y=20,relwidth=1,height=50)

class ReportClass:
    def __init__(self, root):
        self.root = root
        self.root.title("View Student Results")
        self.root.geometry("900x500+200+100")
        self.root.config(bg="white")

        # Header
        header = Frame(self.root, bg="#ff9800")
        header.place(x=0, y=0, relwidth=1, height=60)
        title = Label(header, text="View Student Results", font=("goudy old style", 22, "bold"), bg="#ff9800", fg="white")
        title.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Search Bar
        search_frame = Frame(self.root, bg="white")
        search_frame.place(x=10, y=70, width=870, height=40)
        lbl_search = Label(search_frame, text="Search By | Roll No.", font=("goudy old style", 15), bg="white")
        lbl_search.place(x=0, y=5)
        self.var_search = StringVar()
        txt_search = Entry(search_frame, textvariable=self.var_search, font=("goudy old style", 15), bg="lightyellow")
        txt_search.place(x=180, y=5, width=180)
        btn_search = Button(search_frame, text="Search", font=("goudy old style", 13), bg="#2196f3", fg="white", command=self.search)
        btn_search.place(x=370, y=3, width=100, height=30)
        btn_clear = Button(search_frame, text="Clear", font=("goudy old style", 13), bg="#607d8b", fg="white", command=self.clear)
        btn_clear.place(x=480, y=3, width=100, height=30)

        # Table
        table_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        table_frame.place(x=10, y=120, width=870, height=300)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("goudy old style", 13, "bold"), foreground="#033054")
        style.configure("Treeview", font=("goudy old style", 12), rowheight=28)
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])
        self.result_table = ttk.Treeview(
            table_frame,
            columns=("roll", "name", "course", "marks", "full_marks", "percentage"),
            show="headings"
        )
        self.result_table.heading("roll", text="Roll No")
        self.result_table.heading("name", text="Name")
        self.result_table.heading("course", text="Course")
        self.result_table.heading("marks", text="Marks Obtained")
        self.result_table.heading("full_marks", text="Total Marks")
        self.result_table.heading("percentage", text="Percentage")
        self.result_table.column("roll", width=100, anchor=CENTER)
        self.result_table.column("name", width=150, anchor=CENTER)
        self.result_table.column("course", width=120, anchor=CENTER)
        self.result_table.column("marks", width=120, anchor=CENTER)
        self.result_table.column("full_marks", width=120, anchor=CENTER)
        self.result_table.column("percentage", width=120, anchor=CENTER)
        self.result_table.pack(fill=BOTH, expand=1)

        # Add scrollbars
        scroll_x = Scrollbar(table_frame, orient=HORIZONTAL, command=self.result_table.xview)
        scroll_y = Scrollbar(table_frame, orient=VERTICAL, command=self.result_table.yview)
        self.result_table.configure(xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        # Delete Button
        btn_delete = Button(self.root, text="Delete", font=("goudy old style", 15, "bold"), bg="#f44336", fg="white", command=self.delete)
        btn_delete.place(x=400, y=430, width=120, height=40)

        self.fetch_data()

    def fetch_data(self):
        con = sqlite3.connect("rms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT roll, name, course, marks, full_marks, per FROM result")
            rows = cur.fetchall()
            self.result_table.delete(*self.result_table.get_children())
            for row in rows:
                self.result_table.insert("", END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")
        finally:
            con.close()

    def search(self):
        roll = self.var_search.get().strip()
        if roll == "":
            messagebox.showerror("Error", "Please enter a roll number to search.")
            return
        con = sqlite3.connect("rms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT roll, name, course, marks, full_marks, per FROM result WHERE roll=?", (roll,))
            rows = cur.fetchall()
            self.result_table.delete(*self.result_table.get_children())
            for row in rows:
                self.result_table.insert("", END, values=row)
            if not rows:
                messagebox.showinfo("Not found", "No result found for this roll number.")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")
        finally:
            con.close()

    def clear(self):
        self.var_search.set("")
        self.fetch_data()

    def delete(self):
        selected = self.result_table.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a result to delete.")
            return
        values = self.result_table.item(selected, "values")
        roll = values[0]
        op = messagebox.askyesno("Confirm", f"Do you really want to delete result for Roll No: {roll}?")
        if op:
            con = sqlite3.connect("rms.db")
            cur = con.cursor()
            try:
                cur.execute("DELETE FROM result WHERE roll=?", (roll,))
                con.commit()
                messagebox.showinfo("Deleted", "Result deleted successfully.")
                self.fetch_data()
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to {str(ex)}")
            finally:
                con.close()

# Entry point for standalone run
def main():
    root = Tk()
    app = ReportClass(root)
    root.mainloop()

if __name__ == "__main__":
    main()