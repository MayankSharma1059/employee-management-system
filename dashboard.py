from tkinter import*
from PIL import Image, ImageTk #pip install pillow
from course import CourseClass
from student import StudentClass
from report import ReportClass

import sqlite3
from tkinter import messagebox
import os

class Dashboard:
    def __init__(self,root):
        self.root=root
        self.root.title("Student Result Management System")
        self.root.geometry("1400x700+50+50")
        self.root.config(bg="white")
        
        #===title===
        title=Label(self.root,text="Student Result Management System",font=("goudy old style",20,"bold"),bg="#033054",fg="white").place(x=0,y=0,relwidth=1,height=50)
        
        #===Menu===
        M_Frame=LabelFrame(self.root,text="Menu",font=("times new roman",15),bg="white")
        M_Frame.place(x=10,y=70,width=1340,height=80)
        
        # Calculate button positions for even spacing
        btn_width = 200
        btn_height = 40
        btn_spacing = 20
        total_width = 1340 - 40  # Frame width minus margins
        available_width = total_width - (6 * btn_width)  # Now 6 buttons
        spacing = available_width // 5  # Space between buttons
        
        btn_course=Button(M_Frame,text="Course",font=("goudy old style",15,"bold"),bg="#0b5377",fg="white",cursor="hand2",command=self.add_course)
        btn_course.place(x=20,y=5,width=btn_width,height=btn_height)
        btn_student=Button(M_Frame,text="Student",font=("goudy old style",15,"bold"),bg="#0b5377",fg="white",cursor="hand2",command=self.add_student).place(x=20+btn_width+spacing,y=5,width=btn_width,height=btn_height)
        btn_result=Button(M_Frame,text="Result",font=("goudy old style",15,"bold"),bg="#0b5377",fg="white",cursor="hand2",command=self.add_result).place(x=20+(btn_width+spacing)*2,y=5,width=btn_width,height=btn_height)
        btn_view=Button(M_Frame,text="View Student Result",font=("goudy old style",15,"bold"),bg="#0b5377",fg="white",cursor="hand2",command=self.view_result).place(x=20+(btn_width+spacing)*3,y=5,width=btn_width,height=btn_height)
        btn_logout=Button(M_Frame,text="Logout",font=("goudy old style",15,"bold"),bg="#0b5377",fg="white",cursor="hand2",command=self.logout).place(x=20+(btn_width+spacing)*4,y=5,width=btn_width,height=btn_height)
        btn_exit=Button(M_Frame,text="Exit",font=("goudy old style",15,"bold"),bg="#0b5377",fg="white",cursor="hand2",command=self.exit).place(x=20+(btn_width+spacing)*5,y=5,width=btn_width,height=btn_height)
        
        #===Content Window===
        self.bg_img=Image.open("images/bg.png")
        self.bg_img=self.bg_img.resize((1340,500),Image.LANCZOS)
        self.bg_img=ImageTk.PhotoImage(self.bg_img)
        
        self.lbl_bg=Label(self.root,image=self.bg_img).place(x=10,y=160,width=1340,height=500)
        
        #===Update Details===
        stats_y = 680  # Move below the image (bg image y=160, height=500, so 160+500=660, add some margin)
        stats_width = 300
        stats_height = 100
        stats_spacing = 10
        stats_start_x = (1340 - (3 * stats_width + 2 * stats_spacing)) // 2 + 10  # Centered in the window
        self.lbl_course=Label(self.root,text="Total Courses\n[ 0 ]",font=("goudy old style",20),bd=10,relief=RIDGE,bg="#e43b31",fg="white")
        self.lbl_course.place(x=stats_start_x,y=stats_y,width=stats_width,height=stats_height)
        
        self.lbl_student=Label(self.root,text="Total Students\n[ 0 ]",font=("goudy old style",20),bd=10,relief=RIDGE,bg="#138808",fg="white")
        self.lbl_student.place(x=stats_start_x+stats_width+stats_spacing,y=stats_y,width=stats_width,height=stats_height)
        
        self.lbl_result=Label(self.root,text="Total Results\n[ 0 ]",font=("goudy old style",20),bd=10,relief=RIDGE,bg="#138808",fg="white")
        self.lbl_result.place(x=stats_start_x+2*(stats_width+stats_spacing),y=stats_y,width=stats_width,height=stats_height)
        
        #===Footer===
        footer=Label(self.root,text="SRMS - Student Result Management System\nContact Us: 1234567890",font=("goudy old style",12),bg="#262626",fg="white").pack(side=BOTTOM,fill=X)
        
        #===Update Status===
        self.update_details()
        
    def update_details(self):
        # Update course count
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("select * from course")
            cr = cur.fetchall()
            self.lbl_course.config(text=f"Total Courses\n[{str(len(cr))}]")
            
            cur.execute("select * from student")
            cr = cur.fetchall()
            self.lbl_student.config(text=f"Total Students\n[{str(len(cr))}]")
            
            cur.execute("select * from result")
            cr = cur.fetchall()
            self.lbl_result.config(text=f"Total Results\n[{str(len(cr))}]")
            
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")
        finally:
            con.close()
    
    def add_student(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=StudentClass(self.new_win)
        
    def add_result(self):
        from result import ResultClass
        self.new_win=Toplevel(self.root)
        self.new_obj=ResultClass(self.new_win)
        
    def view_result(self):
        from report import ReportClass
        self.new_win=Toplevel(self.root)
        self.new_obj=ReportClass(self.new_win)
        
    def logout(self):
        op=messagebox.askyesno("Confirm","Do you really want to logout?",parent=self.root)
        if op==True:
            self.root.destroy()
            os.system("python login.py")
            
    def exit(self):
        op=messagebox.askyesno("Confirm","Do you really want to exit?",parent=self.root)
        if op==True:
            self.root.destroy()

    def add_course(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=CourseClass(self.new_win)

if __name__=="__main__":
    root=Tk()
    obj=Dashboard(root)
    root.mainloop() 