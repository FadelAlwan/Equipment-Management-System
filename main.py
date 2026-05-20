import tkinter as tk
from database.db_setup import create_database
from gui.main_window import MainWindow

if __name__ == "__main__":
    create_database()
    root = tk.Tk()
    root.iconbitmap("models/logo.ico")
    app = MainWindow(root)
    root.mainloop()