import tkinter as tk
from tkinter import messagebox, Toplevel
from common.colors import COLORS
from tkinter import ttk

class AccountManagement(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")
        tk.Label(
            self, text="⚙️ Quản lý tài khoản",
            font=("Helvetica", 20, "bold"),
            bg="white", fg=COLORS["primary"]
        ).pack(pady=20)

        table_wrapper = tk.Frame(self, bg="white", highlightbackground="#ccc", highlightthickness=2)
        table_wrapper.pack(fill="both", expand=True, padx=20, pady=10)

        self.table_frame = tk.Frame(table_wrapper, bg="white")
        self.table_frame.pack(fill="both", expand=True)

        self.draw_table()

        tk.Button(
            self,
            text="➕ Thêm tài khoản",
            bg=COLORS["primary"], fg="white",
            font=("Helvetica", 13, "bold"),
            padx=20, pady=8,
            command=self.open_add_form
        ).pack(pady=15)

    def draw_table(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        headers = ["Họ tên", "Email", "Vai trò", "Hành động"]
        for col, header in enumerate(headers):
            tk.Label(
                self.table_frame, text=header,
                font=("Helvetica", 13, "bold"), bg=COLORS["secondary"], fg="white",
                padx=12, pady=10, borderwidth=1, relief="solid"
            ).grid(row=0, column=col, sticky="nsew")

        for i, account in enumerate(self.accounts):
            tk.Label(
                self.table_frame, text=account["name"],
                font=("Helvetica", 12), bg="white",
                padx=12, pady=10, borderwidth=1, relief="solid"
            ).grid(row=i+1, column=0, sticky="nsew")

            tk.Label(
                self.table_frame, text=account["email"],
                font=("Helvetica", 12), bg="white",
                padx=12, pady=10, borderwidth=1, relief="solid"
            ).grid(row=i+1, column=1, sticky="nsew")

            tk.Label(
                self.table_frame, text=account["role"].title(),
                font=("Helvetica", 12), bg="white",
                padx=12, pady=10, borderwidth=1, relief="solid"
            ).grid(row=i+1, column=2, sticky="nsew")

            action_frame = tk.Frame(
                self.table_frame, bg="white",
                borderwidth=1, relief="solid"
            )
            action_frame.grid(row=i+1, column=3, sticky="nsew")

            tk.Button(
                action_frame, text="✏️", width=4,
                bg="#FFD700", font=("Helvetica", 11),
                command=lambda i=i: self.open_edit_form(i)
            ).pack(side="left", padx=5, pady=5)

            tk.Button(
                action_frame, text="🗑️", width=4,
                bg="#FF6347", font=("Helvetica", 11),
                command=lambda i=i: self.delete_account(i)
            ).pack(side="left", padx=5, pady=5)

        for col in range(len(headers)):
            self.table_frame.grid_columnconfigure(col, weight=1)

    def open_add_form(self):
        self.open_account_form()

    def open_edit_form(self, index):
        self.open_account_form(index)

    def open_account_form(self, index=None):
        is_edit = index is not None
        account = self.accounts[index] if is_edit else {"name": "", "email": "", "role": "user"}

        window = Toplevel(self)
        window.title("Sửa tài khoản" if is_edit else "Thêm tài khoản")
        window.geometry("400x300")
        window.configure(bg="white")
        window.resizable(False, False)

        tk.Label(window, text="Thông tin tài khoản", font=("Helvetica", 16, "bold"), bg="white").pack(pady=15)

        form_frame = tk.Frame(window, bg="white")
        form_frame.pack(pady=10, padx=30, fill="both", expand=True)

    # Họ tên
        tk.Label(form_frame, text="Họ tên:", font=("Helvetica", 12), bg="white").grid(row=0, column=0, sticky="w", pady=5)
        name_entry = tk.Entry(form_frame, font=("Helvetica", 12))
        name_entry.grid(row=0, column=1, pady=5, ipadx=10)
        name_entry.insert(0, account["name"])

    # Email
        tk.Label(form_frame, text="Email:", font=("Helvetica", 12), bg="white").grid(row=1, column=0, sticky="w", pady=5)
        email_entry = tk.Entry(form_frame, font=("Helvetica", 12))
        email_entry.grid(row=1, column=1, pady=5, ipadx=10)
        email_entry.insert(0, account["email"])

    # Vai trò (Combobox thay vì Entry)
        tk.Label(form_frame, text="Vai trò:", font=("Helvetica", 12), bg="white").grid(row=2, column=0, sticky="w", pady=5)
        role_var = tk.StringVar()
        role_combobox = ttk.Combobox(form_frame, textvariable=role_var, state="readonly", values=["User", "Admin"], font=("Helvetica", 12), width=17)
        role_combobox.grid(row=2, column=1, pady=5, ipadx=5)
        role_combobox.set(account["role"] if account["role"] in ["User", "Admin"] else "User")


        def save():
            name = name_entry.get().strip()
            email = email_entry.get().strip()
            role = role_var.get().strip().lower()

            if is_edit:
                self.accounts[index] = {"name": name, "email": email, "role": role}
            else:
                self.accounts.append({"name": name, "email": email, "role": role})

            self.draw_table()
            window.destroy()

        btn_text = "Lưu thay đổi" if is_edit else "Thêm tài khoản"
        tk.Button(
            window, text=btn_text, command=save,
            bg=COLORS["primary"], fg="white", font=("Helvetica", 12, "bold"),
            padx=20, pady=8
        ).pack(pady=15)

    def delete_account(self, index):
        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa tài khoản này?", parent=self)
        if confirm:
            del self.accounts[index]
            self.draw_table()
