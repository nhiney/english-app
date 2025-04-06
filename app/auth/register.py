import tkinter as tk
from tkinter import messagebox
import re

def validate_input(username, password, confirm_password):
    if len(username) < 3 or username.isdigit():
        return "Tên người dùng không hợp lệ!"
    
    if password != confirm_password:
        return "Mật khẩu xác nhận không khớp!"
    
    # Mật khẩu mạnh: ít nhất 8 ký tự, có hoa, thường, số, đặc biệt
    if len(password) < 8 or \
       not re.search(r'[A-Z]', password) or \
       not re.search(r'[a-z]', password) or \
       not re.search(r'\d', password) or \
       not re.search(r'[\W_]', password):
        return "Mật khẩu yếu! Cần ít nhất 8 ký tự gồm hoa, thường, số, ký tự đặc biệt."
    
    return None

class RegisterWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Sign Up")
        self.root.geometry("800x400")
        self.root.configure(bg='white')

        # Khung trái: ảnh/logo
        left_frame = tk.Frame(self.root, bg='white')
        left_frame.pack(side="left", fill="both", expand=True)

        logo = tk.PhotoImage(file="D:/Python/english-app/app/auth/login.png")  # Đảm bảo rằng đường dẫn ảnh đúng
        img_label = tk.Label(left_frame, image=logo, bg="white")
        img_label.image = logo  # Giữ tham chiếu để tránh mất ảnh
        img_label.pack(padx=20, pady=60)

        # Khung phải: Form đăng ký
        right_frame = tk.Frame(self.root, bg="white")
        right_frame.pack(side="right", fill="both", expand=True, padx=30)

        tk.Label(right_frame, text="Sign up", font=("Helvetica", 20), fg="dodgerblue", bg="white").pack(pady=10)

        self.username_entry = self._create_entry(right_frame, "Username")
        self.password_entry = self._create_entry(right_frame, "Password", show='*')
        self.confirm_entry = self._create_entry(right_frame, "Confirm Password", show='*')

        self.signup_btn = tk.Button(right_frame, text="Sign up", bg="dodgerblue", fg="white", height=2, command=self.signup)
        self.signup_btn.pack(fill="x", pady=(15, 10))

        tk.Label(right_frame, text="I have an account", bg="white").pack()
        tk.Button(right_frame, text="Sign in", fg="dodgerblue", bg="white", bd=0, command=self.go_to_login).pack()

    def _create_entry(self, parent, label_text, show=None):
        tk.Label(parent, text=label_text, bg="white", anchor='w').pack(fill="x", pady=(5,0))
        entry = tk.Entry(parent, bd=1, relief="solid", show=show)
        entry.pack(fill="x", pady=(0, 5))
        return entry

    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm = self.confirm_entry.get()

        error = validate_input(username, password, confirm)
        if error:
            messagebox.showerror("Lỗi", error)
        else:
            messagebox.showinfo("Thành công", "Đăng ký thành công!")
            self.root.destroy()
            open_login_window()

    def go_to_login(self):
        self.root.destroy()
        open_login_window()

def open_login_window():
    import login  # Giả sử login.py là module trong cùng một thư mục
    login.open_window()  # Chỉ gọi hàm open_window() để mở cửa sổ đăng nhập

if __name__ == "__main__":
    root = tk.Tk()
    app = RegisterWindow(root)
    root.mainloop()
