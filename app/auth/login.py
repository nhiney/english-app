import tkinter as tk
from tkinter import messagebox, ttk
from utils.hash_utils import hash_password
from utils.database import load_database
from common.configs import WINDOW_SIZE
from common.base_window import BaseWindow
from PIL import Image, ImageTk
import os
import sys


class LoginWindow(BaseWindow):
    def __init__(self, root):
        super().__init__(root, "Login", WINDOW_SIZE['WIDTH'], WINDOW_SIZE['HEIGHT'])
        self.root = root
        self.root.title("Đăng nhập")
        self.root.configure(bg='white')

        # Khởi tạo màn hình ở vị trí giữa cửa sổ
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width / 2) - (WINDOW_SIZE['WIDTH'] / 2))
        y = int((screen_height / 2) - (WINDOW_SIZE['HEIGHT'] / 2))
        self.root.geometry(f"{WINDOW_SIZE['WIDTH']}x{WINDOW_SIZE['HEIGHT']}+{x}+{y}")

        # Load image
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            base_path = os.path.join(sys._MEIPASS, 'app')
        else:
            # Running as script
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        image_path = os.path.join(base_path, "assets", "auth2.webp")
        
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found at: {image_path}")

        # Left frame cho ảnh
        self.left_frame = tk.Frame(root, width=(WINDOW_SIZE['WIDTH'] / 3 * 2), height=WINDOW_SIZE['HEIGHT'],
                                   bg='#f0f2f5')
        self.left_frame.pack(side="left", fill="both", expand=False)

        self.left_image = self.load_and_resize_image(image_path, int(WINDOW_SIZE['WIDTH'] / 3 * 2),
                                                     WINDOW_SIZE['HEIGHT'])

        self.image_label = tk.Label(self.left_frame, image=self.left_image, bg='#f0f2f5')
        self.image_label.place(relx=0.5, rely=0.5, anchor="center")

        # Right frame for login form
        self.right_frame = tk.Frame(root, bg="white")
        self.right_frame.pack(side="right", fill="both", expand=True, padx=40)

        # Create login form
        self.create_login_form()

    def load_and_resize_image(self, path, frame_width, frame_height):
        """Tải và resize ảnh theo đúng tỉ lệ để fit vào khung"""
        image = Image.open(path)

        img_ratio = image.width / image.height
        frame_ratio = frame_width / frame_height

        if img_ratio > frame_ratio:
            # Fit theo chiều rộng
            new_width = frame_width
            new_height = int(frame_width / img_ratio)
        else:
            # Fit theo chiều cao
            new_height = frame_height
            new_width = int(frame_height * img_ratio)

        resized = image.resize((new_width, new_height), Image.LANCZOS)
        return ImageTk.PhotoImage(resized)

    def create_login_form(self):
        """Tạo biểu mẫu đăng nhập"""
        # Title for the app
        title_label = tk.Label(self.right_frame, 
                             text="English Learning", 
                             font=("Helvetica", 28, "bold"), 
                             fg="#1a73e8",
                             bg="white")
        title_label.pack(pady=(40, 20))

        # Welcome text
        welcome_label = tk.Label(self.right_frame,
                               text="Welcome back!",
                               font=("Helvetica", 16),
                               fg="#5f6368",
                               bg="white")
        welcome_label.pack(pady=(0, 30))

        # Email field
        email_frame = tk.Frame(self.right_frame, bg="white")
        email_frame.pack(fill="x", pady=5)
        tk.Label(email_frame, 
                text="Email", 
                font=("Helvetica", 12),
                fg="#5f6368",
                bg="white").pack(anchor="w")
        self.entry_email = ttk.Entry(email_frame, width=40)
        self.entry_email.pack(pady=(5, 15))

        # Password field
        password_frame = tk.Frame(self.right_frame, bg="white")
        password_frame.pack(fill="x", pady=5)
        tk.Label(password_frame, 
                text="Password", 
                font=("Helvetica", 12),
                fg="#5f6368",
                bg="white").pack(anchor="w")
        self.entry_password = ttk.Entry(password_frame, show="•", width=40)
        self.entry_password.pack(pady=(5, 20))

        # Login button
        self.btn_login = tk.Button(self.right_frame, 
                                 text="Đăng nhập", 
                                 command=self.login,
                                 font=("Helvetica", 12),
                                 bg="#1a73e8",
                                 fg="white",
                                 relief="flat",
                                 padx=20,
                                 pady=10,
                                 cursor="hand2")
        self.btn_login.pack(pady=10)
        self.btn_login.bind("<Enter>", lambda e: self.btn_login.configure(bg="#1557b0"))
        self.btn_login.bind("<Leave>", lambda e: self.btn_login.configure(bg="#1a73e8"))

        # Register button
        self.btn_register = tk.Button(self.right_frame, 
                                    text="Đăng ký tài khoản mới", 
                                    command=self.open_register_window,
                                    font=("Helvetica", 12),
                                    bg="white",
                                    fg="#1a73e8",
                                    relief="flat",
                                    cursor="hand2")
        self.btn_register.pack(pady=10)
        self.btn_register.bind("<Enter>", lambda e: self.btn_register.configure(fg="#1557b0"))
        self.btn_register.bind("<Leave>", lambda e: self.btn_register.configure(fg="#1a73e8"))

    def login(self):
        """Xử lý đăng nhập."""
        email = self.entry_email.get().strip()
        password = self.entry_password.get().strip()

        database = load_database()

        for user in database["users"]:
            if user["email"] == email and user["password"] == hash_password(password):
                messagebox.showinfo("Thành công", "Đăng nhập thành công!")
                self.root.destroy()
                new_root = tk.Tk()

                """ Mở giao diện trang chủ """
                from home.dashboard import DashboardWindow
                DashboardWindow(new_root, user)
                new_root.mainloop()

                return

        messagebox.showerror("Lỗi", "Email hoặc mật khẩu không đúng!")

    def open_register_window(self):
        """Open register window"""
        self.root.destroy()
        from auth.register import RegisterWindow
        root = tk.Tk()
        app = RegisterWindow(root)
        root.mainloop()
