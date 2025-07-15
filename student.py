from tkinter import*
from PIL import Image, ImageTk
from tkinter import ttk,messagebox
import sqlite3
from tkcalendar import DateEntry

class StudentClass:
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
        title=Label(self.root,text="Manage Student Details",font=("goudy old style",25,"bold"),bg="#033054",fg="white").place(x=10,y=20,relwidth=1,height=50)
        
        #===variables===
        self.var_roll=StringVar()
        self.var_name=StringVar()
        self.var_email=StringVar()
        self.var_gender=StringVar()
        self.var_dob=StringVar()
        self.var_contact=StringVar()
        self.var_course=StringVar()
        self.var_a_date=StringVar()
        self.var_state=StringVar()
        self.var_city=StringVar()
        self.var_pin=StringVar()
        
        #====widgets===
        #===column1===
        lbl_roll=Label(self.root,text="Roll No.",font=("goudy old style",18,'bold'),bg='white').place(x=10,y=100)
        lbl_Name=Label(self.root,text="Name",font=("goudy old style",18,'bold'),bg='white').place(x=10,y=150)
        lbl_Email=Label(self.root,text="Email",font=("goudy old style",18,'bold'),bg='white').place(x=10,y=200)
        lbl_gender=Label(self.root,text="Gender",font=("goudy old style",18,'bold'),bg='white').place(x=10,y=250)
        lbl_state=Label(self.root,text="State",font=("goudy old style",18,'bold'),bg='white').place(x=10,y=300)
        
        #===Entry Fields Column 1===
        self.txt_roll=Entry(self.root,textvariable=self.var_roll,font=("goudy old style",18,'bold'),bg='lightyellow')
        self.txt_roll.place(x=150,y=100,width=200)
        txt_name=Entry(self.root,textvariable=self.var_name,font=("goudy old style",18,'bold'),bg='lightyellow')
        txt_name.place(x=150,y=150,width=200)
        txt_email=Entry(self.root,textvariable=self.var_email,font=("goudy old style",18,'bold'),bg='lightyellow')
        txt_email.place(x=150,y=200,width=200)
        self.txt_gender=ttk.Combobox(self.root,textvariable=self.var_gender,values=("Select","Male","Female","Other"),font=("goudy old style",18,'bold'),state='readonly',justify=CENTER)
        self.txt_gender.place(x=150,y=250,width=200)
        self.txt_gender.current(0)
        txt_state=Entry(self.root,textvariable=self.var_state,font=("goudy old style",18,'bold'),bg='lightyellow')
        txt_state.place(x=150,y=300,width=200)

        #===column2===
        lbl_dob=Label(self.root,text="D.O.B",font=("goudy old style",18,'bold'),bg='white').place(x=370,y=100)
        lbl_contact=Label(self.root,text="Contact",font=("goudy old style",18,'bold'),bg='white').place(x=370,y=150)
        lbl_admission=Label(self.root,text="Admission",font=("goudy old style",18,'bold'),bg='white').place(x=360,y=200)
        lbl_course=Label(self.root,text="Course",font=("goudy old style",18,'bold'),bg='white').place(x=370,y=250)
        
        #===Entry Fields Column 2===
        self.cal_dob=DateEntry(self.root,selectmode='day',date_pattern="dd/MM/yyyy",font=("goudy old style",18,'bold'))
        self.cal_dob.place(x=470,y=100,width=200)
        
        txt_contact=Entry(self.root,textvariable=self.var_contact,font=("goudy old style",18,'bold'),bg='lightyellow')
        txt_contact.place(x=470,y=150,width=200)
        
        self.cal_a_date=DateEntry(self.root,selectmode='day',date_pattern="dd/MM/yyyy",font=("goudy old style",18,'bold'))
        self.cal_a_date.place(x=470,y=200,width=200)
        
        self.course_list=[]
        self.fetch_course()
        self.txt_course=ttk.Combobox(self.root,textvariable=self.var_course,values=self.course_list,font=("goudy old style",18,'bold'),state='readonly',justify=CENTER)
        self.txt_course.place(x=470,y=250,width=200)
        self.txt_course.set("Select")
        
        # Course Button
        self.btn_course=Button(self.root,text='Course',font=("goudy old style",18,"bold"),bg='#2196f3',fg="white",cursor="hand2",command=self.add_course)
        self.btn_course.place(x=680,y=250,width=120,height=35)

        # City and Pin in one row
        lbl_city=Label(self.root,text="City",font=("goudy old style",18,'bold'),bg='white').place(x=370,y=300)
        txt_city=Entry(self.root,textvariable=self.var_city,font=("goudy old style",18,'bold'),bg='lightyellow')
        txt_city.place(x=470,y=300,width=120)
        
        lbl_pin=Label(self.root,text="Pin",font=("goudy old style",18,'bold'),bg='white').place(x=600,y=300)
        txt_pin=Entry(self.root,textvariable=self.var_pin,font=("goudy old style",18,'bold'),bg='lightyellow')
        txt_pin.place(x=680,y=300,width=120)

        # Address at bottom
        lbl_address=Label(self.root,text="Address",font=("goudy old style",18,'bold'),bg='white').place(x=10,y=350)
        self.txt_address=Text(self.root,font=("goudy old style",18,'bold'),bg='lightyellow')
        self.txt_address.place(x=150,y=350,width=500,height=100)

        #===Search Panel===
        self.var_search=StringVar()
        lbl_search_roll=Label(self.root,text="Roll No.",font=("goudy old style",18,'bold'),bg='white').place(x=820,y=100)
        self.txt_search_roll=Entry(self.root,textvariable=self.var_search,font=("goudy old style",18,'bold'),bg='lightyellow')
        self.txt_search_roll.place(x=970,y=100,width=200)
        self.txt_search_roll.bind('<Return>', lambda e: self.search())  # Bind Enter key to search
        btn_search=Button(self.root,text='Search',font=("goudy old style",18,"bold"),bg='#03a9f4',fg="white",cursor="hand2",command=self.search).place(x=1180,y=100,width=120,height=35)
        
        #===Buttons===
        self.btn_add=Button(self.root,text='Save',font=("goudy old style",18,"bold"),bg='#2196f3',fg="white",cursor="hand2",command=self.add)
        self.btn_add.place(x=150,y=600,width=120,height=50)
        self.btn_update=Button(self.root,text="Update",font=("goudy old style",18,"bold"),bg='#4caf50',fg="white",cursor="hand2",command=self.update)
        self.btn_update.place(x=280,y=600,width=120,height=50)
        self.btn_delete=Button(self.root,text="Delete",font=("goudy old style",18,"bold"),bg='#f44336',fg="white",cursor="hand2",command=self.delete)
        self.btn_delete.place(x=410,y=600,width=120,height=50)
        self.btn_clear=Button(self.root,text="Clear",font=("goudy old style",18,"bold"),bg="#607d8b",fg="white",cursor="hand2",command=self.clear_fields)
        self.btn_clear.place(x=540,y=600,width=120,height=50)
        
        #===content===
        self.C_Frame=Frame(self.root,bd=2,relief=RIDGE)
        self.C_Frame.place(x=820,y=150,width=550,height=350)
        
        scrollx=Scrollbar(self.C_Frame,orient=HORIZONTAL)
        scrolly=Scrollbar(self.C_Frame,orient=VERTICAL)
        self.StudentTable=ttk.Treeview(self.C_Frame,columns=("roll","name","email","gender","dob","contact","admission","course","state","city","pin","address"),xscrollcommand=scrollx.set,yscrollcommand=scrolly.set)
        
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.StudentTable.xview)
        scrolly.config(command=self.StudentTable.yview)
        
        self.StudentTable.heading("roll",text="Roll No.")
        self.StudentTable.heading("name",text="Name")
        self.StudentTable.heading("email",text="Email")
        self.StudentTable.heading("gender",text="Gender")
        self.StudentTable.heading("dob",text="D.O.B")
        self.StudentTable.heading("contact",text="Contact")
        self.StudentTable.heading("admission",text="Admission")
        self.StudentTable.heading("course",text="Course")
        self.StudentTable.heading("state",text="State")
        self.StudentTable.heading("city",text="City")
        self.StudentTable.heading("pin",text="PIN")
        self.StudentTable.heading("address",text="Address")
        self.StudentTable["show"]='headings'
        
        self.StudentTable.column("roll",width=100)
        self.StudentTable.column("name",width=100)
        self.StudentTable.column("email",width=100)
        self.StudentTable.column("gender",width=100)
        self.StudentTable.column("dob",width=100)
        self.StudentTable.column("contact",width=100)
        self.StudentTable.column("admission",width=100)
        self.StudentTable.column("course",width=100)
        self.StudentTable.column("state",width=100)
        self.StudentTable.column("city",width=100)
        self.StudentTable.column("pin",width=100)
        self.StudentTable.column("address",width=200)
        
        self.StudentTable.pack(fill=BOTH,expand=1)
        self.StudentTable.bind("<ButtonRelease-1>",self.get_data)
        
        # Show data when application starts
        self.show()
        
        # Add close button with more space below the table
        self.btn_close=Button(self.root,text="Close",font=("goudy old style",18,"bold"),bg="#607d8b",fg="white",cursor="hand2",command=self.close_window)
        self.btn_close.place(x=1180,y=520,width=120,height=35)

    def close_window(self):
        self.root.destroy()

    def create_db(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS student(roll INTEGER PRIMARY KEY,name text,email text,gender text,dob text,contact text,admission text,course text,state text,city text,pin text,address text)")
        con.commit()
        con.close()
        
    def fetch_course(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("select name from course")
            rows = cur.fetchall()
            if len(rows)>0:
                for row in rows:
                    self.course_list.append(row[0])
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")
        finally:
            con.close()
            
    def add(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_roll.get() == "":
                messagebox.showerror("Error", "Roll Number should be required", parent=self.root)
            else:
                cur.execute("select * from student where roll=?", (self.var_roll.get(),))
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror("Error", "Roll Number already exists", parent=self.root)
                else:
                    cur.execute("insert into student (roll,name,email,gender,dob,contact,admission,course,state,city,pin,address) values(?,?,?,?,?,?,?,?,?,?,?,?)", (
                        self.var_roll.get(),
                        self.var_name.get(),
                        self.var_email.get(),
                        self.var_gender.get(),
                        self.cal_dob.get(),
                        self.var_contact.get(),
                        self.cal_a_date.get(),
                        self.var_course.get(),
                        self.var_state.get(),
                        self.var_city.get(),
                        self.var_pin.get(),
                        self.txt_address.get("1.0", END)
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Student Added Successfully", parent=self.root)
                    self.clear_fields()
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")
        finally:
            con.close()
            
    def update(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_roll.get() == "":
                messagebox.showerror("Error", "Roll Number should be required", parent=self.root)
            else:
                cur.execute("select * from student where roll=? and roll!=?", (self.var_roll.get(), self.StudentTable.item(self.StudentTable.focus())["values"][0]))
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror("Error", "Roll Number already exists", parent=self.root)
                else:
                    cur.execute("update student set name=?,email=?,gender=?,dob=?,contact=?,admission=?,course=?,state=?,city=?,pin=?,address=? where roll=?", (
                        self.var_name.get(),
                        self.var_email.get(),
                        self.var_gender.get(),
                        self.cal_dob.get(),
                        self.var_contact.get(),
                        self.cal_a_date.get(),
                        self.var_course.get(),
                        self.var_state.get(),
                        self.var_city.get(),
                        self.var_pin.get(),
                        self.txt_address.get("1.0", END),
                        self.var_roll.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Student Updated Successfully", parent=self.root)
                    self.clear_fields()
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")
        finally:
            con.close()
            
    def delete(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_roll.get() == "":
                messagebox.showerror("Error", "Roll Number should be required", parent=self.root)
            else:
                cur.execute("select * from student where roll=?", (self.var_roll.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Roll Number", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                    if op == True:
                        cur.execute("delete from student where roll=?", (self.var_roll.get(),))
                        con.commit()
                        messagebox.showinfo("Success", "Student Deleted Successfully", parent=self.root)
                        self.clear_fields()
                        self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")
        finally:
            con.close()
            
    def clear_fields(self):
        self.var_roll.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Select")
        self.var_dob.set("")
        self.var_contact.set("")
        self.var_course.set("Select")
        self.var_a_date.set("")
        self.var_state.set("")
        self.var_city.set("")
        self.var_pin.set("")
        self.txt_address.delete("1.0", END)
        self.var_search.set("")
        self.show()
        
    def get_data(self,ev):
        r=self.StudentTable.focus()
        content=self.StudentTable.item(r)
        row=content["values"]
        self.var_roll.set(row[0])
        self.var_name.set(row[1])
        self.var_email.set(row[2])
        self.var_gender.set(row[3])
        self.var_dob.set(row[4])
        self.var_contact.set(row[5])
        self.var_a_date.set(row[6])
        self.var_course.set(row[7])
        self.var_state.set(row[8])
        self.var_city.set(row[9])
        self.var_pin.set(row[10])
        self.txt_address.delete("1.0", END)
        self.txt_address.insert("1.0", row[11])
        
    def show(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("select * from student")
            rows = cur.fetchall()
            self.StudentTable.delete(*self.StudentTable.get_children())
            for row in rows:
                self.StudentTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")
        finally:
            con.close()
            
    def search(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute(f"select * from student where roll LIKE '%{self.var_search.get()}%'")
            rows = cur.fetchall()
            self.StudentTable.delete(*self.StudentTable.get_children())
            for row in rows:
                self.StudentTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")
        finally:
            con.close()

    def add_course(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=CourseClass(self.new_win)
        self.new_win.grab_set()
        self.new_win.focus()

if __name__=="__main__":
    root=Tk()
    obj=StudentClass(root)
    root.mainloop()