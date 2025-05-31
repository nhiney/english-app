import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

class BaseWindow:
    def __init__(self, root, title, width, height):
        self.root = root
        self.root.title(title)
        self.root.configure(bg='white')
        self.image_path = None
        self.left_width_ratio = 2/3
        self.left_image_original = None

        # Center window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def create_split_layout(self, image_path, left_width_ratio=2/3):
        self.image_path = image_path
        self.left_width_ratio = left_width_ratio

        # Left frame for image
        self.left_frame = tk.Frame(self.root, bg='#f0f2f5')
        self.left_frame.pack(side="left", fill="both", expand=True)

        # Right frame for content
        self.right_frame = tk.Frame(self.root, bg="white")
        self.right_frame.pack(side="right", fill="both", expand=True, padx=40)

        # Load original image
        self.left_image_original = Image.open(image_path)

        # Initial image
        self.left_image = self.load_and_resize_image(self.left_image_original, 400, 400)
        self.image_label = tk.Label(self.left_frame, image=self.left_image, bg='#f0f2f5')
        self.image_label.place(relx=0.5, rely=0.5, anchor="center")

        # Bind resize event
        self.root.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        # Calculate new sizes
        total_width = self.root.winfo_width()
        total_height = self.root.winfo_height()
        left_width = int(total_width * self.left_width_ratio)
        left_height = total_height

        # Resize left_frame
        self.left_frame.config(width=left_width, height=left_height)
        # Resize image
        if self.left_image_original:
            self.left_image = self.load_and_resize_image(self.left_image_original, left_width, left_height)
            self.image_label.configure(image=self.left_image)
            self.image_label.image = self.left_image

    def load_and_resize_image(self, image, frame_width, frame_height):
        img_ratio = image.width / image.height
        frame_ratio = frame_width / frame_height

        if img_ratio > frame_ratio:
            new_width = frame_width
            new_height = int(frame_width / img_ratio)
        else:
            new_height = frame_height
            new_width = int(frame_height * img_ratio)

        resized = image.resize((max(1, new_width), max(1, new_height)), Image.LANCZOS)
        return ImageTk.PhotoImage(resized)

    def create_title(self, text, frame, pady=(40, 20)):
        title_label = tk.Label(frame, 
                             text=text, 
                             font=("Helvetica", 28, "bold"), 
                             fg="#1a73e8",
                             bg="white")
        title_label.pack(pady=pady)
        return title_label

    def create_subtitle(self, text, frame, pady=(0, 30)):
        subtitle_label = tk.Label(frame,
                                text=text,
                                font=("Helvetica", 16),
                                fg="#5f6368",
                                bg="white")
        subtitle_label.pack(pady=pady)
        return subtitle_label

    def create_input_field(self, frame, label_text, is_password=False):
        field_frame = tk.Frame(frame, bg="white")
        field_frame.pack(fill="x", pady=5)
        
        tk.Label(field_frame, 
                text=label_text, 
                font=("Helvetica", 12),
                fg="#5f6368",
                bg="white").pack(anchor="w")
                
        entry = ttk.Entry(field_frame, width=40, show="•" if is_password else "")
        entry.pack(pady=(5, 15))
        return entry

    def create_button(self, frame, text, command, is_primary=True, pady=10):
        button = tk.Button(frame, 
                         text=text, 
                         command=command,
                         font=("Helvetica", 12),
                         bg="#1a73e8" if is_primary else "white",
                         fg="white" if is_primary else "#1a73e8",
                         relief="flat",
                         padx=20,
                         pady=10,
                         cursor="hand2")
        button.pack(pady=pady)
        
        if is_primary:
            button.bind("<Enter>", lambda e: button.configure(bg="#1557b0"))
            button.bind("<Leave>", lambda e: button.configure(bg="#1a73e8"))
        else:
            button.bind("<Enter>", lambda e: button.configure(fg="#1557b0"))
            button.bind("<Leave>", lambda e: button.configure(fg="#1a73e8"))
            
        return button 