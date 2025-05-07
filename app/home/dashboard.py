import tkinter as tk
from tkinter import ttk, messagebox

from home.vocabulary_management import VocabularyManagement
from common.colors import COLORS
from common.configs import WINDOW_SIZE


class DashboardWindow:
    def __init__(self, root, user):
        self.root = root
        self.root.title("Trang chủ - Dashboard")

        # Khởi tạo màn hình ở vị trí giữa cửa sổ
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width / 2) - (WINDOW_SIZE['WIDTH'] / 2))
        y = int((screen_height / 2) - (WINDOW_SIZE['HEIGHT'] / 2))
        self.root.geometry(f"{WINDOW_SIZE['WIDTH']}x{WINDOW_SIZE['HEIGHT']}+{x}+{y}")

        self.root.configure(bg=COLORS["background"])  # Set background color
        self.user = user

        # Frame sidebar
        self.sidebar = tk.Frame(root, bg=COLORS["primary"], width=368, height=768)
        self.sidebar.pack(side="left", fill="y")

        # Frame nội dung chính
        self.main_content = tk.Frame(root, bg="white", width=1000, height=768)
        self.main_content.pack(side="right", fill="both", expand=True)

        # Menu điều hướng
        self.menu_items = [
            ("Dashboard", self.show_dashboard),
            ("Từ vựng", self.show_vocabulary_management),
            ("Quản lý tài khoản", self.show_user_management) if user["role"] == "admin" else None,
            ("Đăng xuất", self.logout),
        ]

        for item in self.menu_items:
            if item:
                btn = tk.Button(
                    self.sidebar, text=item[0],
                    fg=COLORS["button_text"],
                    bg=COLORS["button_bg"],
                    activebackground=COLORS["button_bg"],
                    activeforeground=COLORS["button_text"],
                    font=("Arial", 12),
                    command=item[1], width=20, height=2, relief="flat"
                )
                btn.pack(pady=5)

        self.show_dashboard()

    def show_dashboard(self):
        """Hiển thị giao diện Dashboard"""
        for widget in self.main_content.winfo_children():
            widget.destroy()

        tk.Label(self.main_content, text="Dashboard", font=("Arial", 16, "bold"), bg=COLORS["background"]).pack(pady=10)

        stats_frame = tk.Frame(self.main_content, bg=COLORS["background"])
        stats_frame.pack(pady=10)

        ttk.Label(stats_frame, text="Số lượng từ vựng: 0", font=("Arial", 12)).pack(pady=5)
        ttk.Label(stats_frame, text="Số lượng người dùng: 0", font=("Arial", 12)).pack(pady=5)
        ttk.Label(stats_frame, text="Số lượng quản trị viên: 0", font=("Arial", 12)).pack(pady=5)

    def show_vocabulary_management(self):
        """Hiển thị giao diện quản lý từ vựng"""
        """Chuyển đến màn hình Quản lý từ vựng"""
        self.clear_main_frame()
        vocab_ui = VocabularyManagement(self.main_content, self.user)
        vocab_ui.pack(fill="both", expand=True)

    def show_user_management(self):
        """Hiển thị giao diện quản lý tài khoản"""
        messagebox.showinfo("Thông báo", "Chức năng này sẽ được thêm sau!")

    def clear_main_frame(self):
        """Xóa tất cả widget bên trong main_frame để chuyển sang giao diện mới."""
        for widget in self.main_content.winfo_children():
            widget.destroy()

    def logout(self):
        from auth.login import LoginWindow
        self.root.destroy()
        new_root = tk.Tk()
        LoginWindow(new_root)
        new_root.mainloop()
