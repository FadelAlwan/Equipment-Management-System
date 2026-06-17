import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, messagebox
from database.db_manager import add_equipment
from theme import COLORS
from tkcalendar import Calendar
import sqlite3


DEPARTMENTS = [
    "IT", "HR", "Finance", "Operations", "Other"
]


class AddEquipmentForm:
    def __init__(self, parent, on_save_callback):
        self.on_save_callback = on_save_callback

        self.window = ctk.CTkToplevel(parent)
        self.window.after(200, self.window.lift)
        self.window.title("Add New Equipment")
        self.window.geometry("480x730")
        self.window.resizable(True, True)
        self.window.configure(bg=COLORS["bg"])

        self.setup_header()
        self.setup_form()

    def setup_header(self):
        tk.Frame(self.window, bg=COLORS["primary"], height=5).pack(fill="x")
        tk.Label(
            self.window,
            text="Add New Equipment",
            font=("Segoe UI", 13, "bold"),
            bg=COLORS["bg"], fg=COLORS["primary"]
        ).pack(pady=(15, 5))

    def setup_form(self):
        container = tk.Frame(self.window, bg=COLORS["bg"], padx=30)
        container.pack(fill="both", expand=True)

        def make_label(text):
            tk.Label(
                container, text=text,
                bg=COLORS["bg"], fg=COLORS["text"],
                font=("Segoe UI", 9), anchor="w"
            ).pack(fill="x", pady=(8, 1))

        def make_entry():
            e = tk.Entry(
                container,
                bg=COLORS["entry_bg"], fg=COLORS["text"],
                insertbackground=COLORS["text"],
                relief="flat", font=("Segoe UI", 10)
            )
            e.pack(fill="x", ipady=5)
            return e

        self.entries = {}

        for label, key in [
            ("Asset Tag *",              "asset_tag"),
            ("Equipment Type *",         "asset_type"),
            ("Brand",                    "brand"),
            ("Model",                    "model"),
            ("Serial Number",            "serial_number"),
            ("Specs",                    "specs"),
        ]:
            make_label(label)
            self.entries[key] = make_entry()

        
        make_label("Purchase Date")

        self.purchase_date_var = tk.StringVar(value="")

        date_frame = ctk.CTkFrame(container, fg_color="transparent")
        date_frame.pack(fill="x")

        ctk.CTkEntry(
            date_frame,
            textvariable=self.purchase_date_var,
            state="readonly",
            fg_color=COLORS["entry_bg"],
            text_color=COLORS["text"],
            border_color=COLORS["border"],
            font=ctk.CTkFont("Segoe UI", 10)
        ).pack(side="left", fill="x", expand=True, ipady=3)

        ctk.CTkButton(
            date_frame,
            text="📅",
            width=40,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            command=self.open_calendar
        ).pack(side="left", padx=(5, 0))
        
        make_label("Status")
        self.status_var = tk.StringVar(value="Active")
        ttk.OptionMenu(
            container, self.status_var,
            "Active", "Active", "Maintenance", "In Storage"
        ).pack(fill="x")

        make_label("Department")
        self.dept_var = tk.StringVar(value=DEPARTMENTS[0])
        ttk.OptionMenu(
            container, self.dept_var,
            DEPARTMENTS[0], *DEPARTMENTS
        ).pack(fill="x")

        tk.Button(
            container, text="Save Equipment",
            command=self.save,
            bg=COLORS["primary"], fg="white",
            relief="flat", font=("Segoe UI", 11, "bold"),
            cursor="hand2"
        ).pack(fill="x", pady=20, ipady=8)

    def open_calendar(self):
        top = ctk.CTkToplevel(self.window)
        top.title("Select Date")
        top.geometry("300x320")
        top.resizable(False, False)
        top.grab_set()

        cal = Calendar(
            top,
            selectmode="day",
            date_pattern="yyyy-mm-dd",
            background="#2d2d2d",
            foreground="white",
            headersbackground="#0085D0",
            headersforeground="white",
            selectbackground="#0085D0",
            normalbackground="#2d2d2d",
            normalforeground="white",
            weekendbackground="#2d2d2d",
            weekendforeground="#aaaaaa",
            othermonthbackground="#252526",
            othermonthforeground="#666666",
        )
        cal.pack(padx=10, pady=10, fill="both", expand=True)

        def confirm():
            self.purchase_date_var.set(cal.get_date())
            top.destroy()

        ctk.CTkButton(
            top,
            text="Select",
            fg_color="#0085D0",
            hover_color="#006dab",
            command=confirm
        ).pack(pady=(0, 10), padx=20, fill="x")
            
    def save(self):
        asset_tag  = self.entries["asset_tag"].get().strip()
        asset_type = self.entries["asset_type"].get().strip()

        if not asset_tag or not asset_type:
            messagebox.showerror("Missing Fields",
                                 "Asset Tag and Equipment Type are required.")
            return

        try:
            add_equipment(
                asset_tag,
                asset_type,
                self.entries["brand"].get().strip(),
                self.entries["model"].get().strip(),
                self.entries["serial_number"].get().strip(),
                self.status_var.get(),
                self.dept_var.get(),
                self.purchase_date_var.get(),
                self.entries["specs"].get().strip(),
            )
            messagebox.showinfo("Success", "Equipment added successfully.")
            self.on_save_callback()
            self.window.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Duplicate Asset Tag",
                "This Asset Tag already exists. Please use a unique Asset Tag."
        )

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Could not save.\n{e}"
            )