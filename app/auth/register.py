import tkinter as tk
from tkinter import messagebox, ttk
from utils.validators import is_valid_email, is_valid_password
from utils.hash_utils import hash_password
from utils.database import load_database, save_database
from common.configs import WINDOW_SIZE
import os
import sys
from PIL import Image, ImageTk

class RegisterWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Đăng ký tài khoản")
        self.root.configure(bg='white')

        # Căn giữa cửa sổ
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width / 2) - (WINDOW_SIZE['WIDTH'] / 2))
        y = int((screen_height / 2) - (WINDOW_SIZE['HEIGHT'] / 2))
        self.root.geometry(f"{WINDOW_SIZE['WIDTH']}x{WINDOW_SIZE['HEIGHT']}+{x}+{y}")

        # Load ảnh
        if getattr(sys, 'frozen', False):
            base_path = os.path.join(sys._MEIPASS, 'app')
        else:
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        image_path = os.path.join(base_path, "assets", "auth2.webp")
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found at: {image_path}")

        # Frame ảnh
        self.left_frame = tk.Frame(root, width=(WINDOW_SIZE['WIDTH'] / 3 * 2), height=WINDOW_SIZE['HEIGHT'], bg='#f0f2f5')
        self.left_frame.pack(side="left", fill="both", expand=False)

        self.left_image = self.load_and_resize_image(image_path, int(WINDOW_SIZE['WIDTH'] / 3 * 2), WINDOW_SIZE['HEIGHT'])
        self.image_label = tk.Label(self.left_frame, image=self.left_image, bg='#f0f2f5')
        self.image_label.place(relx=0.5, rely=0.5, anchor="center")

        # Frame form
        self.right_frame = tk.Frame(root, bg="white")
        self.right_frame.pack(side="right", fill="both", expand=True, padx=40)

        self.create_register_form()

    def load_and_resize_image(self, path, frame_width, frame_height):
        image = Image.open(path)
        img_ratio = image.width / image.height
        frame_ratio = frame_width / frame_height

        if img_ratio > frame_ratio:
            new_width = frame_width
            new_height = int(frame_width / img_ratio)
        else:
            new_height = frame_height
            new_width = int(frame_height * img_ratio)

        resized = image.resize((new_width, new_height), Image.LANCZOS)
        return ImageTk.PhotoImage(resized)

    def create_register_form(self):
        style = ttk.Style()
        style.configure("TEntry", padding=10, relief="flat", font=("Helvetica", 12))
        style.configure("TButton", padding=6, font=("Helvetica", 12, "bold"))

        # Tiêu đề
        title_label = tk.Label(self.right_frame, text="English Learning", font=("Helvetica", 28, "bold"), fg="#1a73e8", bg="white")
        title_label.pack(pady=(30, 10))

        welcome_label = tk.Label(self.right_frame, text="Create your account", font=("Helvetica", 16), fg="#5f6368", bg="white")
        welcome_label.pack(pady=(0, 25))

        # Các trường nhập
        fields = [
            ("Full Name", "entry_name"),
            ("Email", "entry_email"),
            ("Password", "entry_password"),
            ("Confirm Password", "entry_confirm_password")
        ]

        for label_text, attr_name in fields:
            frame = tk.Frame(self.right_frame, bg="white")
            frame.pack(fill="x", pady=(5, 10))

            label = tk.Label(frame, text=label_text, font=("Helvetica", 12, "bold"), fg="#202124", bg="white")
            label.pack(anchor="w")

            entry = ttk.Entry(frame, width=40, show="•" if "Password" in label_text else "")
            entry.pack(ipady=5, pady=5)

            setattr(self, attr_name, entry)

        # Vai trò
        role_frame = tk.Frame(self.right_frame, bg="white")
        role_frame.pack(fill="x", pady=(5, 15))

        label_role = tk.Label(role_frame, text="Vai trò", font=("Helvetica", 12, "bold"), fg="#202124", bg="white")
        label_role.pack(anchor="w", pady=(0, 5))

        self.role_var = tk.StringVar(value="user")

        radio_user = tk.Radiobutton(role_frame, text="Người dùng (User)", variable=self.role_var, value="user", font=("Helvetica", 11), bg="white", anchor="w")
        radio_admin = tk.Radiobutton(role_frame, text="Quản trị viên (Admin)", variable=self.role_var, value="admin", font=("Helvetica", 11), bg="white", anchor="w")

        radio_user.pack(anchor="w")
        radio_admin.pack(anchor="w")

        # Nút đăng ký
        self.btn_register = tk.Button(
            self.right_frame, 
            text="Đăng ký", 
            command=self.register,
            font=("Helvetica", 12, "bold"),
            bg="#1a73e8",
            fg="white",
            activebackground="#1557b0",
            activeforeground="white",
            relief="flat",
            padx=10,
            pady=8,
            cursor="hand2"
        )
        self.btn_register.pack(pady=(10, 5), ipadx=10)

        # Nút quay lại
        self.btn_back = tk.Button(
            self.right_frame, 
            text="Quay lại Đăng nhập", 
            command=self.open_login_window,
            font=("Helvetica", 11),
            bg="white",
            fg="#1a73e8",
            relief="flat",
            cursor="hand2"
        )
        self.btn_back.pack(pady=5)

        self.btn_register.bind("<Enter>", lambda e: self.btn_register.configure(bg="#1557b0"))
        self.btn_register.bind("<Leave>", lambda e: self.btn_register.configure(bg="#1a73e8"))

        self.btn_back.bind("<Enter>", lambda e: self.btn_back.configure(fg="#1557b0"))
        self.btn_back.bind("<Leave>", lambda e: self.btn_back.configure(fg="#1a73e8"))

    def register(self):
        name = self.entry_name.get().strip()
        email = self.entry_email.get().strip()
        password = self.entry_password.get().strip()
        confirm_password = self.entry_confirm_password.get().strip()
        role = self.role_var.get()

        if len(name) < 2:
            messagebox.showerror("Lỗi", "Họ và tên phải có ít nhất 2 ký tự!")
            return

        if not is_valid_email(email):
            messagebox.showerror("Lỗi", "Email không hợp lệ!")
            return

        if not is_valid_password(password):
            messagebox.showerror("Lỗi", "Mật khẩu phải có ít nhất 8 ký tự, gồm chữ hoa, chữ thường, số và ký tự đặc biệt!")
            return

        if password != confirm_password:
            messagebox.showerror("Lỗi", "Mật khẩu xác nhận không khớp!")
            return

        database = load_database()
        for user in database["users"]:
            if user["email"] == email:
                messagebox.showerror("Lỗi", "Email đã được đăng ký!")
                return

        hashed_password = hash_password(password)
        new_user = {
            "name": name,
            "email": email,
            "password": hashed_password,
            "role": role
        }

        database["users"].append(new_user)
        save_database(database)
        messagebox.showinfo("Thành công", f"Tài khoản {role.upper()} đã được tạo thành công!")

        self.open_login_window()

    def open_login_window(self):
        from auth.login import LoginWindow
        self.root.destroy()
        new_root = tk.Tk()
        LoginWindow(new_root)
        new_root.mainloop()
