import tkinter as tk
from tkinter import ttk, messagebox
from common.base_window import BaseWindow
from common.configs import WINDOW_SIZE
from utils.database import load_word_database, save_word_database

class VocabularyForm(BaseWindow):
    def __init__(self, root, word_data=None):
        super().__init__(root, "Vocabulary Form", WINDOW_SIZE['WIDTH'], WINDOW_SIZE['HEIGHT'])
        self.word_data = word_data
        self.is_edit = word_data is not None
        self.create_ui()
        if self.is_edit:
            self.populate_fields()

    def create_ui(self):
        self.root.configure(bg="#e6f0f7")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", background="#ffffff", foreground="#222", font=("Segoe UI", 11))
        style.configure("TEntry", padding=10, font=("Segoe UI", 11))
        style.configure("TButton", padding=8, font=("Segoe UI", 10, "bold"), background="#4CAF50", foreground="#fff")
        style.configure("TCombobox", padding=10, font=("Segoe UI", 11))

        self.main_frame = tk.Frame(self.root, bg="#e6f0f7")
        self.main_frame.pack(fill="both", expand=True, padx=30, pady=30)

        title_text = "✏️ Edit Word" if self.is_edit else "➕ Add New Word"
        tk.Label(self.main_frame, text=title_text, font=("Segoe UI", 20, "bold"), bg="#e6f0f7", fg="#333").pack(pady=(0, 20))

        form_frame = tk.Frame(self.main_frame, bg="#ffffff", bd=2, relief="groove")
        form_frame.pack(fill="both", expand=True, padx=10, pady=10, ipadx=15, ipady=15)

        form_frame.columnconfigure(1, weight=1)

        def add_label_entry(row, label_text, var=None):
            ttk.Label(form_frame, text=label_text).grid(row=row, column=0, sticky="w", padx=(10, 5), pady=8)
            entry = ttk.Entry(form_frame, textvariable=var, width=40)
            entry.grid(row=row, column=1, sticky="ew", padx=10, pady=8, ipady=6)
            return entry

        def add_label_text(row, label_text, height):
            ttk.Label(form_frame, text=label_text).grid(row=row, column=0, sticky="nw", padx=(10, 5), pady=8)
            frame = tk.Frame(form_frame, bg="#ffffff", bd=1, relief="solid")
            frame.grid(row=row, column=1, sticky="ew", padx=10, pady=8)
            text_widget = tk.Text(frame, height=height, width=50, wrap="word", font=("Segoe UI", 10), bd=0, padx=8, pady=6)
            text_widget.pack(fill="both", expand=True)
            return text_widget

        self.word_var = tk.StringVar()
        self.meaning_var = tk.StringVar()
        self.type_var = tk.StringVar()
        self.answers_var = tk.StringVar()

        add_label_entry(0, "📘 Word:", self.word_var)

        ttk.Label(form_frame, text="🔤 Word Type:").grid(row=2, column=0, sticky="w", padx=(10, 5), pady=8)
        self.type_combobox = ttk.Combobox(form_frame, textvariable=self.type_var, state="readonly",
                                          values=["Verb", "Noun", "Adj", "Adv", "Prep", "Conj"], width=37)
        self.type_combobox.grid(row=2, column=1, sticky="ew", padx=10, pady=8, ipady=4)
        self.type_combobox.set("Verb")

        add_label_entry(1, "VN Vietnamese Meaning:", self.meaning_var)

        add_label_entry(3, "💡 Synonyms (comma-separated) (từ đồng nghĩa):", self.answers_var)
        self.sentences_text = add_label_text(4, "📝 Sentences (ví dụ):", 4)
        self.phrases_text = add_label_text(5, "🔗 Phrases (các cụm từ có chứa từ này):", 4)

        button_frame = tk.Frame(form_frame, bg="#ffffff")
        button_frame.grid(row=6, column=0, columnspan=2, pady=25)

        save_btn = ttk.Button(button_frame, text="💾 Save", command=self.save_word)
        save_btn.pack(side="left", padx=15)

        cancel_btn = ttk.Button(button_frame, text="❌ Cancel", command=self.cancel)
        cancel_btn.pack(side="left", padx=15)

    def populate_fields(self):
        if not self.word_data:
            return
        self.word_var.set(self.word_data.get("word", ""))
        verb_types = self.word_data.get("verb", [])
        self.type_var.set(verb_types[0] if verb_types else "V")
        self.meaning_var.set(self.word_data.get("meaning", ""))
        answers = self.word_data.get("answers", [])
        self.answers_var.set(", ".join(answers))
        sentences = self.word_data.get("sentences", [])
        self.sentences_text.delete("1.0", "end")
        self.sentences_text.insert("1.0", "\n".join(sentences))
        phrases = self.word_data.get("phrases", [])
        self.phrases_text.delete("1.0", "end")
        self.phrases_text.insert("1.0", "\n".join(phrases))

    def save_word(self):
        word = self.word_var.get().strip()
        meaning = self.meaning_var.get().strip()
        word_type = self.type_var.get()
        answers = [a.strip() for a in self.answers_var.get().split(",") if a.strip()]
        sentences = [s.strip() for s in self.sentences_text.get("1.0", "end-1c").split("\n") if s.strip()]
        phrases = [p.strip() for p in self.phrases_text.get("1.0", "end-1c").split("\n") if p.strip()]

        if not word or not answers:
            messagebox.showerror("Error", "Please fill in all required fields.")
            return

        try:
            database = load_word_database()
            new_id = f"W{len(database) + 1:04d}" if not self.is_edit else self.word_data["id"]
            word_data = {
                "word": word,
                "meaning": meaning,
                "answers": answers,
                "sentences": sentences,
                "phrases": phrases,
                "verb": [word_type]
            }

            save_word_database(database)
            messagebox.showinfo("Success", f"Word '{word}' has been {'updated' if self.is_edit else 'added'} successfully!")
            self.root.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save word: {str(e)}")

    def cancel(self):
        if messagebox.askyesno("Confirm", "Cancel without saving?"):
            self.root.destroy()
