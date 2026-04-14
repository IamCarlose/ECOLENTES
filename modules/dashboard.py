import customtkinter as ctk
from widgets.timer import IndustrialTimer
from widgets.gauge import MatplotlibGauge
from app_config import *
import numpy as np
from datetime import datetime
from modules.reporting import IndustrialReportGenerator
import os
from tkinter import messagebox

class KPICard(ctk.CTkFrame):
    def __init__(self, master, title, value, color, **kwargs):
        super().__init__(master, fg_color=PANEL_BG, corner_radius=15, border_width=1, border_color="#334155", **kwargs)
        ctk.CTkLabel(self, text=title, font=("Segoe UI", 10, "bold"), text_color=TEXT_S).pack(pady=(15, 5))
        self.val_lbl = ctk.CTkLabel(self, text=value, font=("Segoe UI", 24, "bold"), text_color=color)
        self.val_lbl.pack(pady=(0, 15))

    def update_val(self, new_val):
        self.val_lbl.configure(text=new_val)

class DashboardModule(ctk.CTkFrame):
    def __init__(self, master, db_manager, user_role, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.db = db_manager
        self.role = user_role
        self.laps_data = [] 
        self.last_lap_time = 0.0
        self.cycle_count = 0
        
        # --- UI LAYOUT ---
        self.kpi_row = ctk.CTkFrame(self, fg_color="transparent")
        self.kpi_row.pack(fill="x", pady=(0, 10))
        
        self.card_last = KPICard(self.kpi_row, "ÚLTIMO REGISTRO", "---", ACCENT_BLUE)
        self.card_last.pack(side="left", fill="both", expand=True, padx=5)
        
        self.card_avg = KPICard(self.kpi_row, "PROMEDIO (TURNO)", "---", ACCENT_GREEN)
        self.card_avg.pack(side="left", fill="both", expand=True, padx=5)
        
        self.card_oee = KPICard(self.kpi_row, "EFICIENCIA OEE (%)", "0%", "#F59E0B")
        self.card_oee.pack(side="left", fill="both", expand=True, padx=5)

        self.main_c = ctk.CTkFrame(self, fg_color="transparent")
        self.main_c.pack(fill="both", expand=True)
        self.main_c.grid_columnconfigure(0, weight=6)
        self.main_c.grid_columnconfigure(1, weight=4)
        
        # LEFT PANEL: TIMER & LOG
        self.p_panel = ctk.CTkFrame(self.main_c, fg_color=PANEL_BG, corner_radius=25, border_width=1, border_color="#334155")
        self.p_panel.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        self.timer_lbl = ctk.CTkLabel(self.p_panel, text="00:00:00", font=("Consolas", 80, "bold"), text_color=TEXT_P)
        self.timer_lbl.pack(pady=(20, 0))
        
        self.lap_lbl = ctk.CTkLabel(self.p_panel, text="PARCIAL: 00:00.00", font=("Consolas", 18, "bold"), text_color=ACCENT_BLUE)
        self.lap_lbl.pack(pady=(0, 15))
        
        self.timer = IndustrialTimer(self.update_live_ui)
        
        # Controls Group
        self.ctrl_f = ctk.CTkFrame(self.p_panel, fg_color="transparent")
        self.ctrl_f.pack(fill="x", padx=30)
        
        self.btn_act = ctk.CTkButton(self.ctrl_f, text="INICIAR CAPTURA", fg_color=ACCENT_GREEN, text_color=BG_MAIN, font=("Segoe UI", 13, "bold"), height=50, command=self.handle_start_lap)
        self.btn_act.pack(fill="x", pady=5)
        
        self.btn_pause = ctk.CTkButton(self.ctrl_f, text="PAUSAR", fg_color="#475569", font=("Segoe UI", 11, "bold"), height=40, command=self.toggle_pause, state="disabled")
        self.btn_pause.pack(fill="x", pady=5)
        
        self.btn_clr = ctk.CTkButton(self.ctrl_f, text="LIMPIAR REINICIAR", fg_color="transparent", text_color=TEXT_S, border_width=1, border_color=TEXT_S, height=35, command=self.clear_active_data)
        self.btn_clr.pack(fill="x", pady=5)

        self.btn_exp = ctk.CTkButton(self.p_panel, text="📊 GENERAR REPORTE PDF", fg_color="#334155", font=("Segoe UI", 11, "bold"), height=40, command=self.export_report)
        self.btn_exp.pack(pady=(10, 5))

        self.btn_xlsx = ctk.CTkButton(self.p_panel, text="📈 GENERAR REPORTE EXCEL (GRAF.)", fg_color="#1E293B", font=("Segoe UI", 11, "bold"), height=40, command=self.export_excel)
        self.btn_xlsx.pack(pady=5)

        # LOG AREA WITH CTKSCROLLABLEFRAME (BETTER USABILITY)
        ctk.CTkLabel(self.p_panel, text="HISTORIAL DE CICLO (INTERACTIVO)", font=("Segoe UI", 10, "bold"), text_color=ACCENT_BLUE).pack(pady=(10, 0))
        
        self.history_scroll = ctk.CTkScrollableFrame(self.p_panel, height=300, fg_color=BG_MAIN, border_width=1, border_color="#334155")
        self.history_scroll.pack(fill="both", expand=True, padx=20, pady=(5, 20))

    def sync_history(self):
        for widget in self.history_scroll.winfo_children(): widget.destroy()
        
        # Header
        header = ctk.CTkFrame(self.history_scroll, fg_color="transparent")
        header.pack(fill="x")
        ctk.CTkLabel(header, text=f"{'ID':<6} | {'VUELTA':<12} | {'TOTAL':<12}", font=("Consolas", 11), text_color=TEXT_S).pack(side="left", padx=10)
        
        for lap in self.laps_data:
            row = ctk.CTkFrame(self.history_scroll, fg_color="transparent")
            row.pack(fill="x", pady=1)
            txt = f"#{lap['id']:02d}    | {lap['lap']:.2f}s     | {lap['total']:.2f}s"
            ctk.CTkLabel(row, text=txt, font=("Consolas", 11), text_color=TEXT_P).pack(side="left", padx=10)

    def clear_active_data(self):
        self.timer.stop(); self.timer.reset()
        self.timer_lbl.configure(text="00:00:00"); self.lap_lbl.configure(text="PARCIAL: 00:00.00")
        self.laps_data = []; self.last_lap_time = 0.0; self.cycle_count = 0
        self.sync_history()
        self.btn_act.configure(text="INICIAR CAPTURA", fg_color=ACCENT_GREEN, state="normal")
        self.btn_pause.configure(text="PAUSAR", state="disabled")

    def handle_start_lap(self):
        if not self.timer.running and self.timer.elapsed == 0:
            self.timer.start()
            self.btn_act.configure(text="MARCAR VUELTA (LAP)", fg_color=ACCENT_BLUE)
            self.btn_pause.configure(state="normal")
        elif self.timer.running:
            cur = self.timer.elapsed
            dur = cur - self.last_lap_time
            self.cycle_count += 1
            self.laps_data.append({'id': self.cycle_count, 'lap': dur, 'total': cur})
            self.last_lap_time = cur
            self.sync_history()
            self.card_last.update_val(f"{dur:.2f}s")
            self.db.log_cycle(dur, "ADMIN", "OK")

    def toggle_pause(self):
        if self.timer.running:
            self.timer.stop()
            self.btn_pause.configure(text="REANUDAR", fg_color=ACCENT_GREEN)
            self.btn_act.configure(state="disabled")
        else:
            self.timer.start()
            self.btn_pause.configure(text="PAUSAR", fg_color="#475569")
            self.btn_act.configure(state="normal")

    def export_report(self):
        rep = IndustrialReportGenerator(self.db)
        try:
            path = rep.generate_pdf()
            os.startfile(path)
            self.btn_exp.configure(text="✓ ENVIADO A PDF", fg_color=ACCENT_GREEN)
        except Exception as e: print(f"Error: {e}")

    def export_excel(self):
        rep = IndustrialReportGenerator(self.db)
        try:
            path = rep.generate_excel()
            if path:
                os.startfile(path)
                self.btn_xlsx.configure(text="✓ EXCEL GENERADO", fg_color=ACCENT_GREEN)
            else:
                messagebox.showerror("Error", "No se pudo generar el reporte Excel.")
        except Exception as e: 
            print(f"Error: {e}")
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")

    def update_live_ui(self, elapsed):
        m, s = divmod(elapsed, 60); ms = int((s - int(s)) * 100)
        self.timer_lbl.configure(text=f"{int(m):02d}:{int(s):02d}:{ms:02d}")
        lap_elapsed = elapsed - self.last_lap_time
        lm, ls = divmod(lap_elapsed, 60); lms = int((ls - int(ls)) * 100)
        self.lap_lbl.configure(text=f"PARCIAL: {int(lm):02d}:{int(ls):02d}.{lms:02d}")
        if elapsed > (STANDARD_TIME * ANDON_THRESHOLD): self.p_panel.configure(border_color=DANGER_P, border_width=2)
        elif elapsed > STANDARD_TIME: self.p_panel.configure(border_color="#F59E0B", border_width=2)
        else: self.p_panel.configure(border_color="#334155", border_width=1)
