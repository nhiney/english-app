import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from service.register_service import RegisterService

class RegisterUI:
    def __init__(self, root, show_login_callback):
        self.root = root
        self.show_login_callback = show_login_callback
        self.register_service = RegisterService()
        
        # Initialize UI variables
        self.fullname_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.confirm_password_var = tk.StringVar()
        
        self.init_ui()
    
    def init_ui(self):
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create main frame
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Đăng ký tài khoản", font=('Arial', 18, 'bold'))
        title_label.pack(pady=20)
        
        # Full Name
        fullname_frame = ttk.Frame(main_frame)
        fullname_frame.pack(fill=tk.X, pady=10)
        
        fullname_label = ttk.Label(fullname_frame, text="Họ và tên:")
        fullname_label.pack(anchor=tk.W)
        
        fullname_entry = ttk.Entry(fullname_frame, textvariable=self.fullname_var, width=40)
        fullname_entry.pack(fill=tk.X, pady=5)
        
        # Email
        email_frame = ttk.Frame(main_frame)
        email_frame.pack(fill=tk.X, pady=10)
        
        email_label = ttk.Label(email_frame, text="Email:")
        email_label.pack(anchor=tk.W)
        
        email_entry = ttk.Entry(email_frame, textvariable=self.email_var, width=40)
        email_entry.pack(fill=tk.X, pady=5)
        
        # Password
        password_frame = ttk.Frame(main_frame)
        password_frame.pack(fill=tk.X, pady=10)
        
        password_label = ttk.Label(password_frame, text="Mật khẩu:")
        password_label.pack(anchor=tk.W)
        
        password_entry = ttk.Entry(password_frame, textvariable=self.password_var, width=40, show="*")
        password_entry.pack(fill=tk.X, pady=5)
        
        # Confirm Password
        confirm_password_frame = ttk.Frame(main_frame)
        confirm_password_frame.pack(fill=tk.X, pady=10)
        
        confirm_password_label = ttk.Label(confirm_password_frame, text="Xác nhận mật khẩu:")
        confirm_password_label.pack(anchor=tk.W)
        
        confirm_password_entry = ttk.Entry(confirm_password_frame, textvariable=self.confirm_password_var, width=40, show="*")
        confirm_password_entry.pack(fill=tk.X, pady=5)
        
        # Password requirements
        password_req_label = ttk.Label(main_frame, text="Mật khẩu phải có ít nhất 8 ký tự, bao gồm chữ hoa, chữ thường, chữ số và ký tự đặc biệt", 
                                     font=('Arial', 10), foreground='#555555')
        password_req_label.pack(anchor=tk.W, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        register_button = ttk.Button(button_frame, text="Đăng ký", command=self.register)
        register_button.pack(side=tk.LEFT, padx=5)
        
        login_button = ttk.Button(button_frame, text="Quay lại đăng nhập", command=self.show_login_callback)
        login_button.pack(side=tk.RIGHT, padx=5)
    
    def register(self):
        fullname = self.fullname_var.get().strip()
        email = self.email_var.get().strip()
        password = self.password_var.get()
        confirm_password = self.confirm_password_var.get()
        
        # Validate full name
        is_valid_fullname, fullname_error = self.register_service.validate_fullname(fullname)
        if not is_valid_fullname:
            messagebox.showerror("Lỗi", fullname_error)
            return
        
        # Validate email
        is_valid_email, email_error = self.register_service.validate_email(email)
        if not is_valid_email:
            messagebox.showerror("Lỗi", email_error)
            return
        
        # Validate password
        is_valid_password, password_error = self.register_service.validate_password(password)
        if not is_valid_password:
            messagebox.showerror("Lỗi", password_error)
            return
        
        # Check if passwords match
        if password != confirm_password:
            messagebox.showerror("Lỗi", "Mật khẩu xác nhận không khớp")
            return
        
        # Register user
        success = self.register_service.register_user(fullname, email, password)
        if success:
            messagebox.showinfo("Thành công", "Đăng ký tài khoản thành công!")
            self.show_login_callback()
