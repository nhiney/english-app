import re
import json
import os

class RegisterService:
    def __init__(self):
        # Initialize user data file
        self.users_file = "users.json"
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                json.dump([], f)
    
    def validate_fullname(self, fullname):
        """
        Validate user's full name
        Returns: (is_valid: bool, error_message: str)
        """
        # Check if fullname is valid (at least 2 characters, only letters and spaces)
        if len(fullname) < 2:
            return False, "Họ và tên phải có ít nhất 2 ký tự"
        
        if not re.match(r'^[a-zA-ZÀ-ỹ\s]+$', fullname):
            return False, "Họ và tên chỉ được chứa chữ cái và khoảng trắng"
        
        return True, ""
    
    def validate_email(self, email):
        """
        Validate user's email
        Returns: (is_valid: bool, error_message: str)
        """
        # Check if email is valid
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return False, "Email không hợp lệ"
        
        # Check if email already exists
        with open(self.users_file, 'r') as f:
            users = json.load(f)
            
        for user in users:
            if user.get('email') == email:
                return False, "Email đã được sử dụng"
        
        return True, ""
    
    def validate_password(self, password):
        """
        Validate user's password
        Returns: (is_valid: bool, error_message: str)
        """
        # Check if password is valid
        if len(password) < 8:
            return False, "Mật khẩu phải có ít nhất 8 ký tự"
        
        if not re.search(r'[A-Z]', password):
            return False, "Mật khẩu phải chứa ít nhất một chữ cái in hoa"
        
        if not re.search(r'[a-z]', password):
            return False, "Mật khẩu phải chứa ít nhất một chữ cái thường"
        
        if not re.search(r'[0-9]', password):
            return False, "Mật khẩu phải chứa ít nhất một chữ số"
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False, "Mật khẩu phải chứa ít nhất một ký tự đặc biệt"
        
        return True, ""
    
    def register_user(self, fullname, email, password):
        """
        Register a new user
        Returns: bool indicating success
        """
        try:
            # Load existing users
            with open(self.users_file, 'r') as f:
                users = json.load(f)
            
            # Add new user
            users.append({
                'fullname': fullname,
                'email': email,
                'password': password,  # Note: In a real app, you'd want to hash this
                'role': 'user'  # Default role
            })
            
            # Save updated user list
            with open(self.users_file, 'w') as f:
                json.dump(users, f, indent=4)
            
            return True
        except Exception as e:
            print(f"Error registering user: {e}")
            return False
