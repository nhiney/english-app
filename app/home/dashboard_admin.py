import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import json
import os

DB_PATH = "data/database.json"

class DashboardAdminWindow:
    def __init__(self, root, user_data):
        self.root = root
        self.user_data = user_data
        self.root.title("Admin Dashboard - English Vocabulary App")
        self.root.geometry("1000x600")
        self.root.configure(bg="#f5f7fa")

        self.create_header()
        self.create_sidebar()
        self.create_main_content()  # ✅ Tạo content_frame ở đây

    # --------------------- Header ---------------------
    def create_header(self):
        header = tk.Frame(self.root, bg="#1a73e8", height=60)
        header.pack(fill="x", side="top")

        tk.Label(header, text="English Vocabulary - Admin", font=("Helvetica", 18, "bold"),
                 fg="white", bg="#1a73e8").pack(side="left", padx=20)

        tk.Label(header, text=f"Xin chào, {self.user_data.get('name', 'Admin')}",
                 font=("Helvetica", 12), fg="white", bg="#1a73e8").pack(side="right", padx=20)

    # --------------------- Sidebar ---------------------
    def create_sidebar(self):
        sidebar = tk.Frame(self.root, bg="#ffffff", width=220)
        sidebar.pack(fill="y", side="left")

        tk.Label(sidebar, text="QUẢN TRỊ", font=("Helvetica", 14, "bold"), bg="white", fg="#1a73e8").pack(pady=20)

        menu_items = [
            ("📊 Tổng quan", self.show_dashboard_overview),
            ("👤 Hồ sơ Admin", self.show_admin_profile),
            ("👤 Quản lý người dùng", self.show_account_management),
            ("📘 Quản lý từ vựng", self.show_vocabulary_management),
            ("📈 Thống kê hệ thống", self.view_stats),
            ("🔓 Đăng xuất", self.logout)
        ]

        for text, command in menu_items:
            btn = tk.Button(
                sidebar, text=text, font=("Helvetica", 12),
                bg="#f1f3f4", fg="#202124", relief="flat", anchor="w",
                padx=20, pady=10, width=20, cursor="hand2", command=command
            )
            btn.pack(pady=5)

    # --------------------- Main Content ---------------------
    def create_main_content(self):
        self.content_frame = tk.Frame(self.root, bg="#f5f7fa")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.show_dashboard_overview()

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_dashboard_overview(self):
        self.clear_content()

        tk.Label(
            self.content_frame,
            text="📊 TỔNG QUAN HỆ THỐNG",
            font=("Helvetica", 18, "bold"),
            bg="#f5f7fa",
            fg="#202124"
        ).pack(anchor="w", pady=(0, 20), padx=10)

        stats = [
            ("👥 Tổng số người dùng", self.count_users(), "#34a853"),
            ("📘 Từ vựng đã thêm", self.count_vocab(), "#fbbc05"),
            ("🛡️ Tài khoản Admin", self.count_admins(), "#ea4335"),
        ]

        card_container = tk.Frame(self.content_frame, bg="#f5f7fa")
        card_container.pack(fill="x", padx=10, pady=10)

        for title, value, color in stats:
            card = tk.Frame(
                card_container,
                bg="white",
                width=260,
                height=120,
                highlightbackground="#dadce0",
                highlightthickness=1
            )
            card.pack_propagate(False)
            card.pack(side="left", padx=15)

            tk.Label(card, text=title, font=("Helvetica", 13, "bold"), bg="white", fg="#202124").pack(pady=(15, 5))
            tk.Label(card, text=str(value), font=("Helvetica", 24, "bold"), bg="white", fg=color).pack()

    # --------------------- Admin Profile ---------------------
    def show_admin_profile(self):
        self.clear_content()
        from .profile_admin import ProfileAdminWindow
        profile_ui = ProfileAdminWindow(self.content_frame, self.user_data, None)
        profile_ui.pack(fill="both", expand=True)

    # --------------------- User Management ---------------------
    def show_account_management(self):
        self.clear_content()
        from .account_management import AccountManagement
        account_ui = AccountManagement(self.content_frame)
        account_ui.pack(fill="both", expand=True)

    # --------------------- Vocab Management ---------------------
    def show_vocabulary_management(self):
        self.clear_content()
        from .vocabulary_management import VocabularyManagement
        vocab_ui = VocabularyManagement(self.content_frame, self.user_data)
        vocab_ui.pack(fill="both", expand=True)

    # --------------------- Stats View ---------------------
    def view_stats(self):
        self.clear_content()
        tk.Label(self.content_frame, text="📈 THỐNG KÊ HỆ THỐNG", font=("Helvetica", 16, "bold"),
                 bg="#f5f7fa", fg="#202124").pack(anchor="w", pady=10)

        stats_texts = [
            f"- Tổng số người dùng: {self.count_users()}",
            f"- Tổng từ vựng: {self.count_vocab()}",
            f"- Tài khoản admin: {self.count_admins()}",
        ]

        for text in stats_texts:
            tk.Label(self.content_frame, text=text, font=("Helvetica", 12), bg="#f5f7fa").pack(anchor="w", pady=2)

    # --------------------- Logout ---------------------
    def logout(self):
        confirm = messagebox.askyesno("Xác nhận đăng xuất", "Bạn có chắc chắn muốn đăng xuất?")
        if confirm:
            self.root.destroy()
            from auth.login import LoginWindow
            root = tk.Tk()
            LoginWindow(root)
            root.mainloop()

    # --------------------- Load & Save JSON ---------------------
    def load_data(self):
        if not os.path.exists(DB_PATH):
            return {"users": [], "vocab": []}
        with open(DB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_data(self, data):
        with open(DB_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    # --------------------- Count Functions ---------------------
    def count_users(self):
        data = self.load_data()
        return len(data.get("users", []))

    def count_vocab(self):
        data = self.load_data()
        return len(data.get("vocab", []))

    def count_admins(self):
        data = self.load_data()
        return len([u for u in data.get("users", []) if u.get("role") == "admin"])
