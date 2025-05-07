import tkinter as tk
from tkinter import messagebox, ttk
from utils.validators import is_valid_email, is_valid_password
from utils.hash_utils import hash_password
from utils.database import load_database, save_database
from common.configs import WINDOW_SIZE
import os
from PIL import Image, ImageTk
import sys

class RegisterWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Đăng ký tài khoản")
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

        # Right frame for register form
        self.right_frame = tk.Frame(root, bg="white")
        self.right_frame.pack(side="right", fill="both", expand=True, padx=40)

        # Create register form
        self.create_register_form()

    def load_and_resize_image(self, path, frame_width, frame_height):
        """Tải và resize ảnh theo đúng tỉ lệ để fit vào khung"""
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
        """Tạo biểu mẫu đăng ký"""
        # Title for the app
        title_label = tk.Label(self.right_frame, 
                             text="English Learning", 
                             font=("Helvetica", 28, "bold"), 
                             fg="#1a73e8",
                             bg="white")
        title_label.pack(pady=(40, 20))

        # Welcome text
        welcome_label = tk.Label(self.right_frame,
                               text="Create your account",
                               font=("Helvetica", 16),
                               fg="#5f6368",
                               bg="white")
        welcome_label.pack(pady=(0, 30))

        # Name field
        name_frame = tk.Frame(self.right_frame, bg="white")
        name_frame.pack(fill="x", pady=5)
        tk.Label(name_frame, 
                text="Full Name", 
                font=("Helvetica", 12),
                fg="#5f6368",
                bg="white").pack(anchor="w")
        self.entry_name = ttk.Entry(name_frame, width=40)
        self.entry_name.pack(pady=(5, 15))

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
        self.entry_password.pack(pady=(5, 15))

        # Confirm Password field
        confirm_frame = tk.Frame(self.right_frame, bg="white")
        confirm_frame.pack(fill="x", pady=5)
        tk.Label(confirm_frame, 
                text="Confirm Password", 
                font=("Helvetica", 12),
                fg="#5f6368",
                bg="white").pack(anchor="w")
        self.entry_confirm_password = ttk.Entry(confirm_frame, show="•", width=40)
        self.entry_confirm_password.pack(pady=(5, 20))

        # Register button
        self.btn_register = tk.Button(self.right_frame, 
                                    text="Đăng ký", 
                                    command=self.register,
                                    font=("Helvetica", 12),
                                    bg="#1a73e8",
                                    fg="white",
                                    relief="flat",
                                    padx=20,
                                    pady=10,
                                    cursor="hand2")
        self.btn_register.pack(pady=10)
        self.btn_register.bind("<Enter>", lambda e: self.btn_register.configure(bg="#1557b0"))
        self.btn_register.bind("<Leave>", lambda e: self.btn_register.configure(bg="#1a73e8"))

        # Back to login button
        self.btn_back = tk.Button(self.right_frame, 
                                text="Quay lại Đăng nhập", 
                                command=self.open_login_window,
                                font=("Helvetica", 12),
                                bg="white",
                                fg="#1a73e8",
                                relief="flat",
                                cursor="hand2")
        self.btn_back.pack(pady=10)
        self.btn_back.bind("<Enter>", lambda e: self.btn_back.configure(fg="#1557b0"))
        self.btn_back.bind("<Leave>", lambda e: self.btn_back.configure(fg="#1a73e8"))

    def register(self):
        """Xử lý đăng ký tài khoản."""
        name = self.entry_name.get().strip()
        email = self.entry_email.get().strip()
        password = self.entry_password.get().strip()
        confirm_password = self.entry_confirm_password.get().strip()

        # Kiểm tra dữ liệu đầu vào
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

        # Kiểm tra email đã tồn tại chưa
        database = load_database()
        for user in database["users"]:
            if user["email"] == email:
                messagebox.showerror("Lỗi", "Email đã được đăng ký!")
                return

        # Mã hóa mật khẩu và lưu vào JSON
        hashed_password = hash_password(password)
        new_user = {"name": name, "email": email, "password": hashed_password, "role": "user"}

        database["users"].append(new_user)
        save_database(database)
        messagebox.showinfo("Thành công", "Đăng ký thành công!")

        self.open_login_window()

    def open_login_window(self):
        """Import LoginWindow here to avoid circular import."""
        from auth.login import LoginWindow  # ✅ Import only inside function
        self.root.destroy()
        new_root = tk.Tk()
        LoginWindow(new_root)
        new_root.mainloop()