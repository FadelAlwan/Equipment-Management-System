import tkinter as tk
from tkinter import ttk, messagebox
from database.db_manager import add_equipment


class AddEquipmentForm:
    def __init__(self, parent, on_save_callback):
        self.parent = parent
        self.on_save_callback = on_save_callback

        self.window = tk.Toplevel(parent)
        self.window.title("Add New Equipment")
        self.window.geometry("500x600")
        self.window.resizable(False, False)

        self.setup_form()
        
        
    
    def setup_form(self):
        container = tk.Frame(self.window, padx=20, pady=20)
        container.pack(fill="both", expand=True)

        fields = [
            ("Asset Tag *", "asset_tag"),
            ("Type *", "asset_type"),
            ("Brand", "brand"),
            ("Model", "model"),
            ("Serial Number", "serial_number"),
            ("Assigned To", "assigned_to"),
            ("Department", "department"),
            ("Purchase Date (YYYY-MM-DD)", "purchase_date"),
            ("Warranty Expiry (YYYY-MM-DD)", "warranty_expiry"),
            ("Specs", "specs"),
            ("Notes", "notes"),
        ]

        self.entries = {}

        for i, (label_text, field_name) in enumerate(fields):
            tk.Label(container, text=label_text, anchor="w").grid(
                row=i, column=0, sticky="w", pady=3)

            entry = tk.Entry(container, width=35)
            entry.grid(row=i, column=1, pady=3, padx=10)

            self.entries[field_name] = entry

        tk.Label(container, text="Status", anchor="w").grid(
            row=len(fields), column=0, sticky="w", pady=3)

        self.status_var = tk.StringVar(value="Active")
        status_dropdown = ttk.OptionMenu(
            container, self.status_var,
            "Active", "Active", "In Repair", "Retired", "In Storage"
        )
        status_dropdown.grid(row=len(fields), column=1, sticky="w", padx=10)

        tk.Button(container, text="Save Equipment",
                  command=self.save, bg="#4CAF50", fg="white",
                  width=20).grid(row=len(fields)+1, column=0,
                                 columnspan=2, pady=20)
    
    
    
    def save(self):
        # Get values from all fields
        asset_tag = self.entries["asset_tag"].get().strip()
        asset_type = self.entries["asset_type"].get().strip()

        # Validate required fields
        if not asset_tag or not asset_type:
            messagebox.showerror("Missing Fields",
                                 "Asset Tag and Type are required.")
            return

        # Collect all values
        brand           = self.entries["brand"].get().strip()
        model           = self.entries["model"].get().strip()
        serial_number   = self.entries["serial_number"].get().strip()
        status          = self.status_var.get()
        assigned_to     = self.entries["assigned_to"].get().strip()
        department      = self.entries["department"].get().strip()
        purchase_date   = self.entries["purchase_date"].get().strip()
        warranty_expiry = self.entries["warranty_expiry"].get().strip()
        specs           = self.entries["specs"].get().strip()
        notes           = self.entries["notes"].get().strip()

        try:
            add_equipment(
                asset_tag, asset_type, brand, model, serial_number,
                status, assigned_to, department, purchase_date,
                warranty_expiry, specs, notes
            )
            messagebox.showinfo("Success", "Equipment added successfully.")
            self.on_save_callback()  # refresh the main table
            self.window.destroy()   # close the popup

        except Exception as e:
            messagebox.showerror("Error", f"Could not save equipment.\n{e}")