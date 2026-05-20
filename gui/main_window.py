import tkinter as tk
from tkinter import ttk, messagebox
from database.db_manager import (
    get_all_equipment,
    search_equipment,
    delete_equipment
)


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("IT Equipment Manager")
        self.root.geometry("1100x600")

        self.setup_search_bar()
        self.setup_buttons()
        self.setup_table()
        self.load_data()

    def setup_search_bar(self):
        frame = tk.Frame(self.root)
        frame.pack(fill="x", padx=10, pady=5)

        tk.Label(frame, text="Search:").pack(side="left")

        self.search_var = tk.StringVar()
        search_entry = tk.Entry(frame, textvariable=self.search_var, width=40)
        search_entry.pack(side="left", padx=5)

        tk.Button(frame, text="Search", command=self.perform_search).pack(side="left")
        tk.Button(frame, text="Clear", command=self.clear_search).pack(side="left", padx=5)

    def setup_buttons(self):
        frame = tk.Frame(self.root)
        frame.pack(fill="x", padx=10, pady=5)

        tk.Button(frame, text="Add Equipment",
                  command=self.open_add_form, bg="#4CAF50", fg="white").pack(side="left", padx=5)

        tk.Button(frame, text="Edit Equipment",
                  command=self.open_edit_form, bg="#2196F3", fg="white").pack(side="left", padx=5)

        tk.Button(frame, text="Delete Equipment",
                  command=self.delete_selected, bg="#f44336", fg="white").pack(side="left", padx=5)

        tk.Button(frame, text="Export to Excel",
                  command=self.export_to_excel, bg="#FF9800", fg="white").pack(side="left", padx=5)

    def setup_table(self):
        frame = tk.Frame(self.root)
        frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("ID", "Tag", "Type", "Brand", "Model",
                   "Status", "Assigned To", "Department", "Purchase Date")

        self.table = ttk.Treeview(frame, columns=columns, show="headings")

        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=120)

        scrollbar = ttk.Scrollbar(frame, orient="vertical",
                                  command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)

        self.table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def load_data(self, data=None):
        for row in self.table.get_children():
            self.table.delete(row)

        rows = data if data is not None else get_all_equipment()

        for row in rows:
            self.table.insert("", "end", values=(
                row[0],
                row[1],
                row[2],
                row[3],
                row[4],
                row[6],
                row[7],
                row[8],
                row[9],
            ))

    def perform_search(self):
        keyword = self.search_var.get().strip()
        if keyword:
            results = search_equipment(keyword)
            self.load_data(results)

    def clear_search(self):
        self.search_var.set("")
        self.load_data()

    def get_selected_id(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an equipment first.")
            return None
        row = self.table.item(selected[0])["values"]
        return row[0]

    def delete_selected(self):
        equipment_id = self.get_selected_id()
        if equipment_id is None:
            return
        confirm = messagebox.askyesno("Confirm Delete",
                                      "Are you sure you want to delete this equipment?")
        if confirm:
            delete_equipment(equipment_id)
            self.load_data()

    def open_add_form(self):
        pass

    def open_edit_form(self):
        pass

    def export_to_excel(self):
        pass