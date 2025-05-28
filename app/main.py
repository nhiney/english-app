import os
import sys

if getattr(sys, 'frozen', False):
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

if application_path not in sys.path:
    sys.path.append(application_path)

from auth.login import LoginWindow
import tkinter as tk

def main():
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()