import customtkinter as ctk
from app_config import *

class SMEDModule(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        ctk.CTkLabel(self, text="ANÁLISIS SMED (Single Minute Exchange of Die)", font=("Arial", 20, "bold"), text_color=EMERALD).pack(pady=10)
        
        # Registration Frame
        self.entry_frame = ctk.CTkFrame(self, fg_color=CARD_BG, corner_radius=15)
        self.entry_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(self.entry_frame, text="Tarea / Actividad:").grid(row=0, column=0, padx=10, pady=10)
        self.task_entry = ctk.CTkEntry(self.entry_frame, width=200)
        self.task_entry.grid(row=0, column=1, padx=10, pady=10)
        
        ctk.CTkLabel(self.entry_frame, text="Tipo:").grid(row=0, column=2, padx=10, pady=10)
        self.task_type = ctk.CTkOptionMenu(self.entry_frame, values=["Interna", "Externa"], fg_color=BLUE_PREMIUM)
        self.task_type.grid(row=0, column=3, padx=10, pady=10)
        
        self.add_btn = ctk.CTkButton(self.entry_frame, text="Añadir Tarea", fg_color=EMERALD, command=self.add_task)
        self.add_btn.grid(row=0, column=4, padx=10, pady=10)
        
        # Table of tasks
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color=CARD_BG, corner_radius=15, height=400)
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Headers
        headers = ["Tarea", "Tipo", "Optimización Sugerida"]
        for i, h in enumerate(headers):
            ctk.CTkLabel(self.scroll_frame, text=h, font=("Arial", 12, "bold"), text_color=BLUE_PREMIUM).grid(row=0, column=i, padx=40, pady=10)

        self.row_count = 1

    def add_task(self):
        task = self.task_entry.get()
        t_type = self.task_type.get()
        if not task: return
        
        suggestion = "Convertir a Externa" if t_type == "Interna" else "Estandarizar"
        
        ctk.CTkLabel(self.scroll_frame, text=task).grid(row=self.row_count, column=0, padx=40, pady=5)
        ctk.CTkLabel(self.scroll_frame, text=t_type).grid(row=self.row_count, column=1, padx=40, pady=5)
        ctk.CTkLabel(self.scroll_frame, text=suggestion, text_color=EMERALD).grid(row=self.row_count, column=2, padx=40, pady=5)
        
        self.row_count += 1
        self.task_entry.delete(0, 'end')
