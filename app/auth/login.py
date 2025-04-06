from tkinter import *
from tkinter import messagebox
import os
import sys

# Tạo cửa sổ chính
root = Tk()
root.title('Login')
root.geometry('925x500+300+200')
root.configure(bg="#fff")
root.resizable(False, False)

def signin():
    username = user.get()
    password = code.get()

    if username == 'admin' and password == '1234':
        screen = Toplevel(root)
        screen.title("App")
        screen.geometry('925x500+300+200')
        screen.config(bg="white")

        Label(screen, text='Hello Everyone!', bg='#fff', font=('Calibri(Body)', 50, 'bold')).pack(expand=True)
        screen.mainloop()
    elif username != 'admin' and password != '1234':
        messagebox.showerror("Invalid", "Invalid username and password")
    elif password != "1234":
        messagebox.showerror("Invalid", "Invalid password")
    elif username != 'admin':
        messagebox.showerror("Invalid", "Invalid username")

# Tính đường dẫn đến image
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(BASE_DIR, 'login.png')

# Load ảnh
img = PhotoImage(file=image_path)
Label(root, image=img, bg='white').place(x=50, y=50)

# Tạo khung nhập
frame = Frame(root, width=500, height=500, bg="white")
frame.place(x=480, y=70)
heading = Label(frame, text='Sign in', fg='#57a1f8', bg='white', font=('Microsoft Yahei UI Light', 23, 'bold'))
heading.place(x=100, y=5)

def on_enter(e):
    user.delete(0, 'end')

def on_leave(e):
    name = user.get()
    if name == '':
        user.insert(0, 'Username')

# ô nhập username
user = Entry(frame, width=25, fg='black', border=0, bg="white", font=('Microsoft Yahei UI Light', 11))
user.place(x=30, y=80)
user.insert(0, 'Username')
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)
Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

def on_enter(e):
    code.delete(0, 'end')

def on_leave(e):
    name = code.get()
    if name == '':
        code.insert(0, 'Password')

# ô nhập password
code = Entry(frame, width=25, fg='black', border=0, bg="white", font=('Microsoft Yahei UI Light', 11))
code.place(x=30, y=150)
code.insert(0, 'Password')
code.bind('<FocusIn>', on_enter)
code.bind('<FocusOut>', on_leave)
Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)

Button(frame, width=39, pady=7, text='Sign in', bg='#57a1f8', fg='white', border=0, command=signin).place(x=35, y=204)

label = Label(frame, text="Don't have an account?", fg='black', bg='white', font=('Microsoft Yahei UI Light', 9))
label.place(x=75, y=270)

# Nút Sign up
sign_up = Button(frame, width=6, text='Sign up', border=0, bg='white', cursor='hand2', fg='#57a1f8', command=lambda: go_to_register())
sign_up.place(x=215, y=270)

def go_to_register():
    root.destroy()  # Đóng cửa sổ đăng nhập
    open_register_window()  # Mở cửa sổ đăng ký

def open_register_window():
    import register  # Import file register.py từ thư mục đã thêm vào sys.path
    register.open_window()  # Gọi hàm open_window() trong register.py để mở cửa sổ đăng ký

root.mainloop()
