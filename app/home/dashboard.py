import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

from home.vocabulary_management import VocabularyManagement
from common.configs import WINDOW_SIZE

class DashboardWindow:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.root.title("English Learning Dashboard")

       
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = int((screen_width / 2) - (WINDOW_SIZE['WIDTH'] / 2))
        y = int((screen_height / 2) - (WINDOW_SIZE['HEIGHT'] / 2))
        root.geometry(f"{WINDOW_SIZE['WIDTH']}x{WINDOW_SIZE['HEIGHT']}+{x}+{y}")
        root.configure(bg="#F0F9FF")
        root.resizable(False, False)

        
        self.sidebar = tk.Frame(root, bg="#1E3A8A", width=240)
        self.sidebar.pack(side="left", fill="y")

        
        self.main_content = tk.Frame(root, bg="#F8FAFC")
        self.main_content.pack(side="right", fill="both", expand=True)

        
        tk.Label(
            self.sidebar,
            text=f"👤 {user.get('name', 'User')}",
            bg="#1E3A8A", fg="white",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=(30, 20))

        
        self.menu_items = [
            ("🏠 Dashboard", self.show_dashboard),
            ("📚 Vocabulary", self.show_vocabulary_management),
            ("👤 Profile", self.show_profile),
            ("🛠️ Manage Users", self.show_user_management) if user.get("role") == "admin" else None,
            ("🚪 Log out", self.logout),
        ]

        for item in self.menu_items:
            if item:
                btn = tk.Label(
                    self.sidebar, text=item[0], bg="#1E3A8A", fg="white",
                    font=("Segoe UI", 13), anchor="w",
                    padx=20, pady=12, cursor="hand2"
                )
                btn.pack(fill="x", padx=10, pady=4)
                btn.bind("<Button-1>", lambda e, func=item[1]: func())
                btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#374EA2"))
                btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#1E3A8A"))

        self.show_dashboard()

    def clear_main_frame(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.clear_main_frame()

        
        tk.Label(
            self.main_content, text="📊 Learning Overview",
            font=("Segoe UI", 22, "bold"), bg="#F8FAFC", fg="#1D4ED8"
        ).pack(pady=(10, 10))

        tk.Label(
            self.main_content, text=f"Welcome back, {self.user.get('name', '')} 👋",
            font=("Segoe UI", 14), bg="#F8FAFC", fg="#475569"
        ).pack()

        
        stats_frame = tk.Frame(self.main_content, bg="#F8FAFC")
        stats_frame.pack(pady=30)

        self.create_stat_box(stats_frame, "📝 Words Learned", 48, "#E0F2FE", 0, 0)
        self.create_stat_box(stats_frame, "🎯 Today's Goal", "12 / 20", "#DBEAFE", 0, 1)
        self.create_stat_box(stats_frame, "📅 Streak Days", 5, "#D1FAE5", 1, 0)
        self.create_stat_box(stats_frame, "⏱️ Study Time", "25 mins", "#FDE68A", 1, 1)

    def create_stat_box(self, parent, label, value, color, row, column):
        box = tk.Frame(parent, bg=color, bd=0, highlightbackground="#94A3B8", highlightthickness=1)
        box.grid(row=row, column=column, padx=20, pady=15, ipadx=30, ipady=25, sticky="nsew")

        box.bind("<Enter>", lambda e, b=box: b.config(bg="#C7D2FE"))
        box.bind("<Leave>", lambda e, b=box: b.config(bg=color))
        box.bind("<Button-1>", lambda e, l=label: self.show_detail_popup(l))

        tk.Label(box, text=label, bg=color, font=("Segoe UI", 12, "bold"), fg="#1E293B").pack(pady=(0, 10))
        tk.Label(box, text=str(value), bg=color, font=("Segoe UI", 20, "bold"), fg="#0F172A").pack()

        for child in box.winfo_children():
            child.bind("<Button-1>", lambda e, l=label: self.show_detail_popup(l))

    def show_detail_popup(self, label):
        detail = {
            "📝 Words Learned": "You have learned 48 words in total.\nKeep it up!",
            "🎯 Today's Goal": "Your goal is 20 words today.\nYou've learned 12 so far.",
            "📅 Streak Days": "You have a learning streak of 5 consecutive days!",
            "⏱️ Study Time": "Total study time today: 25 minutes.\nTry to reach 30 minutes!"
        }

        top = tk.Toplevel(self.root)
        top.title(label)
        top.geometry("400x220")
        top.configure(bg="#F9FAFB")
        top.grab_set()

        tk.Label(top, text=label, font=("Segoe UI", 16, "bold"), bg="#F9FAFB", fg="#1E3A8A").pack(pady=12)
        tk.Label(top, text=detail.get(label, "No additional information."),
                 bg="#F9FAFB", font=("Segoe UI", 12), wraplength=350, justify="left").pack(pady=10, padx=20)

        tk.Button(top, text="Close", command=top.destroy,
                  bg="#1E3A8A", fg="white", font=("Segoe UI", 11, "bold"),
                  padx=10, pady=3, relief="flat", activebackground="#3B82F6").pack(pady=10)

    def show_vocabulary_management(self):
        self.clear_main_frame()
        vocab_ui = VocabularyManagement(self.main_content, self.user)
        vocab_ui.pack(fill="both", expand=True)

    def show_user_management(self):
        self.clear_main_frame()
        from home.user_management import UserManagement
        user_mgmt = UserManagement(self.main_content)
        user_mgmt.pack(fill="both", expand=True)

    def show_profile(self):
        self.clear_main_frame()
        from home.profile_user import Profile
        profile = Profile(self.main_content, self.user)
        profile.pack(fill="both", expand=True)

    def logout(self):
        confirm = messagebox.askyesno("Confirmation", "Are you sure you want to log out?")
        if confirm:
            from auth.login import LoginWindow
            self.root.destroy()
            new_root = tk.Tk()
            LoginWindow(new_root)
            new_root.mainloop()
