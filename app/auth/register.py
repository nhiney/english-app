from tkinter import *
from tkinter import messagebox
import os
import ast

# Tạo cửa sổ chính
window=Tk()
window. title('Login')
window.geometry('925x500+300+200')
window. configure(bg="#fff")
window.resizable(False,False)

def signup():
    username=user.get()
    password=code.get()
    confirm_password=confirm_code.get()
    if password==confirm_password:
        try:
            file=open('datasheet.txt','r+')
            d=file.read()
            r=ast.literal_eval(d)

            dict2={username:password}
            r.update(dict2)
            file.truncate(0)
            file.close()

            file=open('datasheet.txt','w')
            w=file.write(str(r))
            messagebox.showinfo('Signup','Sucessfully sign up')
        except:
            file=open('datasheet.txt','w')
            pp=str({'Username':'password'})
            file.write(pp)
            file.close()
    else:
        messagebox.showerror('Invalid',"both password should match")
        
# Tính đường dẫn đến image
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(BASE_DIR, 'login.png')

# Load ảnh
img=PhotoImage(file=image_path)
Label(window,image=img,bg='white').place(x=50,y=50)

# Tạo khung nhập
frame=Frame(window,width=500, height=390,bg="#fff")
frame.place (x=480,y=50)

heading=Label(frame,text='Sign up',fg='#57a1f8',bg='white',font=('Microsoft Yahei UI Light',23,'bold'))
heading.place(x=100,y=5)
###-----------------------------------------------------------------------------------------------
def on_enter(e):
    user.delete(0,'end')
def on_leave(e):
    name=user.get()
    if name=='':
        user.insert(0,'Username')
# ô nhập username
user=Entry(frame,width=25,fg='black',border=0,bg="white",font=('Microsoft Yahei UI Light',11))
user.place(x=30,y=80)
user.insert(0,'Username')
user.bind('<FocusIn>',on_enter)
user.bind('<FocusOut>',on_leave)
Frame(frame,width=295,height=2,bg='black').place(x=25,y=107)

####--------------------------------------------------------------------------------------
def on_enter(e):
    code.delete(0,'end')
def on_leave(e):
    name=code.get()
    if name=='':
        code.insert(0,'Password')
code=Entry(frame,width=25,fg='black',border=0,bg="white",font=('Microsoft Yahei UI Light',11))
code.place(x=30,y=150)
code.insert(0,'Password')
code.bind('<FocusIn>',on_enter)
code.bind('<FocusOut>',on_leave)
Frame(frame,width=295,height=2,bg='black').place(x=25,y=177)
####--------------------------------------------------------------------------------------
def on_enter(e):
    confirm_code.delete(0,'end')
def on_leave(e):
    if  confirm_code.get()=='':
         confirm_code.insert(0,'Confirm password')
confirm_code=Entry(frame,width=25,fg='black',border=0,bg="white",font=('Microsoft Yahei UI Light',11))
confirm_code.place(x=30,y=220)
confirm_code.insert(0,'Confirm Password')
confirm_code.bind('<FocusIn>',on_enter)
confirm_code.bind('<FocusOut>',on_leave)
Frame(frame,width=295,height=2,bg='black').place(x=25,y=247)

###############################################################################################

Button(frame,width=39,pady=7,text='Sign up',bg='#57a1f8',fg='white',border=0,command=signup).place(x=35,y=280)
label=Label(frame,text="I have an account",fg='black',bg='white',font=('Microsoft Yahei UI Light',9))
label.place(x=90,y=340)

signin=Button(frame,width=6,text='Sign in',border=0,bg='white',cursor='hand2',fg='#57a1f8')
signin.place(x=200,y=340)

window.mainloop()