import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

from home.vocabulary_management import VocabularyManagement
from common.colors import COLORS
from common.configs import WINDOW_SIZE

class DashboardWindow:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.root.title("English Learning Dashboard")

        # Căn giữa cửa sổ
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = int((screen_width / 2) - (WINDOW_SIZE['WIDTH'] / 2))
        y = int((screen_height / 2) - (WINDOW_SIZE['HEIGHT'] / 2))
        root.geometry(f"{WINDOW_SIZE['WIDTH']}x{WINDOW_SIZE['HEIGHT']}+{x}+{y}")
        root.configure(bg="white")
        root.resizable(False, False)

        # Sidebar
        self.sidebar = tk.Frame(root, bg=COLORS["primary"], width=250)
        self.sidebar.pack(side="left", fill="y")

        self.main_content = tk.Frame(root, bg="white")
        self.main_content.pack(side="right", fill="both", expand=True)

        # Tiêu đề người dùng
        tk.Label(
            self.sidebar,
            text=f"👤 {user.get('name', 'Người dùng')}",
            bg=COLORS["primary"],
            fg="white",
            font=("Helvetica", 16, "bold")
        ).pack(pady=(30, 20))

        # Menu sidebar
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
                    fg="white", bg=COLORS["primary"],
                    font=("Helvetica", 13), anchor="w",
                    relief="flat", padx=30,
                    activebackground=COLORS["secondary"],
                    activeforeground="white",
                    command=item[1],
                    cursor="hand2"
                )
                btn.pack(fill="x", pady=4)

        self.show_dashboard()

    def clear_main_frame(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.clear_main_frame()

        tk.Label(
            self.main_content, text="📊 Tổng quan học tập",
            font=("Helvetica", 22, "bold"), bg="white", fg=COLORS["primary"]
        ).pack(pady=(30, 10))

        tk.Label(
            self.main_content, text=f"Chào mừng trở lại, {self.user.get('name', '')} 👋",
            font=("Helvetica", 14), bg="white", fg="gray"
        ).pack()

        stats_frame = tk.Frame(self.main_content, bg="white")
        stats_frame.pack(pady=20)

        self.create_stat_box(stats_frame, "📝 Từ vựng đã học", 48)
        self.create_stat_box(stats_frame, "🎯 Mục tiêu hôm nay", "12 / 20")
        self.create_stat_box(stats_frame, "📅 Chuỗi ngày học", 5)
        self.create_stat_box(stats_frame, "⏱️ Thời gian hôm nay", "25 phút")

        self.create_profile_preview()

    def create_stat_box(self, parent, label, value):
        box = tk.Frame(parent, bg=COLORS["light"], bd=1, relief="solid")
        box.pack(side="left", padx=20, ipadx=25, ipady=25)

        tk.Label(box, text=label, bg=COLORS["light"], font=("Helvetica", 12)).pack(pady=(0, 10))
        tk.Label(box, text=str(value), bg=COLORS["light"], font=("Helvetica", 18, "bold"), fg=COLORS["primary"]).pack()

    def create_profile_preview(self):
        frame = tk.Frame(self.main_content, bg="white", bd=1, relief="solid")
        frame.pack(pady=20, padx=40, fill="x")

        image_path = "assets/avatar.png"
        try:
            avatar_img = Image.open(image_path).resize((100, 100))
        except:
            avatar_img = Image.new("RGB", (100, 100), color="gray")
        avatar_tk = ImageTk.PhotoImage(avatar_img)

        img_label = tk.Label(frame, image=avatar_tk, bg="white")
        img_label.image = avatar_tk
        img_label.pack(side="left", padx=20, pady=20)

        info_frame = tk.Frame(frame, bg="white")
        info_frame.pack(side="left", padx=10, pady=20, anchor="w")

        user_name = self.user.get("name", "Người dùng")
        email = self.user.get("email", "no-email@example.com")
        role = self.user.get("role", "user")
        join_date = self.user.get("join_date", "01/01/2024")

        tk.Label(info_frame, text=f"Họ tên: {user_name}", font=("Helvetica", 13), bg="white").pack(anchor="w")
        tk.Label(info_frame, text=f"Email: {email}", font=("Helvetica", 13), bg="white").pack(anchor="w")
        tk.Label(info_frame, text=f"Vai trò: {role.title()}", font=("Helvetica", 13), bg="white").pack(anchor="w")
        tk.Label(info_frame, text=f"Ngày tham gia: {join_date}", font=("Helvetica", 13), bg="white").pack(anchor="w")

        tk.Button(
            info_frame, text="Chỉnh sửa hồ sơ",
            command=self.open_edit_profile_window,
            bg=COLORS["primary"], fg="white",
            font=("Helvetica", 11),
            padx=10, pady=2, cursor="hand2"
        ).pack(anchor="w", pady=(10, 0))

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

        tk.Button(top, text="Lưu", command=save_changes, bg=COLORS["primary"], fg="white",
                  font=("Helvetica", 12), padx=10).pack(pady=20)

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
