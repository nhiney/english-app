import re

def is_valid_email(email):
    """Kiểm tra định dạng email hợp lệ."""
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None

def is_valid_password(password):
    """Kiểm tra mật khẩu có ít nhất 8 ký tự, gồm chữ hoa, chữ thường, số, ký tự đặc biệt."""
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    return True