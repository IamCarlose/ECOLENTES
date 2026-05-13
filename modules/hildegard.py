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
        self.mon_p = ctk.CTkScrollableFrame(self, fg_color=PANEL_BG, corner_radius=25, border_width=1, border_color="#E2E8F0")
        self.mon_p.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        ctk.CTkLabel(self.mon_p, text="HILDEGARD Industrial Data", font=("Segoe UI", 20, "bold"), text_color=TEXT_P).pack(pady=(30, 5))
        ctk.CTkLabel(self.mon_p, text="Toma de Datos Modular", font=("Segoe UI", 11), text_color=TEXT_S).pack(pady=(0, 20))
        
        # --- INPUTS ---
        # Temp Input
        self.temp_f = self.create_input_section(self.mon_p, "CONTROL DE TEMPERATURA", ACCENT_BLUE, "Temp (°C)", self.save_temp)
        # Pressure Input
        self.press_f = self.create_input_section(self.mon_p, "CONTROL DE PRESIÓN", ACCENT_GOLD, "Presión (PSI)", self.save_pressure)
        # RPM Input
        self.rpm_f = self.create_input_section(self.mon_p, "CONTROL DE RPM / RAPIDEZ", ACCENT_GREEN, "RPM / m/min", self.save_rpm)
        # Diameter Input
        self.diam_f = self.create_input_section(self.mon_p, "CONTROL DE DIÁMETRO", ACCENT_STEEL, "Diám (mm)", self.save_quick_diameter)

        self.btn_clear_all = ctk.CTkButton(self.mon_p, text="🧨 BORRAR HISTORIAL MODULAR", fg_color="transparent", text_color=DANGER_P, 
                                          border_width=1, border_color=DANGER_P, font=("Segoe UI", 10, "bold"), height=30, command=self.clear_all_logs)
        self.btn_clear_all.pack(pady=20)

        # 2. HISTORY PANEL (RIGHT)
        self.hist_f = ctk.CTkFrame(self, fg_color=PANEL_BG, corner_radius=25, border_width=1, border_color="#E2E8F0")
        self.hist_f.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        self.tab_view = ctk.CTkTabview(self.hist_f, fg_color="transparent", segmented_button_selected_color=ACCENT_BLUE)
        self.tab_view.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tab_temp = self.tab_view.add("TEMPERATURA")
        self.tab_press = self.tab_view.add("PRESIÓN")
        self.tab_rpm = self.tab_view.add("RPM")
        self.tab_diam = self.tab_view.add("DIÁMETRO")
        
        self.scroll_temp = ctk.CTkScrollableFrame(self.tab_temp, fg_color="transparent")
        self.scroll_temp.pack(fill="both", expand=True)
        
        self.scroll_press = ctk.CTkScrollableFrame(self.tab_press, fg_color="transparent")
        self.scroll_press.pack(fill="both", expand=True)
        
        self.scroll_rpm = ctk.CTkScrollableFrame(self.tab_rpm, fg_color="transparent")
        self.scroll_rpm.pack(fill="both", expand=True)

        self.scroll_diam = ctk.CTkScrollableFrame(self.tab_diam, fg_color="transparent")
        self.scroll_diam.pack(fill="both", expand=True)
        
        self.refresh_all()

    def create_input_section(self, parent, title, color, placeholder, command):
        frame = ctk.CTkFrame(parent, fg_color=BG_MAIN, corner_radius=20)
        frame.pack(fill="x", padx=30, pady=10)
        ctk.CTkLabel(frame, text=title, font=("Segoe UI", 12, "bold"), text_color=color).pack(pady=10)
        
        row = ctk.CTkFrame(frame, fg_color="transparent")
        row.pack(fill="x", padx=20, pady=10)
        
        entry = ctk.CTkEntry(row, placeholder_text=placeholder, height=40, font=("Segoe UI", 12))
        entry.pack(side="left", fill="x", expand=True, padx=5)
        
        btn = ctk.CTkButton(frame, text=f"💾 REGISTRAR {title.split()[-1]}", fg_color=color, text_color=BG_MAIN, 
                            font=("Segoe UI", 11, "bold"), height=40, command=lambda: command(entry))
        btn.pack(pady=(0, 15), padx=25, fill="x")
        return entry

    def create_dual_input_section(self, parent, title, color, ph1, ph2, command):
        frame = ctk.CTkFrame(parent, fg_color=BG_MAIN, corner_radius=20)
        frame.pack(fill="x", padx=30, pady=10)
        ctk.CTkLabel(frame, text=title, font=("Segoe UI", 12, "bold"), text_color=color).pack(pady=10)
        
        row = ctk.CTkFrame(frame, fg_color="transparent")
        row.pack(fill="x", padx=20, pady=10)
        
        entry1 = ctk.CTkEntry(row, placeholder_text=ph1, height=40, font=("Segoe UI", 12))
        entry1.pack(side="left", fill="x", expand=True, padx=5)

        entry2 = ctk.CTkEntry(row, placeholder_text=ph2, height=40, font=("Segoe UI", 12))
        entry2.pack(side="left", fill="x", expand=True, padx=5)
        
        btn = ctk.CTkButton(frame, text=f"💾 REGISTRAR {title.split()[-1]}", fg_color=color, text_color=BG_MAIN, 
                            font=("Segoe UI", 11, "bold"), height=40, command=lambda: command(entry1, entry2))
        btn.pack(pady=(0, 15), padx=25, fill="x")
        return (entry1, entry2)

    def save_temp(self, entry):
        try:
            val = float(entry.get())
            self.db.log_temp(val)
            entry.delete(0, 'end'); self.refresh_temp()
        except ValueError: messagebox.showerror("Error", "Temperatura inválida")

    def save_pressure(self, entry):
        try:
            val = float(entry.get())
            self.db.log_pressure(val)
            entry.delete(0, 'end'); self.refresh_press()
        except ValueError: messagebox.showerror("Error", "Presión inválida")

    def save_rpm(self, entry):
        try:
            val = float(entry.get())
            self.db.log_rpm(val)
            entry.delete(0, 'end'); self.refresh_rpm()
        except ValueError: messagebox.showerror("Error", "RPM inválida")

    def save_diameter(self, e1, e2):
        try:
            diam = float(e1.get())
            metraje = float(e2.get())
            self.db.log_diameter(diam, metraje)
            e1.delete(0, 'end')
            e2.delete(0, 'end')
            self.refresh_diameter()
        except ValueError: messagebox.showerror("Error", "Valores de diámetro o metraje inválidos")

    def save_quick_diameter(self, entry):
        try:
            diam = float(entry.get())
            self.db.log_diameter(diam, 0.0)
            entry.delete(0, 'end')
            self.refresh_diameter()
        except ValueError: messagebox.showerror("Error", "Valor de diámetro inválido")

    def refresh_all(self):
        self.refresh_temp(); self.refresh_press(); self.refresh_rpm(); self.refresh_diameter()

    def refresh_temp(self):
        for widget in self.scroll_temp.winfo_children(): widget.destroy()
        logs = self.db.get_temp_logs()
        for lid, ts, v, notes in logs:
            row = EntryRow(self.scroll_temp, lid, ts, [v], ["°C"], lambda lid, vals: self.db.update_temp_log(lid, vals[0]), self.delete_temp)
            row.pack(fill="x", pady=2)

    def delete_temp(self, lid):
        if messagebox.askyesno("Borrar", "¿Eliminar este registro de Temperatura?"):
            self.db.delete_temp_log(lid); self.refresh_temp()

    def refresh_press(self):
        for widget in self.scroll_press.winfo_children(): widget.destroy()
        logs = self.db.get_pressure_logs()
        for lid, ts, v, notes in logs:
            row = EntryRow(self.scroll_press, lid, ts, [v], ["PSI"], lambda lid, vals: self.db.update_pressure_log(lid, vals[0]), self.delete_press)
            row.pack(fill="x", pady=2)

    def delete_press(self, lid):
        if messagebox.askyesno("Borrar", "¿Eliminar este registro de Presión?"):
            self.db.delete_pressure_log(lid); self.refresh_press()

    def refresh_rpm(self):
        for widget in self.scroll_rpm.winfo_children(): widget.destroy()
        logs = self.db.get_rpm_logs()
        for lid, ts, v, notes in logs:
            row = EntryRow(self.scroll_rpm, lid, ts, [v], ["RPM"], lambda lid, vals: self.db.update_rpm_log(lid, vals[0]), self.delete_rpm)
            row.pack(fill="x", pady=2)

    def delete_rpm(self, lid):
        if messagebox.askyesno("Borrar", "¿Eliminar este registro de RPM?"):
            self.db.delete_rpm_log(lid); self.refresh_rpm()

    def refresh_diameter(self):
        for widget in self.scroll_diam.winfo_children(): widget.destroy()
        logs = self.db.get_diameter_logs()
        for lid, ts, diam, metraje, notes in logs:
            row = EntryRow(self.scroll_diam, lid, ts, [diam], ["mm"], 
                           lambda lid, vals: self.db.update_diameter_log(lid, vals[0], 0.0), self.delete_diameter)
            row.pack(fill="x", pady=2)

    def delete_diameter(self, lid):
        if messagebox.askyesno("Borrar", "¿Eliminar este registro de Diámetro?"):
            self.db.delete_diameter_log(lid); self.refresh_diameter()

    def clear_all_logs(self):
        if messagebox.askyesno("Confirmar", "¿Borrar TODO el historial modular?"):
            self.db.clear_modular_logs(); self.refresh_all()

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
        self.show_view()

    def show_view(self):
        for w in self.container.winfo_children(): w.destroy()
        for i, v in enumerate(self.values):
            ctk.CTkLabel(self.container, text=f"{v}{self.units[i]}", font=("Segoe UI", 11, "bold"), text_color=TEXT_P).pack(side="left", padx=10)
        ctk.CTkButton(self, text="✏️", width=30, height=30, fg_color="transparent", hover_color="#334155", command=self.show_edit).pack(side="right", padx=5)
        ctk.CTkButton(self, text="🗑️", width=30, height=30, fg_color="transparent", hover_color=DANGER_P, command=lambda: self.on_delete(self.entry_id)).pack(side="right", padx=5)

    def show_edit(self):
        for w in self.container.winfo_children(): w.destroy()
        for w in self.winfo_children(): 
            if isinstance(w, ctk.CTkButton): w.destroy()
        self.entries = []
        for i, v in enumerate(self.values):
            ent = ctk.CTkEntry(self.container, width=60, height=25)
            ent.insert(0, str(v)); ent.pack(side="left", padx=5)
            self.entries.append(ent)
        ctk.CTkButton(self, text="💾", width=30, height=30, fg_color=ACCENT_GREEN, command=self.save_edit).pack(side="right", padx=5)
        ctk.CTkButton(self, text="❌", width=30, height=30, fg_color="#475569", command=self.show_view).pack(side="right", padx=5)

    def save_edit(self):
        try:
            new_vals = [float(e.get()) for e in self.entries]
            self.on_save(self.entry_id, new_vals); self.show_view()
        except ValueError: messagebox.showerror("Error", "Valores inválidos")
