import customtkinter as ctk
from app_config import *

import numpy as np

class MonitoringModule(ctk.CTkFrame):
    def __init__(self, master, db_manager, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.db = db_manager
        
        # HEADER
        header = ctk.CTkFrame(self, fg_color=PANEL_BG, corner_radius=20, border_width=1, border_color="#334155")
        header.pack(fill="x", padx=10, pady=10)
        ctk.CTkLabel(header, text="🖥️ SUPERVISOR & ENGINEERING MONITOR", font=("Segoe UI", 18, "bold"), text_color=ACCENT_BLUE).pack(side="left", padx=30, pady=25)
        
        btn_refresh = ctk.CTkButton(header, text="🔄 ACTUALIZAR DATOS", fg_color=ACCENT_BLUE, text_color=BG_MAIN, font=("Segoe UI", 11, "bold"), width=150, height=35, command=self.refresh_dashboard)
        btn_refresh.pack(side="right", padx=30)

        # SPLIT LAYOUT
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # LEFT PANEL: CAPABILITY & ALERTS
        self.left_panel = ctk.CTkFrame(self, fg_color="transparent")
        self.left_panel.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Capability Card
        self.cap_card = ctk.CTkFrame(self.left_panel, fg_color=PANEL_BG, corner_radius=20, border_width=1, border_color="#334155")
        self.cap_card.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(self.cap_card, text="CAPACIDAD DEL PROCESO (DIÁMETRO)", font=("Segoe UI", 12, "bold"), text_color=TEXT_S).pack(pady=10)
        
        self.lbl_cp = ctk.CTkLabel(self.cap_card, text="Cp: --", font=("Segoe UI", 24, "bold"), text_color=TEXT_P)
        self.lbl_cp.pack(pady=5)
        self.lbl_cpk = ctk.CTkLabel(self.cap_card, text="Cpk: --", font=("Segoe UI", 24, "bold"), text_color=TEXT_P)
        self.lbl_cpk.pack(pady=5)
        
        self.lbl_alert = ctk.CTkLabel(self.cap_card, text="SIN DATOS SUFICIENTES", font=("Segoe UI", 12, "bold"), text_color=ACCENT_GOLD)
        self.lbl_alert.pack(pady=15)

        # Quality Stats Card
        self.qual_card = ctk.CTkFrame(self.left_panel, fg_color=PANEL_BG, corner_radius=20, border_width=1, border_color="#334155")
        self.qual_card.pack(fill="both", expand=True)
        ctk.CTkLabel(self.qual_card, text="RESUMEN DE CALIDAD", font=("Segoe UI", 12, "bold"), text_color=TEXT_S).pack(pady=10)
        
        self.lbl_total_batches = ctk.CTkLabel(self.qual_card, text="Lotes Totales: --", font=("Segoe UI", 14), text_color=TEXT_P)
        self.lbl_total_batches.pack(pady=5)
        self.lbl_total_defects = ctk.CTkLabel(self.qual_card, text="Botellas Malas (Total): --", font=("Segoe UI", 14), text_color=DANGER_P)
        self.lbl_total_defects.pack(pady=5)

        self.lbl_total_defects.pack(pady=5)

        # RIGHT PANEL: BATCH REGISTRY
        self.right_panel = ctk.CTkFrame(self, fg_color=PANEL_BG, corner_radius=20, border_width=1, border_color="#334155")
        self.right_panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        header_f = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        header_f.pack(fill="x", padx=10, pady=10)
        
        header_f.grid_columnconfigure(0, weight=1)
        header_f.grid_columnconfigure(1, weight=1)
        header_f.grid_columnconfigure(2, weight=1)
        
        ctk.CTkLabel(header_f, text="REGISTRO DE LOTES (PRODUCCIÓN)", font=("Segoe UI", 12, "bold"), text_color=TEXT_S).grid(row=0, column=1)
        ctk.CTkButton(header_f, text="🧨 LIMPIAR HISTORIAL", fg_color="transparent", text_color=DANGER_P, border_width=1, border_color=DANGER_P, height=28, font=("Segoe UI", 10, "bold"), command=self.clear_all_batches).grid(row=0, column=2, sticky="e")
        
        # Manual Lote Entry Form
        self.manual_f = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        self.manual_f.pack(fill="x", padx=10, pady=(0, 10))
        
        self.ent_op = ctk.CTkEntry(self.manual_f, placeholder_text="Operador", width=120)
        self.ent_op.pack(side="left", padx=5)
        
        self.ent_dur = ctk.CTkEntry(self.manual_f, placeholder_text="Duración (min)", width=120)
        self.ent_dur.pack(side="left", padx=5)
        
        self.ent_def = ctk.CTkEntry(self.manual_f, placeholder_text="Defectos", width=100)
        self.ent_def.pack(side="left", padx=5)
        
        self.btn_add_lot = ctk.CTkButton(self.manual_f, text="➕ REGISTRAR LOTE", fg_color=ACCENT_GREEN, command=self.add_manual_lot)
        self.btn_add_lot.pack(side="left", padx=10)

        # Batch Table Header (Aligned with scrollable area)
        h_frame = ctk.CTkFrame(self.right_panel, fg_color=BG_MAIN, height=35, corner_radius=10)
        h_frame.pack(fill="x", padx=(5, 22), pady=(0, 10))
        cols = ["LOTE ID", "OPERADOR", "DURACIÓN", "DEFECTOS", "ESTADO"]
        for i, col in enumerate(cols):
            h_frame.grid_columnconfigure(i, weight=1)
            ctk.CTkLabel(h_frame, text=col, font=("Segoe UI", 10, "bold"), text_color=TEXT_S).grid(row=0, column=i, padx=5, pady=5)
        
        # Spacer column exactly matching the buttons in BatchRow
        h_frame.grid_columnconfigure(5, weight=0)
        btn_dummy = ctk.CTkFrame(h_frame, fg_color="transparent")
        btn_dummy.grid(row=0, column=5, sticky="e", padx=5)
        ctk.CTkButton(btn_dummy, text="", width=30, height=30, fg_color="transparent").pack(side="left")
        ctk.CTkButton(btn_dummy, text="", width=30, height=30, fg_color="transparent").pack(side="left")
            
        self.scroll_batches = ctk.CTkScrollableFrame(self.right_panel, fg_color="transparent")
        self.scroll_batches.pack(fill="both", expand=True, padx=5, pady=5)

        self.refresh_dashboard()

    def add_manual_lot(self):
        op = self.ent_op.get() or "Manual"
        try:
            dur = float(self.ent_dur.get())
        except ValueError:
            dur = 0.0
        try:
            defs = int(self.ent_def.get())
        except ValueError:
            defs = 0
            
        self.db.log_cycle(dur, op, "Completado", rejects=defs)
        self.ent_dur.delete(0, 'end')
        self.ent_def.delete(0, 'end')
        self.refresh_dashboard()

    def refresh_dashboard(self):
        # 1. Calculate Cp and Cpk
        d_logs = self.db.get_diameter_logs()
        diameters = [float(log[2]) for log in d_logs]
        
        if len(diameters) > 1:
            mean = np.mean(diameters)
            std = np.std(diameters, ddof=1)
            
            if std > 0:
                cp = (USL_DIAMETER - LSL_DIAMETER) / (6 * std)
                cpk_u = (USL_DIAMETER - mean) / (3 * std)
                cpk_l = (mean - LSL_DIAMETER) / (3 * std)
                cpk = min(cpk_u, cpk_l)
                
                self.lbl_cp.configure(text=f"Cp: {cp:.2f}")
                self.lbl_cpk.configure(text=f"Cpk: {cpk:.2f}")
                
                if cpk < 1.0:
                    self.lbl_alert.configure(text="⚠️ ALERTA: PROCESO INCAPAZ (Cpk < 1)", text_color=DANGER_P)
                elif cpk < 1.33:
                    self.lbl_alert.configure(text="⚠️ ADVERTENCIA: CAPACIDAD MARGINAL", text_color=ACCENT_GOLD)
                else:
                    self.lbl_alert.configure(text="✅ PROCESO ESTABLE Y CAPAZ", text_color=ACCENT_GREEN)
            else:
                self.lbl_cp.configure(text="Cp: N/A (Std=0)")
                self.lbl_cpk.configure(text="Cpk: N/A")
                self.lbl_alert.configure(text="DATOS CONSTANTES (Std=0)", text_color=TEXT_P)
        else:
            self.lbl_cp.configure(text="Cp: --")
            self.lbl_cpk.configure(text="Cpk: --")
            self.lbl_alert.configure(text="SIN DATOS SUFICIENTES", text_color=ACCENT_GOLD)

        # 2. Refresh Batches (Production Cycles)
        for w in self.scroll_batches.winfo_children(): w.destroy()
        
        cycles = self.db.get_full_history()
        # To display "Lote 1", "Lote 2", we need to know their ascending order.
        # get_full_history() returns DESC (newest first). Let's reverse it to assign sequential numbers, then reverse back.
        cycles_asc = list(reversed(cycles))
        
        total_defects = 0
        total_batches = len(cycles)
        
        for idx in range(len(cycles_asc)-1, -1, -1):
            cycle = cycles_asc[idx]
            cid = cycle[0]
            dur = cycle[2]
            op = cycle[3]
            stat = cycle[4]
            rejects = cycle[7] if len(cycle) > 7 else 0
            
            total_defects += rejects
            display_id = idx + 1 # Lote 1, Lote 2...
            
            row = BatchRow(self.scroll_batches, cid, display_id, op, dur, rejects, stat, self.save_batch_edit, self.delete_batch)
            row.pack(fill="x", pady=2)
            
        self.lbl_total_batches.configure(text=f"Lotes Totales Registrados: {total_batches}")
        self.lbl_total_defects.configure(text=f"Botellas Malas (Total): {total_defects}")

    def save_batch_edit(self, cid, op, dur, defects):
        self.db.update_cycle(cid, op, dur, defects)
        self.refresh_dashboard()

    def delete_batch(self, cid):
        from tkinter import messagebox
        if messagebox.askyesno("Borrar", "¿Eliminar este lote?"):
            self.db.delete_cycle(cid)
            self.refresh_dashboard()

    def clear_all_batches(self):
        from tkinter import messagebox
        if messagebox.askyesno("Confirmar", "¿Estás seguro de borrar TODO el historial de lotes?"):
            self.db.clear_all_cycles()
            self.refresh_dashboard()

class BatchRow(ctk.CTkFrame):
    def __init__(self, master, cid, display_id, op, dur, rejects, stat, on_save, on_delete):
        super().__init__(master, fg_color="transparent", border_width=1, border_color=BG_MAIN)
        self.cid = cid
        self.display_id = display_id
        self.op = op
        self.dur = dur
        self.rejects = rejects
        self.stat = stat
        self.on_save = on_save
        self.on_delete = on_delete
        
        for i in range(5): self.grid_columnconfigure(i, weight=1)
        self.grid_columnconfigure(5, weight=0)
        
        self.show_view()

    def show_view(self):
        for w in self.winfo_children(): w.destroy()
        ctk.CTkLabel(self, text=f"Lote {self.display_id}", font=("Segoe UI", 11, "bold"), text_color=ACCENT_BLUE).grid(row=0, column=0, padx=5, pady=5)
        ctk.CTkLabel(self, text=str(self.op), font=("Segoe UI", 11), text_color=TEXT_P).grid(row=0, column=1, padx=5, pady=5)
        ctk.CTkLabel(self, text=f"{self.dur:.1f} min", font=("Segoe UI", 11), text_color=TEXT_S).grid(row=0, column=2, padx=5, pady=5)
        
        color_def = DANGER_P if self.rejects > 0 else TEXT_S
        ctk.CTkLabel(self, text=f"{self.rejects} pcs", font=("Segoe UI", 11, "bold"), text_color=color_def).grid(row=0, column=3, padx=5, pady=5)
        
        stat_color = ACCENT_GREEN if "Completado" in self.stat else ACCENT_GOLD
        ctk.CTkLabel(self, text=self.stat, font=("Segoe UI", 11, "bold"), text_color=stat_color).grid(row=0, column=4, padx=5, pady=5)

        btn_f = ctk.CTkFrame(self, fg_color="transparent")
        btn_f.grid(row=0, column=5, sticky="e", padx=5)
        ctk.CTkButton(btn_f, text="✏️", width=30, height=30, fg_color="transparent", hover_color="#334155", command=self.show_edit).pack(side="left")
        ctk.CTkButton(btn_f, text="🗑️", width=30, height=30, fg_color="transparent", hover_color=DANGER_P, command=lambda: self.on_delete(self.cid)).pack(side="left")

    def show_edit(self):
        dialog = ctk.CTkToplevel(self.winfo_toplevel())
        dialog.title("Editar Lote")
        dialog.geometry("300x400")
        dialog.attributes('-topmost', True)
        dialog.grab_set()
        
        ctk.CTkLabel(dialog, text=f"Editando Lote {self.display_id}", font=("Segoe UI", 16, "bold")).pack(pady=15)
        
        ctk.CTkLabel(dialog, text="Operador:").pack(pady=2)
        ent_op = ctk.CTkEntry(dialog)
        ent_op.insert(0, str(self.op))
        ent_op.pack(pady=5)
        
        ctk.CTkLabel(dialog, text="Duración (min):").pack(pady=2)
        ent_dur = ctk.CTkEntry(dialog)
        ent_dur.insert(0, str(self.dur))
        ent_dur.pack(pady=5)
        
        ctk.CTkLabel(dialog, text="Defectos (botellas):").pack(pady=2)
        ent_def = ctk.CTkEntry(dialog)
        ent_def.insert(0, str(self.rejects))
        ent_def.pack(pady=5)
        
        def save():
            try:
                new_op = ent_op.get()
                new_dur = float(ent_dur.get())
                new_def = int(ent_def.get())
                # Destroy dialog first to avoid widget destruction errors
                dialog.destroy()
                # Schedule the save and refresh safely
                self.winfo_toplevel().after(50, lambda: self.on_save(self.cid, new_op, new_dur, new_def))
            except ValueError:
                from tkinter import messagebox
                messagebox.showerror("Error", "Asegúrate de ingresar números válidos para la duración y defectos.")
                
        ctk.CTkButton(dialog, text="💾 GUARDAR CAMBIOS", fg_color=ACCENT_GREEN, command=save).pack(pady=20)

