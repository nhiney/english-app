import tkinter as tk
from tkinter import ttk
import os
import sys

# Thêm đường dẫn thư mục chứa login.py vào sys.path
sys.path.append(os.path.abspath("D:/Python/english-app/app/auth"))

# Hàm chuyển đến cửa sổ đăng nhập
def go_to_login():
    root.destroy()
    open_login_window()

# Hàm mở cửa sổ đăng nhập
def open_login_window():
    import login  # Bây giờ Python sẽ tìm login.py trong thư mục đã thêm vào sys.path
    login.open_window()  # Mở cửa sổ đăng nhập

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Ứng dụng Từ vựng Tiếng Anh")
root.geometry("1000x600")

# ===== Khung Menu bên trái =====
frame_menu = tk.Frame(root, bg="lightgray", width=150)
frame_menu.pack(side="left", fill="y")

tk.Label(frame_menu, text="MENU", font=("Arial", 12, "bold"), bg="lightgray").pack(pady=10)
tk.Button(frame_menu, text="Dashboard", width=15).pack(pady=5)
tk.Button(frame_menu, text="Từ vựng", width=15).pack(pady=5)
tk.Button(frame_menu, text="Tài khoản", width=15).pack(pady=5)

# Thêm nút Đăng xuất với sự kiện chuyển đến cửa sổ đăng nhập
tk.Button(frame_menu, text="Đăng xuất", width=15, command=go_to_login).pack(pady=5)

tk.Label(frame_menu, text="\nĐăng nhập như: admin\nVai trò: user", font=("Arial", 9), bg="lightgray").pack(side="bottom", pady=10)

# ===== Khung chính =====
frame_main = tk.Frame(root)
frame_main.pack(side="left", fill="both", expand=True, padx=10, pady=10)

tk.Label(frame_main, text="Dashboard", font=("Arial", 16, "bold")).pack(anchor="w")

# ===== Các ô thống kê =====
frame_stats = tk.Frame(frame_main)
frame_stats.pack(fill="x", pady=10)

def create_stat_box(parent, title, value):
    frame = tk.Frame(parent, bd=1, relief="solid", padx=20, pady=10)
    tk.Label(frame, text=title, font=("Arial", 10)).pack()
    tk.Label(frame, text=str(value), font=("Arial", 18, "bold")).pack()
    return frame

create_stat_box(frame_stats, "Từ vựng", 0).pack(side="left", padx=10)
create_stat_box(frame_stats, "Người dùng", 1).pack(side="left", padx=10)
create_stat_box(frame_stats, "Quản trị viên", 0).pack(side="left", padx=10)

# ===== Tìm kiếm từ vựng =====
frame_search = tk.Frame(frame_main)
frame_search.pack(fill="x", pady=10)

tk.Label(frame_search, text="Tìm kiếm từ vựng:").pack(side="left")
entry_search = tk.Entry(frame_search, width=30)
entry_search.pack(side="left", padx=5)
tk.Button(frame_search, text="Tìm").pack(side="left")

# ===== Danh sách từ vựng =====
tk.Label(frame_main, text="Danh sách từ vựng", font=("Arial", 14, "bold")).pack(anchor="w", pady=(10, 5))

columns = ("Từ vựng", "Nghĩa", "Ví dụ")
tree = ttk.Treeview(frame_main, columns=columns, show="headings", height=15)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=200)

tree.pack(fill="both", expand=True)

# ===== Khởi chạy ứng dụng =====
root.mainloop()
