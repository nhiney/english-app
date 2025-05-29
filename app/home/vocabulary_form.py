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
        # Main background
        self.root.configure(bg="#f7f9fc")

        # Main frame
        self.main_frame = tk.Frame(self.root, bg="#f7f9fc")
        self.main_frame.pack(fill="both", expand=True, padx=30, pady=30)

        # Title
        title_text = "Edit Word" if self.is_edit else "Add New Word"
        self.create_title(title_text, self.main_frame)

        # Form
        form_frame = tk.Frame(self.main_frame, bg="#ffffff", bd=1, relief="solid")
        form_frame.pack(fill="both", expand=True, pady=20, padx=10, ipadx=20, ipady=20)

        # Styles
        label_font = ("Segoe UI", 11)
        entry_width = 42
        field_bg = "#ffffff"

        def create_labeled_entry(parent, text, var=None):
            frame = tk.Frame(parent, bg=field_bg)
            frame.pack(fill="x", pady=6)
            tk.Label(frame, text=text, font=label_font, bg=field_bg, fg="#333").pack(side="left", padx=(0, 10))
            entry = ttk.Entry(frame, textvariable=var, width=entry_width)
            entry.pack(side="left", fill="x", expand=True)
            return entry

        def create_labeled_text(parent, text, height):
            frame = tk.Frame(parent, bg=field_bg)
            frame.pack(fill="x", pady=6)
            tk.Label(frame, text=text, font=label_font, bg=field_bg, fg="#333").pack(side="left", padx=(0, 10))
            text_widget = tk.Text(frame, height=height, width=entry_width)
            text_widget.pack(side="left", fill="x", expand=True)
            return text_widget

        # Word
        self.word_var = tk.StringVar()
        create_labeled_entry(form_frame, "Word:", self.word_var)

        # Unit ID
        self.unit_var = tk.StringVar()
        create_labeled_entry(form_frame, "Unit ID:", self.unit_var)

        # Word Type
        frame_type = tk.Frame(form_frame, bg=field_bg)
        frame_type.pack(fill="x", pady=6)
        tk.Label(frame_type, text="Word Type:", font=label_font, bg=field_bg, fg="#333").pack(side="left", padx=(0, 10))
        self.type_var = tk.StringVar()
        type_combobox = ttk.Combobox(frame_type, textvariable=self.type_var,
                                     values=["V", "N", "Adj", "Adv", "Prep", "Conj"],
                                     state="readonly", width=entry_width - 3)
        type_combobox.pack(side="left", fill="x", expand=True)
        type_combobox.set("V")

        # Answers
        self.answers_var = tk.StringVar()
        create_labeled_entry(form_frame, "Answers:", self.answers_var)

        # Sentences
        self.sentences_text = create_labeled_text(form_frame, "Sentences:", height=3)

        # Phrases
        self.phrases_text = create_labeled_text(form_frame, "Phrases:", height=3)

        # Buttons
        button_frame = tk.Frame(form_frame, bg=field_bg)
        button_frame.pack(pady=15)

        # Save button
        save_btn = tk.Button(button_frame, text="Save", font=("Segoe UI", 10, "bold"),
                             bg="#4CAF50", fg="white", padx=15, pady=6,
                             command=self.save_word)
        save_btn.pack(side="left", padx=10)

        # Cancel button
        cancel_btn = tk.Button(button_frame, text="Cancel", font=("Segoe UI", 10),
                               bg="#dcdcdc", fg="black", padx=15, pady=6,
                               command=self.cancel)
        cancel_btn.pack(side="left", padx=10)

    def populate_fields(self):
        if not self.word_data:
            return
        self.word_var.set(self.word_data.get("word", ""))
        self.unit_var.set(str(self.word_data.get("unitId", "")))
        verb_types = self.word_data.get("verb", [])
        self.type_var.set(verb_types[0] if verb_types else "V")
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
        unit_id = self.unit_var.get().strip()
        word_type = self.type_var.get()
        answers = [a.strip() for a in self.answers_var.get().split(",") if a.strip()]
        sentences = [s.strip() for s in self.sentences_text.get("1.0", "end-1c").split("\n") if s.strip()]
        phrases = [p.strip() for p in self.phrases_text.get("1.0", "end-1c").split("\n") if p.strip()]

        if not word or not unit_id or not answers:
            messagebox.showerror("Error", "Please fill in all required fields.")
            return

        try:
            database = load_word_database()
            new_id = f"U{unit_id}_{len(database) + 1:02d}" if not self.is_edit else self.word_data["id"]
            word_data = {
                "id": new_id,
                "unitId": int(unit_id),
                "word": word,
                "answers": answers,
                "sentences": sentences,
                "phrases": phrases,
                "verb": [word_type]
            }

            if self.is_edit:
                for i, w in enumerate(database):
                    if w["id"] == self.word_data["id"]:
                        database[i] = word_data
                        break
            else:
                database.append(word_data)

            save_word_database(database)
            messagebox.showinfo("Success", f"Word '{word}' has been {'updated' if self.is_edit else 'added'} successfully!")
            self.root.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save word: {str(e)}")

    def cancel(self):
        if messagebox.askyesno("Confirm", "Cancel without saving?"):
            self.root.destroy()

