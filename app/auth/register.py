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

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width / 2) - (WINDOW_SIZE['WIDTH'] / 2))
        y = int((screen_height / 2) - (WINDOW_SIZE['HEIGHT'] / 2))
        self.root.geometry(f"{WINDOW_SIZE['WIDTH']}x{WINDOW_SIZE['HEIGHT']}+{x}+{y}")

        if getattr(sys, 'frozen', False):
            base_path = os.path.join(sys._MEIPASS, 'app')
        else:
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        image_path = os.path.join(base_path, "assets", "auth2.webp")
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found at: {image_path}")

        # Left frame (image)
        self.left_frame = tk.Frame(root, width=(WINDOW_SIZE['WIDTH'] * 2 // 3), bg='#e3f2fd')
        self.left_frame.pack(side="left", fill="both")

        self.left_image = self.load_and_resize_image(image_path, int(WINDOW_SIZE['WIDTH'] * 2 / 3), WINDOW_SIZE['HEIGHT'])
        self.image_label = tk.Label(self.left_frame, image=self.left_image, bg='#e3f2fd')
        self.image_label.place(relx=0.5, rely=0.5, anchor="center")

        # Right frame (form)
        self.right_frame = tk.Frame(root, bg="white")
        self.right_frame.pack(side="right", fill="both", expand=True, padx=30)

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
        title = tk.Label(self.right_frame, text="English Learning", font=("Helvetica", 26, "bold"), fg="#1a73e8", bg="white")
        title.pack(pady=(40, 5))

        subtitle = tk.Label(self.right_frame, text="Tạo tài khoản mới", font=("Helvetica", 14), fg="#5f6368", bg="white")
        subtitle.pack(pady=(0, 25))

        # Fields
        fields = [
            ("Họ và tên", "entry_name"),
            ("Email", "entry_email"),
            ("Mật khẩu", "entry_password"),
            ("Xác nhận mật khẩu", "entry_confirm_password")
        ]

        for label_text, attr_name in fields:
            frame = tk.Frame(self.right_frame, bg="white")
            frame.pack(fill="x", pady=(5, 12))

            label = tk.Label(frame, text=label_text, font=("Helvetica", 11, "bold"), fg="#202124", bg="white")
            label.pack(anchor="w")

            entry = ttk.Entry(frame, width=40, show="•" if "mật khẩu" in label_text.lower() else "")
            entry.pack(ipady=6, pady=4)

            setattr(self, attr_name, entry)

        # Vai trò
        role_frame = tk.Frame(self.right_frame, bg="white")
        role_frame.pack(fill="x", pady=(10, 15))

        label_role = tk.Label(role_frame, text="Vai trò", font=("Helvetica", 11, "bold"), fg="#202124", bg="white")
        label_role.pack(anchor="w", pady=(0, 5))

        self.role_var = tk.StringVar(value="user")

        radio_user = tk.Radiobutton(role_frame, text="Người dùng", variable=self.role_var, value="user", bg="white", font=("Helvetica", 10), anchor="w")
        radio_admin = tk.Radiobutton(role_frame, text="Quản trị viên", variable=self.role_var, value="admin", bg="white", font=("Helvetica", 10), anchor="w")

        radio_user.pack(anchor="w")
        radio_admin.pack(anchor="w")

        # Register Button
        self.btn_register = tk.Button(
            self.right_frame,
            text="Đăng ký",
            command=self.register,
            font=("Helvetica", 12, "bold"),
            bg="#1a73e8",
            fg="white",
            activebackground="#1669c1",
            relief="flat",
            padx=10,
            pady=10,
            cursor="hand2"
        )
        self.btn_register.pack(pady=(20, 10), ipadx=10, fill="x")

        # Back Button
        self.btn_back = tk.Button(
            self.right_frame,
            text="← Quay lại đăng nhập",
            command=self.open_login_window,
            font=("Helvetica", 10),
            bg="white",
            fg="#1a73e8",
            relief="flat",
            cursor="hand2"
        )
        self.btn_back.pack()

        # Hover effects
        self.btn_register.bind("<Enter>", lambda e: self.btn_register.configure(bg="#1557b0"))
        self.btn_register.bind("<Leave>", lambda e: self.btn_register.configure(bg="#1a73e8"))

        self.btn_back.bind("<Enter>", lambda e: self.btn_back.configure(fg="#0c47a1"))
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
            messagebox.showerror("Lỗi", "Mật khẩu cần có ít nhất 8 ký tự gồm chữ hoa, thường, số và ký tự đặc biệt!")
            return

        if password != confirm_password:
            messagebox.showerror("Lỗi", "Xác nhận mật khẩu không khớp!")
            return

        database = load_database()
        if any(user["email"] == email for user in database["users"]):
            messagebox.showerror("Lỗi", "Email đã được đăng ký!")
            return

        new_user = {
            "name": name,
            "email": email,
            "password": hash_password(password),
            "role": role
        }

        database["users"].append(new_user)
        save_database(database)
        messagebox.showinfo("Thành công", f"Tài khoản {role.upper()} đã được tạo!")

        self.open_login_window()

    def open_login_window(self):
        from auth.login import LoginWindow
        self.root.destroy()
        new_root = tk.Tk()
        LoginWindow(new_root)
        new_root.mainloop()
