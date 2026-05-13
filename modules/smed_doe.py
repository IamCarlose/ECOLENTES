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

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class DOEModule(ctk.CTkFrame):
    def __init__(self, master, db_manager, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.db = db_manager
        
        # Header
        header = ctk.CTkFrame(self, fg_color=PANEL_BG, corner_radius=20, border_width=1, border_color="#334155")
        header.pack(fill="x", padx=10, pady=10)
        ctk.CTkLabel(header, text="📈 ENGINEERING DOE & STATISTICAL DASHBOARD", font=("Segoe UI", 18, "bold"), text_color=ACCENT_BLUE).pack(side="left", padx=30, pady=25)
        
        btn_refresh = ctk.CTkButton(header, text="🔄 ACTUALIZAR GRÁFICOS", fg_color=ACCENT_BLUE, text_color=BG_MAIN, font=("Segoe UI", 11, "bold"), width=150, height=35, command=self.plot_graphs)
        btn_refresh.pack(side="right", padx=30)

        # Matplotlib Figure Container
        self.chart_container = ctk.CTkFrame(self, fg_color=PANEL_BG, corner_radius=25, border_width=1, border_color="#334155")
        self.chart_container.pack(fill="both", expand=True, padx=10, pady=10)

        self.fig = Figure(figsize=(12, 8), dpi=100, facecolor=PANEL_BG)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_container)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=15, pady=15)
        
        self.plot_graphs()

    def plot_graphs(self):
        self.fig.clf()
        
        # Grid layout for subplots
        ax1 = self.fig.add_subplot(221) # X-R Chart
        ax2 = self.fig.add_subplot(222) # Histogram
        ax3 = self.fig.add_subplot(212) # Scatter Plot
        
        for ax in [ax1, ax2, ax3]:
            ax.set_facecolor(PANEL_BG)
            ax.tick_params(colors=TEXT_S)
            for spine in ax.spines.values():
                spine.set_color('#E2E8F0')

        # --- Data Fetching ---
        d_logs = self.db.get_diameter_logs()
        diameters = [log[2] for log in d_logs][::-1] # Reverse for chronological order
        
        t_logs = self.db.get_temp_logs()
        r_logs = self.db.get_rpm_logs()
        temps = [log[2] for log in t_logs]
        rpms = [log[2] for log in r_logs]
        
        # --- 1. X-R (Individuals) Control Chart: Diameter vs Time ---
        ax1.set_title("Gráfico de Control: Diámetro vs Tiempo", color=TEXT_P, fontsize=10, weight='bold')
        if diameters:
            ax1.plot(diameters, marker='o', color=ACCENT_BLUE, linestyle='-', markersize=4)
            ax1.axhline(NOMINAL_DIAMETER, color=ACCENT_GREEN, linestyle='--', label='Nominal')
            ax1.axhline(USL_DIAMETER, color=DANGER_P, linestyle=':', label='USL')
            ax1.axhline(LSL_DIAMETER, color=DANGER_P, linestyle=':', label='LSL')
            ax1.legend(loc='upper right', fontsize=8)
        else:
            ax1.text(0.5, 0.5, "Sin Datos", ha='center', va='center', color=TEXT_S)

        # --- 2. Histogram: Diameter Distribution ---
        ax2.set_title("Histograma de Distribución de Diámetro", color=TEXT_P, fontsize=10, weight='bold')
        if diameters:
            ax2.hist(diameters, bins=10, color=ACCENT_GREEN, alpha=0.7, edgecolor='white')
            ax2.axvline(NOMINAL_DIAMETER, color=TEXT_P, linestyle='dashed', linewidth=1)
        else:
            ax2.text(0.5, 0.5, "Sin Datos", ha='center', va='center', color=TEXT_S)

        # --- 3. Scatter Plot: Temp vs RPM ---
        ax3.set_title("Correlación: Temperatura (Boquilla) vs Velocidad Tracción (RPM)", color=TEXT_P, fontsize=10, weight='bold')
        min_len = min(len(temps), len(rpms))
        if min_len > 0:
            # Pair sequentially for demonstration
            ax3.scatter(temps[:min_len], rpms[:min_len], color=ACCENT_GOLD, alpha=0.8, edgecolors='w', s=50)
            ax3.set_xlabel("Temperatura (°C)", color=TEXT_S, fontsize=9)
            ax3.set_ylabel("RPM", color=TEXT_S, fontsize=9)
            
            # Trendline
            z = np.polyfit(temps[:min_len], rpms[:min_len], 1)
            p = np.poly1d(z)
            ax3.plot(temps[:min_len], p(temps[:min_len]), color=DANGER_P, linestyle="--", alpha=0.5)
        else:
            ax3.text(0.5, 0.5, "Datos Insuficientes para Correlación", ha='center', va='center', color=TEXT_S)

        self.fig.tight_layout()
        self.canvas.draw()
