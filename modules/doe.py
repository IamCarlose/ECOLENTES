import customtkinter as ctk
from app_config import *

class DOEModule(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        ctk.CTkLabel(self, text="DISEÑO DE EXPERIMENTOS (DOE)", font=("Arial", 20, "bold"), text_color=EMERALD).pack(pady=10)
        
        # Matrix Generation Frame
        self.control_frame = ctk.CTkFrame(self, fg_color=CARD_BG, corner_radius=15)
        self.control_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(self.control_frame, text="Factor A (Temp):").grid(row=0, column=0, padx=10, pady=10)
        self.fact_a = ctk.CTkEntry(self.control_frame, width=100, placeholder_text="240-260")
        self.fact_a.grid(row=0, column=1, padx=10, pady=10)
        
        ctk.CTkLabel(self.control_frame, text="Factor B (Presión):").grid(row=0, column=2, padx=10, pady=10)
        self.fact_b = ctk.CTkEntry(self.control_frame, width=100, placeholder_text="100-130")
        self.fact_b.grid(row=0, column=3, padx=10, pady=10)
        
        self.gen_btn = ctk.CTkButton(self.control_frame, text="Generar Matriz 2^2", fg_color=EMERALD, command=self.generate_matrix)
        self.gen_btn.grid(row=0, column=4, padx=10, pady=10)
        
        # Result Table
        self.table_frame = ctk.CTkFrame(self, fg_color=CARD_BG, corner_radius=15)
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.headers = ["Ensayo", "Factor A", "Factor B", "Resultado (Yield)"]
        for i, h in enumerate(self.headers):
            ctk.CTkLabel(self.table_frame, text=h, font=("Arial", 12, "bold"), text_color=BLUE_PREMIUM).grid(row=0, column=i, padx=50, pady=10)

    def generate_matrix(self):
        # Clear previous (except headers)
        for widget in self.table_frame.winfo_children():
            if int(widget.grid_info()["row"]) > 0:
                widget.destroy()
                
        # Generate 2^2 Matrix (-1, +1)
        runs = [
            (1, "-", "-"),
            (2, "+", "-"),
            (3, "-", "+"),
            (4, "+", "+")
        ]
        
        for i, (run, a, b) in enumerate(runs):
            row = i + 1
            ctk.CTkLabel(self.table_frame, text=str(run)).grid(row=row, column=0, padx=50, pady=5)
            ctk.CTkLabel(self.table_frame, text=a).grid(row=row, column=1, padx=50, pady=5)
            ctk.CTkLabel(self.table_frame, text=b).grid(row=row, column=2, padx=50, pady=5)
            # Entry for result
            ctk.CTkEntry(self.table_frame, width=80, placeholder_text="0.0").grid(row=row, column=3, padx=50, pady=5)
