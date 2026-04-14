import customtkinter as ctk
from app_config import *
from datetime import datetime
from tkinter import messagebox

class HildegardModule(ctk.CTkFrame):
    def __init__(self, master, db_manager, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.db = db_manager
        
        # --- UI LAYOUT ---
        self.grid_columnconfigure(0, weight=1) # Main Inputs
        self.grid_columnconfigure(1, weight=1) # History Panel
        self.grid_rowconfigure(0, weight=1)
        
        # 1. MONITORING PANEL (LEFT)
        self.mon_p = ctk.CTkFrame(self, fg_color=PANEL_BG, corner_radius=25, border_width=1, border_color="#E2E8F0")
        self.mon_p.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        ctk.CTkLabel(self.mon_p, text="HILDEGARD 2.0 CONTROL", font=("Segoe UI", 20, "bold"), text_color=TEXT_P).pack(pady=(30, 5))
        ctk.CTkLabel(self.mon_p, text="Termoformado & Rapidez Industrial", font=("Segoe UI", 11), text_color=TEXT_S).pack(pady=(0, 20))
        
        # --- TECHNICAL DATA INPUT (Temp/Pressure) ---
        self.tech_f = ctk.CTkFrame(self.mon_p, fg_color=BG_MAIN, corner_radius=20)
        self.tech_f.pack(fill="x", padx=30, pady=10)
        
        ctk.CTkLabel(self.tech_f, text="CONDICIONES DEL TERMOFORMADOR", font=("Segoe UI", 12, "bold"), text_color=ACCENT_BLUE).pack(pady=10)
        
        self.inp_row1 = ctk.CTkFrame(self.tech_f, fg_color="transparent")
        self.inp_row1.pack(fill="x", padx=20, pady=10)
        
        self.ent_t = ctk.CTkEntry(self.inp_row1, placeholder_text="Temp (°C)", height=40, font=("Segoe UI", 12))
        self.ent_t.pack(side="left", fill="x", expand=True, padx=5)
        
        self.ent_p = ctk.CTkEntry(self.inp_row1, placeholder_text="Presión (PSI)", height=40, font=("Segoe UI", 12))
        self.ent_p.pack(side="left", fill="x", expand=True, padx=5)
        
        self.btn_save_tech = ctk.CTkButton(self.tech_f, text="💾 CARGAR Tº / P", fg_color=ACCENT_BLUE, text_color=BG_MAIN, 
                                          font=("Segoe UI", 11, "bold"), height=40, command=self.save_tech)
        self.btn_save_tech.pack(pady=(0, 15), padx=25, fill="x")

        # --- SPEED DATA INPUT ---
        self.speed_f = ctk.CTkFrame(self.mon_p, fg_color=BG_MAIN, corner_radius=20)
        self.speed_f.pack(fill="x", padx=30, pady=10)
        
        ctk.CTkLabel(self.speed_f, text="CONTROL DE RAPIDEZ DE PRODUCCIÓN", font=("Segoe UI", 12, "bold"), text_color=ACCENT_GREEN).pack(pady=10)
        
        self.inp_row2 = ctk.CTkFrame(self.speed_f, fg_color="transparent")
        self.inp_row2.pack(fill="x", padx=20, pady=10)
        
        self.ent_v = ctk.CTkEntry(self.inp_row2, placeholder_text="Rapidez (m/min)", height=40, font=("Segoe UI", 12))
        self.ent_v.pack(side="left", fill="x", expand=True, padx=5)
        
        self.btn_save_speed = ctk.CTkButton(self.speed_f, text="⚡ REGISTRAR RAPIDEZ", fg_color=ACCENT_GREEN, text_color=BG_MAIN, 
                                           font=("Segoe UI", 11, "bold"), height=40, command=self.save_speed)
        self.btn_save_speed.pack(pady=(0, 15), padx=25, fill="x")

        self.btn_clear_all = ctk.CTkButton(self.mon_p, text="🧨 BORRAR HISTORIAL TOTAL", fg_color="transparent", text_color=DANGER_P, 
                                          border_width=1, border_color=DANGER_P, font=("Segoe UI", 10, "bold"), height=30, command=self.clear_all_logs)
        self.btn_clear_all.pack(pady=20)

        # 2. HISTORY PANEL (RIGHT)
        self.hist_f = ctk.CTkFrame(self, fg_color=PANEL_BG, corner_radius=25, border_width=1, border_color="#E2E8F0")
        self.hist_f.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        self.tab_view = ctk.CTkTabview(self.hist_f, fg_color="transparent", segmented_button_selected_color=ACCENT_BLUE)
        self.tab_view.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tab_tech = self.tab_view.add("TERMOFORMADO (T/P)")
        self.tab_speed = self.tab_view.add("RAPIDEZ (V)")
        
        # Technical History List
        self.scroll_tech = ctk.CTkScrollableFrame(self.tab_tech, fg_color="transparent")
        self.scroll_tech.pack(fill="both", expand=True)
        
        # Speed History List
        self.scroll_speed = ctk.CTkScrollableFrame(self.tab_speed, fg_color="transparent")
        self.scroll_speed.pack(fill="both", expand=True)
        
        self.refresh_all()

    def save_tech(self):
        try:
            t, p = float(self.ent_t.get()), float(self.ent_p.get())
            self.db.log_hildegard(t, p)
            self.ent_t.delete(0, 'end'); self.ent_p.delete(0, 'end')
            self.refresh_tech()
        except ValueError: messagebox.showerror("Error", "Datos de Temp/Presión inválidos")

    def save_speed(self):
        try:
            v = float(self.ent_v.get())
            self.db.log_hildegard_speed(v)
            self.ent_v.delete(0, 'end')
            self.refresh_speed()
        except ValueError: messagebox.showerror("Error", "Dato de Rapidez inválido")

    def refresh_all(self):
        self.refresh_tech(); self.refresh_speed()

    def refresh_tech(self):
        for widget in self.scroll_tech.winfo_children(): widget.destroy()
        logs = self.db.get_hildegard_logs()
        for lid, ts, t, p, notes in logs:
            row = EntryRow(self.scroll_tech, lid, ts, [t, p], ["°C", "PSI"], self.update_tech, self.delete_tech)
            row.pack(fill="x", pady=2)

    def refresh_speed(self):
        for widget in self.scroll_speed.winfo_children(): widget.destroy()
        logs = self.db.get_hildegard_speed_logs()
        for lid, ts, v, notes in logs:
            row = EntryRow(self.scroll_speed, lid, ts, [v], ["m/min"], self.update_speed, self.delete_speed)
            row.pack(fill="x", pady=2)

    def update_tech(self, lid, values):
        self.db.update_hildegard_log(lid, values[0], values[1])
        self.refresh_tech()

    def delete_tech(self, lid):
        if messagebox.askyesno("Borrar", "¿Eliminar este registro de Termoformado?"):
            self.db.delete_hildegard_log(lid)
            self.refresh_tech()

    def update_speed(self, lid, values):
        self.db.update_hildegard_speed(lid, values[0])
        self.refresh_speed()

    def delete_speed(self, lid):
        if messagebox.askyesno("Borrar", "¿Eliminar este registro de Rapidez?"):
            self.db.delete_hildegard_speed(lid)
            self.refresh_speed()

    def clear_all_logs(self):
        if messagebox.askyesno("Confirmar", "¿Borrar TODO el historial de Hildegard 2.0?"):
            self.db.clear_hildegard_logs()
            self.db.clear_hildegard_speed_logs()
            self.refresh_all()

class EntryRow(ctk.CTkFrame):
    def __init__(self, master, entry_id, ts, values, units, on_save, on_delete):
        super().__init__(master, fg_color=BG_MAIN, corner_radius=10)
        self.entry_id = entry_id
        self.values = values
        self.units = units
        self.on_save = on_save
        self.on_delete = on_delete
        
        dt = datetime.fromisoformat(ts).strftime("%H:%M")
        ctk.CTkLabel(self, text=f"[{dt}]", font=("Consolas", 10), text_color=TEXT_S).pack(side="left", padx=10)
        
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(side="left", fill="x", expand=True)
        
        self.labels = []
        self.entries = []
        
        self.show_view()

    def show_view(self):
        for w in self.container.winfo_children(): w.destroy()
        self.labels = []
        for i, v in enumerate(self.values):
            lbl = ctk.CTkLabel(self.container, text=f"{v}{self.units[i]}", font=("Segoe UI", 11, "bold"), text_color=TEXT_P)
            lbl.pack(side="left", padx=10)
            self.labels.append(lbl)
            
        ctk.CTkButton(self, text="✏️", width=30, height=30, fg_color="transparent", hover_color="#334155", command=self.show_edit).pack(side="right", padx=5)
        ctk.CTkButton(self, text="🗑️", width=30, height=30, fg_color="transparent", hover_color=DANGER_P, command=lambda: self.on_delete(self.entry_id)).pack(side="right", padx=5)

    def show_edit(self):
        for w in self.container.winfo_children(): w.destroy()
        for w in self.winfo_children(): 
            if isinstance(w, ctk.CTkButton): w.destroy()
            
        self.entries = []
        for i, v in enumerate(self.values):
            ent = ctk.CTkEntry(self.container, width=60, height=25, font=("Segoe UI", 10))
            ent.insert(0, str(v))
            ent.pack(side="left", padx=5)
            self.entries.append(ent)
            ctk.CTkLabel(self.container, text=self.units[i], font=("Segoe UI", 9), text_color=TEXT_S).pack(side="left")

        ctk.CTkButton(self, text="💾", width=30, height=30, fg_color=ACCENT_GREEN, command=self.save_edit).pack(side="right", padx=5)
        ctk.CTkButton(self, text="❌", width=30, height=30, fg_color="#475569", command=self.show_view).pack(side="right", padx=5)

    def save_edit(self):
        try:
            new_vals = [float(e.get()) for e in self.entries]
            self.on_save(self.entry_id, new_vals)
        except ValueError: messagebox.showerror("Error", "Valores inválidos")
