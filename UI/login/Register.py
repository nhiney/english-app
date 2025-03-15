import tkinter as tk
from tkinter import ttk, messagebox
import re
import json
import os

class VocabularyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("English Vocabulary Manager")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        
        # Set app style
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#F0F0F0')
        self.style.configure('TLabel', background='#F0F0F0', font=('Arial', 12))
        self.style.configure('TButton', font=('Arial', 12))
        self.style.configure('TEntry', font=('Arial', 12))
        
        # Initialize user data file
        self.users_file = "users.json"
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                json.dump([], f)
        
        # Show the registration form
        self.show_register_form()
    
    def show_register_form(self):
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
        
        self.fullname_var = tk.StringVar()
        fullname_entry = ttk.Entry(fullname_frame, textvariable=self.fullname_var, width=40)
        fullname_entry.pack(fill=tk.X, pady=5)
        
        # Email
        email_frame = ttk.Frame(main_frame)
        email_frame.pack(fill=tk.X, pady=10)
        
        email_label = ttk.Label(email_frame, text="Email:")
        email_label.pack(anchor=tk.W)
        
        self.email_var = tk.StringVar()
        email_entry = ttk.Entry(email_frame, textvariable=self.email_var, width=40)
        email_entry.pack(fill=tk.X, pady=5)
        
        # Password
        password_frame = ttk.Frame(main_frame)
        password_frame.pack(fill=tk.X, pady=10)
        
        password_label = ttk.Label(password_frame, text="Mật khẩu:")
        password_label.pack(anchor=tk.W)
        
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(password_frame, textvariable=self.password_var, width=40, show="*")
        password_entry.pack(fill=tk.X, pady=5)
        
        # Confirm Password
        confirm_password_frame = ttk.Frame(main_frame)
        confirm_password_frame.pack(fill=tk.X, pady=10)
        
        confirm_password_label = ttk.Label(confirm_password_frame, text="Xác nhận mật khẩu:")
        confirm_password_label.pack(anchor=tk.W)
        
        self.confirm_password_var = tk.StringVar()
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
        
        login_button = ttk.Button(button_frame, text="Quay lại đăng nhập", command=self.show_login_form)
        login_button.pack(side=tk.RIGHT, padx=5)
    
    def show_login_form(self):
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create main frame
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Đăng nhập", font=('Arial', 18, 'bold'))
        title_label.pack(pady=20)
        
        # Email
        email_frame = ttk.Frame(main_frame)
        email_frame.pack(fill=tk.X, pady=10)
        
        email_label = ttk.Label(email_frame, text="Email:")
        email_label.pack(anchor=tk.W)
        
        self.login_email_var = tk.StringVar()
        email_entry = ttk.Entry(email_frame, textvariable=self.login_email_var, width=40)
        email_entry.pack(fill=tk.X, pady=5)
        
        # Password
        password_frame = ttk.Frame(main_frame)
        password_frame.pack(fill=tk.X, pady=10)
        
        password_label = ttk.Label(password_frame, text="Mật khẩu:")
        password_label.pack(anchor=tk.W)
        
        self.login_password_var = tk.StringVar()
        password_entry = ttk.Entry(password_frame, textvariable=self.login_password_var, width=40, show="*")
        password_entry.pack(fill=tk.X, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        login_button = ttk.Button(button_frame, text="Đăng nhập", command=self.login)
        login_button.pack(side=tk.LEFT, padx=5)
        
        register_button = ttk.Button(button_frame, text="Đăng ký tài khoản", command=self.show_register_form)
        register_button.pack(side=tk.RIGHT, padx=5)
    
    def validate_fullname(self, fullname):
        # Check if fullname is valid (at least 2 characters, only letters and spaces)
        if len(fullname) < 2:
            return False, "Họ và tên phải có ít nhất 2 ký tự"
        
        if not re.match(r'^[a-zA-ZÀ-ỹ\s]+$', fullname):
            return False, "Họ và tên chỉ được chứa chữ cái và khoảng trắng"
        
        return True, ""
    
    def validate_email(self, email):
        # Check if email is valid
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return False, "Email không hợp lệ"
        
        # Check if email already exists
        with open(self.users_file, 'r') as f:
            users = json.load(f)
            
        for user in users:
            if user.get('email') == email:
                return False, "Email đã được sử dụng"
        
        return True, ""
    
    def validate_password(self, password):
        # Check if password is valid
        if len(password) < 8:
            return False, "Mật khẩu phải có ít nhất 8 ký tự"
        
        if not re.search(r'[A-Z]', password):
            return False, "Mật khẩu phải chứa ít nhất một chữ cái in hoa"
        
        if not re.search(r'[a-z]', password):
            return False, "Mật khẩu phải chứa ít nhất một chữ cái thường"
        
        if not re.search(r'[0-9]', password):
            return False, "Mật khẩu phải chứa ít nhất một chữ số"
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False, "Mật khẩu phải chứa ít nhất một ký tự đặc biệt"
        
        return True, ""
    
    def register(self):
        fullname = self.fullname_var.get().strip()
        email = self.email_var.get().strip()
        password = self.password_var.get()
        confirm_password = self.confirm_password_var.get()
        
        # Validate full name
        is_valid_fullname, fullname_error = self.validate_fullname(fullname)
        if not is_valid_fullname:
            messagebox.showerror("Lỗi", fullname_error)
            return
        
        # Validate email
        is_valid_email, email_error = self.validate_email(email)
        if not is_valid_email:
            messagebox.showerror("Lỗi", email_error)
            return
        
        # Validate password
        is_valid_password, password_error = self.validate_password(password)
        if not is_valid_password:
            messagebox.showerror("Lỗi", password_error)
            return
        
        # Check if passwords match
        if password != confirm_password:
            messagebox.showerror("Lỗi", "Mật khẩu xác nhận không khớp")
            return
        
        # Save user data
        with open(self.users_file, 'r') as f:
            users = json.load(f)
        
        # Add new user
        users.append({
            'fullname': fullname,
            'email': email,
            'password': password,  # Note: In a real app, you'd want to hash this
            'role': 'user'  # Default role
        })
        
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=4)
        
        messagebox.showinfo("Thành công", "Đăng ký tài khoản thành công!")
        self.show_login_form()
    
    def login(self):
        email = self.login_email_var.get().strip()
        password = self.login_password_var.get()
        
        # Load users
        with open(self.users_file, 'r') as f:
            users = json.load(f)
        
        # Find matching user
        for user in users:
            if user.get('email') == email and user.get('password') == password:
                messagebox.showinfo("Thành công", f"Chào mừng {user.get('fullname')}!")
                # Here you would navigate to the main app
                return
        
        messagebox.showerror("Lỗi", "Email hoặc mật khẩu không đúng")

if __name__ == "__main__":
    root = tk.Tk()
    app = VocabularyApp(root)
    root.mainloop()