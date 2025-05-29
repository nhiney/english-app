import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

# Đường dẫn đến file dữ liệu
DB_PATH = "data/database.json"

class ProfileAdminWindow(tk.Frame):
    def __init__(self, parent, user_data, on_update_callback=None):
        super().__init__(parent, bg="#f5f7fa")
        self.user_data = user_data
        self.on_update_callback = on_update_callback
        self.build_ui()

    def build_ui(self):
        tk.Label(
            self,
            text="👤 THÔNG TIN QUẢN TRỊ VIÊN",
            font=("Helvetica", 16, "bold"),
            bg="#f5f7fa",
            fg="#202124"
        ).pack(anchor="w", pady=(20, 10), padx=30)

        form_frame = tk.Frame(self, bg="#f5f7fa")
        form_frame.pack(anchor="w", padx=30, pady=10)

        # Họ tên
        tk.Label(form_frame, text="Họ tên:", bg="#f5f7fa", font=("Helvetica", 12)).grid(row=0, column=0, sticky="e", pady=5, padx=(0, 10))
        self.name_entry = tk.Entry(form_frame, font=("Helvetica", 12), width=30)
        self.name_entry.grid(row=0, column=1, pady=5)
        self.name_entry.insert(0, self.user_data.get("name", ""))

        # Số điện thoại
        tk.Label(form_frame, text="Số điện thoại:", bg="#f5f7fa", font=("Helvetica", 12)).grid(row=1, column=0, sticky="e", pady=5, padx=(0, 10))
        self.phone_entry = tk.Entry(form_frame, font=("Helvetica", 12), width=30)
        self.phone_entry.grid(row=1, column=1, pady=5)
        self.phone_entry.insert(0, self.user_data.get("phone", ""))

        # Giới tính
        tk.Label(form_frame, text="Giới tính:", bg="#f5f7fa", font=("Helvetica", 12)).grid(row=2, column=0, sticky="e", pady=5, padx=(0, 10))
        self.gender_var = tk.StringVar(value=self.user_data.get("gender", "Khác"))
        gender_combobox = ttk.Combobox(form_frame, textvariable=self.gender_var, values=["Nam", "Nữ", "Khác"], font=("Helvetica", 12), state="readonly", width=28)
        gender_combobox.grid(row=2, column=1, pady=5)

        # Email (không cho chỉnh sửa)
        tk.Label(form_frame, text="Email:", bg="#f5f7fa", font=("Helvetica", 12)).grid(row=3, column=0, sticky="e", pady=5, padx=(0, 10))
        self.email_entry = tk.Entry(form_frame, font=("Helvetica", 12), width=30, state="disabled")
        self.email_entry.grid(row=3, column=1, pady=5)
        self.email_entry.insert(0, self.user_data.get("email", ""))

        # Nút cập nhật
        tk.Button(
            self,
            text="💾 Cập nhật thông tin",
            font=("Helvetica", 12, "bold"),
            bg="#1a73e8",
            fg="white",
            padx=10,
            pady=5,
            command=self.update_info
        ).pack(pady=20)

    def update_info(self):
        new_name = self.name_entry.get().strip()
        new_phone = self.phone_entry.get().strip()
        new_gender = self.gender_var.get()

        if not new_name:
            messagebox.showwarning("Lỗi", "Họ tên không được để trống.")
            return

        data = self.load_data()
        updated = False

        for user in data.get("users", []):
            if user.get("email") == self.user_data.get("email"):
                user["name"] = new_name
                user["phone"] = new_phone
                user["gender"] = new_gender

                self.user_data["name"] = new_name
                self.user_data["phone"] = new_phone
                self.user_data["gender"] = new_gender

                updated = True
                break

        if updated:
            self.save_data(data)
            messagebox.showinfo("Thành công", "Cập nhật thông tin thành công.")
            if self.on_update_callback:
                self.on_update_callback()
        else:
            messagebox.showerror("Lỗi", "Không tìm thấy người dùng trong dữ liệu.")

    def load_data(self):
        if not os.path.exists(DB_PATH):
            return {"users": [], "vocab": []}
        try:
            with open(DB_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"users": [], "vocab": []}

    def save_data(self, data):
        with open(DB_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
