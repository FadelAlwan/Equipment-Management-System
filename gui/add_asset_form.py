import tkinter as tk
from tkinter import ttk, messagebox
from database.db_manager import add_equipment
from theme import COLORS


DEPARTMENTS = [
    "IT", "HR", "Finance", "Operations", "Other"
]


class AddEquipmentForm:
    def __init__(self, parent, on_save_callback):
        self.on_save_callback = on_save_callback

        self.window = tk.Toplevel(parent)
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
            ("Assigned To",              "assigned_to"),
            ("Purchase Date (YYYY-MM-DD)", "purchase_date"),
            ("Specs",                    "specs"),
        ]:
            make_label(label)
            self.entries[key] = make_entry()

        # Status dropdown
        make_label("Status")
        self.status_var = tk.StringVar(value="Active")
        ttk.OptionMenu(
            container, self.status_var,
            "Active", "Active", "Maintenance", "In Storage"
        ).pack(fill="x")

        # Department dropdown
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
                self.entries["assigned_to"].get().strip(),
                self.dept_var.get(),
                self.entries["purchase_date"].get().strip(),
                self.entries["specs"].get().strip(),
            )
            messagebox.showinfo("Success", "Equipment added successfully.")
            self.on_save_callback()
            self.window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Could not save.\n{e}")