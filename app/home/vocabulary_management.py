import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from home.vocabulary_form import VocabularyForm
from utils.database import load_word_database, save_word_database


class VocabularyManagement(tk.Frame):
    def __init__(self, parent, user):
        super().__init__(parent, bg="#f4f6f8")
        self.parent = parent
        self.user = user

        self.create_ui()
        self.load_vocabulary_data()

    def create_ui(self):
        tk.Label(self, text="📘 Vocabulary Management", font=("Segoe UI", 18, "bold"), fg="#2c3e50", bg="#f4f6f8").pack(pady=15)

        
        search_frame = tk.Frame(self, bg="#f4f6f8")
        search_frame.pack(pady=5, fill="x", padx=20)

        tk.Label(search_frame, text="🔎 Search:", bg="#f4f6f8", font=("Segoe UI", 10)).pack(side="left", padx=5)
        self.search_entry = tk.Entry(search_frame, font=("Segoe UI", 10), width=25)
        self.search_entry.pack(side="left", padx=5)
        tk.Button(search_frame, text="Search", command=self.search_word, bg="#3498db", fg="white", relief="flat",
                  font=("Segoe UI", 10, "bold")).pack(side="left", padx=5)

        tk.Label(search_frame, text="📂 Filter by type:", bg="#f4f6f8", font=("Segoe UI", 10)).pack(side="left", padx=10)
        self.filter_combobox = ttk.Combobox(search_frame, values=["All", "N", "V", "Adj"], font=("Segoe UI", 10), width=10)
        self.filter_combobox.current(0)
        self.filter_combobox.pack(side="left", padx=5)
        tk.Button(search_frame, text="Filter", command=self.filter_words, bg="#2ecc71", fg="white", relief="flat",
                  font=("Segoe UI", 10, "bold")).pack(side="left", padx=5)

        
        table_frame = tk.Frame(self, bg="#f4f6f8")
        table_frame.pack(pady=10, padx=20, fill="both", expand=True)

        columns = ("Word", "Type", "Sentences", "Phrases")
        self.word_table = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=25)
        style.map("Treeview", background=[("selected", "#dcdde1")])

        for col in columns:
            self.word_table.heading(col, text=col)
            self.word_table.column(col, anchor="center", width=150)

        self.word_table.pack(fill="both", expand=True)

        
        btn_frame = tk.Frame(self, bg="#f4f6f8")
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="💾 Export JSON", command=self.export_json,
                  bg="#16a085", fg="white", font=("Segoe UI", 10), relief="flat", width=14).pack(side="left", padx=5)

        if self.user["role"] == "Admin":
            tk.Button(btn_frame, text="📂 Import JSON", command=self.import_json,
                      bg="#8e44ad", fg="white", font=("Segoe UI", 10), relief="flat", width=14).pack(side="left", padx=5)
            tk.Button(btn_frame, text="➕ Add Word", command=self.add_word,
                      bg="#2980b9", fg="white", font=("Segoe UI", 10), relief="flat", width=14).pack(side="left", padx=5)
            tk.Button(btn_frame, text="✏️ Edit", command=self.edit_word,
                      bg="#f39c12", fg="white", font=("Segoe UI", 10), relief="flat", width=14).pack(side="left", padx=5)
            tk.Button(btn_frame, text="❌ Delete", command=self.delete_word,
                      bg="#e74c3c", fg="white", font=("Segoe UI", 10), relief="flat", width=14).pack(side="left", padx=5)

    def load_vocabulary_data(self):
        try:
            vocabulary_list = load_word_database()
            self.word_table.delete(*self.word_table.get_children())

            for item in vocabulary_list:
                self.word_table.insert("", "end", values=(
                    item.get("word", ""),
                    ", ".join(item.get("verb", []) or []),
                    ", ".join(item.get("sentences", []) or []),
                    ", ".join(item.get("phrases", []) or [])
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Cannot load data: {e}")

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
                if keyword in word_text or any(keyword in s.lower() for s in sentences):
                    filtered_words.append(word)

            self.word_table.delete(*self.word_table.get_children())

            if not filtered_words:
                messagebox.showinfo("Notice", "No word found.")
            else:
                for item in filtered_words:
                    self.word_table.insert("", "end", values=(
                        item.get("word", ""),
                        ", ".join(item.get("verb", []) or []),
                        ", ".join(item.get("sentences", []) or []),
                        ", ".join(item.get("phrases", []) or [])
                    ))
        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {e}")

    def filter_words(self):
        filter_value = self.filter_combobox.get()
        try:
            vocabulary_list = load_word_database()
            filtered_words = vocabulary_list if filter_value == "All" else [
                word for word in vocabulary_list if filter_value in word.get("verb", [])
            ]

            self.word_table.delete(*self.word_table.get_children())
            for item in filtered_words:
                self.word_table.insert("", "end", values=(
                    item.get("word", ""),
                    ", ".join(item.get("verb", []) or []),
                    ", ".join(item.get("sentences", []) or []),
                    ", ".join(item.get("phrases", []) or [])
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Filter failed: {e}")

    def add_word(self):
        new_root = tk.Toplevel(self.parent)
        VocabularyForm(new_root)

    def edit_word(self):
        selected = self.word_table.selection()
        word_text = self.word_table.item(selected[0])["values"][1]
        if not selected:
            messagebox.showerror("Error", "Please select a word to edit.")
            return
        try:
            vocabulary_list = load_word_database()
            word_data = next((w for w in vocabulary_list if w["word"] == word_text), None)
            if not word_data:
                messagebox.showerror("Error", "Word not found.")
                return

            new_root = tk.Toplevel(self.parent)
            VocabularyForm(new_root, word_data)
            self.parent.wait_window(new_root)
            self.load_vocabulary_data()
        except Exception as e:
            messagebox.showerror("Error", f"Edit failed: {e}")

    def delete_word(self):
        selected = self.word_table.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a word to delete.")
            return

        word_text = self.word_table.item(selected[0])["values"][1]

        if not messagebox.askyesno("Confirm", f"Are you sure you want to delete '{word_text}'?"):
            return

        try:
            database = load_word_database()
            database = [w for w in database if w["word"] != word_text]
            save_word_database(database)
            self.load_vocabulary_data()
            messagebox.showinfo("Success", f"'{word_text}' has been deleted.")
        except Exception as e:
            messagebox.showerror("Error", f"Delete failed: {e}")

    def import_json(self):
        file_path = filedialog.askopenfilename(
            title="Select JSON file to import",
            filetypes=[("JSON files", "*.json")]
        )
        if not file_path:
            return

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                imported_data = json.load(file)

            if not isinstance(imported_data, list):
                raise ValueError("Invalid JSON format")

            database = load_word_database()
            existing_ids = {w["word"] for w in database}
            for item in imported_data:
                if item["word"] not in existing_ids:
                    database.append(item)

            save_word_database(database)
            self.load_vocabulary_data()
            messagebox.showinfo("Success", "Imported successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Import failed: {e}")

    def export_json(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            title="Save vocabulary as JSON"
        )
        if not file_path:
            return

        try:
            data = load_word_database()
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Success", "Exported successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {e}")
