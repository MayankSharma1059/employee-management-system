from tkinter import*
from PIL import Image, ImageTk
from tkinter import ttk,messagebox
import sqlite3
import os

class ResultClass:
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
        
        #===variables===
        self.var_roll=StringVar()
        self.var_name=StringVar()
        self.var_course=StringVar()
        self.var_marks=StringVar()
        self.var_full_marks=StringVar()
        self.var_per=StringVar()
        
        #====widgets===
        #===column1===
        lbl_select=Label(self.root,text="Select Student",font=("goudy old style",20,'bold'),bg='white').place(x=50,y=100)
        lbl_name=Label(self.root,text="Name",font=("goudy old style",18,'bold'),bg='white').place(x=50,y=160)
        lbl_course=Label(self.root,text="Course",font=("goudy old style",18,'bold'),bg='white').place(x=50,y=220)
        lbl_marks_ob=Label(self.root,text="Marks Obtained",font=("goudy old style",18,'bold'),bg='white').place(x=50,y=280)
        lbl_full_marks=Label(self.root,text="Full Marks",font=("goudy old style",18,'bold'),bg='white').place(x=50,y=340)
        
        #===Entry Fields===
        # Student Search Frame
        search_frame = Frame(self.root, bg="white")
        search_frame.place(x=280, y=100, width=400, height=40)
        
        self.txt_student=ttk.Combobox(search_frame,textvariable=self.var_roll,values=(),font=("goudy old style",18,'bold'),state='readonly',justify=CENTER)
        self.txt_student.place(x=0,y=0,width=280,height=40)
        self.txt_student.set("Select")
        self.txt_student.bind('<<ComboboxSelected>>', self.fetch_student_details)
        
        btn_search=Button(search_frame,text='Search',font=("goudy old style",15,"bold"),bg='#03a9f4',fg="white",cursor="hand2",command=self.search_student).place(x=290,y=0,width=100,height=40)
        
        txt_name=Entry(self.root,textvariable=self.var_name,font=("goudy old style",18,'bold'),bg='lightyellow',state='readonly')
        txt_name.place(x=280,y=160,width=200)
        
        txt_course=Entry(self.root,textvariable=self.var_course,font=("goudy old style",18,'bold'),bg='lightyellow',state='readonly')
        txt_course.place(x=280,y=220,width=200)
        
        txt_marks=Entry(self.root,textvariable=self.var_marks,font=("goudy old style",18,'bold'),bg='lightyellow')
        txt_marks.place(x=280,y=280,width=200)
        
        txt_full_marks=Entry(self.root,textvariable=self.var_full_marks,font=("goudy old style",18,'bold'),bg='lightyellow')
        txt_full_marks.place(x=280,y=340,width=200)
        
        #===Buttons===
        self.btn_add=Button(self.root,text='Save',font=("goudy old style",18,"bold"),bg='#2196f3',fg="white",cursor="hand2",command=self.add)
        self.btn_add.place(x=50,y=420,width=120,height=50)
        self.btn_update=Button(self.root,text="Update",font=("goudy old style",18,"bold"),bg='#4caf50',fg="white",cursor="hand2",command=self.update)
        self.btn_update.place(x=180,y=420,width=120,height=50)
        self.btn_delete=Button(self.root,text="Delete",font=("goudy old style",18,"bold"),bg='#f44336',fg="white",cursor="hand2",command=self.delete)
        self.btn_delete.place(x=310,y=420,width=120,height=50)
        self.btn_clear=Button(self.root,text="Clear",font=("goudy old style",18,"bold"),bg="#607d8b",fg="white",cursor="hand2",command=self.clear_fields)
        self.btn_clear.place(x=440,y=420,width=120,height=50)
        
        # Add close button
        self.btn_close=Button(self.root,text="Close",font=("goudy old style",18,"bold"),bg="#607d8b",fg="white",cursor="hand2",command=self.close_window)
        self.btn_close.place(x=570,y=420,width=120,height=50)
        
        #===Result Image===
        try:
            self.result_img=Image.open("images/result.jpg")
            self.result_img=self.result_img.resize((500,300),Image.LANCZOS)
            self.result_img=ImageTk.PhotoImage(self.result_img)
            
            self.lbl_result_img=Label(self.root,image=self.result_img,bg="white")
            self.lbl_result_img.place(x=700,y=100,width=500,height=300)
        except Exception as e:
            print(f"Error loading image: {str(e)}")
            # Create a placeholder label if image fails to load
            self.lbl_result_img=Label(self.root,text="Result Image",font=("goudy old style",20,"bold"),bg="white")
            self.lbl_result_img.place(x=700,y=100,width=500,height=300)
        
        # Fetch student data
        self.fetch_roll()

    def create_db(self):
        try:
            con = sqlite3.connect(database="rms.db")
            cur = con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS result(rid INTEGER PRIMARY KEY AUTOINCREMENT,roll text,name text,course text,marks text,full_marks text,per text)")
            con.commit()
        except Exception as ex:
            messagebox.showerror("Error", f"Database Error: {str(ex)}")
        finally:
            if 'con' in locals():
                con.close()

    def fetch_roll(self):
        try:
            con = sqlite3.connect(database="rms.db")
            cur = con.cursor()
            cur.execute("select roll from student")
            rows = cur.fetchall()
            if len(rows)>0:
                self.txt_student['values'] = [row[0] for row in rows]
        except Exception as ex:
            messagebox.showerror("Error", f"Error fetching roll numbers: {str(ex)}")
        finally:
            if 'con' in locals():
                con.close()

    def clear_fields(self):
        self.var_roll.set("Select")
        self.var_name.set("")
        self.var_course.set("")
        self.var_marks.set("")
        self.var_full_marks.set("")
        self.var_per.set("")

    def delete(self):
        try:
            con = sqlite3.connect(database="rms.db")
            cur = con.cursor()
            if self.var_roll.get() == "Select":
                messagebox.showerror("Error", "Please select student", parent=self.root)
            else:
                cur.execute("select * from result where roll=?", (self.var_roll.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Select result from list", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                    if op == True:
                        cur.execute("delete from result where roll=?", (self.var_roll.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Result deleted successfully", parent=self.root)
                        self.clear_fields()
        except Exception as ex:
            messagebox.showerror("Error", f"Error deleting result: {str(ex)}")
        finally:
            if 'con' in locals():
                con.close()

    def add(self):
        try:
            con = sqlite3.connect(database="rms.db")
            cur = con.cursor()
            if self.var_roll.get() == "Select":
                messagebox.showerror("Error", "Please select student", parent=self.root)
            elif not self.var_marks.get() or not self.var_full_marks.get():
                messagebox.showerror("Error", "Please enter marks", parent=self.root)
            else:
                cur.execute("select * from result where roll=?", (self.var_roll.get(),))
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror("Error", "Result already exists", parent=self.root)
                else:
                    try:
                        marks = float(self.var_marks.get())
                        full_marks = float(self.var_full_marks.get())
                        if marks > full_marks:
                            messagebox.showerror("Error", "Marks obtained cannot be greater than full marks", parent=self.root)
                            return
                        per = round((marks * 100) / full_marks, 2)
                        cur.execute("insert into result (roll,name,course,marks,full_marks,per) values(?,?,?,?,?,?)", (
                            self.var_roll.get(),
                            self.var_name.get(),
                            self.var_course.get(),
                            self.var_marks.get(),
                            self.var_full_marks.get(),
                            str(per)
                        ))
                        con.commit()
                        messagebox.showinfo("Success", "Result Added Successfully", parent=self.root)
                        self.clear_fields()
                    except ValueError:
                        messagebox.showerror("Error", "Please enter valid numbers for marks", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error adding result: {str(ex)}")
        finally:
            if 'con' in locals():
                con.close()

    def update(self):
        try:
            con = sqlite3.connect(database="rms.db")
            cur = con.cursor()
            if self.var_roll.get() == "Select":
                messagebox.showerror("Error", "Please select student", parent=self.root)
            elif not self.var_marks.get() or not self.var_full_marks.get():
                messagebox.showerror("Error", "Please enter marks", parent=self.root)
            else:
                cur.execute("select * from result where roll=?", (self.var_roll.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Select result from list", parent=self.root)
                else:
                    try:
                        marks = float(self.var_marks.get())
                        full_marks = float(self.var_full_marks.get())
                        if marks > full_marks:
                            messagebox.showerror("Error", "Marks obtained cannot be greater than full marks", parent=self.root)
                            return
                        per = round((marks * 100) / full_marks, 2)
                        cur.execute("update result set name=?,course=?,marks=?,full_marks=?,per=? where roll=?", (
                            self.var_name.get(),
                            self.var_course.get(),
                            self.var_marks.get(),
                            self.var_full_marks.get(),
                            str(per),
                            self.var_roll.get()
                        ))
                        con.commit()
                        messagebox.showinfo("Success", "Result Updated Successfully", parent=self.root)
                        self.clear_fields()
                    except ValueError:
                        messagebox.showerror("Error", "Please enter valid numbers for marks", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error updating result: {str(ex)}")
        finally:
            if 'con' in locals():
                con.close()

    def close_window(self):
        self.root.destroy()

    def fetch_student_details(self, ev=None):
        try:
            con = sqlite3.connect(database="rms.db")
            cur = con.cursor()
            if self.var_roll.get() == "Select":
                self.var_name.set("")
                self.var_course.set("")
            else:
                cur.execute("select name,course from student where roll=?", (self.var_roll.get(),))
                row = cur.fetchone()
                if row != None:
                    self.var_name.set(row[0])
                    self.var_course.set(row[1])
                else:
                    messagebox.showerror("Error", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error fetching student details: {str(ex)}")
        finally:
            if 'con' in locals():
                con.close()

    def search_student(self):
        try:
            con = sqlite3.connect(database="rms.db")
            cur = con.cursor()
            if self.var_roll.get() == "Select":
                messagebox.showerror("Error", "Please select student", parent=self.root)
            else:
                cur.execute("select * from student where roll=?", (self.var_roll.get(),))
                row = cur.fetchone()
                if row != None:
                    self.var_name.set(row[1])
                    self.var_course.set(row[2])
                else:
                    messagebox.showerror("Error", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error searching student: {str(ex)}")
        finally:
            if 'con' in locals():
                con.close()

if __name__=="__main__":
    root=Tk()
    obj=ResultClass(root)
    root.mainloop()