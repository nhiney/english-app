import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import os

DB_PATH = os.path.abspath("app/data/database.json")


class DashboardAdminWindow:
    def __init__(self, root, user_data):
        self.root = root
        self.user_data = user_data
        self.root.title("Admin Dashboard - English Vocabulary App")

        self.root.geometry("1100x650")
        self.root.configure(bg="#e3edf7")

        self.create_header()
        self.create_sidebar()
        self.create_main_content()

    def create_header(self):
        header = tk.Frame(self.root, bg="#1f3a93", height=60)
        header.pack(fill="x", side="top")

        tk.Label(header, text="📘 English Vocabulary - Admin Dashboard",
                 font=("Segoe UI", 18, "bold"), fg="white", bg="#1f3a93").pack(side="left", padx=25)

        tk.Label(header, text=f"Hello, {self.user_data.get('name', 'Admin')} 👋",
                 font=("Segoe UI", 12), fg="white", bg="#1f3a93").pack(side="right", padx=25)

    def create_sidebar(self):
        sidebar = tk.Frame(self.root, bg="white", width=230)
        sidebar.pack(fill="y", side="left")

        tk.Label(sidebar, text="ADMIN MENU", font=("Segoe UI", 14, "bold"),
                 bg="white", fg="#1f3a93").pack(pady=(20, 10))

        menu_items = [
            ("📊 Overview", self.show_dashboard_overview),
            ("👤 Admin Profile", self.show_admin_profile),
            ("👥 User Management", self.show_account_management),
            ("📚 Vocabulary", self.show_vocabulary_management),
            ("📈 Statistics", self.view_stats),
            ("🚪 Log Out", self.logout)
        ]

        for text, command in menu_items:
            btn = tk.Button(
                sidebar, text=text, font=("Segoe UI", 12),
                bg="#f5f6fa", fg="#2c3e50", relief="flat", anchor="w",
                padx=25, pady=10, width=20, cursor="hand2", command=command,
                activebackground="#d6e0f0", activeforeground="#000"
            )
            btn.pack(pady=5)

    def create_main_content(self):
        self.content_frame = tk.Frame(self.root, bg="#e3edf7")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.show_dashboard_overview()

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_dashboard_overview(self):
        self.clear_content()
        tk.Label(
            self.content_frame,
            text="📊 SYSTEM OVERVIEW",
            font=("Segoe UI", 20, "bold"),
            bg="#e3edf7",
            fg="#2c3e50"
        ).pack(anchor="w", pady=(0, 20), padx=10)

        stats = [
            ("👥", "Total Users", self.count_users(), "#27ae60"),
            ("📚", "Vocabulary Entries", self.count_vocab(), "#e67e22"),
            ("🛡️", "Admin Accounts", self.count_admins(), "#c0392b"),
        ]

        card_container = tk.Frame(self.content_frame, bg="#e3edf7")
        card_container.pack(padx=10, pady=10, fill="x")

        
        for col in range(len(stats)):
            card_container.columnconfigure(col, weight=1)

        for i, (icon, title, value, color) in enumerate(stats):
            
            card = tk.Frame(
                card_container,
                bg="white",
                width=300,
                height=150,
                bd=0,
                highlightthickness=2,
                highlightbackground=color
            )
            card.grid(row=0, column=i, padx=15, pady=15, sticky="nsew")
            card.grid_propagate(False)

            icon_label = tk.Label(
                card, text=icon, font=("Segoe UI Emoji", 36),
                bg="white", fg=color
            )
            icon_label.pack(pady=(15, 5))

            tk.Label(
                card, text=title,
                font=("Segoe UI", 13, "bold"),
                bg="white", fg="#2c3e50"
            ).pack()

            tk.Label(
                card, text=str(value),
                font=("Segoe UI", 26, "bold"),
                bg="white", fg=color
            ).pack(pady=(5, 0))


    def show_admin_profile(self):
        self.clear_content()
        try:
            from .profile_admin import ProfileAdminWindow
            profile_ui = ProfileAdminWindow(self.content_frame, self.user_data, None)
            profile_ui.pack(fill="both", expand=True)
        except Exception as e:
            tk.Label(self.content_frame, text="Failed to load Admin Profile.",
                     font=("Segoe UI", 14), fg="red", bg="#e3edf7").pack(pady=20)
            print("Error loading profile_admin:", e)

    def show_account_management(self):
        self.clear_content()
        from .account_management import AccountManagement
        account_ui = AccountManagement(self.content_frame)
        account_ui.pack(fill="both", expand=True)

    def show_vocabulary_management(self):
        self.clear_content()
        try:
            from .vocabulary_management import VocabularyManagement
            vocab_ui = VocabularyManagement(self.content_frame, self.user_data)
            vocab_ui.pack(fill="both", expand=True)
        except Exception as e:
            tk.Label(self.content_frame, text="Failed to load Vocabulary Management.",
                     font=("Segoe UI", 14), fg="red", bg="#e3edf7").pack(pady=20)
            print("Error loading vocabulary_management:", e)

    def view_stats(self):
        self.clear_content()
        tk.Label(
            self.content_frame,
            text="📈 SYSTEM STATISTICS",
            font=("Segoe UI", 20, "bold"),
            bg="#e3edf7",
            fg="#2c3e50"
        ).pack(anchor="w", pady=(0, 20), padx=10)

        stats = [
            ("👥", "Total Users", self.count_users(), "#27ae60"),
            ("📚", "Vocabulary Entries", self.count_vocab(), "#e67e22"),
            ("🛡️", "Admin Accounts", self.count_admins(), "#c0392b"),
        ]

        for icon, title, value, color in stats:
            stat_card = tk.Frame(
                self.content_frame,
                bg="white",
                height=100,
                bd=0,
                highlightthickness=2,
                highlightbackground=color
            )
            stat_card.pack(fill="x", padx=15, pady=10)

            stat_card.columnconfigure(1, weight=1)

            icon_label = tk.Label(
                stat_card,
                text=icon,
                font=("Segoe UI Emoji", 24),
                bg="white",
                fg=color,
                width=4,
                height=2
            )
            icon_label.grid(row=0, column=0, padx=(10, 15), pady=10)

            info_frame = tk.Frame(stat_card, bg="white")
            info_frame.grid(row=0, column=1, sticky="w")

            tk.Label(
                info_frame,
                text=title,
                font=("Segoe UI", 14, "bold"),
                bg="white",
                fg="#2c3e50"
            ).pack(anchor="w")

            tk.Label(
                info_frame,
                text=str(value),
                font=("Segoe UI", 18, "bold"),
                bg="white",
                fg=color
            ).pack(anchor="w")

    def logout(self):
        confirm = messagebox.askyesno("Confirm Logout", "Are you sure you want to log out?")
        if confirm:
            self.root.destroy()
            from auth.login import LoginWindow
            root = tk.Tk()
            LoginWindow(root)
            root.mainloop()

    def load_data(self):
        if not os.path.exists(DB_PATH):
            return {"users": [], "vocab": []}
        with open(DB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_data(self, data):
        with open(DB_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def count_users(self):
        data = self.load_data()
        return len(data.get("users", []))

    def count_admins(self):
        data = self.load_data()
        return sum(1 for u in data.get("users", []) if u.get("role") == "Admin")

    def count_vocab(self):
        data = self.load_data()
        return len(data.get("vocab", []))
