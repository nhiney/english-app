import json
import os
import sys

def get_base_path():
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        return os.path.join(sys._MEIPASS, 'app')
    else:
        # Running as script
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASE_PATH = get_base_path()
DATABASE_PATH = os.path.join(BASE_PATH, "data", "database.json")
WORD_DATABASE_PATH = os.path.join(BASE_PATH, "data", "vocabulary.json")

def ensure_data_directory():
    """Ensure the data directory exists"""
    data_dir = os.path.dirname(DATABASE_PATH)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

def load_database():
    """Tải dữ liệu từ file JSON."""
    ensure_data_directory()
    if not os.path.exists(DATABASE_PATH):
        return {"users": []}

    with open(DATABASE_PATH, "r", encoding="utf-8") as file:
        return json.load(file)

def save_database(data):
    """Lưu dữ liệu vào file JSON."""
    ensure_data_directory()
    with open(DATABASE_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def load_word_database():
    """Tải dữ liệu từ file JSON."""
    ensure_data_directory()
    if not os.path.exists(WORD_DATABASE_PATH):
        return []

    with open(WORD_DATABASE_PATH, "r", encoding="utf-8") as file:
        return json.load(file)

def save_word_database(data):
    """Lưu dữ liệu từ vựng vào file JSON."""
    ensure_data_directory()
    with open(WORD_DATABASE_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)