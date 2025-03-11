### Xây dựng ứng dụng quản lý từ vựng tiếng Anh

#### Chức năng chính
- Ứng dụng cho phép quản trị viên quản lý (CRUD) tài khoản và phân quyền người dùng.  
- Người dùng có thể xem, tìm kiếm, lưu từ vựng và tải từ vựng đã lưu về máy.  
- Quản trị viên có thể quản lý (CRUD) từ vựng, nhập từ vựng từ file JSON hoặc tải từ vựng từ nguồn bên ngoài về ứng dụng.  


### Design giao diện

#### **Màn hình đăng nhập (Login)**
- Ô nhập **Email/Username**
- Ô nhập **Mật khẩu**
- Nút **Đăng nhập**
- Nút **Quên mật khẩu?**
- Nút **Đăng ký tài khoản mới** (dẫn đến màn hình đăng ký)
- Hiển thị thông báo lỗi nếu nhập sai tài khoản/mật khẩu

#### **Màn hình đăng ký (Register)**
- Ô nhập **Họ và tên**
- Ô nhập **Email**
- Ô nhập **Mật khẩu**
- Ô nhập **Xác nhận mật khẩu**
- Nút **Đăng ký**
- Nút **Quay lại đăng nhập**
- Thông báo lỗi nếu nhập sai hoặc thiếu thông tin

#### **Màn hình trang chủ (Dashboard)**
- Thanh **Menu điều hướng** (Dashboard, Từ vựng, Quản lý tài khoản, Đăng xuất)
- Thống kê số lượng từ vựng đã lưu
- **Tìm kiếm từ vựng**
- Danh sách **từ vựng gần đây**
- Nút **Thêm từ vựng mới**

#### **Màn hình quản lý từ vựng (Vocabulary Management)**
- Danh sách **từ vựng đã lưu**
- Ô **tìm kiếm từ vựng**
- **Bộ lọc** theo danh mục, ngày thêm, trạng thái
- Nút **Thêm từ vựng mới**
- Nút **Chỉnh sửa/Xóa từ vựng**
- Nút **Nhập từ file JSON**
- Nút **Xuất từ vựng ra file**

#### **Màn hình thêm/sửa từ vựng**
- Ô nhập **Từ vựng**
- Ô nhập **Nghĩa của từ**
- Ô nhập **Loại từ** (danh từ, động từ, tính từ,...)
- Ô nhập **Ví dụ sử dụng**
- Tùy chọn **thêm Ghi chú**
- Nút **Lưu lại**
- Nút **Hủy**

#### **Màn hình nhập từ vựng từ file JSON**
- Khu vực **kéo-thả hoặc chọn file JSON**
- Hiển thị danh sách **từ vựng trong file JSON**
- Nút **Nhập dữ liệu**
- Nút **Hủy**

#### **Màn hình tải từ vựng về máy**
- Tùy chọn **xuất file** (JSON, CSV, TXT)
- Nút **Tải xuống**
- Nút **Hủy**

#### **Màn hình quản lý tài khoản (User Management)**
- **Chỉ dành cho quản trị viên**
- Danh sách **tài khoản người dùng**
- Nút **Thêm tài khoản mới**
- Nút **Chỉnh sửa/Xóa tài khoản**
- Tùy chọn **Phân quyền** (admin/user)

#### **Màn hình hồ sơ cá nhân (User Profile)**
- Hiển thị **Tên, Email, Ảnh đại diện**
- Nút **Chỉnh sửa thông tin cá nhân**
- Nút **Đổi mật khẩu**
- Nút **Đăng xuất**

#### **Màn hình phân quyền người dùng**
- **Chỉ dành cho quản trị viên**
- Danh sách **người dùng**
- Tùy chọn **Cấp quyền**
