# Ứng dụng quản lý từ vựng Tiếng Anh


## Source Structure

```tree
project_root/
│── app/
│   │── main.py                     # Điểm khởi chạy ứng dụng
│   │── config.py                    # Cấu hình chung của ứng dụng
│   │── auth/                         
│   │   │── login.py                  # Xử lý đăng nhập
│   │   │── register.py               # Xử lý đăng ký
│   │   │── auth_utils.py             # Hàm tiện ích cho xác thực người dùng
│   │
│   │── models/                       
│   │   │── user_model.py             # Định nghĩa model User
│   │   │── vocabulary_model.py       # Định nghĩa model Vocabulary
│   │
│   │── views/                        
│   │   │── login_view.py             # Giao diện đăng nhập
│   │   │── register_view.py          # Giao diện đăng ký
│   │   │── dashboard_view.py         # Giao diện trang chủ
│   │   │── vocabulary_view.py        # Giao diện danh sách từ vựng
│   │   │── user_management_view.py   # Giao diện quản lý tài khoản
│   │   │── profile_view.py           # Giao diện hồ sơ cá nhân
│   │
│   │── controllers/                  
│   │   │── user_controller.py        # Xử lý logic tài khoản
│   │   │── vocabulary_controller.py  # Xử lý logic từ vựng
│   │   │── permission_controller.py  # Xử lý phân quyền
│   │
│   │── utils/                        
│   │   │── validators.py             # Xác thực dữ liệu đầu vào
│   │   │── file_handler.py           # Xử lý file nhập/xuất
│   │   │── database.py               # Kết nối và xử lý database
│   │
│   │── assets/                        # Chứa tài nguyên như icon, ảnh
│   │── data/                          # Chứa file JSON dữ liệu từ vựng
│
│── requirements.txt                   # Danh sách thư viện cần cài đặt
│── README.md                          # Hướng dẫn sử dụng
│── .gitignore                          # Các file cần bỏ qua khi đẩy lên git
```


## How to run
### First run
```bash
pip install -r requirements.txt
```

### Trigger run development app
```bash
python app/main.py
python -m app.main
```

## How to build

### First run
```bash
pip install --upgrade pip

#or 

pip install pyinstaller

```

### Trigger build
```bash
rm -rf build dist
rmdir /s build
rmdir /s dist
pyinstaller app.spec
```

---

### Another way

```bash
pyinstaller --name EnglishApp --add-data "app/data;app/data" --hidden-import auth --hidden-import home --hidden-import common --hidden-import utils --hidden-import app.auth --hidden-import app.home --hidden-import app.common --hidden-import app.utils app/main.py
pyinstaller --onefile --windowed app/main.py
```

### Cách để cài đặt một thư viện vào trong requirment.txt

```bash
pip install requests && pip freeze > requirements.txt
```

### Hướng dẫn sử dụng ứng dụng
```bash
admin: yennhi0906@gmail.com
pass: YENnhi0906@
user: yennhi2005@gmail.com
pass: YENnhi2005@
```
