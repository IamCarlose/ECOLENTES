import customtkinter as ctk
from app_config import *

class EditableTable(ctk.CTkScrollableFrame):
    def __init__(self, master, columns, **kwargs):
        super().__init__(master, fg_color="transparent", scrollbar_button_color=ACCENT_GREEN, **kwargs)
        self.columns = columns
        self.rows = []
        self._build_header()

    def _build_header(self):
        if hasattr(self, 'h_frame'):
            self.h_frame.destroy()
            
        self.h_frame = ctk.CTkFrame(self, fg_color=BG_MAIN, height=45, corner_radius=10)
        self.h_frame.pack(fill="x", padx=10, pady=(0, 15))
        
        # Configure Grid Weights for Columns
        num_cols = len(self.columns)
        for i in range(num_cols):
            self.h_frame.grid_columnconfigure(i, weight=1)
            
        for i, col in enumerate(self.columns):
            lbl = ctk.CTkLabel(self.h_frame, text=col.upper(), font=("Segoe UI", 10, "bold"), text_color=TEXT_S)
            lbl.grid(row=0, column=i, padx=5, sticky="w")

    def reset_table(self, new_columns):
        for row in self.rows:
            row["f"].destroy()
        self.rows = []
        self.columns = new_columns
        self._build_header()
        self.update_idletasks()

    def add_row(self, vals=None):
        r_frame = ctk.CTkFrame(self, fg_color="transparent", height=45)
        r_frame.pack(fill="x", padx=10, pady=4)
        
        num_cols = len(self.columns)
        entries = []
        for i in range(num_cols):
            r_frame.grid_columnconfigure(i, weight=1)
            txt = vals[i] if vals and i < len(vals) else ""
            e = ctk.CTkEntry(r_frame, height=38, fg_color=BG_MAIN, border_width=1, border_color="#1E293B", text_color=TEXT_P)
            e.insert(0, txt)
            e.grid(row=0, column=i, padx=5, sticky="ew")
            entries.append(e)
            
        # Delete Button (Fixed on the right)
        r_frame.grid_columnconfigure(num_cols, weight=0)
        btn = ctk.CTkButton(r_frame, text="×", width=32, height=32, fg_color="#450A0A", text_color=DANGER_P, hover_color=DANGER_P, command=lambda f=r_frame: self.delete_row(f))
        btn.grid(row=0, column=num_cols, padx=(10, 5))
        
        self.rows.append({"f": r_frame, "e": entries})
        self.update_idletasks()

    def delete_row(self, frame):
        for i, r in enumerate(self.rows):
            if r["f"] == frame:
                frame.destroy()
                self.rows.pop(i)
                break

    def get_data(self):
        return [[e.get() for e in r["e"]] for r in self.rows]
