# profile_user.py
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


class Profile(tk.Frame):
    def __init__(self, parent, user):
        super().__init__(parent, bg="white")
        self.user = user

        tk.Label(self, text="👤 Hồ sơ cá nhân", font=("Helvetica", 18, "bold"), bg="white").pack(pady=20)

        container = tk.Frame(self, bg="white", padx=20, pady=20, bd=1, relief="solid")
        container.pack(pady=10)

        try:
            img = Image.open("assets/avatar.png")
        except FileNotFoundError:
            img = Image.new("RGB", (100, 100), color="gray")

        img = img.resize((100, 100))
        self.avatar = ImageTk.PhotoImage(img)
        tk.Label(container, image=self.avatar, bg="white").grid(row=0, column=0, rowspan=4, padx=10, pady=10)

        # Gán các giá trị từ user
        name = user.get("name", "Người dùng")
        email = user.get("email", "email@example.com")
        join_date = user.get("join_date", "01/01/2024")

        self.username_label = tk.Label(container, text=f"Tên: {name}", bg="white", font=("Arial", 12))
        self.username_label.grid(row=0, column=1, sticky="w", padx=10, pady=5)

        self.email_label = tk.Label(container, text=f"Email: {email}", bg="white", font=("Arial", 12))
        self.email_label.grid(row=1, column=1, sticky="w", padx=10, pady=5)

        self.password_label = tk.Label(container, text="Mật khẩu: ********", bg="white", font=("Arial", 12))
        self.password_label.grid(row=2, column=1, sticky="w", padx=10, pady=5)

        self.join_date_label = tk.Label(container, text=f"Ngày tham gia: {join_date}", bg="white", font=("Arial", 12))
        self.join_date_label.grid(row=3, column=1, sticky="w", padx=10, pady=5)

        tk.Button(self, text="✏️ Chỉnh sửa hồ sơ", command=self.edit_profile,
                  bg="#4CAF50", fg="white", font=("Arial", 11, "bold"), padx=10, pady=5,
                  relief="flat").pack(pady=20)

    def edit_profile(self):
        EditProfileDialog(self, "Chỉnh sửa hồ sơ")


class EditProfileDialog(tk.Toplevel):
    def __init__(self, parent, title):
        super().__init__(parent)
        self.title(title)
        self.geometry("350x300")
        self.configure(bg="white")
        self.resizable(False, False)
        self.parent = parent

        tk.Label(self, text=title, font=("Helvetica", 14, "bold"), bg="white").pack(pady=10)

        form_frame = tk.Frame(self, bg="white")
        form_frame.pack(pady=5, padx=20)

        current_name = self.parent.user.get("name", "")
        current_email = self.parent.user.get("email", "")

        tk.Label(form_frame, text="Tên:", font=("Arial", 12), bg="white").grid(row=0, column=0, sticky="w", pady=5)
        self.name_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
        self.name_entry.insert(0, current_name)
        self.name_entry.grid(row=0, column=1, pady=5)

        tk.Label(form_frame, text="Email:", font=("Arial", 12), bg="white").grid(row=1, column=0, sticky="w", pady=5)
        self.email_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
        self.email_entry.insert(0, current_email)
        self.email_entry.grid(row=1, column=1, pady=5)

        tk.Label(form_frame, text="Mật khẩu:", font=("Arial", 12), bg="white").grid(row=2, column=0, sticky="w", pady=5)
        self.password_entry = tk.Entry(form_frame, font=("Arial", 12), show="*", width=30)
        self.password_entry.insert(0, "password123")
        self.password_entry.grid(row=2, column=1, pady=5)

        tk.Button(self, text="💾 Lưu thay đổi", command=self.save_profile,
                  bg="#2196F3", fg="white", font=("Arial", 11, "bold"), padx=10, pady=5,
                  relief="flat").pack(pady=15)

    def save_profile(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not name or not email or not password:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng điền đầy đủ thông tin.")
            return

        messagebox.showinfo("Thành công", "Thông tin đã được cập nhật.")

        self.parent.user['name'] = name
        self.parent.user['email'] = email

        self.parent.username_label.config(text=f"Tên: {name}")
        self.parent.email_label.config(text=f"Email: {email}")
        self.parent.password_label.config(text="Mật khẩu: ********")

        self.destroy()
