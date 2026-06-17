import customtkinter as ctk
from database.db_setup import create_database
from gui.main_window import MainWindow

if __name__ == "__main__":
    create_database()

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.iconbitmap("models/logo.ico")
    app = MainWindow(root)
    root.mainloop()