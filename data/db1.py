import tkinter as tk
from tkinter import messagebox

class Dashboard:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.title("Dashboard - Quản lý Từ Vựng")
        self.root.geometry("800x500")
        self.root.configure(bg='#f0f0f0')
        self.root.resizable(False, False)

        # Khung trái: Menu điều hướng
        self.left_frame = tk.Frame(self.root, bg="#2E3B4E", width=200)
        self.left_frame.pack(side="left", fill="y")

        # Logo/Ảnh
        logo = tk.PhotoImage(file="D:/Python/english-app/app/auth/login.png")  # Đảm bảo rằng đường dẫn ảnh đúng
        img_label = tk.Label(self.left_frame, image=logo, bg="#2E3B4E")
        img_label.image = logo  # Giữ tham chiếu để tránh mất ảnh
        img_label.pack(pady=20)

        # Các nút chức năng
        self.create_sidebar_button("Xem Từ Vựng", self.view_vocab)
        self.create_sidebar_button("Thêm Từ Mới", self.add_vocab)
        self.create_sidebar_button("Thống Kê", self.view_stats)
        self.create_sidebar_button("Đăng Xuất", self.logout)

        # Khung phải: Nội dung Dashboard
        self.right_frame = tk.Frame(self.root, bg="white")
        self.right_frame.pack(side="right", fill="both", expand=True)

        # Tiêu đề Dashboard
        tk.Label(self.right_frame, text=f"Chào mừng, {self.username}", font=("Helvetica", 18, "bold"), fg="#333", bg="white").pack(pady=20)

    def create_sidebar_button(self, text, command):
        button = tk.Button(self.left_frame, text=text, font=("Helvetica", 14), bg="#3B4A61", fg="white", relief="flat", width=20, height=2, command=command)
        button.pack(pady=10, padx=20)

    def view_vocab(self):
        # Mở cửa sổ xem từ vựng
        messagebox.showinfo("Xem Từ Vựng", "Tính năng này đang được phát triển!")

    def add_vocab(self):
        # Mở cửa sổ thêm từ vựng
        messagebox.showinfo("Thêm Từ Mới", "Tính năng này đang được phát triển!")

    def view_stats(self):
        # Mở cửa sổ thống kê
        messagebox.showinfo("Thống Kê", "Tính năng này đang được phát triển!")

    def logout(self):
        # Đăng xuất và quay lại cửa sổ trước
        self.root.quit()


def open_dashboard(username="admin"):
    root = tk.Tk()
    app = Dashboard(root, username)
    root.mainloop()

if __name__ == "__main__":
    open_dashboard()  # Trực tiếp mở Dashboard mà không cần màn hình đăng nhập
