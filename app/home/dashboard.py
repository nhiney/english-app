import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

from home.vocabulary_management import VocabularyManagement
from common.colors import COLORS
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
        root.configure(bg="#fefefe")
        root.resizable(False, False)

        # Sidebar
        self.sidebar = tk.Frame(root, bg="#4DA8DA", width=250)
        self.sidebar.pack(side="left", fill="y")

        self.main_content = tk.Frame(root, bg="#fefefe")
        self.main_content.pack(side="right", fill="both", expand=True)

        # Sidebar header
        tk.Label(
            self.sidebar,
            text=f"👤 {user.get('name', 'Người dùng')}",
            bg="#4DA8DA", fg="white",
            font=("Helvetica", 16, "bold")
        ).pack(pady=(30, 20))

        self.menu_items = [
            ("🏠 Trang chủ", self.show_dashboard),
            ("📚 Từ vựng", self.show_vocabulary_management),
            ("👤 Hồ sơ", self.show_profile),
            ("⚙️ Quản lý tài khoản", self.show_user_management) if user.get("role") == "admin" else None,
            ("🚪 Đăng xuất", self.logout),
        ]

        for item in self.menu_items:
            if item:
                btn = tk.Button(
                    self.sidebar, text=item[0],
                    fg="white", bg="#4DA8DA",
                    font=("Helvetica", 13), anchor="w",
                    relief="flat", padx=30,
                    activebackground="#A0D2EB",
                    activeforeground="white",
                    command=item[1],
                    cursor="hand2"
                )
                btn.pack(fill="x", pady=5)

        self.show_dashboard()

    def clear_main_frame(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.clear_main_frame()

        tk.Label(
            self.main_content, text="📊 Tổng quan học tập",
            font=("Helvetica", 22, "bold"), bg="#fefefe", fg="#4DA8DA"
        ).pack(pady=(30, 10))

        tk.Label(
            self.main_content, text=f"Chào mừng trở lại, {self.user.get('name', '')} 👋",
            font=("Helvetica", 14), bg="#fefefe", fg="gray"
        ).pack()

        stats_frame = tk.Frame(self.main_content, bg="#fefefe")
        stats_frame.pack(pady=20)

        self.create_stat_box(stats_frame, "📝 Từ vựng đã học", 48)
        self.create_stat_box(stats_frame, "🎯 Mục tiêu hôm nay", "12 / 20")
        self.create_stat_box(stats_frame, "📅 Chuỗi ngày học", 5)
        self.create_stat_box(stats_frame, "⏱️ Thời gian hôm nay", "25 phút")

        # Đã bỏ phần create_profile_preview()

    def create_stat_box(self, parent, label, value):
        box = tk.Frame(parent, bg="white", bd=2, relief="groove",
                       highlightbackground="#4DA8DA", highlightcolor="#4DA8DA", highlightthickness=1)
        box.pack(side="left", padx=15, ipadx=25, ipady=20)

        tk.Label(box, text=label, bg="white", font=("Helvetica", 12, "bold"), fg="#4DA8DA").pack(pady=(0, 10))
        tk.Label(box, text=str(value), bg="white", font=("Helvetica", 18, "bold"), fg="#333").pack()

    def show_vocabulary_management(self):
        self.clear_main_frame()
        vocab_ui = VocabularyManagement(self.main_content, self.user)
        vocab_ui.pack(fill="both", expand=True)

    def show_user_management(self):
        self.clear_main_frame()
        tk.Label(self.main_content, text="⚙️ Quản lý tài khoản", font=("Helvetica", 18, "bold"), bg="white").pack(pady=30)
        tk.Label(self.main_content, text="Tính năng đang được phát triển.", font=("Helvetica", 12), bg="white").pack()

    def show_profile(self):
        self.clear_main_frame()
        from home.profile_user import Profile
        profile = Profile(self.main_content, self.user)
        profile.pack(fill="both", expand=True)

    def logout(self):
        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn đăng xuất?")
        if confirm:
            from auth.login import LoginWindow
            self.root.destroy()
            new_root = tk.Tk()
            LoginWindow(new_root)
            new_root.mainloop()

    def open_edit_profile_window(self):
        top = tk.Toplevel(self.root)
        top.title("Chỉnh sửa hồ sơ")
        top.geometry("400x300")
        top.configure(bg="white")
        top.grab_set()

        tk.Label(top, text="Chỉnh sửa hồ sơ", font=("Helvetica", 16, "bold"), bg="white").pack(pady=10)

        tk.Label(top, text="Họ tên:", bg="white").pack(anchor="w", padx=20)
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
                messagebox.showwarning("Lỗi", "Vui lòng điền đầy đủ thông tin.")

        tk.Button(top, text="Lưu", command=save_changes, bg="#4DA8DA", fg="white",
                  font=("Helvetica", 12), padx=10).pack(pady=20)
