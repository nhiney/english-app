import tkinter as tk
from tkinter import ttk, messagebox
import json
from tkinter import filedialog
from home.vocabulary_form import VocabularyForm
from utils.database import load_word_database, save_word_database


class VocabularyManagement(tk.Frame):
    def __init__(self, parent, user):
        super().__init__(parent, bg="#f4f6f8")  # Màu nền nhẹ nhàng
        self.parent = parent
        self.user = user

        self.create_ui()
        self.load_vocabulary_data()

    def create_ui(self):
        """Tạo giao diện quản lý từ vựng"""
        tk.Label(self, text="📘 Quản lý từ vựng", font=("Segoe UI", 18, "bold"), fg="#2c3e50", bg="#f4f6f8").pack(pady=15)

        # Thanh tìm kiếm và bộ lọc
        search_frame = tk.Frame(self, bg="#f4f6f8")
        search_frame.pack(pady=5, fill="x", padx=20)

        tk.Label(search_frame, text="🔎 Tìm kiếm:", bg="#f4f6f8", font=("Segoe UI", 10)).pack(side="left", padx=5)
        self.search_entry = tk.Entry(search_frame, font=("Segoe UI", 10), width=25)
        self.search_entry.pack(side="left", padx=5)
        tk.Button(search_frame, text="Tìm", command=self.search_word, bg="#3498db", fg="white", relief="flat",
                  font=("Segoe UI", 10, "bold")).pack(side="left", padx=5)

        tk.Label(search_frame, text="📂 Lọc theo loại từ:", bg="#f4f6f8", font=("Segoe UI", 10)).pack(side="left", padx=10)
        self.filter_combobox = ttk.Combobox(search_frame, values=["All", "N", "V", "Adj"], font=("Segoe UI", 10), width=10)
        self.filter_combobox.current(0)
        self.filter_combobox.pack(side="left", padx=5)
        tk.Button(search_frame, text="Lọc", command=self.filter_words, bg="#2ecc71", fg="white", relief="flat",
                  font=("Segoe UI", 10, "bold")).pack(side="left", padx=5)

        # Bảng hiển thị từ vựng
        table_frame = tk.Frame(self, bg="#f4f6f8")
        table_frame.pack(pady=10, padx=20, fill="both", expand=True)

        columns = ("ID", "Từ vựng", "Loại từ", "Câu ví dụ", "Cụm từ")
        self.word_table = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#ecf0f1")
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=25)
        style.map("Treeview", background=[("selected", "#dcdde1")])

        for col in columns:
            self.word_table.heading(col, text=col)
            self.word_table.column(col, anchor="center", width=150)

        self.word_table.pack(fill="both", expand=True)

        # Nút thao tác
        btn_frame = tk.Frame(self, bg="#f4f6f8")
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="📂 Nhập JSON", command=self.import_json,
                  bg="#8e44ad", fg="white", font=("Segoe UI", 10), relief="flat", width=14).pack(side="left", padx=5)

        if self.user["role"] == "admin":
            tk.Button(btn_frame, text="➕ Thêm từ mới", command=self.add_word,
                      bg="#2980b9", fg="white", font=("Segoe UI", 10), relief="flat", width=14).pack(side="left", padx=5)
            tk.Button(btn_frame, text="✏️ Chỉnh sửa", command=self.edit_word,
                      bg="#f39c12", fg="white", font=("Segoe UI", 10), relief="flat", width=14).pack(side="left", padx=5)
            tk.Button(btn_frame, text="❌ Xóa", command=self.delete_word,
                      bg="#e74c3c", fg="white", font=("Segoe UI", 10), relief="flat", width=14).pack(side="left", padx=5)
            tk.Button(btn_frame, text="💾 Xuất JSON", command=self.export_json,
                      bg="#16a085", fg="white", font=("Segoe UI", 10), relief="flat", width=14).pack(side="left", padx=5)

    def load_vocabulary_data(self):
        try:
            vocabulary_list = load_word_database()
            self.word_table.delete(*self.word_table.get_children())

            for item in vocabulary_list:
                self.word_table.insert("", "end", values=(
                    item.get("id", ""),
                    item.get("word", ""),
                    ", ".join(item.get("verb", []) or []),
                    ", ".join(item.get("sentences", []) or []),
                    ", ".join(item.get("phrases", []) or [])
                ))

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu: {e}")

    def search_word(self):
        keyword = self.search_entry.get().strip().lower()
        if not keyword:
            self.load_vocabulary_data()
            return

        filtered_words = []
        try:
            vocabulary_list = load_word_database()
            for word in vocabulary_list:
                word_text = word.get("word", "").lower()
                sentences = word.get("sentences", [])
                is_in_word = keyword in word_text
                is_in_sentences = any(keyword in s.lower() for s in sentences)
                if is_in_word or is_in_sentences:
                    filtered_words.append(word)

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
            messagebox.showerror("Lỗi", f"Không thể tìm kiếm: {e}")

    def filter_words(self):
        filter_value = self.filter_combobox.get()
        try:
            vocabulary_list = load_word_database()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu: {e}")
            return

        if filter_value == "All":
            filtered_words = vocabulary_list
        else:
            filtered_words = [word for word in vocabulary_list if filter_value in word.get("verb", [])]

        self.word_table.delete(*self.word_table.get_children())
        for item in filtered_words:
            self.word_table.insert("", "end", values=(
                item.get("id", ""),
                item.get("word", ""),
                ", ".join(item.get("verb", []) or []),
                ", ".join(item.get("sentences", []) or []),
                ", ".join(item.get("phrases", []) or [])
            ))

    def add_word(self):
        new_root = tk.Toplevel(self.parent)
        VocabularyForm(new_root)

    def edit_word(self):
        selected = self.word_table.selection()
        if not selected:
            messagebox.showerror("Lỗi", "Vui lòng chọn từ để chỉnh sửa.")
            return

        word_id = self.word_table.item(selected[0])["values"][0]

        try:
            vocabulary_list = load_word_database()
            word_data = next((w for w in vocabulary_list if w["id"] == word_id), None)

            if not word_data:
                messagebox.showerror("Lỗi", "Không tìm thấy từ.")
                return

            new_root = tk.Toplevel(self.parent)
            VocabularyForm(new_root, word_data)
            self.parent.wait_window(new_root)
            self.load_vocabulary_data()

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể chỉnh sửa từ: {e}")

    def delete_word(self):
        selected = self.word_table.selection()
        if not selected:
            messagebox.showerror("Lỗi", "Vui lòng chọn từ để xóa.")
            return

        word_id = self.word_table.item(selected[0])["values"][0]
        word_text = self.word_table.item(selected[0])["values"][1]

        if not messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa từ '{word_text}'?"):
            return

        try:
            database = load_word_database()
            database = [w for w in database if w["id"] != word_id]
            save_word_database(database)
            self.load_vocabulary_data()
            messagebox.showinfo("Thành công", f"Đã xóa từ '{word_text}'.")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xóa: {e}")

    def import_json(self):
        messagebox.showinfo("Thông báo", "Chức năng này đang được phát triển...")

    def export_json(self):
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

        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All Files", "*.*")],
            title="Chọn nơi lưu file"
        )

        if not file_path:
            return

        try:
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(vocabulary_data, file, indent=4, ensure_ascii=False)

            messagebox.showinfo("Thành công", "Xuất dữ liệu thành công!")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xuất dữ liệu: {e}")
