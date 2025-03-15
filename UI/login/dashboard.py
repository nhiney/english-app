import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class VocabularyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ứng dụng Từ vựng Tiếng Anh")
        self.root.geometry("800x600")
        
        # Khởi tạo file dữ liệu
        self.users_file = "users.json"
        self.vocab_file = "vocabulary.json"
        
        # Tạo file nếu chưa tồn tại
        for file_path in [self.users_file, self.vocab_file]:
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    json.dump([], f)
        
        # Người dùng hiện tại
        self.current_user = None
        
        # Hiển thị màn hình đăng nhập
        self.show_login_form()
    
    def show_login_form(self):
        # Xóa các widget hiện tại
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Tạo khung đăng nhập
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True)
        
        # Tiêu đề
        ttk.Label(frame, text="Đăng Nhập", font=('Arial', 16)).pack(pady=10)
        
        # Form đăng nhập
        ttk.Label(frame, text="Email:").pack(anchor="w", pady=5)
        self.email_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.email_var, width=30).pack(pady=5)
        
        ttk.Label(frame, text="Mật khẩu:").pack(anchor="w", pady=5)
        self.password_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.password_var, width=30, show="*").pack(pady=5)
        
        # Nút
        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Đăng nhập", command=self.login).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Đăng ký", command=self.show_register_form).pack(side="left", padx=5)
    
    def show_register_form(self):
        # Xóa các widget hiện tại
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Tạo khung đăng ký
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True)
        
        # Tiêu đề
        ttk.Label(frame, text="Đăng Ký Tài Khoản", font=('Arial', 16)).pack(pady=10)
        
        # Form đăng ký
        ttk.Label(frame, text="Họ và tên:").pack(anchor="w", pady=5)
        self.fullname_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.fullname_var, width=30).pack(pady=5)
        
        ttk.Label(frame, text="Email:").pack(anchor="w", pady=5)
        self.reg_email_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.reg_email_var, width=30).pack(pady=5)
        
        ttk.Label(frame, text="Mật khẩu:").pack(anchor="w", pady=5)
        self.reg_password_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.reg_password_var, width=30, show="*").pack(pady=5)
        
        ttk.Label(frame, text="Xác nhận mật khẩu:").pack(anchor="w", pady=5)
        self.confirm_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.confirm_var, width=30, show="*").pack(pady=5)
        
        # Nút
        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Đăng ký", command=self.register).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Quay lại", command=self.show_login_form).pack(side="left", padx=5)
    
    def register(self):
        # Lấy dữ liệu từ form
        fullname = self.fullname_var.get().strip()
        email = self.reg_email_var.get().strip()
        password = self.reg_password_var.get()
        confirm = self.confirm_var.get()
        
        # Kiểm tra dữ liệu
        if not fullname or len(fullname) < 3:
            messagebox.showerror("Lỗi", "Họ tên phải có ít nhất 3 ký tự")
            return
            
        if not email or "@" not in email:
            messagebox.showerror("Lỗi", "Email không hợp lệ")
            return
            
        if not password or len(password) < 6:
            messagebox.showerror("Lỗi", "Mật khẩu phải có ít nhất 6 ký tự")
            return
            
        if password != confirm:
            messagebox.showerror("Lỗi", "Mật khẩu xác nhận không khớp")
            return
        
        # Đọc dữ liệu người dùng
        with open(self.users_file, 'r') as f:
            users = json.load(f)
        
        # Kiểm tra email đã tồn tại chưa
        for user in users:
            if user.get('email') == email:
                messagebox.showerror("Lỗi", "Email đã được sử dụng")
                return
        
        # Thêm người dùng mới
        users.append({
            'fullname': fullname,
            'email': email,
            'password': password,
            'role': 'user'  # Vai trò mặc định là user
        })
        
        # Lưu dữ liệu
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=4)
        
        messagebox.showinfo("Thành công", "Đăng ký tài khoản thành công!")
        self.show_login_form()
    
    def login(self):
        # Lấy dữ liệu từ form
        email = self.email_var.get().strip()
        password = self.password_var.get()
        
        # Đọc dữ liệu người dùng
        with open(self.users_file, 'r') as f:
            users = json.load(f)
        
        # Kiểm tra thông tin đăng nhập
        for user in users:
            if user.get('email') == email and user.get('password') == password:
                self.current_user = user
                messagebox.showinfo("Thành công", f"Chào mừng, {user.get('fullname')}!")
                self.show_dashboard()
                return
        
        messagebox.showerror("Lỗi", "Email hoặc mật khẩu không đúng")
    
    def show_dashboard(self):
        # Xóa các widget hiện tại
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Tạo giao diện chính
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)
        
        # Tạo menu bên trái
        menu_frame = ttk.Frame(main_frame, width=200)
        menu_frame.pack(side="left", fill="y")
        
        ttk.Label(menu_frame, text="MENU", font=('Arial', 14)).pack(pady=10)
        
        # Nút menu
        ttk.Button(menu_frame, text="Dashboard", command=self.show_dashboard, width=20).pack(pady=5)
        ttk.Button(menu_frame, text="Từ vựng", command=self.show_vocabulary, width=20).pack(pady=5)
        ttk.Button(menu_frame, text="Tài khoản", command=self.show_profile, width=20).pack(pady=5)
        ttk.Button(menu_frame, text="Đăng xuất", command=self.logout, width=20).pack(pady=5)
        
        # Hiển thị thông tin người dùng
        user_info = ttk.Frame(menu_frame, padding=10)
        user_info.pack(side="bottom", fill="x")
        
        ttk.Label(user_info, text=f"Đăng nhập như: {self.current_user.get('fullname')}").pack()
        ttk.Label(user_info, text=f"Vai trò: {self.current_user.get('role')}").pack()
        
        # Nội dung chính
        content_frame = ttk.Frame(main_frame, padding=20)
        content_frame.pack(side="right", fill="both", expand=True)
        
        # Tiêu đề
        ttk.Label(content_frame, text="Dashboard", font=('Arial', 16)).pack(anchor="w", pady=10)
        
        # Thống kê
        stats_frame = ttk.Frame(content_frame)
        stats_frame.pack(fill="x", pady=10)
        
        # Đếm số lượng từ vựng và người dùng
        vocab_count = self.count_vocabulary()
        user_count, admin_count = self.count_users()
        
        # Hiển thị thống kê
        stat1 = ttk.LabelFrame(stats_frame, text="Từ vựng")
        stat1.pack(side="left", padx=10, fill="both", expand=True)
        ttk.Label(stat1, text=str(vocab_count), font=('Arial', 20)).pack(pady=10)
        
        stat2 = ttk.LabelFrame(stats_frame, text="Người dùng")
        stat2.pack(side="left", padx=10, fill="both", expand=True)
        ttk.Label(stat2, text=str(user_count), font=('Arial', 20)).pack(pady=10)
        
        stat3 = ttk.LabelFrame(stats_frame, text="Quản trị viên")
        stat3.pack(side="left", padx=10, fill="both", expand=True)
        ttk.Label(stat3, text=str(admin_count), font=('Arial', 20)).pack(pady=10)
        
        # Tìm kiếm
        search_frame = ttk.Frame(content_frame)
        search_frame.pack(fill="x", pady=10)
        
        ttk.Label(search_frame, text="Tìm kiếm từ vựng:").pack(side="left")
        self.search_var = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.search_var, width=30).pack(side="left", padx=5)
        ttk.Button(search_frame, text="Tìm", command=self.search_vocabulary).pack(side="left")
        
        # Tiêu đề và nút thêm từ mới
        vocab_header = ttk.Frame(content_frame)
        vocab_header.pack(fill="x", pady=10)
        
        ttk.Label(vocab_header, text="Danh sách từ vựng", font=('Arial', 14)).pack(side="left")
        
        # Chỉ hiển thị nút thêm nếu là admin
        if self.current_user.get('role') == 'admin':
            ttk.Button(vocab_header, text="Thêm từ mới", command=self.add_vocabulary).pack(side="right")
        
        # Danh sách từ vựng
        vocab_frame = ttk.Frame(content_frame)
        vocab_frame.pack(fill="both", expand=True)
        
        # Tạo Treeview để hiển thị từ vựng
        columns = ("word", "meaning", "example")
        self.vocab_tree = ttk.Treeview(vocab_frame, columns=columns, show="headings")
        
        # Thêm thanh cuộn
        scrollbar = ttk.Scrollbar(vocab_frame, orient="vertical", command=self.vocab_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.vocab_tree.configure(yscrollcommand=scrollbar.set)
        
        # Đặt tiêu đề cột
        self.vocab_tree.heading("word", text="Từ vựng")
        self.vocab_tree.heading("meaning", text="Nghĩa")
        self.vocab_tree.heading("example", text="Ví dụ")
        
        # Đặt độ rộng cột
        self.vocab_tree.column("word", width=150)
        self.vocab_tree.column("meaning", width=200)
        self.vocab_tree.column("example", width=300)
        
        self.vocab_tree.pack(fill="both", expand=True)
        
        # Gắn sự kiện double-click để xem chi tiết
        self.vocab_tree.bind("<Double-1>", self.view_vocabulary)
        
        # Tải danh sách từ vựng
        self.load_vocabulary()
    
    def count_vocabulary(self):
        """Đếm số lượng từ vựng"""
        try:
            with open(self.vocab_file, 'r') as f:
                vocabulary = json.load(f)
                return len(vocabulary)
        except:
            return 0
    
    def count_users(self):
        """Đếm số lượng người dùng và admin"""
        try:
            with open(self.users_file, 'r') as f:
                users = json.load(f)
                admin_count = sum(1 for user in users if user.get('role') == 'admin')
                user_count = len(users) - admin_count
                return user_count, admin_count
        except:
            return 0, 0
    
    def load_vocabulary(self, search_term=""):
        """Tải danh sách từ vựng"""
        # Xóa dữ liệu cũ
        for item in self.vocab_tree.get_children():
            self.vocab_tree.delete(item)
        
        try:
            with open(self.vocab_file, 'r') as f:
                vocabulary = json.load(f)
            
            # Lọc theo từ khóa tìm kiếm
            if search_term:
                search_term = search_term.lower()
                vocabulary = [v for v in vocabulary if search_term in v.get('word', '').lower() or 
                                                    search_term in v.get('meaning', '').lower()]
            
            # Thêm từ vào danh sách
            for vocab in vocabulary:
                self.vocab_tree.insert("", "end", values=(
                    vocab.get('word', ''),
                    vocab.get('meaning', ''),
                    vocab.get('example', '')
                ))
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu: {str(e)}")
    
    def search_vocabulary(self):
        """Tìm kiếm từ vựng"""
        search_term = self.search_var.get().strip()
        self.load_vocabulary(search_term)
    
    def view_vocabulary(self, event):
        """Xem chi tiết từ vựng"""
        # Lấy mục đã chọn
        selected = self.vocab_tree.selection()
        if not selected:
            return
        
        # Lấy giá trị của mục đã chọn
        values = self.vocab_tree.item(selected[0], 'values')
        if not values:
            return
        
        word = values[0]
        
        # Tìm từ vựng trong file JSON
        try:
            with open(self.vocab_file, 'r') as f:
                vocabulary = json.load(f)
            
            # Tìm từ vựng
            vocab_item = next((v for v in vocabulary if v.get('word') == word), None)
            if not vocab_item:
                return
            
            # Tạo cửa sổ xem chi tiết
            view_window = tk.Toplevel(self.root)
            view_window.title(f"Chi tiết: {word}")
            view_window.geometry("400x300")
            
            # Khung nội dung
            frame = ttk.Frame(view_window, padding=20)
            frame.pack(fill="both", expand=True)
            
            # Hiển thị thông tin
            ttk.Label(frame, text="Từ vựng:", font=('Arial', 12, 'bold')).pack(anchor="w")
            ttk.Label(frame, text=vocab_item.get('word', '')).pack(anchor="w", pady=(0, 10))
            
            ttk.Label(frame, text="Nghĩa:", font=('Arial', 12, 'bold')).pack(anchor="w")
            ttk.Label(frame, text=vocab_item.get('meaning', '')).pack(anchor="w", pady=(0, 10))
            
            ttk.Label(frame, text="Ví dụ:", font=('Arial', 12, 'bold')).pack(anchor="w")
            example_text = tk.Text(frame, height=5, width=40, wrap="word")
            example_text.insert("1.0", vocab_item.get('example', ''))
            example_text.config(state="disabled")  # Chỉ đọc
            example_text.pack(pady=(0, 10))
            
            # Nút điều khiển
            button_frame = ttk.Frame(frame)
            button_frame.pack(fill="x", pady=10)
            
            # Nút sửa và xóa chỉ hiển thị cho admin
            if self.current_user.get('role') == 'admin':
                ttk.Button(button_frame, text="Sửa", 
                         command=lambda: self.edit_vocabulary(vocab_item, view_window)).pack(side="left", padx=5)
                
                ttk.Button(button_frame, text="Xóa", 
                         command=lambda: self.delete_vocabulary(vocab_item, view_window)).pack(side="left", padx=5)
            
            ttk.Button(button_frame, text="Đóng", command=view_window.destroy).pack(side="right")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể mở chi tiết: {str(e)}")
    
    def add_vocabulary(self):
        """Thêm từ vựng mới (chỉ dành cho admin)"""
        if self.current_user.get('role') != 'admin':
            messagebox.showerror("Lỗi", "Bạn không có quyền thêm từ vựng")
            return
        
        # Tạo cửa sổ thêm từ
        add_window = tk.Toplevel(self.root)
        add_window.title("Thêm từ vựng mới")
        add_window.geometry("400x350")
        
        # Khung nội dung
        frame = ttk.Frame(add_window, padding=20)
        frame.pack(fill="both", expand=True)
        
        # Form nhập liệu
        ttk.Label(frame, text="Từ vựng:").pack(anchor="w", pady=5)
        word_var = tk.StringVar()
        ttk.Entry(frame, textvariable=word_var, width=30).pack(fill="x")
        
        ttk.Label(frame, text="Nghĩa:").pack(anchor="w", pady=5)
        meaning_var = tk.StringVar()
        ttk.Entry(frame, textvariable=meaning_var, width=30).pack(fill="x")
        
        ttk.Label(frame, text="Ví dụ:").pack(anchor="w", pady=5)
        example_text = tk.Text(frame, height=5, width=30)
        example_text.pack(fill="x")
        
        # Nút điều khiển
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill="x", pady=20)
        
        # Hàm lưu từ vựng
        def save_vocabulary():
            word = word_var.get().strip()
            meaning = meaning_var.get().strip()
            example = example_text.get("1.0", "end-1c").strip()
            
            if not word or not meaning:
                messagebox.showerror("Lỗi", "Từ vựng và nghĩa không được để trống")
                return
            
            try:
                with open(self.vocab_file, 'r') as f:
                    vocabulary = json.load(f)
                
                # Kiểm tra từ đã tồn tại chưa
                if any(v.get('word') == word for v in vocabulary):
                    messagebox.showerror("Lỗi", f"Từ vựng '{word}' đã tồn tại")
                    return
                
                # Thêm từ mới
                vocabulary.append({
                    'word': word,
                    'meaning': meaning,
                    'example': example,
                    'added_by': self.current_user.get('email')
                })
                
                with open(self.vocab_file, 'w') as f:
                    json.dump(vocabulary, f, indent=4)
                
                messagebox.showinfo("Thành công", f"Đã thêm từ vựng '{word}'")
                add_window.destroy()
                self.load_vocabulary()  # Tải lại danh sách
                
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể lưu từ vựng: {str(e)}")
        
        ttk.Button(button_frame, text="Lưu", command=save_vocabulary).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Hủy", command=add_window.destroy).pack(side="right")
    
    def edit_vocabulary(self, vocab_item, parent_window):
        """Sửa từ vựng (chỉ dành cho admin)"""
        if self.current_user.get('role') != 'admin':
            messagebox.showerror("Lỗi", "Bạn không có quyền sửa từ vựng")
            return
        
        # Đóng cửa sổ chi tiết
        parent_window.destroy()
        
        # Tạo cửa sổ sửa từ
        edit_window = tk.Toplevel(self.root)
        edit_window.title(f"Sửa từ vựng: {vocab_item.get('word')}")
        edit_window.geometry("400x350")
        
        # Khung nội dung
        frame = ttk.Frame(edit_window, padding=20)
        frame.pack(fill="both", expand=True)
        
        # Form nhập liệu
        ttk.Label(frame, text="Từ vựng:").pack(anchor="w", pady=5)
        word_var = tk.StringVar(value=vocab_item.get('word', ''))
        ttk.Entry(frame, textvariable=word_var, width=30).pack(fill="x")
        
        ttk.Label(frame, text="Nghĩa:").pack(anchor="w", pady=5)
        meaning_var = tk.StringVar(value=vocab_item.get('meaning', ''))
        ttk.Entry(frame, textvariable=meaning_var, width=30).pack(fill="x")
        
        ttk.Label(frame, text="Ví dụ:").pack(anchor="w", pady=5)
        example_text = tk.Text(frame, height=5, width=30)
        example_text.insert("1.0", vocab_item.get('example', ''))
        example_text.pack(fill="x")
        
        # Nút điều khiển
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill="x", pady=20)
        
        # Hàm lưu thay đổi
        def save_changes():
            word = word_var.get().strip()
            meaning = meaning_var.get().strip()
            example = example_text.get("1.0", "end-1c").strip()
            
            if not word or not meaning:
                messagebox.showerror("Lỗi", "Từ vựng và nghĩa không được để trống")
                return
            
            try:
                with open(self.vocab_file, 'r') as f:
                    vocabulary = json.load(f)
                
                # Kiểm tra từ đã tồn tại chưa (nếu đã đổi từ)
                if word != vocab_item.get('word') and any(v.get('word') == word for v in vocabulary):
                    messagebox.showerror("Lỗi", f"Từ vựng '{word}' đã tồn tại")
                    return
                
                # Cập nhật từ vựng
                for v in vocabulary:
                    if v.get('word') == vocab_item.get('word'):
                        v['word'] = word
                        v['meaning'] = meaning
                        v['example'] = example
                        v['updated_by'] = self.current_user.get('email')
                        break
                
                with open(self.vocab_file, 'w') as f:
                    json.dump(vocabulary, f, indent=4)
                
                messagebox.showinfo("Thành công", f"Đã cập nhật từ vựng '{word}'")
                edit_window.destroy()
                self.load_vocabulary()  # Tải lại danh sách
                
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể cập nhật từ vựng: {str(e)}")
        
        ttk.Button(button_frame, text="Lưu", command=save_changes).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Hủy", command=edit_window.destroy).pack(side="right")
    
    def delete_vocabulary(self, vocab_item, parent_window):
        """Xóa từ vựng (chỉ dành cho admin)"""
        if self.current_user.get('role') != 'admin':
            messagebox.showerror("Lỗi", "Bạn không có quyền xóa từ vựng")
            return
        
        # Xác nhận xóa
        confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa từ '{vocab_item.get('word')}'?")
        if not confirm:
            return
        
        try:
            with open(self.vocab_file, 'r') as f:
                vocabulary = json.load(f)
            
            # Xóa từ vựng
            vocabulary = [v for v in vocabulary if v.get('word') != vocab_item.get('word')]
            
            with open(self.vocab_file, 'w') as f:
                json.dump(vocabulary, f, indent=4)
            
            messagebox.showinfo("Thành công", f"Đã xóa từ vựng '{vocab_item.get('word')}'")
            parent_window.destroy()
            self.load_vocabulary()  # Tải lại danh sách
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xóa từ vựng: {str(e)}")
    
    def show_vocabulary(self):
        """Hiển thị trang từ vựng"""
        # Hiện tại chỉ chuyển hướng về dashboard
        self.show_dashboard()
    
    def show_profile(self):
        """Hiển thị trang quản lý tài khoản"""
        # Xóa các widget hiện tại
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Tạo giao diện chính
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)
        
        # Tạo menu bên trái (giống dashboard)
        menu_frame = ttk.Frame(main_frame, width=200)
        menu_frame.pack(side="left", fill="y")
        
        ttk.Label(menu_frame, text="MENU", font=('Arial', 14)).pack(pady=10)
        
        # Nút menu
        ttk.Button(menu_frame, text="Dashboard", command=self.show_dashboard, width=20).pack(pady=5)
        ttk.Button(menu_frame, text="Từ vựng", command=self.show_vocabulary, width=20).pack(pady=5)
        ttk.Button(menu_frame, text="Tài khoản", command=self.show_profile, width=20).pack(pady=5)
        ttk.Button(menu_frame, text="Đăng xuất", command=self.logout, width=20).pack(pady=5)
        
        # Hiển thị thông tin người dùng
        user_info = ttk.Frame(menu_frame, padding=10)
        user_info.pack(side="bottom", fill="x")
        
        ttk.Label(user_info, text=f"Đăng nhập như: {self.current_user.get('fullname')}").pack()
        ttk.Label(user_info, text=f"Vai trò: {self.current_user.get('role')}").pack()
        
        # Nội dung chính
        content_frame = ttk.Frame(main_frame, padding=20)
        content_frame.pack(side="right", fill="both", expand=True)
        
        # Tiêu đề
        ttk.Label(content_frame, text="Quản lý tài khoản", font=('Arial', 16)).pack(anchor="w", pady=10)
        
        # Hiển thị thông tin người dùng
        info_frame = ttk.Frame(content_frame, padding=10)
        info_frame.pack(fill="x", pady=10)
        
        ttk.Label(info_frame, text="Họ và tên:", font=('Arial', 12, 'bold')).grid(row=0, column=0, sticky="w", pady=5)
        ttk.Label(info_frame, text=self.current_user.get('fullname')).grid(row=0, column=1, sticky="w", pady=5)
        
        ttk.Label(info_frame, text="Email:", font=('Arial', 12, 'bold')).grid(row=1, column=0, sticky="w", pady=5)
        ttk.Label(info_frame, text=self.current_user.get('email')).grid(row=1, column=1, sticky="w", pady=5)
        
        ttk.Label(info_frame, text="Vai trò:", font=('Arial', 12, 'bold')).grid(row=2, column=0, sticky="w", pady=5)
        ttk.Label(info_frame, text=self.current_user.get('role')).grid(row=2, column=1, sticky="w", pady=5)
        
        # Nút chức năng
        button_frame = ttk.Frame(content_frame)
        button_frame.pack(fill="x", pady=20)
        
        ttk.Button(button_frame, text="Đổi mật khẩu", command=self.change_password).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cập nhật thông tin", command=self.edit_profile).pack(side="left", padx=5)
        
        # Hiển thị phần quản lý người dùng cho admin
        if self.current_user.get('role') == 'admin':
            admin_frame = ttk.Frame(content_frame)
            admin_frame.pack(fill="x", pady=20)
            
            ttk.Label(admin_frame, text="Quản lý người dùng (Admin)", font=('Arial', 14, 'bold')).pack(anchor="w", pady=10)
            ttk.Button(admin_frame, text="Quản lý người dùng", command=self.manage_users).pack(anchor="w")
    
    def change_password(self):
        """Đổi mật khẩu"""
        # Tạo cửa sổ đổi mật khẩu
        change_window = tk.Toplevel(self.root)
        change_window.title("Đổi mật khẩu")
        change_window.geometry("400x250")
        
        # Khung nội dung
        frame = ttk.Frame(change_window, padding=20)
        frame.pack(fill="both", expand=True)
        
        # Form nhập liệu
        ttk.Label(frame, text="Mật khẩu hiện tại:").pack(anchor="w", pady=5)
        current_var = tk.StringVar()
        ttk.Entry(frame, textvariable=current_var, show="*", width=30).pack(fill="x")
        
        ttk.Label(frame, text="Mật khẩu mới:").pack(anchor="w", pady=5)
        new_var = tk.StringVar()
        ttk.Entry(frame, textvariable=new_var, show="*", width=30).pack(fill="x")
        
        ttk.Label(frame, text="Xác nhận mật khẩu mới:").pack(anchor="w", pady=5)
        confirm_var = tk.StringVar()
        ttk.Entry(frame, textvariable=confirm_var, show="*", width=30).pack(fill="x")
        
        # Nút điều khiển
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill="x", pady=20)
        
        # Hàm lưu mật khẩu mới
        def save_password():
            current = current_var.get()
            new = new_var.get()
            confirm = confirm_var.get()
            
            # Kiểm tra mật khẩu hiện tại
            if current != self.current_user.get('password'):
                messagebox.showerror("Lỗi", "Mật khẩu hiện tại không đúng")
                return
            
            # Kiểm tra mật khẩu mới
            if len(new) < 6:
                messagebox.showerror("Lỗi", "Mật khẩu mới phải có ít nhất 6 ký tự")
                return
            
            # Kiểm tra xác nhận
            if new != confirm:
                messagebox.showerror("Lỗi", "Mật khẩu xác nhận không khớp")
                return
            
            try:
                with open(self.users_file, 'r') as f:
                    users = json.load(f)
                
                # Cập nhật mật khẩu
                for user in users:
                    if user.get('email') == self.current_user.get('email'):
                        user['password'] = new
                        self.current_user = user  # Cập nhật người dùng hiện tại
                        break
                
                with open(self.users_file, 'w') as f:
                    json.dump(users, f, indent=4)
                
                messagebox.showinfo("Thành công", "Đổi mật khẩu thành công!")
                change_window.destroy()
                
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể cập nhật mật khẩu: {str(e)}")
        
        ttk.Button(button_frame, text="Lưu", command=save_password).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Hủy", command=change_window.destroy).pack(side="right")
    
    def edit_profile(self):
        """Cập nhật thông tin cá nhân"""
        # Tạo cửa sổ cập nhật thông tin
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Cập nhật thông tin")
        edit_window.geometry("400x150")
        
        # Khung nội dung
        frame = ttk.Frame(edit_window, padding=20)
        frame.pack(fill="both", expand=True)
        
        # Form nhập liệu
        ttk.Label(frame, text="Họ và tên:").pack(anchor="w", pady=5)
        fullname_var = tk.StringVar(value=self.current_user.get('fullname', ''))
        ttk.Entry(frame, textvariable=fullname_var, width=30).pack(fill="x")
        
        # Nút điều khiển
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill="x", pady=20)
        
        # Hàm lưu thông tin
        def save_profile():
            fullname = fullname_var.get().strip()
            
            if not fullname or len(fullname) < 3:
                messagebox.showerror("Lỗi", "Họ tên phải có ít nhất 3 ký tự")
                return
            
            try:
                with open(self.users_file, 'r') as f:
                    users = json.load(f)
                
                # Cập nhật thông tin
                for user in users:
                    if user.get('email') == self.current_user.get('email'):
                        user['fullname'] = fullname
                        self.current_user = user  # Cập nhật người dùng hiện tại
                        break
                
                with open(self.users_file, 'w') as f:
                    json.dump(users, f, indent=4)
                
                messagebox.showinfo("Thành công", "Cập nhật thông tin thành công!")
                edit_window.destroy()
                self.show_profile()  # Tải lại trang profile
                
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể cập nhật thông tin: {str(e)}")
        
        ttk.Button(button_frame, text="Lưu", command=save_profile).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Hủy", command=edit_window.destroy).pack(side="right")
    
    def manage_users(self):
        """Quản lý người dùng (chỉ dành cho admin)"""
        if self.current_user.get('role') != 'admin':
            messagebox.showerror("Lỗi", "Bạn không có quyền quản lý người dùng")
            return
        
        # Tạo cửa sổ quản lý người dùng
        manage_window = tk.Toplevel(self.root)
        manage_window.title("Quản lý người dùng")
        manage_window.geometry("600x400")
        
        # Khung nội dung
        frame = ttk.Frame(manage_window, padding=20)
        frame.pack(fill="both", expand=True)
        
        # Tiêu đề
        ttk.Label(frame, text="Danh sách người dùng", font=('Arial', 14)).pack(anchor="w", pady=10)
        
        # Danh sách người dùng
        list_frame = ttk.Frame(frame)
        list_frame.pack(fill="both", expand=True)
        
        # Tạo Treeview
        columns = ("fullname", "email", "role")
        user_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        # Thêm thanh cuộn
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=user_tree.yview)
        scrollbar.pack(side="right", fill="y")
        user_tree.configure(yscrollcommand=scrollbar.set)
        
        # Đặt tiêu đề cột
        user_tree.heading("fullname", text="Họ và tên")
        user_tree.heading("email", text="Email")
        user_tree.heading("role", text="Vai trò")
        
        # Đặt độ rộng cột
        user_tree.column("fullname", width=200)
        user_tree.column("email", width=200)
        user_tree.column("role", width=100)
        
        user_tree.pack(fill="both", expand=True)
        
        # Tải danh sách người dùng
        try:
            with open(self.users_file, 'r') as f:
                users = json.load(f)
            
            for user in users:
                user_tree.insert("", "end", values=(
                    user.get('fullname', ''),
                    user.get('email', ''),
                    user.get('role', '')
                ))
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải danh sách người dùng: {str(e)}")
        
        # Nút chức năng
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill="x", pady=10)
        
        # Hàm thêm người dùng
        def add_user():
            # Tạo cửa sổ thêm người dùng
            add_window = tk.Toplevel(manage_window)
            add_window.title("Thêm người dùng")
            add_window.geometry("400x300")
            
            # Khung nội dung
            add_frame = ttk.Frame(add_window, padding=20)
            add_frame.pack(fill="both", expand=True)
            
            # Form nhập liệu
            ttk.Label(add_frame, text="Họ và tên:").pack(anchor="w", pady=5)
            fullname_var = tk.StringVar()
            ttk.Entry(add_frame, textvariable=fullname_var, width=30).pack(fill="x")
            
            ttk.Label(add_frame, text="Email:").pack(anchor="w", pady=5)
            email_var = tk.StringVar()
            ttk.Entry(add_frame, textvariable=email_var, width=30).pack(fill="x")
            
            ttk.Label(add_frame, text="Mật khẩu:").pack(anchor="w", pady=5)
            password_var = tk.StringVar()
            ttk.Entry(add_frame, textvariable=password_var, width=30, show="*").pack(fill="x")
            
            # Chọn vai trò
            ttk.Label(add_frame, text="Vai trò:").pack(anchor="w", pady=5)
            role_var = tk.StringVar(value="user")
            
            role_frame = ttk.Frame(add_frame)
            role_frame.pack(fill="x")
            
            ttk.Radiobutton(role_frame, text="Người dùng", variable=role_var, value="user").pack(side="left", padx=5)
            ttk.Radiobutton(role_frame, text="Quản trị viên", variable=role_var, value="admin").pack(side="left")
            
            # Nút chức năng
            add_button_frame = ttk.Frame(add_frame)
            add_button_frame.pack(fill="x", pady=20)
            
            # Hàm lưu người dùng
            def save_user():
                fullname = fullname_var.get().strip()
                email = email_var.get().strip()
                password = password_var.get()
                role = role_var.get()
                
                # Kiểm tra dữ liệu
                if not fullname or len(fullname) < 3:
                    messagebox.showerror("Lỗi", "Họ tên phải có ít nhất 3 ký tự")
                    return
                
                if not email or "@" not in email:
                    messagebox.showerror("Lỗi", "Email không hợp lệ")
                    return
                
                if not password or len(password) < 6:
                    messagebox.showerror("Lỗi", "Mật khẩu phải có ít nhất 6 ký tự")
                    return
                
                try:
                    with open(self.users_file, 'r') as f:
                        users = json.load(f)
                    
                    # Kiểm tra email đã tồn tại chưa
                    if any(u.get('email') == email for u in users):
                        messagebox.showerror("Lỗi", "Email đã được sử dụng")
                        return
                    
                    # Thêm người dùng mới
                    users.append({
                        'fullname': fullname,
                        'email': email,
                        'password': password,
                        'role': role
                    })
                    
                    with open(self.users_file, 'w') as f:
                        json.dump(users, f, indent=4)
                    
                    messagebox.showinfo("Thành công", "Thêm người dùng thành công!")
                    add_window.destroy()
                    
                    # Tải lại danh sách
                    user_tree.delete(*user_tree.get_children())
                    for user in users:
                        user_tree.insert("", "end", values=(
                            user.get('fullname', ''),
                            user.get('email', ''),
                            user.get('role', '')
                        ))
                    
                except Exception as e:
                    messagebox.showerror("Lỗi", f"Không thể thêm người dùng: {str(e)}")
            
            ttk.Button(add_button_frame, text="Lưu", command=save_user).pack(side="left", padx=5)
            ttk.Button(add_button_frame, text="Hủy", command=add_window.destroy).pack(side="right")
        
        # Hàm xóa người dùng
        def delete_user():
            # Lấy mục đã chọn
            selected = user_tree.selection()
            if not selected:
                messagebox.showerror("Lỗi", "Vui lòng chọn một người dùng để xóa")
                return
            
            # Lấy email của người dùng đã chọn
            values = user_tree.item(selected[0], 'values')
            if not values:
                return
            
            email = values[1]
            
            # Không thể xóa chính mình
            if email == self.current_user.get('email'):
                messagebox.showerror("Lỗi", "Bạn không thể xóa tài khoản của chính mình")
                return
            
            # Xác nhận xóa
            confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa người dùng '{email}'?")
            if not confirm:
                return
            
            try:
                with open(self.users_file, 'r') as f:
                    users = json.load(f)
                
                # Xóa người dùng
                users = [u for u in users if u.get('email') != email]
                
                with open(self.users_file, 'w') as f:
                    json.dump(users, f, indent=4)
                
                messagebox.showinfo("Thành công", f"Đã xóa người dùng '{email}'")
                
                # Tải lại danh sách
                user_tree.delete(*user_tree.get_children())
                for user in users:
                    user_tree.insert("", "end", values=(
                        user.get('fullname', ''),
                        user.get('email', ''),
                        user.get('role', '')
                    ))
                
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xóa người dùng: {str(e)}")
        
        # Hàm thay đổi vai trò
        def change_role():
            # Lấy mục đã chọn
            selected = user_tree.selection()
            if not selected:
                messagebox.showerror("Lỗi", "Vui lòng chọn một người dùng để thay đổi vai trò")
                return
            
            # Lấy email và vai trò hiện tại
            values = user_tree.item(selected[0], 'values')
            if not values:
                return
            
            email = values[1]
            current_role = values[2]
            
            # Không thể thay đổi vai trò của chính mình
            if email == self.current_user.get('email'):
                messagebox.showerror("Lỗi", "Bạn không thể thay đổi vai trò của chính mình")
                return
            
            # Vai trò mới là ngược lại vai trò hiện tại
            new_role = "user" if current_role == "admin" else "admin"
            
            # Xác nhận thay đổi
            confirm = messagebox.askyesno("Xác nhận", 
                                        f"Bạn có chắc muốn thay đổi vai trò của '{email}' từ '{current_role}' thành '{new_role}'?")
            if not confirm:
                return
            
            try:
                with open(self.users_file, 'r') as f:
                    users = json.load(f)
                
                # Thay đổi vai trò
                for user in users:
                    if user.get('email') == email:
                        user['role'] = new_role
                        break
                
                with open(self.users_file, 'w') as f:
                    json.dump(users, f, indent=4)
                
                messagebox.showinfo("Thành công", f"Đã thay đổi vai trò của '{email}' thành '{new_role}'")
                
                # Tải lại danh sách
                user_tree.delete(*user_tree.get_children())
                for user in users:
                    user_tree.insert("", "end", values=(
                        user.get('fullname', ''),
                        user.get('email', ''),
                        user.get('role', '')
                    ))
                
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể thay đổi vai trò: {str(e)}")
        
        # Thêm các nút chức năng
        ttk.Button(button_frame, text="Thêm người dùng", command=add_user).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Xóa người dùng", command=delete_user).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Thay đổi vai trò", command=change_role).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Đóng", command=manage_window.destroy).pack(side="right")
    
    def logout(self):
        """Đăng xuất"""
        self.current_user = None
        self.show_login_form()

# Hàm main để chạy ứng dụng
def main():
    root = tk.Tk()
    app = VocabularyApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()