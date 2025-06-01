import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

DB_PATH = os.path.abspath("app/data/database.json")

class AccountManagement(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f5f7fa")
        self.users = []
        self.filtered_users = []
        self.load_data()

        self.style = ttk.Style()
        self.style.theme_use("clam")

        
        self.style.configure("Treeview.Heading", font=("Segoe UI", 12, "bold"), background="#2980b9", foreground="white")
        
        self.style.configure("Treeview", font=("Segoe UI", 11), rowheight=28, background="white", foreground="#333", fieldbackground="white")
        
        self.style.map("Treeview", background=[("selected", "#3498db")], foreground=[("selected", "white")])

        self.create_widgets()
        self.apply_filters()

    def load_data(self):
        if not os.path.exists(DB_PATH):
            self.users = []
            return
        with open(DB_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.users = data.get("users", [])

    def save_data(self):
        if not os.path.exists(DB_PATH):
            data = {"users": self.users, "vocab": []}
        else:
            with open(DB_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            data["users"] = self.users
        with open(DB_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def create_widgets(self):
        
        title = tk.Label(self, text="Account Management", bg="#f5f7fa", fg="#2c3e50", font=("Segoe UI", 20, "bold"))
        title.pack(pady=(20,10))

        
        top_frame = tk.Frame(self, bg="#f5f7fa")
        top_frame.pack(fill="x", padx=25, pady=(0, 15))

        tk.Label(top_frame, text="Search:", bg="#f5f7fa", font=("Segoe UI", 11)).pack(side="left")
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(top_frame, textvariable=self.search_var, width=35, font=("Segoe UI", 11))
        search_entry.pack(side="left", padx=(8, 25))
        search_entry.bind("<KeyRelease>", lambda e: self.apply_filters())

        tk.Label(top_frame, text="Filter Role:", bg="#f5f7fa", font=("Segoe UI", 11)).pack(side="left")
        self.role_filter_var = tk.StringVar(value="All")
        role_options = ["All", "Admin", "User"]
        role_menu = ttk.Combobox(top_frame, textvariable=self.role_filter_var, values=role_options, state="readonly", width=15, font=("Segoe UI", 11))
        role_menu.pack(side="left", padx=8)
        role_menu.bind("<<ComboboxSelected>>", lambda e: self.apply_filters())

        
        btn_frame = tk.Frame(self, bg="#f5f7fa")
        btn_frame.pack(fill="x", padx=25, pady=(0, 15))

        def style_btn(btn, bg, fg="white"):
            btn.configure(
                bg=bg, fg=fg, font=("Segoe UI", 11, "bold"), relief="flat",
                activebackground=self.darken_color(bg, 0.85),
                bd=0, highlightthickness=0, padx=12, pady=6
            )
            btn.bind("<Enter>", lambda e: btn.config(bg=self.darken_color(bg, 0.85)))
            btn.bind("<Leave>", lambda e: btn.config(bg=bg))

        btn_add = tk.Button(btn_frame, text="Add Account", command=self.add_account)
        style_btn(btn_add, "#27ae60")
        btn_add.pack(side="left", padx=6)

        btn_edit = tk.Button(btn_frame, text="Edit Selected", command=self.edit_account)
        style_btn(btn_edit, "#2980b9")
        btn_edit.pack(side="left", padx=6)

        btn_delete = tk.Button(btn_frame, text="Delete Selected", command=self.delete_account)
        style_btn(btn_delete, "#c0392b")
        btn_delete.pack(side="left", padx=6)

        btn_refresh = tk.Button(btn_frame, text="Refresh", command=self.apply_filters)
        style_btn(btn_refresh, "#7f8c8d")
        btn_refresh.pack(side="right", padx=6)

        
        tree_frame = tk.Frame(self, bg="#f5f7fa")
        tree_frame.pack(fill="both", expand=True, padx=25, pady=(0, 25))

        columns = ("id", "name", "email", "role")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse", height=15)
        self.tree.pack(side="left", fill="both", expand=True)

        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("email", text="Email")
        self.tree.heading("role", text="Role")

        self.tree.column("id", width=60, anchor="center")
        self.tree.column("name", width=180, anchor="w")
        self.tree.column("email", width=230, anchor="w")
        self.tree.column("role", width=100, anchor="center")

        
        self.tree.tag_configure("oddrow", background="#eaf2f8")
        self.tree.tag_configure("evenrow", background="white")

        
        self.tree.bind("<Motion>", self.on_treeview_hover)

    def darken_color(self, hex_color, factor=0.9):
        hex_color = hex_color.lstrip("#")
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        dark_rgb = tuple(max(0, int(c*factor)) for c in rgb)
        return "#%02x%02x%02x" % dark_rgb

    def on_treeview_hover(self, event):
        row_id = self.tree.identify_row(event.y)

        for item in self.tree.get_children():
            tags = list(self.tree.item(item, "tags"))
            if "hover" in tags:
                tags.remove("hover")
                self.tree.item(item, tags=tags)
        
        if row_id:
            tags = list(self.tree.item(row_id, "tags"))
            if "hover" not in tags:
                tags.append("hover")
                self.tree.item(row_id, tags=tags)

        
        self.style.configure("Treeview", background="white")
        self.tree.tag_configure("hover", background="#d1e7ff")

    def apply_filters(self):
        search_text = self.search_var.get().lower()
        role_filter = self.role_filter_var.get()

        self.filtered_users = []
        for user in self.users:
            matches_search = (
                search_text in user.get("name", "").lower() or
                search_text in user.get("email", "").lower()
            )
            matches_role = (role_filter == "All" or user.get("role") == role_filter)
            if matches_search and matches_role:
                self.filtered_users.append(user)

        self.refresh_treeview(display_filtered=True)

    def refresh_treeview(self, display_filtered=False):
        for i in self.tree.get_children():
            self.tree.delete(i)

        data_to_show = self.filtered_users if display_filtered else self.users
        for idx, user in enumerate(data_to_show):
            tag = "evenrow" if idx % 2 == 0 else "oddrow"
            self.tree.insert("", "end", values=(
                user.get("id", ""),
                user.get("name", ""),
                user.get("email", ""),
                user.get("role", "")
            ), tags=(tag,))

    def add_account(self):
        AccountDialog(self, "Add New Account", None, self.save_new_account)

    def save_new_account(self, user_data):
        max_id = max([u.get("id", 0) for u in self.users], default=0)
        user_data["id"] = max_id + 1
        self.users.append(user_data)
        self.save_data()
        self.apply_filters()

    def edit_account(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an account to edit.")
            return
        selected_id = int(self.tree.item(selected[0], "values")[0])
        user = next((u for u in self.users if u.get("id") == selected_id), None)
        if user:
            AccountDialog(self, "Edit Account", user, self.save_edited_account)

    def save_edited_account(self, updated_user):
        for idx, user in enumerate(self.users):
            if user.get("id") == updated_user.get("id"):
                self.users[idx] = updated_user
                break
        self.save_data()
        self.apply_filters()

    def delete_account(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an account to delete.")
            return
        selected_id = int(self.tree.item(selected[0], "values")[0])
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this account?")
        if confirm:
            self.users = [u for u in self.users if u.get("id") != selected_id]
            self.save_data()
            self.apply_filters()

class AccountDialog(tk.Toplevel):
    def __init__(self, parent, title, user_data, callback):
        super().__init__(parent)
        self.title(title)
        self.callback = callback
        self.user_data = user_data or {}

        self.configure(bg="#f5f7fa")
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        
        self.geometry(self.center_window(400, 320))

        self.create_widgets()

        
        if user_data:
            self.fill_data()

    def center_window(self, w, h):
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        x = (screen_w - w) // 2
        y = (screen_h - h) // 2
        return f"{w}x{h}+{x}+{y}"

    def create_widgets(self):
        pad_x = 20
        pad_y = 10
        font_label = ("Segoe UI", 11)
        font_entry = ("Segoe UI", 11)

        tk.Label(self, text="Name:", bg="#f5f7fa", font=font_label).place(x=pad_x, y=30)
        self.name_var = tk.StringVar()
        self.entry_name = ttk.Entry(self, textvariable=self.name_var, font=font_entry, width=35)
        self.entry_name.place(x=pad_x, y=55)

        tk.Label(self, text="Email:", bg="#f5f7fa", font=font_label).place(x=pad_x, y=90)
        self.email_var = tk.StringVar()
        self.entry_email = ttk.Entry(self, textvariable=self.email_var, font=font_entry, width=35)
        self.entry_email.place(x=pad_x, y=115)

        tk.Label(self, text="Role:", bg="#f5f7fa", font=font_label).place(x=pad_x, y=150)
        self.role_var = tk.StringVar(value="user")
        role_combo = ttk.Combobox(self, textvariable=self.role_var, values=["admin", "user"], state="readonly", font=font_entry, width=33)
        role_combo.place(x=pad_x, y=175)

        
        btn_save = tk.Button(self, text="Save", bg="#27ae60", fg="white", font=("Segoe UI", 11, "bold"),
                             command=self.on_save, relief="flat", padx=12, pady=6)
        btn_save.place(x=pad_x, y=230)

        btn_cancel = tk.Button(self, text="Cancel", bg="#c0392b", fg="white", font=("Segoe UI", 11, "bold"),
                               command=self.destroy, relief="flat", padx=12, pady=6)
        btn_cancel.place(x=pad_x + 100, y=230)

    def fill_data(self):
        self.name_var.set(self.user_data.get("name", ""))
        self.email_var.set(self.user_data.get("email", ""))
        self.role_var.set(self.user_data.get("role", "user"))

    def on_save(self):
        name = self.name_var.get().strip()
        email = self.email_var.get().strip()
        role = self.role_var.get()

        if not name or not email:
            messagebox.showerror("Error", "Name and Email cannot be empty.")
            return
        if "@" not in email or "." not in email:
            messagebox.showerror("Error", "Please enter a valid email address.")
            return

        user = {
            "id": self.user_data.get("id", None),
            "name": name,
            "email": email,
            "role": role
        }

        self.callback(user)
        self.destroy()

def center_window(root, width=900, height=650):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root.geometry(f"{width}x{height}+{x}+{y}")

def main():
    root = tk.Tk()
    root.title("Account Management")
    root.configure(bg="#f5f7fa")
    center_window(root)
    app = AccountManagement(root)
    app.pack(fill="both", expand=True)
    root.mainloop()

if __name__ == "__main__":
    main()
