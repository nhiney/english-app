import tkinter as tk
from tkinter import ttk, messagebox
from common.base_window import BaseWindow
from common.configs import WINDOW_SIZE
from utils.database import load_word_database, save_word_database
import json

class VocabularyForm(BaseWindow):
    def __init__(self, root, word_data=None):
        super().__init__(root, "Vocabulary Form", WINDOW_SIZE['WIDTH'], WINDOW_SIZE['HEIGHT'])
        self.word_data = word_data
        self.is_edit = word_data is not None
        
        # Create UI
        self.create_ui()
        
        # If editing, populate fields
        if self.is_edit:
            self.populate_fields()

    def create_ui(self):
        # Main container
        self.main_frame = tk.Frame(self.root, bg="white")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        title = "Edit Word" if self.is_edit else "Add New Word"
        self.create_title(title, self.main_frame)

        # Form fields
        form_frame = tk.Frame(self.main_frame, bg="white")
        form_frame.pack(fill="both", expand=True, pady=20)

        # Word field
        word_frame = tk.Frame(form_frame, bg="white")
        word_frame.pack(fill="x", pady=5)
        
        tk.Label(word_frame, 
                text="Word:", 
                font=("Helvetica", 12),
                fg="#5f6368",
                bg="white").pack(side="left", padx=(0, 10))
        
        self.word_var = tk.StringVar()
        word_entry = ttk.Entry(word_frame, 
                             textvariable=self.word_var,
                             width=40)
        word_entry.pack(side="left", fill="x", expand=True)

        # Unit ID field
        unit_frame = tk.Frame(form_frame, bg="white")
        unit_frame.pack(fill="x", pady=5)
        
        tk.Label(unit_frame, 
                text="Unit ID:", 
                font=("Helvetica", 12),
                fg="#5f6368",
                bg="white").pack(side="left", padx=(0, 10))
        
        self.unit_var = tk.StringVar()
        unit_entry = ttk.Entry(unit_frame, 
                             textvariable=self.unit_var,
                             width=40)
        unit_entry.pack(side="left", fill="x", expand=True)

        # Word type field
        type_frame = tk.Frame(form_frame, bg="white")
        type_frame.pack(fill="x", pady=5)
        
        tk.Label(type_frame, 
                text="Word Type:", 
                font=("Helvetica", 12),
                fg="#5f6368",
                bg="white").pack(side="left", padx=(0, 10))
        
        self.type_var = tk.StringVar()
        type_combobox = ttk.Combobox(type_frame, 
                                   textvariable=self.type_var,
                                   values=["V", "N", "Adj", "Adv", "Prep", "Conj"],
                                   state="readonly",
                                   width=37)
        type_combobox.pack(side="left", fill="x", expand=True)
        type_combobox.set("V")

        # Answers field
        answers_frame = tk.Frame(form_frame, bg="white")
        answers_frame.pack(fill="x", pady=5)
        
        tk.Label(answers_frame, 
                text="Answers:", 
                font=("Helvetica", 12),
                fg="#5f6368",
                bg="white").pack(side="left", padx=(0, 10))
        
        self.answers_var = tk.StringVar()
        answers_entry = ttk.Entry(answers_frame, 
                                textvariable=self.answers_var,
                                width=40)
        answers_entry.pack(side="left", fill="x", expand=True)

        # Sentences field
        sentences_frame = tk.Frame(form_frame, bg="white")
        sentences_frame.pack(fill="x", pady=5)
        
        tk.Label(sentences_frame, 
                text="Sentences:", 
                font=("Helvetica", 12),
                fg="#5f6368",
                bg="white").pack(side="left", padx=(0, 10))
        
        self.sentences_text = tk.Text(sentences_frame, 
                                    height=3,
                                    width=40)
        self.sentences_text.pack(side="left", fill="x", expand=True)

        # Phrases field
        phrases_frame = tk.Frame(form_frame, bg="white")
        phrases_frame.pack(fill="x", pady=5)
        
        tk.Label(phrases_frame, 
                text="Phrases:", 
                font=("Helvetica", 12),
                fg="#5f6368",
                bg="white").pack(side="left", padx=(0, 10))
        
        self.phrases_text = tk.Text(phrases_frame, 
                                  height=3,
                                  width=40)
        self.phrases_text.pack(side="left", fill="x", expand=True)

        # Buttons
        buttons_frame = tk.Frame(form_frame, bg="white")
        buttons_frame.pack(fill="x", pady=20)
        
        self.create_button(buttons_frame, 
                         "Save", 
                         self.save_word,
                         is_primary=True)
        
        self.create_button(buttons_frame, 
                         "Cancel", 
                         self.cancel,
                         is_primary=False)

    def populate_fields(self):
        """Populate form fields with existing word data"""
        if not self.word_data:
            return
            
        try:
            # Set basic fields
            self.word_var.set(self.word_data.get("word", ""))
            self.unit_var.set(str(self.word_data.get("unitId", "")))
            
            # Set word type (get first type if multiple)
            verb_types = self.word_data.get("verb", [])
            self.type_var.set(verb_types[0] if verb_types else "V")
            
            # Set answers (join array with commas)
            answers = self.word_data.get("answers", [])
            self.answers_var.set(", ".join(answers))
            
            # Set sentences (join array with newlines)
            sentences = self.word_data.get("sentences", [])
            self.sentences_text.delete("1.0", "end")
            self.sentences_text.insert("1.0", "\n".join(sentences))
            
            # Set phrases (join array with newlines)
            phrases = self.word_data.get("phrases", [])
            self.phrases_text.delete("1.0", "end")
            self.phrases_text.insert("1.0", "\n".join(phrases))
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load word data: {str(e)}")

    def save_word(self):
        """Save word to database"""
        # Get form data
        word = self.word_var.get().strip()
        unit_id = self.unit_var.get().strip()
        word_type = self.type_var.get()
        answers = [a.strip() for a in self.answers_var.get().split(",") if a.strip()]
        sentences = [s.strip() for s in self.sentences_text.get("1.0", "end-1c").split("\n") if s.strip()]
        phrases = [p.strip() for p in self.phrases_text.get("1.0", "end-1c").split("\n") if p.strip()]

        # Validate input
        if not word:
            messagebox.showerror("Error", "Word is required!")
            return
            
        if not unit_id:
            messagebox.showerror("Error", "Unit ID is required!")
            return
            
        if not answers:
            messagebox.showerror("Error", "At least one answer is required!")
            return

        try:
            # Load database (array of words)
            database = load_word_database()
            
            # Generate new ID for new words
            new_id = f"U{unit_id}_{len(database) + 1:02d}" if not self.is_edit else self.word_data["id"]
            
            # Prepare word data
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
                # Update existing word
                for i, w in enumerate(database):
                    if w["id"] == self.word_data["id"]:
                        database[i] = word_data
                        break
            else:
                # Add new word
                database.append(word_data)
            
            # Save to database
            save_word_database(database)
            
            # Show success message
            messagebox.showinfo("Success", 
                              f"Word '{word}' has been {'updated' if self.is_edit else 'added'} successfully!")
            
            # Close form
            self.root.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save word: {str(e)}")

    def cancel(self):
        """Close form without saving"""
        if messagebox.askyesno("Confirm", "Are you sure you want to cancel? Any unsaved changes will be lost."):
            self.root.destroy() 