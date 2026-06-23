import os
import customtkinter as ctk
from database.db_setup import create_database
from gui.main_window import MainWindow

if __name__ == "__main__":
    create_database()

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()

    BASE_DIR = os.path.dirname(
        os.path.abspath(__file__)
    )

    ICON_PATH = os.path.join(
        BASE_DIR,
        "models",
        "logo.ico"
    )

    root.iconbitmap(ICON_PATH)

    app = MainWindow(root)
    root.mainloop()