import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
from common.colors import COLORS
from common.base_window import BaseWindow

class DashboardAdmin(tk.Frame):
    def __init__(self, parent, user):
        super().__init__(parent, bg="white")
        self.user = user
        self.users_file = "data/users.json"
        self.vocab_file = "data/vocab.json"
        self.build_ui()

    def build_ui(self):
        sidebar = tk.Frame(self, bg=COLORS["primary"], width=250)
        sidebar.pack(side="left", fill="y")

        tk.Label(
            sidebar,
            text=f"👤 {self.user.get('name', 'Admin')}",
            bg=COLORS["primary"],
            fg="white",
            font=("Helvetica", 16, "bold")
        ).pack(pady=(30, 20))

        menu_items = [
            ("📊 Tổng quan", self.show_overview),
            ("👥 Quản lý người dùng", self.show_user_management),
            ("📚 Quản lý từ vựng", self.show_vocab_management),
            ("📈 Thống kê học tập", self.show_statistics),
            ("⚙️ Cài đặt hệ thống", self.show_settings),
            ("🚪 Đăng xuất", self.logout),
        ]

        for item in menu_items:
            tk.Button(
                sidebar,
                text=item[0],
                fg="white",
                bg=COLORS["primary"],
                font=("Helvetica", 13),
                anchor="w",
                relief="flat",
                padx=30,
                activebackground=COLORS["secondary"],
                activeforeground="white",
                command=item[1],
                cursor="hand2"
            ).pack(fill="x", pady=4)

        self.content_frame = tk.Frame(self, bg="white")
        self.content_frame.pack(side="right", fill="both", expand=True)
        self.show_overview()

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_overview(self):
        self.clear_content()
        users, admins = self.load_user_stats()
        total_vocab = self.count_vocab()

        tk.Label(self.content_frame, text="📊 Tổng quan hệ thống", font=("Helvetica", 22, "bold"), fg=COLORS["primary"], bg="white").pack(pady=(30, 10))
        tk.Label(self.content_frame, text=f"Xin chào, quản trị viên {self.user.get('name', '')} 👋", font=("Helvetica", 14), fg="gray", bg="white").pack()

        stats_frame = tk.Frame(self.content_frame, bg="white")
        stats_frame.pack(pady=20)

        self.create_stat_box(stats_frame, "👤 Tổng số người dùng", users)
        self.create_stat_box(stats_frame, "🔐 Số quản trị viên", admins)
        self.create_stat_box(stats_frame, "📚 Từ vựng hệ thống", total_vocab)
        self.create_stat_box(stats_frame, "📝 Hoạt động hôm nay", 37)

    def create_stat_box(self, parent, label, value):
        box = tk.Frame(parent, bg=COLORS["light"], bd=1, relief="solid")
        box.pack(side="left", padx=20, ipadx=25, ipady=25)
        tk.Label(box, text=label, bg=COLORS["light"], font=("Helvetica", 12)).pack(pady=(0, 10))
        tk.Label(box, text=str(value), bg=COLORS["light"], font=("Helvetica", 18, "bold"), fg=COLORS["primary"]).pack()

    def show_user_management(self):
        self.clear_content()
        tk.Label(self.content_frame, text="📋 Danh sách người dùng", font=("Helvetica", 14, "bold"), bg="white").pack(pady=10)

        btn_frame = tk.Frame(self.content_frame, bg="white")
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="➕ Thêm người dùng", command=self.add_user, bg=COLORS["primary"], fg="white", padx=10).pack(side="left", padx=10)

        columns = ("Tên", "Email", "Vai trò", "Ngày tham gia")
        self.tree = ttk.Treeview(self.content_frame, columns=columns, show="headings", height=10)
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        self.load_users_table()
        self.tree.bind("<Double-1>", self.edit_or_delete_user)

    def show_vocab_management(self):
        self.clear_content()
        tk.Label(self.content_frame, text="📚 Danh sách từ vựng", font=("Helvetica", 14, "bold"), bg="white").pack(pady=10)

        btn_frame = tk.Frame(self.content_frame, bg="white")
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="➕ Thêm từ mới", command=self.add_vocab, bg=COLORS["primary"], fg="white", padx=10).pack(side="left", padx=10)

        columns = ("Từ", "Nghĩa", "Loại")
        tree = ttk.Treeview(self.content_frame, columns=columns, show="headings", height=10)
        tree.pack(fill="both", expand=True, padx=20, pady=10)

        try:
            with open(self.vocab_file, "r") as f:
                vocabs = json.load(f)
        except:
            vocabs = []

        for word in vocabs:
            tree.insert("", "end", values=(word.get("word", ""), word.get("meaning", ""), word.get("type", "")))

    def show_statistics(self):
        self.clear_content()
        tk.Label(self.content_frame, text="📈 Thống kê học tập", font=("Helvetica", 14, "bold"), bg="white").pack(pady=20)
        tk.Label(self.content_frame, text="Tổng số lượt học hôm nay: 37\nTừ vựng học nhiều nhất: 'Environment'\nNgười dùng hoạt động: 12", bg="white", font=("Helvetica", 12)).pack()

    def show_settings(self):
        self.clear_content()
        tk.Label(self.content_frame, text="⚙️ Cài đặt hệ thống", font=("Helvetica", 14, "bold"), bg="white").pack(pady=20)

        name = simpledialog.askstring("Cập nhật tên", "Nhập tên quản trị viên mới:")
        if name:
            self.user["name"] = name
            try:
                with open(self.users_file, "r+") as f:
                    users = json.load(f)
                    for u in users:
                        if u["email"] == self.user["email"]:
                            u["name"] = name
                            break
                    f.seek(0)
                    json.dump(users, f, indent=4)
                    f.truncate()
                messagebox.showinfo("Thành công", "Đã cập nhật tên.")
            except:
                messagebox.showerror("Lỗi", "Không thể cập nhật tên.")

    def logout(self):
        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn đăng xuất?")
        if confirm:
            self.master.destroy()
            from auth.login import LoginWindow
            root = tk.Tk()
            LoginWindow(root)
            root.mainloop()

    def load_user_stats(self):
        try:
            with open(self.users_file, "r") as f:
                users = json.load(f)
        except:
            users = []
        return len(users), sum(1 for u in users if u.get("role") == "admin")

    def count_vocab(self):
        try:
            with open(self.vocab_file, "r") as f:
                vocabs = json.load(f)
            return len(vocabs)
        except:
            return 0

    def load_users_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        try:
            with open(self.users_file, "r") as f:
                users = json.load(f)
        except:
            users = []
        for user in users:
            self.tree.insert("", "end", values=(user.get("name", ""), user.get("email", ""), user.get("role", "user").capitalize(), user.get("join_date", "")))

    def edit_or_delete_user(self, event):
        item = self.tree.focus()
        values = self.tree.item(item, "values")
        if not values:
            return
        action = messagebox.askquestion("Chọn hành động", f"Bạn muốn xóa người dùng '{values[0]}'?", icon="warning")
        if action == "yes":
            self.delete_user(values[1])

    def delete_user(self, email):
        try:
            with open(self.users_file, "r") as f:
                users = json.load(f)
            users = [u for u in users if u.get("email") != email]
            with open(self.users_file, "w") as f:
                json.dump(users, f, indent=4)
            messagebox.showinfo("Xóa thành công", "Người dùng đã bị xóa.")
            self.load_users_table()
        except:
            messagebox.showerror("Lỗi", "Không thể xóa người dùng.")

    def add_user(self):
        name = simpledialog.askstring("Tên", "Nhập tên người dùng:")
        email = simpledialog.askstring("Email", "Nhập email:")
        role = simpledialog.askstring("Vai trò", "Nhập vai trò (user/admin):")
        join_date = simpledialog.askstring("Ngày tham gia", "Nhập ngày (dd/mm/yyyy):")
        if name and email:
            try:
                with open(self.users_file, "r+") as f:
                    users = json.load(f)
                    users.append({"name": name, "email": email, "role": role, "join_date": join_date})
                    f.seek(0)
                    json.dump(users, f, indent=4)
                    f.truncate()
                self.load_users_table()
            except:
                messagebox.showerror("Lỗi", "Không thể thêm người dùng.")

    def add_vocab(self):
        word = simpledialog.askstring("Từ", "Nhập từ tiếng Anh:")
        meaning = simpledialog.askstring("Nghĩa", "Nhập nghĩa:")
        word_type = simpledialog.askstring("Loại", "Nhập loại từ (noun, verb,...):")
        if word and meaning:
            try:
                with open(self.vocab_file, "r+") as f:
                    data = json.load(f)
                    data.append({"word": word, "meaning": meaning, "type": word_type})
                    f.seek(0)
                    json.dump(data, f, indent=4)
                    f.truncate()
                messagebox.showinfo("Thành công", "Đã thêm từ mới.")
                self.show_vocab_management()
            except:
                messagebox.showerror("Lỗi", "Không thể thêm từ mới.")

from home.vocabulary_management import VocabularyManagement

class DashboardAdmin(tk.Frame):
    def __init__(self, parent, user):
        super().__init__(parent)
        self.user = user
        self.content_frame = tk.Frame(self, bg="white")
        self.content_frame.pack(fill="both", expand=True)
        
        # Nút menu quản lý từ vựng
        tk.Button(self, text="📚 Quản lý từ vựng", command=self.show_vocabulary_management).pack()
    
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_vocabulary_management(self):
        self.clear_content()
        vocab_frame = VocabularyManagement(self.content_frame, self.user)
        vocab_frame.pack(fill="both", expand=True)


if __name__ == "__main__":
    fake_user = {"name": "Admin", "email": "admin@example.com", "role": "admin"}
    root = tk.Tk()
    app = DashboardAdmin(root, fake_user)
    root.mainloop()
