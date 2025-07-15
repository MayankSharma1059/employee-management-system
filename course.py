from tkinter import*
from PIL import Image, ImageTk #pip install pillow
from tkinter import ttk,messagebox
import sqlite3

def create_db():
    con = sqlite3.connect(database="rms.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS course(cid INTEGER PRIMARY KEY AUTOINCREMENT,name text, duration text, charges text, description text)")
    con.commit()
    con.close()

class CourseClass:
    def __init__(self,root):
          self.root=root
          self.root.title("Student Result Management System")
          self.root.geometry("1400x700+50+50")  # Increased window size
          self.root.config(bg="white")
          self.root.focus_force()
          
          # Initialize database
          create_db()
          
          #===title===
          title=Label(self.root,text="Manage Course Details",font=("goudy old style",25,"bold"),bg="#033054",fg="white").place(x=10,y=20,relwidth=1,height=50)  # Increased font and height
          #===variables===
          self.var_course=StringVar()
          self.var_duration=StringVar()
          self.var_charges=DoubleVar()

          #====widgets===
          lbl_courseName=Label(self.root,text="Course Name",font=("goudy old style",18,'bold'),bg='white').place(x=10,y=100)  # Increased font
          lbl_duration=Label(self.root,text="Duration",font=("goudy old style",18,'bold'),bg='white').place(x=10,y=150)  # Increased font
          lbl_charges=Label(self.root,text="Charges",font=("goudy old style",18,'bold'),bg='white').place(x=10,y=200)  # Increased font
          lbl_description=Label(self.root,text="Description",font=("goudy old style",18,'bold'),bg='white').place(x=10,y=250)  # Increased font


          #====Entryfeilds=====
          self.txt_courseName=Entry(self.root,textvariable=self.var_course,font=("goudy old style",18,'bold'),bg='lightyellow')  # Increased font
          self.txt_courseName.place(x=150,y=100,width=250)  # Increased width
          txt_duration=Entry(self.root,textvariable=self.var_duration,font=("goudy old style",18,'bold'),bg='lightyellow')  # Increased font
          txt_duration.place(x=150,y=150,width=250)  # Increased width
          txt_charges=Entry(self.root,textvariable=self.var_charges,font=("goudy old style",18,'bold'),bg='lightyellow')  # Increased font
          txt_charges.place(x=150,y=200,width=250)  # Increased width
          self.txt_description=Text(self.root,font=("goudy old style",18,'bold'),bg='lightyellow')  # Increased font
          self.txt_description.place(x=150,y=250,width=500,height=200)  # Increased width and height

          #=====Buttons======
          self.btn_add=Button(self.root,text='Save',font=("goudy old style",18,"bold"),bg='#2196f3',fg="white",cursor="hand2",command=self.add)  # Increased font
          self.btn_add.place(x=150,y=500,width=120,height=50)  # Increased size
          self.btn_update=Button(self.root,text="Update",font=("goudy old style",18,"bold"),bg='#4caf50',fg="white",cursor="hand2",command=self.update)  # Increased font
          self.btn_update.place(x=280,y=500,width=120,height=50)  # Increased size
          self.btn_delete=Button(self.root,text="Delete",font=("goudy old style",18,"bold"),bg='#f44336',fg="white",cursor="hand2",command=self.delete)  # Increased font
          self.btn_delete.place(x=410,y=500,width=120,height=50)  # Increased size
          self.btn_clear=Button(self.root,text="Clear",font=("goudy old style",18,"bold"),bg="#607d8b",fg="white",cursor="hand2",command=self.clear_fields)  # Increased font
          self.btn_clear.place(x=540,y=500,width=120,height=50)  # Increased size

          #====Search Panel====
          self.var_search=StringVar()
          lbl_search_courseName=Label(self.root,text="Course Name",font=("goudy old style",18,'bold'),bg='white').place(x=720,y=100)  # Increased font
          txt_search_courseName=Entry(self.root,textvariable=self.var_search,font=("goudy old style",18,'bold'),bg='lightyellow').place(x=870,y=100,width=250)  # Increased font and width
          btn_search=Button(self.root,text='Search',font=("goudy old style",18,"bold"),bg='#03a9f4',fg="white",cursor="hand2",command=self.search).place(x=1130,y=100,width=120,height=35)  # Increased font and size

          #======content====
          self.C_Frame=Frame(self.root,bd=2,relief=RIDGE)
          self.C_Frame.place(x=720,y=150,width=550,height=500)  # Increased size

          scrollx=Scrollbar(self.C_Frame,orient=HORIZONTAL)
          scrolly=Scrollbar(self.C_Frame,orient=VERTICAL)
          self.CourseTable=ttk.Treeview(self.C_Frame,columns=("cid","name","duration","charges","description"),xscrollcommand=scrollx.set,yscrollcommand=scrolly.set)

          scrollx.pack(side=BOTTOM,fill=X)
          scrolly.pack(side=RIGHT,fill=Y)
          scrollx.config(command=self.CourseTable.xview)
          scrolly.config(command=self.CourseTable.yview)

          self.CourseTable.heading("cid",text="Course ID")
          self.CourseTable.heading("name",text="Name")
          self.CourseTable.heading("duration",text="Duration")
          self.CourseTable.heading("charges",text="Charges")
          self.CourseTable.heading("description",text="Description")
          self.CourseTable["show"]='headings'
          self.CourseTable.column("cid",width=100)
          self.CourseTable.column("name",width=100)
          self.CourseTable.column("duration",width=100)
          self.CourseTable.column("charges",width=100)
          self.CourseTable.column("description",width=150)
          
          self.CourseTable.pack(fill=BOTH,expand=1)
          self.CourseTable.bind("<ButtonRelease-1>",self.get_data)
          
          # Show data when application starts
          self.show()

#============================================================================================================
    def get_data(self,ev):
        r=self.CourseTable.focus()
        content=self.CourseTable.item(r)
        row=content["values"]
        self.var_course.set(row[1])
        self.var_duration.set(row[2])
        self.var_charges.set(row[3])
        self.txt_description.delete("1.0", END)
        self.txt_description.insert("1.0", row[4])

    def add(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_course.get() == "":
                messagebox.showerror("Error", "Course Name should be required", parent=self.root)
            else:
                print("Checking for existing course...")
                cur.execute("select * from course where name=?", (self.var_course.get(),))
                row = cur.fetchone()
                
                if row != None:
                    messagebox.showerror("Error", "Course Name already present", parent=self.root)
                else:
                    print("Adding new course...")
                    cur.execute("insert into course (name,duration,charges,description) values(?,?,?,?)", (
                        self.var_course.get(),
                        self.var_duration.get(),
                        self.var_charges.get(),
                        self.txt_description.get("1.0", END)
                    ))
                    con.commit()
                    print("Course added successfully!")
                    messagebox.showinfo("Success", "Course Added Successfully", parent=self.root)
                    self.clear_fields()
                    self.show()
                    
        except Exception as ex:
            print(f"Error occurred: {str(ex)}")
            messagebox.showerror("Error", f"Error due to {str(ex)}")
        finally:
            con.close()

    def update(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_course.get() == "":
                messagebox.showerror("Error", "Course Name should be required", parent=self.root)
            else:
                cur.execute("select * from course where name=? and cid!=?", (self.var_course.get(), self.CourseTable.item(self.CourseTable.focus())["values"][0]))
                row = cur.fetchone()
                
                if row != None:
                    messagebox.showerror("Error", "Course Name already present", parent=self.root)
                else:
                    cur.execute("update course set name=?, duration=?, charges=?, description=? where cid=?", (
                        self.var_course.get(),
                        self.var_duration.get(),
                        self.var_charges.get(),
                        self.txt_description.get("1.0", END),
                        self.CourseTable.item(self.CourseTable.focus())["values"][0]
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Course Updated Successfully", parent=self.root)
                    self.clear_fields()
                    self.show()
                    
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")
        finally:
            con.close()

    def clear_fields(self):
        self.var_course.set("")
        self.var_duration.set("")
        self.var_charges.set("")
        self.var_search.set("")
        self.txt_description.delete("1.0", END)
        self.txt_description.insert("1.0", "")

    def show(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            print("Fetching all courses...")
            cur.execute("select * from course")
            rows = cur.fetchall()
            print(f"Found {len(rows)} courses")
            self.CourseTable.delete(*self.CourseTable.get_children())
            for row in rows:
                print(f"Adding row: {row}")
                self.CourseTable.insert('', END, values=row)
        except Exception as ex:
            print(f"Error occurred: {str(ex)}")
            messagebox.showerror("Error", f"Error due to {str(ex)}")
        finally:
            con.close()

    def delete(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_course.get() == "":
                messagebox.showerror("Error", "Please select a course to delete", parent=self.root)
            else:
                op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                if op == True:
                    cur.execute("delete from course where cid=?", (self.CourseTable.item(self.CourseTable.focus())["values"][0],))
                    con.commit()
                    messagebox.showinfo("Success", "Course Deleted Successfully", parent=self.root)
                    self.clear_fields()
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")
        finally:
            con.close()

    def search(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute(f"select * from course where name LIKE '%{self.var_search.get()}%'")
            rows = cur.fetchall()
            self.CourseTable.delete(*self.CourseTable.get_children())
            for row in rows:
                self.CourseTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")
        finally:
            con.close()

if __name__=="__main__":
        root=Tk()
        obj= CourseClass(root)
        root.mainloop()