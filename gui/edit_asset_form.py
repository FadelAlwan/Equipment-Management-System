import tkinter as tk
from tkinter import ttk, messagebox
from database.db_manager import update_equipment, get_equipment_by_id
from theme import COLORS
import sqlite3


DEPARTMENTS = [
    "IT", "HR", "Finance", "Operations", "Other"
]


class EditEquipmentForm:
    def __init__(self, parent, equipment_id, on_save_callback):
        self.equipment_id = equipment_id
        self.on_save_callback = on_save_callback

        self.data = get_equipment_by_id(equipment_id)
        if not self.data:
            messagebox.showerror("Error", "Equipment not found.")
            return

        self.window = tk.Toplevel(parent)
        self.window.title("Edit Equipment")
        self.window.geometry("480x730")
        self.window.resizable(True, True)
        self.window.configure(bg=COLORS["bg"])

        self.setup_header()
        self.setup_form()

    def setup_header(self):
        tk.Frame(self.window, bg=COLORS["primary"], height=5).pack(fill="x")
        tk.Label(
            self.window,
            text="Edit Equipment",
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

        def make_entry(value=""):
            e = tk.Entry(
                container,
                bg=COLORS["entry_bg"], fg=COLORS["text"],
                insertbackground=COLORS["text"],
                relief="flat", font=("Segoe UI", 10)
            )
            e.pack(fill="x", ipady=5)
            if value:
                e.insert(0, str(value))
            return e

        self.entries = {}

        for label, key, value in [
            ("Asset Tag *",               "asset_tag",      self.data[1]),
            ("Equipment Type *",          "asset_type",     self.data[2]),
            ("Brand",                     "brand",          self.data[3]),
            ("Model",                     "model",          self.data[4]),
            ("Serial Number",             "serial_number",  self.data[5]),
            ("Purchase Date (YYYY-MM-DD)","purchase_date",  self.data[8]),
            ("Specs",                     "specs",          self.data[9]),
        ]:
            make_label(label)
            self.entries[key] = make_entry(value)

        # Status dropdown
        make_label("Status")
        self.status_var = tk.StringVar(value=self.data[6])
        ttk.OptionMenu(
            container, self.status_var,
            self.data[6], "Active", "Maintenance", "In Storage"
        ).pack(fill="x")

        # Department dropdown
        make_label("Department")
        current_dept = self.data[7] if self.data[7] in DEPARTMENTS else DEPARTMENTS[0]
        self.dept_var = tk.StringVar(value=current_dept)
        ttk.OptionMenu(
            container, self.dept_var,
            current_dept, *DEPARTMENTS
        ).pack(fill="x")

        tk.Button(
            container, text="Update Equipment",
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
            update_equipment(
                self.equipment_id,
                asset_tag,
                asset_type,
                self.entries["brand"].get().strip(),
                self.entries["model"].get().strip(),
                self.entries["serial_number"].get().strip(),
                self.status_var.get(),
                self.dept_var.get(),
                self.entries["purchase_date"].get().strip(),
                self.entries["specs"].get().strip(),
            )
            messagebox.showinfo("Success", "Equipment updated successfully.")
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
                f"Could not update.\n{e}"
            )