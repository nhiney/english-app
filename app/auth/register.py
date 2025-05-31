import tkinter as tk
from tkinter import messagebox, ttk
from utils.hash_utils import hash_password
from utils.database import load_database, save_database
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


class RegisterWindow(BaseWindow):
    def __init__(self, root):
        super().__init__(root, "Register", WINDOW_SIZE['WIDTH'], WINDOW_SIZE['HEIGHT'])
        self.root = root
        self.root.title("Register")
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

        # Left panel with image
        self.left_frame = tk.Frame(root, width=(WINDOW_SIZE['WIDTH'] * 2 // 3), height=WINDOW_SIZE['HEIGHT'], bg='#e8f0fe')
        self.left_frame.pack(side="left", fill="both", expand=False)
        self.left_image = self.load_and_resize_image(image_path, int(WINDOW_SIZE['WIDTH'] * 2 / 3), WINDOW_SIZE['HEIGHT'])
        tk.Label(self.left_frame, image=self.left_image, bg='#e8f0fe').place(relx=0.5, rely=0.5, anchor="center")

        # Right panel with form
        self.right_frame = tk.Frame(root, bg="white")
        self.right_frame.pack(side="right", fill="both", expand=True, padx=40)

        self.role_var = tk.StringVar(value="user")
        self.create_register_form(base_path)

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

    def create_register_form(self, base_path):
        icon_path = os.path.join(base_path, "assets", "books.png")
        if os.path.exists(icon_path):
            icon_img = Image.open(icon_path).resize((64, 64), Image.LANCZOS)
            self.icon_photo = ImageTk.PhotoImage(icon_img)
            tk.Label(self.right_frame, image=self.icon_photo, bg="white").pack(pady=(40, 10))

        tk.Label(self.right_frame, text="Register Account", font=("Segoe UI", 26, "bold"), fg="#007bff", bg="white").pack(pady=(0, 10))

        tk.Label(self.right_frame, text="Start your English journey!", font=("Segoe UI", 14), fg="#666", bg="white").pack(pady=(0, 30))

        # Name
        self.entry_name = PlaceholderEntry(self.right_frame, placeholder="Full name", font=("Segoe UI", 12), width=30)
        self.entry_name.pack(pady=10, ipady=8)

        # Email
        self.entry_email = PlaceholderEntry(self.right_frame, placeholder="Email", font=("Segoe UI", 12), width=30)
        self.entry_email.pack(pady=10, ipady=8)

        # Password
        self.entry_password = PlaceholderEntry(self.right_frame, placeholder="Password", font=("Segoe UI", 12), width=30)
        self.entry_password.pack(pady=10, ipady=8)

        # Confirm password
        self.entry_confirm = PlaceholderEntry(self.right_frame, placeholder="Confirm password", font=("Segoe UI", 12), width=30)
        self.entry_confirm.pack(pady=10, ipady=8)

        # Role option
        role_frame = tk.Frame(self.right_frame, bg="white")
        role_frame.pack(pady=(10, 10))
        tk.Radiobutton(role_frame, text="User", variable=self.role_var, value="user", font=("Segoe UI", 11), bg="white").pack(side="left", padx=10)
        tk.Radiobutton(role_frame, text="Admin", variable=self.role_var, value="admin", font=("Segoe UI", 11), bg="white").pack(side="left", padx=10)

        # Register button
        self.btn_register = tk.Button(
            self.right_frame,
            text="📝 Register",
            command=self.register,
            font=("Segoe UI", 12, "bold"),
            bg="#28a745",
            fg="white",
            activebackground="#218838",
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2",
            width=26
        )
        self.btn_register.pack(pady=(20, 10), ipady=4)
        self.btn_register.bind("<Enter>", lambda e: self.btn_register.configure(bg="#218838"))
        self.btn_register.bind("<Leave>", lambda e: self.btn_register.configure(bg="#28a745"))

        # Back to login
        self.btn_login = tk.Button(
            self.right_frame,
            text="Already have an account? Login",
            command=self.open_login_window,
            font=("Segoe UI", 11, "underline"),
            bg="white",
            fg="#007bff",
            relief="flat",
            cursor="hand2"
        )
        self.btn_login.pack(pady=5)
        self.btn_login.bind("<Enter>", lambda e: self.btn_login.configure(fg="#0056b3"))
        self.btn_login.bind("<Leave>", lambda e: self.btn_login.configure(fg="#007bff"))

    def register(self):
        name = self.entry_name.get().strip()
        email = self.entry_email.get().strip()
        password = self.entry_password.get().strip()
        confirm = self.entry_confirm.get().strip()
        role = self.role_var.get()

        if not name or not email or not password or not confirm or \
           name == "Full name" or email == "Email" or password == "Password" or confirm == "Confirm password":
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        db = load_database()
        if any(user["email"] == email for user in db.get("users", [])):
            messagebox.showerror("Error", "Email already registered.")
            return

        db.setdefault("users", []).append({
            "name": name,
            "email": email,
            "password": hash_password(password),
            "role": role
        })

        save_database(db)
        messagebox.showinfo("Success", "Account registered successfully!")
        self.open_login_window()

    def open_login_window(self):
        self.root.destroy()
        from auth.login import LoginWindow
        root = tk.Tk()
        app = LoginWindow(root)
        root.mainloop()
