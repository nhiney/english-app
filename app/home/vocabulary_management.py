import tkinter as tk
from tkinter import ttk, messagebox
import json
from tkinter import filedialog
from home.vocabulary_form import VocabularyForm
from utils.database import load_word_database, save_word_database


class VocabularyManagement(tk.Frame):
    def __init__(self, parent, user):
        super().__init__(parent, bg="white")
        self.parent = parent
        self.user = user

        self.create_ui()
        self.load_vocabulary_data()

    def create_ui(self):
        """Tạo giao diện quản lý từ vựng"""
        tk.Label(self, text="Quản lý từ vựng", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

        # Thanh tìm kiếm và bộ lọc
        search_frame = tk.Frame(self, bg="white")
        search_frame.pack(pady=5, fill="x")

        tk.Label(search_frame, text="Tìm kiếm:", bg="white").pack(side="left", padx=5)
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side="left", padx=5)
        tk.Button(search_frame, text="🔍", command=self.search_word).pack(side="left", padx=5)

        tk.Label(search_frame, text="Lọc theo loại từ:", bg="white").pack(side="left", padx=10)
        self.filter_combobox = ttk.Combobox(search_frame, values=["All", "N", "V", "Adj"])
        self.filter_combobox.current(0)
        self.filter_combobox.pack(side="left", padx=5)
        tk.Button(search_frame, text="Lọc", command=self.filter_words).pack(side="left", padx=5)

        # Bảng hiển thị từ vựng
        columns = ("ID", "Từ vựng", "Loại từ", "Câu ví dụ", "Cụm từ")
        self.word_table = ttk.Treeview(self, columns=columns, show="headings", height=10)

        for col in columns:
            self.word_table.heading(col, text=col)
            self.word_table.column(col, width=120)

        self.word_table.pack(pady=10, fill="both", expand=True)

        btn_frame = tk.Frame(self, bg="white")
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="📂 Nhập JSON", command=self.import_json).pack(side="left", padx=5)
        
        # Nút thao tác (Chỉ dành cho Admin)
        if self.user["role"] == "admin":
            tk.Button(btn_frame, text="➕ Thêm từ mới", command=self.add_word).pack(side="left", padx=5)
            tk.Button(btn_frame, text="✏️ Chỉnh sửa", command=self.edit_word).pack(side="left", padx=5)
            tk.Button(btn_frame, text="❌ Xóa", command=self.delete_word).pack(side="left", padx=5)
            tk.Button(btn_frame, text="💾 Xuất JSON", command=self.export_json).pack(side="left", padx=5)

    def load_vocabulary_data(self):
        """Load danh sách từ vựng từ file JSON và hiển thị trên bảng"""
        try:
            vocabulary_list = load_word_database()

            self.word_table.delete(*self.word_table.get_children())  # Clear bảng trước khi load mới

            for item in vocabulary_list:
                self.word_table.insert("", "end", values=(
                    item.get("id", ""),
                    item.get("word", ""),
                    ", ".join(item.get("verb", []) or []),
                    ", ".join(item.get("sentences", []) or []),
                    ", ".join(item.get("phrases", []) or [])
                ))

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu từ vựng: {e}")

    def search_word(self):
        """Lọc danh sách từ vựng dựa trên từ khóa nhập vào"""
        keyword = self.search_entry.get().strip().lower()

        if not keyword:
            self.load_vocabulary_data()  # Nếu không nhập gì, hiển thị toàn bộ danh sách
            return

        # Tạo danh sách mới chứa các từ vựng phù hợp
        filtered_words = []
        try:
            vocabulary_list = load_word_database()

            # Tìm từ vựng khớp với giá trị tìm kiếm
            for word in vocabulary_list:
                word_text = word.get("word", "").lower()  # Lấy từ vựng và chuyển về chữ thường
                sentences = word.get("sentences", [])  # Lấy danh sách câu ví dụ

                # Kiểm tra nếu từ khóa có trong từ vựng
                is_in_word = keyword in word_text

                # Kiểm tra nếu từ khóa có trong bất kỳ câu ví dụ nào
                is_in_sentences = False
                for sentence in sentences:
                    if keyword in sentence.lower():
                        is_in_sentences = True
                        break  # Nếu tìm thấy trong 1 câu, không cần kiểm tra tiếp

                # Nếu từ khóa xuất hiện trong từ vựng hoặc câu ví dụ, thêm vào danh sách kết quả
                if is_in_word or is_in_sentences:
                    filtered_words.append(word)

            # Xóa dữ liệu cũ trước khi cập nhật bảng
            self.word_table.delete(*self.word_table.get_children())

            for item in filtered_words:
                self.word_table.insert("", "end", values=(
                    item.get("id", ""),
                    item.get("word", ""),
                    ", ".join(item.get("verb", []) or []),
                    ", ".join(item.get("sentences", []) or []),
                    ", ".join(item.get("phrases", []) or [])
                ))

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tìm kiếm từ vựng: {e}")

    def filter_words(self):
        """Lọc danh sách từ vựng theo loại từ"""
        filter_value = self.filter_combobox.get()  # Lấy giá trị đang chọn trong dropdown

        # Load dữ liệu từ JSON
        try:
            vocabulary_list = load_word_database()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu từ vựng: {e}")
            return

        # Nếu chọn "Tất cả", hiển thị toàn bộ danh sách
        if filter_value == "All":
            filtered_words = vocabulary_list
        else:
            # Lọc danh sách từ vựng theo loại từ được chọn
            filtered_words = []
            for word in vocabulary_list:
                word_types = word.get("verb", [])  # Lấy danh sách loại từ (có thể mở rộng nếu có danh từ, tính từ)
                if filter_value in word_types:
                    filtered_words.append(word)

        # Cập nhật lại bảng từ vựng
        self.word_table.delete(*self.word_table.get_children())  # Xóa dữ liệu cũ
        for item in filtered_words:
            self.word_table.insert("", "end", values=(
                item.get("id", ""),
                item.get("word", ""),
                ", ".join(item.get("verb", []) or []),
                ", ".join(item.get("sentences", []) or []),
                ", ".join(item.get("phrases", []) or [])
            ))

    def add_word(self):
        """Open form to add new word"""
        new_root = tk.Toplevel(self.parent)
        VocabularyForm(new_root)

    def edit_word(self):
        """Open form to edit selected word"""
        selected = self.word_table.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a word to edit!")
            return
            
        # Get the word ID from the selected row
        word_id = self.word_table.item(selected[0])["values"][0]
        
        try:
            # Load database and find the word
            vocabulary_list = load_word_database()
                
            # Find the word in the database
            word_data = None
            for word in vocabulary_list:
                if word["id"] == word_id:
                    word_data = word
                    break
                    
            if not word_data:
                messagebox.showerror("Error", "Word not found in database!")
                return
                
            # Open edit form with the word data
            new_root = tk.Toplevel(self.parent)
            VocabularyForm(new_root, word_data)
            
            # Wait for the form to close
            self.parent.wait_window(new_root)
            
            # Refresh the vocabulary list after editing
            self.load_vocabulary_data()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to edit word: {str(e)}")

    def delete_word(self):
        """Delete selected word"""
        selected = self.word_table.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a word to delete!")
            return
            
        word_id = self.word_table.item(selected[0])["values"][0]
        word = self.word_table.item(selected[0])["values"][1]
        
        # Confirm deletion
        if not messagebox.askyesno("Confirm Deletion", 
                                 f"Are you sure you want to delete the word '{word}'?\nThis action cannot be undone."):
            return
            
        try:
            database = load_word_database()
            
            # Remove word from database
            database = [w for w in database if w["id"] != word_id]
            save_word_database(database)
            
            # Refresh list
            self.load_vocabulary_data()
            
            messagebox.showinfo("Success", f"Word '{word}' has been deleted successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete word: {str(e)}")

    def import_json(self):
        """Nhập từ JSON (Chưa triển khai)"""
        pass

    def export_json(self):
        """Xuất dữ liệu từ vựng ra file JSON"""
        # Lấy toàn bộ dữ liệu hiện có trong bảng
        vocabulary_data = []
        for row in self.word_table.get_children():
            values = self.word_table.item(row, "values")
            vocabulary_data.append({
                "id": values[0],
                "word": values[1],
                "verb": values[2].split(", "),
                "sentences": values[3].split(", "),
                "phrases": values[4].split(", ")
            })

        # Hiển thị hộp thoại chọn nơi lưu file
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All Files", "*.*")],
            title="Chọn nơi lưu file"
        )

        if not file_path:  # Nếu người dùng không chọn file thì thoát
            return

        # Ghi dữ liệu ra file JSON
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(vocabulary_data, file, indent=4, ensure_ascii=False)

            messagebox.showinfo("Thành công", "Xuất dữ liệu thành công!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xuất dữ liệu: {e}")