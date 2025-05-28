# profile.py

class EditProfileWindow:
    def __init__(self, parent):
        self.frame = tk.Frame(parent)
        self.frame.pack(fill="both", expand=True)
        
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.frame, text="Chỉnh sửa hồ sơ", font=("Arial", 16)).pack(pady=10)
        
        tk.Label(self.frame, text="Tên:").pack(pady=5)
        self.name_entry = tk.Entry(self.frame)
        self.name_entry.pack(pady=5)
        
        tk.Label(self.frame, text="Email:").pack(pady=5)
        self.email_entry = tk.Entry(self.frame)
        self.email_entry.pack(pady=5)
        
        tk.Button(self.frame, text="Lưu thay đổi", command=self.save_profile).pack(pady=10)

    def save_profile(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        
        # Kiểm tra và lưu thông tin
        if name and email:
            print("Thông tin đã được cập nhật.")
