import tkinter as tk
from tkinter import messagebox, simpledialog
from common.colors import COLORS

class AccountManagement(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")
        self.accounts = [
            {"name": "Admin", "email": "admin@example.com", "role": "admin"},
            {"name": "User 1", "email": "user1@example.com", "role": "user"},
            {"name": "User 2", "email": "user2@example.com", "role": "user"},
        ]

        tk.Label(
            self, text="⚙️ Quản lý tài khoản",
            font=("Helvetica", 18, "bold"), bg="white", fg=COLORS["primary"]
        ).pack(pady=20)

        self.table_frame = tk.Frame(self, bg="white")
        self.table_frame.pack(fill="both", expand=True, padx=20)

        self.draw_table()

        tk.Button(
            self, text="➕ Thêm tài khoản", bg=COLORS["primary"], fg="white",
            font=("Helvetica", 12), padx=10, pady=4,
            command=self.add_account
        ).pack(pady=10)

    def draw_table(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        headers = ["Họ tên", "Email", "Vai trò", "Hành động"]
        for col, header in enumerate(headers):
            tk.Label(
                self.table_frame, text=header,
                font=("Helvetica", 12, "bold"), bg=COLORS["secondary"], fg="white",
                padx=10, pady=5, borderwidth=1, relief="solid"
            ).grid(row=0, column=col, sticky="nsew")

        for i, account in enumerate(self.accounts):
            tk.Label(
                self.table_frame, text=account["name"], bg="white", font=("Helvetica", 11),
                borderwidth=1, relief="solid", padx=10, pady=5
            ).grid(row=i+1, column=0, sticky="nsew")
            tk.Label(
                self.table_frame, text=account["email"], bg="white", font=("Helvetica", 11),
                borderwidth=1, relief="solid", padx=10, pady=5
            ).grid(row=i+1, column=1, sticky="nsew")
            tk.Label(
                self.table_frame, text=account["role"].title(), bg="white", font=("Helvetica", 11),
                borderwidth=1, relief="solid", padx=10, pady=5
            ).grid(row=i+1, column=2, sticky="nsew")

            action_frame = tk.Frame(self.table_frame, bg="white")
            action_frame.grid(row=i+1, column=3, sticky="nsew")
            tk.Button(action_frame, text="✏️", width=4, bg="#FFD700", command=lambda i=i: self.edit_account(i)).pack(side="left", padx=2)
            tk.Button(action_frame, text="🗑️", width=4, bg="#FF6347", command=lambda i=i: self.delete_account(i)).pack(side="left", padx=2)

    def add_account(self):
        name = simpledialog.askstring("Thêm tài khoản", "Nhập họ tên:")
        email = simpledialog.askstring("Thêm tài khoản", "Nhập email:")
        role = simpledialog.askstring("Thêm tài khoản", "Nhập vai trò (admin/user):")

        if name and email and role in ["admin", "user"]:
            self.accounts.append({"name": name, "email": email, "role": role})
            self.draw_table()
        else:
            messagebox.showwarning("Lỗi", "Vui lòng nhập đúng thông tin!")

    def edit_account(self, index):
        account = self.accounts[index]
        name = simpledialog.askstring("Sửa tài khoản", "Họ tên:", initialvalue=account["name"])
        email = simpledialog.askstring("Sửa tài khoản", "Email:", initialvalue=account["email"])
        role = simpledialog.askstring("Sửa tài khoản", "Vai trò (admin/user):", initialvalue=account["role"])

        if name and email and role in ["admin", "user"]:
            self.accounts[index] = {"name": name, "email": email, "role": role}
            self.draw_table()
        else:
            messagebox.showwarning("Lỗi", "Thông tin không hợp lệ.")

    def delete_account(self, index):
        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa tài khoản này?")
        if confirm:
            del self.accounts[index]
            self.draw_table()
