import customtkinter as ctk
from tkinter import messagebox
from database.db_manager import add_equipment, get_next_asset_tag
from theme import COLORS
from tkcalendar import Calendar
import sqlite3


DEPARTMENTS = [
    "IT", "HR", "Finance", "Operations", "Other"]

EQUIPMENT_TYPES = [
    "💻Laptop","Desktop PC","Monitor","Printer","Router","UPS","Server","Access Point","Scanner","Projector","Other"]

TYPE_PREFIX = {
    "Laptop": "LAP",
    "Desktop PC": "PC",
    "Monitor": "MON",
    "Printer": "PRN",
    "Router": "RTR",
    "UPS": "UPS",
    "Server": "SRV",
    "Access Point": "AP",
    "Scanner": "SCN",
    "Projector": "PRJ",
    "Other": "MISC"
}

class AddEquipmentForm:
    def __init__(self, parent, on_save_callback):
        self.on_save_callback = on_save_callback

        self.window = ctk.CTkToplevel(parent)
        self.window.after(200, self.window.lift)
        self.window.title("Add New Equipment")
        self.window.geometry("480x780")
        self.window.resizable(True, True)
        self.window.configure(fg_color=COLORS["bg"])

        self.setup_header()
        self.setup_form()

    def setup_header(self):
        ctk.CTkFrame(self.window, fg_color=COLORS["primary"], height=5, corner_radius=0).pack(fill="x")
        ctk.CTkLabel(self.window,text="Add New Equipment",font=("Segoe UI", 13, "bold"),fg_color=COLORS["bg"], text_color=COLORS["primary"]).pack(pady=(15, 5))

    def setup_form(self):
        container = ctk.CTkScrollableFrame(self.window, fg_color=COLORS["bg"])
        container.pack(fill="both", expand=True, padx=30)

        def make_label(text):
            ctk.CTkLabel(container, text=text,fg_color="transparent", text_color=COLORS["text"],font=ctk.CTkFont("Segoe UI", 11), anchor="w").pack(fill="x", pady=(8, 1))

        def make_entry():
            e = ctk.CTkEntry(container, fg_color=COLORS["entry_bg"], text_color=COLORS["text"],border_color=COLORS["border"], font=ctk.CTkFont("Segoe UI", 12))
            e.pack(fill="x", ipady=5)
            return e

        self.entries = {}

        make_label("Equipment Type *")

        self.asset_type_var = ctk.StringVar(
            value=EQUIPMENT_TYPES[0]
        )

        self.asset_type_combo = ctk.CTkOptionMenu(
            container,
            values=EQUIPMENT_TYPES,
            variable=self.asset_type_var,
            command=self.on_type_changed,
            fg_color=COLORS["entry_bg"],
            button_color=COLORS["primary"],
            button_hover_color=COLORS["primary_hover"],
            text_color=COLORS["text"],
            font=ctk.CTkFont("Segoe UI", 12)
        )

        self.asset_type_combo.pack(
            fill="x",
            pady=(0, 4)
        )
        

        for label, key in [
            ("Asset Tag *",              "asset_tag"),
            ("Brand",                    "brand"),
            ("Model",                    "model"),
            ("Serial Number",            "serial_number"),
            ("Specs",                    "specs"),
        ]:
            make_label(label)
            self.entries[key] = make_entry()
            
            
        self.on_type_changed(
            self.asset_type_var.get()
        )

        make_label("Purchase Date")
        self.purchase_date_var = ctk.StringVar(value="")
        date_frame = ctk.CTkFrame(container, fg_color="transparent")
        date_frame.pack(fill="x")

        ctk.CTkEntry(
            date_frame,
            textvariable=self.purchase_date_var,
            state="readonly",
            fg_color=COLORS["entry_bg"],
            text_color=COLORS["text"],
            border_color=COLORS["border"],
            font=ctk.CTkFont("Segoe UI", 12)
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
        self.status_var = ctk.StringVar(value="Active")
        ctk.CTkOptionMenu(
            container,
            variable=self.status_var,
            values=["Active", "Maintenance", "In Storage"],
            fg_color=COLORS["entry_bg"],
            button_color=COLORS["primary"],
            button_hover_color=COLORS["primary_hover"],
            text_color=COLORS["text"],
            font=ctk.CTkFont("Segoe UI", 12)
        ).pack(fill="x", pady=(0, 4))

        make_label("Department")
        self.dept_var = ctk.StringVar(value=DEPARTMENTS[0])
        ctk.CTkOptionMenu(
            container,
            variable=self.dept_var,
            values=DEPARTMENTS,
            fg_color=COLORS["entry_bg"],
            button_color=COLORS["primary"],
            button_hover_color=COLORS["primary_hover"],
            text_color=COLORS["text"],
            font=ctk.CTkFont("Segoe UI", 12)
        ).pack(fill="x", pady=(0, 4))

        ctk.CTkButton(container, text="Save Equipment",command=self.save,fg_color=COLORS["primary"], text_color="white",
              hover_color=COLORS["primary_hover"],
              font=ctk.CTkFont("Segoe UI", 13, "bold")).pack(fill="x", pady=20, ipady=8)

    def on_type_changed(self, selected_type):

        prefix = TYPE_PREFIX.get(
            selected_type,
            "AST"
        )

        new_tag = get_next_asset_tag(prefix)

        current_value = self.entries["asset_tag"].get().strip()

        if (
            not current_value
            or current_value.startswith(
                tuple(TYPE_PREFIX.values())
            )
        ):
            self.entries["asset_tag"].delete(
                0,
                "end"
            )

            self.entries["asset_tag"].insert(
                0,
                new_tag
            )
    
    
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
        asset_type = self.asset_type_combo.get()

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