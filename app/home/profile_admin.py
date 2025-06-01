import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from PIL import Image, ImageTk
import json
import os

DB_PATH = "data/database.json"

class ProfileAdminWindow(tk.Frame):
    def __init__(self, parent, user_data, on_update_callback=None):
        super().__init__(parent, bg="#f5f7fa")
        self.user_data = user_data
        self.on_update_callback = on_update_callback
        self.avatar_img = None
        self.avatar_path = self.user_data.get("avatar", None)
        self.build_ui()

    def build_ui(self):
        
        tk.Label(
            self,
            text="👤 THÔNG TIN QUẢN TRỊ VIÊN",
            font=("Helvetica", 18, "bold"),
            bg="#f5f7fa",
            fg="#202124"
        ).pack(anchor="w", pady=(20, 15), padx=30)

        content_frame = tk.Frame(self, bg="#f5f7fa")
        content_frame.pack(padx=30, pady=10, fill="x")

        
        avatar_frame = tk.Frame(content_frame, width=150, height=150, bg="#e1e8f7", bd=2, relief="groove")
        avatar_frame.pack(side="left", padx=(0, 30), pady=10)
        avatar_frame.pack_propagate(False)  

        self.avatar_label = tk.Label(avatar_frame, bg="#e1e8f7")
        self.avatar_label.pack(expand=True)

        
        self.load_avatar_image(self.avatar_path)

        
        tk.Button(
            avatar_frame,
            text="📷 Chọn ảnh đại diện",
            font=("Helvetica", 10),
            bg="#1a73e8",
            fg="white",
            relief="flat",
            command=self.choose_avatar
        ).pack(fill="x", pady=5)

        
        form_frame = tk.Frame(content_frame, bg="#f5f7fa")
        form_frame.pack(side="left", fill="x", expand=True)

        
        tk.Label(form_frame, text="Họ tên:", bg="#f5f7fa", font=("Helvetica", 12)).grid(row=0, column=0, sticky="e", pady=8, padx=(0, 10))
        self.name_entry = tk.Entry(form_frame, font=("Helvetica", 12), width=35)
        self.name_entry.grid(row=0, column=1, pady=8)
        self.name_entry.insert(0, self.user_data.get("name", ""))

        
        tk.Label(form_frame, text="Số điện thoại:", bg="#f5f7fa", font=("Helvetica", 12)).grid(row=1, column=0, sticky="e", pady=8, padx=(0, 10))
        self.phone_entry = tk.Entry(form_frame, font=("Helvetica", 12), width=35)
        self.phone_entry.grid(row=1, column=1, pady=8)
        self.phone_entry.insert(0, self.user_data.get("phone", ""))

        
        tk.Label(form_frame, text="Giới tính:", bg="#f5f7fa", font=("Helvetica", 12)).grid(row=2, column=0, sticky="e", pady=8, padx=(0, 10))
        self.gender_var = tk.StringVar(value=self.user_data.get("gender", "Khác"))
        gender_combobox = ttk.Combobox(form_frame, textvariable=self.gender_var, values=["Nam", "Nữ", "Khác"], font=("Helvetica", 12), state="readonly", width=33)
        gender_combobox.grid(row=2, column=1, pady=8)

        
        tk.Label(form_frame, text="Email:", bg="#f5f7fa", font=("Helvetica", 12)).grid(row=3, column=0, sticky="e", pady=8, padx=(0, 10))
        self.email_entry = tk.Entry(form_frame, font=("Helvetica", 12), width=35, state="disabled")
        self.email_entry.grid(row=3, column=1, pady=8)
        self.email_entry.insert(0, self.user_data.get("email", ""))

        
        tk.Button(
            self,
            text="💾 Cập nhật thông tin",
            font=("Helvetica", 12, "bold"),
            bg="#1a73e8",
            fg="white",
            padx=15,
            pady=8,
            relief="flat",
            command=self.update_info
        ).pack(pady=25)

    def load_avatar_image(self, path):
        
        if path and os.path.exists(path):
            try:
                img = Image.open(path)
                img = img.resize((140, 140), Image.LANCZOS)
                self.avatar_img = ImageTk.PhotoImage(img)
                self.avatar_label.config(image=self.avatar_img)
            except Exception:
                self.avatar_label.config(text="Ảnh không hợp lệ", fg="red", font=("Helvetica", 10))
        else:
            
            self.avatar_label.config(image="", text="Chưa có ảnh", fg="#666", font=("Helvetica", 12, "italic"))

    def choose_avatar(self):
        filetypes = [("Image files", "*.png *.jpg *.jpeg *.bmp *.gif"), ("All files", "*.*")]
        filepath = filedialog.askopenfilename(title="Chọn ảnh đại diện", filetypes=filetypes)
        if filepath:
            
            self.avatar_path = filepath
            self.load_avatar_image(self.avatar_path)

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
                user["avatar"] = self.avatar_path

                self.user_data["name"] = new_name
                self.user_data["phone"] = new_phone
                self.user_data["gender"] = new_gender
                self.user_data["avatar"] = self.avatar_path

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
