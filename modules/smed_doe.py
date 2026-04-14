import customtkinter as ctk
from app_config import *
from widgets.editable_table import EditableTable
import math

class SMEDModule(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        header = ctk.CTkFrame(self, fg_color=PANEL_BG, corner_radius=20, border_width=1, border_color="#334155")
        header.pack(fill="x", padx=10, pady=10)
        ctk.CTkLabel(header, text="OPTIMIZACIÓN SMED", font=("Segoe UI", 18, "bold"), text_color=ACCENT_GREEN).pack(side="left", padx=30, pady=25)
        
        ctk.CTkButton(header, text="+ AÑADIR TAREA", fg_color=ACCENT_GREEN, text_color=BG_MAIN, font=("Segoe UI", 11, "bold"), width=150, height=35, command=lambda: self.table.add_row()).pack(side="right", padx=30)

        self.t_container = ctk.CTkFrame(self, fg_color=PANEL_BG, corner_radius=25, border_width=1, border_color="#334155")
        self.t_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.table = EditableTable(self.t_container, columns=["Tarea", "Categoría", "Tiempo", "Mejora"], height=500)
        self.table.pack(fill="both", expand=True, padx=15, pady=15)
        self.table.add_row(["Set-up Molde", "Interna", "15 min", "--"])

class DOEModule(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        # Refined Control Panel
        ctrl = ctk.CTkFrame(self, fg_color=PANEL_BG, corner_radius=20, border_width=1, border_color="#334155")
        ctrl.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(ctrl, text="DISEÑO DE EXPERIMENTOS (DOE)", font=("Segoe UI", 18, "bold"), text_color=ACCENT_BLUE).pack(side="left", padx=30, pady=25)
        
        entry_box = ctk.CTkFrame(ctrl, fg_color="transparent")
        entry_box.pack(side="left", padx=20)
        ctk.CTkLabel(entry_box, text="CANT. CORRIDAS (N):", font=("Segoe UI", 10, "bold"), text_color=TEXT_S).pack(side="left", padx=5)
        self.n_val = ctk.CTkEntry(entry_box, width=60, placeholder_text="4", fg_color=BG_MAIN)
        self.n_val.pack(side="left")
        self.n_val.insert(0, "4")
        
        self.btn_gen = ctk.CTkButton(ctrl, text="GENERAR MATRIZ MUESTRAL", fg_color=ACCENT_BLUE, text_color=TEXT_P, font=("Segoe UI", 11, "bold"), width=250, height=45, command=self.build_matrix)
        self.btn_gen.pack(side="left", padx=10)

        # Added: Manual Add Row Button
        self.btn_add = ctk.CTkButton(ctrl, text="+ AÑADIR FILA", fg_color="transparent", border_width=1, border_color=ACCENT_BLUE, text_color=TEXT_P, font=("Segoe UI", 10, "bold"), width=120, height=45, command=lambda: self.table.add_row(["", "-", "-", ""]))
        self.btn_add.pack(side="right", padx=30)

        # Success Message (Hidden by default)
        self.msg = ctk.CTkLabel(self, text="", font=("Segoe UI", 11), text_color=ACCENT_GREEN)
        self.msg.pack(pady=5)

        self.t_container = ctk.CTkFrame(self, fg_color=PANEL_BG, corner_radius=25, border_width=1, border_color="#334155")
        self.t_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.table = EditableTable(self.t_container, columns=["Corrida", "Factor A", "Factor B", "Respuesta"], height=500)
        self.table.pack(fill="both", expand=True, padx=15, pady=15)

    def build_matrix(self):
        try:
            n = int(self.n_val.get())
            if n < 1 or n > 50: raise ValueError
        except:
            self.msg.configure(text="Error: Ingrese un valor de N válido (1-50)", text_color=DANGER_P)
            return

        # Let's keep a standard DOE header for ease of use
        cols = ["ORDEN", "FACTOR A", "FACTOR B", "RESPUESTA (Y)"]
        self.table.reset_table(cols)
        
        for i in range(n):
            # Try to populate with some default pattern for first 2 factors if N=4
            row = [str(i+1)]
            if n == 4: # Classic 2^2 hint
                a = "+" if i in [1, 3] else "-"
                b = "+" if i in [2, 3] else "-"
                row.extend([a, b])
            else:
                row.extend(["-", "-"]) # Default blanks
            row.append("") 
            self.table.add_row(row)
        
        self.msg.configure(text=f"✓ Se han generado {n} corridas experimentales.", text_color=ACCENT_GREEN)
        self.update_idletasks()
