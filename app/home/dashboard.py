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

        # Center the window
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = int((screen_width / 2) - (WINDOW_SIZE['WIDTH'] / 2))
        y = int((screen_height / 2) - (WINDOW_SIZE['HEIGHT'] / 2))
        root.geometry(f"{WINDOW_SIZE['WIDTH']}x{WINDOW_SIZE['HEIGHT']}+{x}+{y}")
        root.configure(bg="#F0F8FF")
        root.resizable(False, False)

        # Sidebar
        self.sidebar = tk.Frame(root, bg="#1E40AF", width=260)
        self.sidebar.pack(side="left", fill="y")

        self.main_content = tk.Frame(root, bg="#F0F8FF", highlightbackground="#CBD5E1", highlightthickness=2)
        self.main_content.pack(side="right", fill="both", expand=True)

        # Sidebar Header
        tk.Label(
            self.sidebar,
            text=f"👤 {user.get('name', 'User')}",
            bg="#1E40AF", fg="white",
            font=("Helvetica", 16, "bold")
        ).pack(pady=(30, 20))

        # Sidebar menu
        self.menu_items = [
            ("🏠 Dashboard", self.show_dashboard),
            ("📚 Vocabulary", self.show_vocabulary_management),
            ("👤 Profile", self.show_profile),
            ("🛠️ Manage Users", self.show_user_management) if user.get("role") == "admin" else None,
            ("🚪 Log out", self.logout),
        ]

        for item in self.menu_items:
            if item:
                btn = tk.Button(
                    self.sidebar, text=item[0],
                    fg="white", bg="#1E40AF",
                    font=("Helvetica", 13, "bold"), anchor="w",
                    relief="flat", padx=30, bd=0,
                    activebackground="#3B82F6",
                    activeforeground="white",
                    command=item[1],
                    cursor="hand2"
                )
                btn.pack(fill="x", pady=6, padx=10, ipady=6)

        self.show_dashboard()

    def clear_main_frame(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.clear_main_frame()

        tk.Label(
            self.main_content, text="📊 Learning Overview",
            font=("Helvetica", 22, "bold"), bg="#F0F8FF", fg="#1E3A8A"
        ).pack(pady=(30, 10))

        tk.Label(
            self.main_content, text=f"Welcome back, {self.user.get('name', '')} 👋",
            font=("Helvetica", 14), bg="#F0F8FF", fg="#1E3A8A"
        ).pack()

        stats_frame = tk.Frame(self.main_content, bg="#F0F8FF")
        stats_frame.pack(pady=30)

        self.create_stat_box(stats_frame, "📝 Words Learned", 48, "#DBEAFE")
        self.create_stat_box(stats_frame, "🎯 Today's Goal", "12 / 20", "#BFDBFE")
        self.create_stat_box(stats_frame, "📅 Streak Days", 5, "#93C5FD")
        self.create_stat_box(stats_frame, "⏱️ Study Time", "25 mins", "#60A5FA")

    def create_stat_box(self, parent, label, value, color):
        box = tk.Frame(
            parent,
            bg=color,
            bd=2,
            highlightbackground="white",
            highlightthickness=2,
            relief="raised"
        )
        box.pack(side="left", padx=15, ipadx=30, ipady=25)

        tk.Label(box, text=label, bg=color, font=("Helvetica", 12, "bold"), fg="#1E3A8A").pack(pady=(0, 10))
        tk.Label(box, text=str(value), bg=color, font=("Helvetica", 20, "bold"), fg="#1E3A8A").pack()

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

    def open_edit_profile_window(self):
        top = tk.Toplevel(self.root)
        top.title("Edit Profile")
        top.geometry("400x300")
        top.configure(bg="white")
        top.grab_set()

        tk.Label(top, text="Edit Profile", font=("Helvetica", 16, "bold"), bg="white", fg="#1E3A8A").pack(pady=10)

        tk.Label(top, text="Full Name:", bg="white").pack(anchor="w", padx=20)
        name_entry = tk.Entry(top)
        name_entry.insert(0, self.user.get("name", ""))
        name_entry.pack(padx=20, fill="x")

        tk.Label(top, text="Email:", bg="white").pack(anchor="w", padx=20, pady=(10, 0))
        email_entry = tk.Entry(top)
        email_entry.insert(0, self.user.get("email", ""))
        email_entry.pack(padx=20, fill="x")

        def save_changes():
            new_name = name_entry.get().strip()
            new_email = email_entry.get().strip()
            if new_name and new_email:
                self.user["name"] = new_name
                self.user["email"] = new_email
                top.destroy()
                self.show_dashboard()
            else:
                messagebox.showwarning("Warning", "Please fill in all fields.")

        tk.Button(top, text="Save", command=save_changes, bg="#1E40AF", fg="white",
                  font=("Helvetica", 12), padx=10).pack(pady=20)
