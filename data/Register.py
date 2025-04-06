import tkinter as tk
from tkinter import messagebox

class HomePage:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.title("Trang Chủ")
        self.root.geometry("800x400")
        self.root.configure(bg='white')

        # Khung trái: ảnh/logo
        left_frame = tk.Frame(self.root, bg='white')
        left_frame.pack(side="left", fill="both", expand=True)

        logo = tk.PhotoImage(file="D:/Python/english-app/app/auth/logo.png")  # Đảm bảo rằng đường dẫn ảnh đúng
        img_label = tk.Label(left_frame, image=logo, bg="white")
        img_label.image = logo  # Giữ tham chiếu để tránh mất ảnh
        img_label.pack(padx=20, pady=60)

        # Khung phải: Nội dung trang chủ
        right_frame = tk.Frame(self.root, bg="white")
        right_frame.pack(side="right", fill="both", expand=True, padx=30)

        # Chào mừng người dùng
        tk.Label(right_frame, text="Chào mừng, {}".format(self.username), font=("Helvetica", 20), fg="dodgerblue", bg="white").pack(pady=30)

        # Các nút chức năng
        self.account_btn = tk.Button(right_frame, text="Quản lý tài khoản", bg="dodgerblue", fg="white", height=2, command=self.manage_account)
        self.account_btn.pack(fill="x", pady=10)

        self.logout_btn = tk.Button(right_frame, text="Đăng xuất", bg="red", fg="white", height=2, command=self.logout)
        self.logout_btn.pack(fill="x", pady=10)

    def manage_account(self):
        # Thêm các chức năng quản lý tài khoản tại đây
        messagebox.showinfo("Quản lý tài khoản", "Tính năng này đang được phát triển!")

    def logout(self):
        # Đăng xuất và quay lại cửa sổ đăng nhập
        self.root.destroy()
        open_login_window()

def open_home_page(username):
    root = tk.Tk()
    app = HomePage(root, username)
    root.mainloop()

def open_login_window():
    root = tk.Tk()
    root.title("Login")
    root.geometry("800x400")
    root.configure(bg='white')

    def login():
        username = username_entry.get()
        password = password_entry.get()

        # Mã hóa mật khẩu
        hashed_password = hash_password(password)

        try:
            if os.path.exists('datasheet.txt'):
                with open('datasheet.txt', 'r') as file:
                    d = file.read()
                    r = ast.literal_eval(d) if d else {}

                    if username in r and r[username] == hashed_password:
                        messagebox.showinfo('Login', 'Login successful')
                        open_home_page(username)  # Chuyển sang trang chủ sau khi đăng nhập thành công
                    else:
                        messagebox.showerror('Login', 'Invalid username or password')
            else:
                messagebox.showerror('Login', 'No user data found')
        except Exception as e:
            messagebox.showerror('Error', f"An error occurred: {str(e)}")

    # Giao diện đăng nhập
    frame = tk.Frame(root, bg="white")
    frame.pack(padx=30, pady=30)

    tk.Label(frame, text="Login", font=("Helvetica", 20), fg="dodgerblue", bg="white").pack(pady=10)

    username_entry = tk.Entry(frame, bd=1, relief="solid", font=("Helvetica", 12))
    username_entry.pack(fill="x", pady=(10, 5))
    username_entry.insert(0, "Username")

    password_entry = tk.Entry(frame, bd=1, relief="solid", show="*", font=("Helvetica", 12))
    password_entry.pack(fill="x", pady=(10, 5))
    password_entry.insert(0, "Password")

    login_button = tk.Button(frame, text="Login", bg="dodgerblue", fg="white", height=2, command=login)
    login_button.pack(fill="x", pady=(15, 10))

    root.mainloop()

if __name__ == "__main__":
    open_login_window()  # Mở cửa sổ đăng nhập đầu tiên
