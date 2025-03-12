# Xây dựng ứng dụng quản lý từ vựng tiếng Anh

## Chức năng chính
- Ứng dụng cho phép **quản trị viên** quản lý (CRUD) tài khoản và phân quyền người dùng.
- **Người dùng** có thể xem, tìm kiếm, lưu từ vựng và tải từ vựng đã lưu về máy.
- **Quản trị viên** có thể quản lý (CRUD) từ vựng, nhập từ vựng từ file JSON hoặc tải từ vựng từ nguồn bên ngoài về ứng dụng.

## Phân quyền
- **Người dùng bị hạn chế**:
  - Không thể chỉnh sửa, xóa từ vựng.
  - Không thể nhập từ file JSON.
  - Không thể quản lý tài khoản và phân quyền người dùng.
  - Chỉ có thể xem danh sách từ vựng công khai.

- **Những gì người dùng có thể thấy**:
  - Danh sách từ vựng.
  - Tìm kiếm và lọc từ vựng.
  - Tải xuống danh sách từ vựng.

- **Những gì quản trị viên có thể thấy**:
  - Tất cả nội dung mà người dùng có thể thấy.
  - Quản lý từ vựng (CRUD).
  - Quản lý tài khoản người dùng và phân quyền.

---

### **Màn hình đăng nhập (Login)**
- Ô nhập **Email/Username**.
- Ô nhập **Mật khẩu**.
- Nút **Đăng nhập** (mã hóa mật khẩu trước khi lưu).
- Nút **Đăng ký tài khoản mới** (dẫn đến màn hình đăng ký)( đăng ký cũng phải mã hoá mk).
- Hiển thị thông báo lỗi nếu nhập sai tài khoản/mật khẩu.

### **Màn hình đăng ký (Register)**
- Ô nhập **Họ và tên**. (kiểm tra xem người dùng nhập tên có hợp lệ không, vd: người dùng chỉ nhập một chữ cái, hay một chữ số thì không được....)
- Ô nhập **Email** (kiểm tra email hợp lệ).
- Ô nhập **Mật khẩu** (kiểm tra phải có ít nhất 8 ký tự, vd: bao gồm chữ hoa, chữ thường, chữ số, ký tự đặc biệt...).
- Ô nhập **Xác nhận mật khẩu**.
- Nút **Đăng ký**.(Trước khi nhấn nút đăng ký phải xác nhận tt đầu vào có hợp lệ ko ( mk phải có 8 kí tự, mk có chữ hoa, chữ thường, chữ số, kí tự đặc biệt ))
- Nút **Quay lại đăng nhập**.
- Thông báo lỗi nếu nhập sai hoặc thiếu thông tin.
 (gọi chung mấy cái kiểm tra đó là cần phải: xác nhận tt đầu vào trước khi đăng kí)

### **Màn hình trang chủ (Dashboard)**
- Thanh **Menu điều hướng** (Dashboard, Từ vựng, Quản lý tài khoản, Đăng xuất).
- Thống kê số lượng từ vựng đã lưu, số lượng người dùng và quản trị viên.
- **Tìm kiếm từ vựng**.
- **Danh sách từ vựng**.
- Nút **Thêm từ vựng mới** (chỉ dành cho quản trị viên).
- Người dùng bị giới hạn một số tính năng nào ở trong màn hình trang chủ (phân quyền)

### **Màn hình quản lý từ vựng (Vocabulary Management)**
- Danh sách **từ vựng đã lưu**.
- Ô **tìm kiếm từ vựng**.
- **Bộ lọc** theo từ loại, trường từ vựng,...
- Nút **Thêm từ vựng mới** (chỉ dành cho quản trị viên).
- Nút **Chỉnh sửa/Xóa từ vựng** (hiển thị thông báo xác nhận trước và sau khi chỉnh sửa/xóa) - (một số key word để tìm: message popup, confirm dialog, alert confirm, prompt modal)
- Nút **Nhập từ file JSON** (kiểm tra cấu trúc file trước khi nhập).
- Nút **Xuất từ vựng ra file** (người dùng có thể chọn định dạng file để xuất ra).

### **Màn hình thêm/sửa từ vựng**
- Ô nhập **Từ vựng**.
- Ô nhập **Nghĩa của từ**.
- Ô nhập **Loại từ** (danh từ, động từ, tính từ,...).
- Ô nhập **Ví dụ sử dụng** (câu mẫu, cụm từ).
- Nút **Lưu lại** (kiểm tra hợp lệ trước khi lưu, không chứa ký tự đặc biệt như `@#&`, cần phải xác thực thông tin đầu vào) -> lưu gồm những tt ở trên (ngày sửa, người sửa)
- Nút **Hủy** (hiển thị thông báo và xác nhận trước khi hủy, vd: sau khi hủy thì làm gì, nó sẽ back lại trang trước hay là trở về màn hình trang chủ..).

### **Màn hình nhập từ vựng từ file JSON**
- **chọn file JSON** (kiểm tra dữ liệu trước khi nhập( nếu file không có dữ liệu hoặc dữ liệu không hợp lệ thì thông báo).
- Hiển thị danh sách **từ vựng trong file JSON**.
- Nút **Nhập dữ liệu**.
- Nút **Hủy** (hiển thị thông báo xác nhận).
 
### **Màn hình tải từ vựng về máy (Export)**
- Xuất từ vựng ra file **JSON** (có thể hỗ trợ thêm PDF, TXT, CSV nếu có thời gian).
- Nút **Tải xuống** (hiển thị hộp thoại chọn nơi lưu, thông báo sau khi tải xong).
- Nút **Back** (quay lại màn hình trước đó).
  
### **Màn hình quản lý tài khoản (User Management)**
- **Chỉ dành cho quản trị viên**.
- Danh sách **tài khoản người dùng**.
- Nút **Thêm tài khoản mới**.
- Nút **Chỉnh sửa/Xóa tài khoản**.
- **Tùy chọn phân quyền** (Admin/User).
- **Tìm kiếm tài khoản**.

### **Màn hình hồ sơ cá nhân (User Profile)**
- Hiển thị **Tên, Email, Ảnh đại diện**.
- Nút **Chỉnh sửa thông tin cá nhân**.
- Nút **Đổi mật khẩu**.
- Nút **Đăng xuất**.

### **Màn hình chi tiết từ vựng**
- Hiển thị **từ vựng**, nghĩa, loại từ, ví dụ sử dụng.
- **Tùy chọn lưu từ vựng vào danh sách cá nhân**.

### **Màn hình thêm/sửa/xóa tài khoản**
- Chỉ dành cho **quản trị viên**.
- Thêm người dùng với thông tin **họ tên, email, mật khẩu**.
- Chỉnh sửa thông tin tài khoản.
- Xóa tài khoản (hiển thị xác nhận trước khi xóa).

### **Chỉnh sửa phân quyền**
- **Chỉ dành cho quản trị viên**.
- Danh sách **người dùng**.
- Tùy chọn **Cấp quyền (Admin/User)**.
- Nút **Lưu thay đổi**.
