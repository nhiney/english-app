import tkinter as tk
from tkinter import messagebox, ttk
from utils.hash_utils import hash_password
from utils.database import load_database
from common.configs import WINDOW_SIZE
from common.base_window import BaseWindow
from PIL import Image, ImageTk
import os
import sys


class PlaceholderEntry(ttk.Entry):
    def __init__(self, master=None, placeholder="", color='grey', **kwargs):
        super().__init__(master, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['foreground']
        self.bind("<FocusIn>", self._clear_placeholder)
        self.bind("<FocusOut>", self._add_placeholder)
        self._add_placeholder()

    def _clear_placeholder(self, e=None):
        if self.get() == self.placeholder:
            self.delete(0, tk.END)
            self.config(foreground=self.default_fg_color, show="•" if "password" in self.placeholder.lower() else "")

    def _add_placeholder(self, e=None):
        if not self.get():
            self.config(foreground=self.placeholder_color, show="")
            self.insert(0, self.placeholder)


class LoginWindow(BaseWindow):
    def __init__(self, root):
        super().__init__(root, "Login", WINDOW_SIZE['WIDTH'], WINDOW_SIZE['HEIGHT'])
        self.root = root
        self.root.title("Login")
        self.root.configure(bg='#fefefe')

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width / 2) - (WINDOW_SIZE['WIDTH'] / 2))
        y = int((screen_height / 2) - (WINDOW_SIZE['HEIGHT'] / 2))
        self.root.geometry(f"{WINDOW_SIZE['WIDTH']}x{WINDOW_SIZE['HEIGHT']}+{x}+{y}")

        if getattr(sys, 'frozen', False):
            base_path = os.path.join(sys._MEIPASS, 'app')
        else:
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        image_path = os.path.join(base_path, "assets", "auth3.png")
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found at: {image_path}")

        self.left_frame = tk.Frame(root, width=(WINDOW_SIZE['WIDTH'] * 2 // 3), height=WINDOW_SIZE['HEIGHT'], bg='#e8f0fe')
        self.left_frame.pack(side="left", fill="both", expand=False)
        self.left_image = self.load_and_resize_image(image_path, int(WINDOW_SIZE['WIDTH'] * 2 / 3), WINDOW_SIZE['HEIGHT'])
        tk.Label(self.left_frame, image=self.left_image, bg='#e8f0fe').place(relx=0.5, rely=0.5, anchor="center")

        self.right_frame = tk.Frame(root, bg="white")
        self.right_frame.pack(side="right", fill="both", expand=True, padx=40)

        self.is_admin_var = tk.BooleanVar(value=False)
        self.create_login_form(base_path)

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

    def create_login_form(self, base_path):
        icon_path = os.path.join(base_path, "assets", "books.png")
        if os.path.exists(icon_path):
            icon_img = Image.open(icon_path).resize((64, 64), Image.LANCZOS)
            self.icon_photo = ImageTk.PhotoImage(icon_img)
            tk.Label(self.right_frame, image=self.icon_photo, bg="white").pack(pady=(40, 10))

        tk.Label(
            self.right_frame,
            text="English Learning",
            font=("Segoe UI", 28, "bold"),
            fg="#007bff",
            bg="white"
        ).pack(pady=(0, 10))

        tk.Label(
            self.right_frame,
            text="Welcome back!",
            font=("Segoe UI", 14),
            fg="#666",
            bg="white"
        ).pack(pady=(0, 30))

        # Email entry
        self.entry_email = PlaceholderEntry(self.right_frame, placeholder="Email", font=("Segoe UI", 12), width=30)
        self.entry_email.pack(pady=10, ipady=8, anchor="center")

        # Password entry
        self.entry_password = PlaceholderEntry(self.right_frame, placeholder="Password", font=("Segoe UI", 12), width=30)
        self.entry_password.pack(pady=10, ipady=8, anchor="center")

        # Admin checkbox with alignment
        checkbox_frame = tk.Frame(self.right_frame, bg="white")
        checkbox_frame.pack(pady=(0, 10), anchor="center")

        self.admin_checkbox = tk.Checkbutton(
            checkbox_frame,
            text="Login as admin",
            variable=self.is_admin_var,
            font=("Segoe UI", 11),
            bg="white",
            fg="#333",
            selectcolor="white",
            padx=6
        )
        self.admin_checkbox.pack(ipadx=160, anchor="w")  # ipadx to match width with entry

        # Login button
        self.btn_login = tk.Button(
            self.right_frame,
            text="🔐 Login",
            command=self.login,
            font=("Segoe UI", 12, "bold"),
            bg="#007bff",
            fg="white",
            activebackground="#0056b3",
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2",
            width=26
        )
        self.btn_login.pack(pady=(20, 10), ipady=4)
        self.btn_login.bind("<Enter>", lambda e: self.btn_login.configure(bg="#0056b3"))
        self.btn_login.bind("<Leave>", lambda e: self.btn_login.configure(bg="#007bff"))

        # Register link
        self.btn_register = tk.Button(
            self.right_frame,
            text="Don't have an account? Sign up",
            command=self.open_register_window,
            font=("Segoe UI", 11, "underline"),
            bg="white",
            fg="#007bff",
            relief="flat",
            cursor="hand2"
        )
        self.btn_register.pack(pady=5)
        self.btn_register.bind("<Enter>", lambda e: self.btn_register.configure(fg="#0056b3"))
        self.btn_register.bind("<Leave>", lambda e: self.btn_register.configure(fg="#007bff"))

    def login(self):
        email = self.entry_email.get().strip()
        password = self.entry_password.get().strip()
        is_admin_login = self.is_admin_var.get()

        if not email or email == "Email" or not password or password == "Password":
            messagebox.showerror("Error", "Please enter both Email and Password!")
            return

        database = load_database()
        for user in database.get("users", []):
            if user["email"] == email and user["password"] == hash_password(password):
                role = user.get("role", "user")
                if is_admin_login and role != "admin":
                    messagebox.showerror("Access Denied", "This account is not an admin!")
                    return
                messagebox.showinfo("Welcome", f"Hello, {user.get('name', 'User')}!")
                self.root.destroy()
                new_root = tk.Tk()
                if role == "admin":
                    from home.dashboard_admin import DashboardAdminWindow
                    DashboardAdminWindow(new_root, user)
                else:
                    from home.dashboard import DashboardWindow
                    DashboardWindow(new_root, user)
                new_root.mainloop()
                return
        messagebox.showerror("Login Failed", "Invalid email or password!")

    def open_register_window(self):
        self.root.destroy()
        from auth.register import RegisterWindow
        root = tk.Tk()
        app = RegisterWindow(root)
        root.mainloop()
