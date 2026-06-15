import tkinter as tk
import pandas as pd
from tkinter import ttk, messagebox, filedialog
from database.db_manager import (
    get_all_equipment,
    search_equipment,
    delete_equipment,
    get_statistics,
    filter_by_status
)
from theme import COLORS
from openpyxl.worksheet.table import Table
from openpyxl.worksheet.table import TableStyleInfo
from openpyxl.styles import PatternFill, Font



class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("IT Equipment Manager")
        self.root.geometry("1150x620")
        self.root.configure(bg=COLORS["bg"])

        self.setup_header()
        self.setup_dashboard()
        self.setup_search_bar()
        self.setup_buttons()
        self.setup_table()
        self.load_data()

    def setup_header(self):
        header = tk.Frame(self.root, bg=COLORS["primary"], pady=12)
        header.pack(fill="x")
        tk.Label(
            header,
            text="  IT Equipment Manager",
            font=("Segoe UI", 16, "bold"),
            bg=COLORS["primary"],
            fg="white"
        ).pack(side="left", padx=20)
    
    def setup_dashboard(self):
        frame = tk.Frame(self.root, bg=COLORS["bg"])
        frame.pack(fill="x", padx=15, pady=(10, 5))

        self.total_label = self.create_stat_card(
            frame, "Total Assets", COLORS["primary"]
        )

        self.active_label = self.create_stat_card(
            frame, "Active", COLORS["success"]
        )

        self.maintenance_label = self.create_stat_card(
            frame, "Maintenance", "#d4a017"
        )

        self.storage_label = self.create_stat_card(
            frame, "In Storage", COLORS["surface_light"]
        )

        self.refresh_dashboard()
    
    def create_stat_card(self, parent, title, color):
        card = tk.Frame(
            parent,
            bg=color,
            padx=15,
            pady=10
        )

        card.pack(
            side="left",
            expand=True,
            fill="x",
            padx=5
        )

        tk.Label(
            card,
            text=title,
            bg=color,
            fg="white",
            font=("Segoe UI", 10)
        ).pack()

        value_label = tk.Label(
            card,
            text="0",
            bg=color,
            fg="white",
            font=("Segoe UI", 16, "bold")
        )

        value_label.pack()

        return value_label
    
    def refresh_dashboard(self):
        stats = get_statistics()

        self.total_label.config(
            text=str(stats["total"])
        )

        self.active_label.config(
            text=str(stats["active"])
        )

        self.maintenance_label.config(
            text=str(stats["maintenance"])
        )

        self.storage_label.config(
            text=str(stats["storage"])
        )
    

    def setup_search_bar(self):
        frame = tk.Frame(self.root, bg=COLORS["bg"], pady=8)
        frame.pack(fill="x", padx=15)

        tk.Label(
            frame, text="Search:",
            bg=COLORS["bg"], fg=COLORS["text"],
            font=("Segoe UI", 10)
        ).pack(side="left")

        self.search_var = tk.StringVar()
        tk.Entry(
            frame,
            textvariable=self.search_var,
            width=40,
            bg=COLORS["entry_bg"],
            fg=COLORS["text"],
            insertbackground=COLORS["text"],
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightbackground=COLORS["border"],
            highlightcolor=COLORS["primary"],
            font=("Segoe UI", 10)
        ).pack(side="left", padx=8, ipady=5)

        tk.Button(
            frame, text="Search",
            command=self.perform_search,
            bg=COLORS["primary"], fg="white",
            relief="flat", font=("Segoe UI", 10),
            cursor="hand2"
        ).pack(side="left", padx=3, ipady=4)

        tk.Label(
            frame,
            text="Status:",
            bg=COLORS["bg"],
            fg=COLORS["text"],
            font=("Segoe UI", 10)
        ).pack(side="left", padx=(15, 5))
        
        self.status_filter = tk.StringVar(value="All")

        ttk.OptionMenu(
            frame,
            self.status_filter,
            "All",
            "All",
            "Active",
            "Maintenance",
            "In Storage",
            command=self.apply_status_filter
        ).pack(side="left")

    def setup_buttons(self):
        frame = tk.Frame(self.root, bg=COLORS["bg"], pady=5)
        frame.pack(fill="x", padx=15)

        buttons = [
            ("＋  Add Equipment",    self.open_add_form,    COLORS["success"]),
            ("✎  Edit Equipment",   self.open_edit_form,   COLORS["primary"]),
            ("✕  Delete Equipment", self.delete_selected,  COLORS["danger"]),
            ("⬇  Export to Excel",  self.export_to_excel,  COLORS["warning"]),
        ]

        for text, command, color in buttons:
            tk.Button(
                frame, text=text,
                command=command,
                bg=color, fg="white",
                relief="flat",
                font=("Segoe UI", 10, "bold"),
                cursor="hand2",
                padx=12
            ).pack(side="left", padx=5, ipady=6)

    def setup_table(self):
        frame = tk.Frame(self.root, bg=COLORS["bg"])
        frame.pack(fill="both", expand=True, padx=15, pady=10)

        columns = ("ID", "Tag", "Type", "Brand", "Model", "Serial Number", "Status", "Department", "Purchase Date", "Specs")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                         background=COLORS["surface"],
                         foreground=COLORS["text"],
                         fieldbackground=COLORS["surface"],
                         rowheight=30,
                         font=("Segoe UI", 10))
        style.configure("Treeview.Heading",
                         background=COLORS["primary"],
                         foreground="white",
                         font=("Segoe UI", 10, "bold"),
                         relief="flat")
        style.map("Treeview",
                  background=[("selected", COLORS["selection"])],
                  foreground=[("selected", "white")])

        self.table = ttk.Treeview(frame, columns=columns, show="headings")

        col_widths = {
            "ID": 40, "Tag": 90, "Type": 90, "Brand": 90,
            "Model": 110, "Status": 90, "Department": 140,
            "Purchase Date": 110, "Specs": 160
        }

        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=col_widths.get(col, 100))

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
                row[0],   # id
                row[1],   # asset_tag
                row[2],   # asset_type
                row[3],   # brand
                row[4],   # model
                row[5],   # serial_number
                row[6],   # status
                row[7],   # assigned_department
                row[8],   # purchase_date
                row[9],  # specs
            ))
        self.refresh_dashboard()

    def perform_search(self):
        keyword = self.search_var.get().strip()
        if keyword:
            results = search_equipment(keyword)
            self.load_data(results)

    def apply_status_filter(self, selected_status):
        if selected_status == "All":
            self.load_data()
        else:
            rows = filter_by_status(selected_status)
            self.load_data(rows)

    def get_selected_id(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showwarning("No Selection",
                                   "Please select an equipment first.")
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
        from gui.add_asset_form import AddEquipmentForm
        AddEquipmentForm(self.root, self.load_data)

    def open_edit_form(self):
        from gui.edit_asset_form import EditEquipmentForm
        equipment_id = self.get_selected_id()
        if equipment_id is None:
            return
        EditEquipmentForm(self.root, equipment_id, self.load_data)

    def export_to_excel(self):
        rows = get_all_equipment()

        if not rows:
            messagebox.showwarning("No Data", "There is no equipment to export Please add some equipment first.")
            return
        
        columns = [
            "ID", "Asset Tag", "Type", "Brand", "Model",
            "Serial Number", "Status", "Department",
            "Purchase Date", "Specs"
        ]

        
        df = pd.DataFrame(rows, columns=columns)

        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            initialfile="equipment_report.xlsx",
            title="Save Excel Report"
        )

        if not file_path:
            return  

        try:
            with pd.ExcelWriter(
                file_path,
                engine="openpyxl"
            ) as writer:

                df.to_excel(
                    writer,
                    index=False,
                    sheet_name="Equipment"
                )

                workbook = writer.book
                worksheet = writer.sheets["Equipment"]
                
                worksheet.insert_rows(1)
                worksheet["A1"] = "IT Equipment Report"
                
                worksheet["A1"].font = Font(
                    size=16,
                    bold=True
                )

                table = Table(
                    displayName="EquipmentTable",
                    ref=f"A2:J{worksheet.max_row}"
                )

                style = TableStyleInfo(
                    name="TableStyleMedium2",
                    showFirstColumn=False,
                    showLastColumn=False,
                    showRowStripes=True,
                    showColumnStripes=False
                )

                table.tableStyleInfo = style
                worksheet.add_table(table)
            
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter

                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass

                    worksheet.column_dimensions[column_letter].width = max_length + 3
                worksheet.freeze_panes = "A3"
                green_fill = PatternFill(
                    start_color="C6EFCE",
                    end_color="C6EFCE",
                    fill_type="solid"
                )

                yellow_fill = PatternFill(
                    start_color="FFEB9C",
                    end_color="FFEB9C",
                    fill_type="solid"
                )

                red_fill = PatternFill(
                    start_color="FFC7CE",
                    end_color="FFC7CE",
                    fill_type="solid"
                )

                for row in range(3, worksheet.max_row + 1):

                    status_cell = worksheet[f"G{row}"]

                    if status_cell.value == "Active":
                        status_cell.fill = green_fill

                    elif status_cell.value == "Maintenance":
                        status_cell.fill = yellow_fill

                    elif status_cell.value == "Inactive":
                        status_cell.fill = red_fill

            messagebox.showinfo(
                "Success",
                f"Data exported successfully to:\n{file_path}"
            )

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Could not export file.\n{e}"
            )