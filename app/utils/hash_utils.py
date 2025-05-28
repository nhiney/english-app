import hashlib

def hash_password(password):
    """Mã hóa mật khẩu bằng SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()