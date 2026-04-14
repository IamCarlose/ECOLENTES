import customtkinter as ctk
from app_config import *
from database import DatabaseManager
from widgets.top_bar import TopBar
from widgets.gauge import MatplotlibGauge
from modules.login import LoginModule
from modules.dashboard import DashboardModule
from modules.smed_doe import SMEDModule, DOEModule
from modules.spaghetti import SpaghettiModule
from modules.hildegard import HildegardModule

class EcolentesStunningOS(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- CORE SETUP ---
        self.title("Ecolentes OS v4.0 - Stunning Industrial Series")
        self.geometry("1450x900")
        self.configure(fg_color=BG_MAIN)
        setup_branding_theme()
        
        self.db = DatabaseManager()
        self.u_name = None
        self.u_role = None
        
        # Display Area
        self.main_c = ctk.CTkFrame(self, fg_color="transparent")
        self.main_c.pack(fill="both", expand=True)
        
        self.modules = {} # Cache for state persistence
        self.load_login_view()

    def load_login_view(self):
        self.clear_frame(self.main_c)
        self.login = LoginModule(self.main_c, self.on_auth_success, self.db)
        self.login.pack(fill="both", expand=True)

    def on_auth_success(self, name, role):
        self.u_name = name
        self.u_role = role
        self.launch_interface()

    def launch_interface(self):
        self.clear_frame(self.main_c)
        
        # Persistent Header (Solving navigation issues)
        self.header = TopBar(self.main_c, self.u_name, self.load_login_view)
        self.header.pack(side="top", fill="x")
        
        # Application Container
        self.app_b = ctk.CTkFrame(self.main_c, fg_color="transparent")
        self.app_b.pack(side="top", fill="both", expand=True)
        
        # Stunning Navigation Sidebar
        self.side = ctk.CTkFrame(self.app_b, width=280, fg_color=BG_MAIN, corner_radius=0)
        self.side.pack(side="left", fill="y")
        self.side.pack_propagate(False)
        
        # Logo Label in Sidebar
        ctk.CTkLabel(self.side, text="ECOLENTES OS 4.0", font=("Segoe UI", 24, "bold"), text_color=TEXT_P).pack(pady=(40, 5))
        ctk.CTkLabel(self.side, text="— QUALITY ASSURANCE —", font=("Segoe UI", 9, "bold"), text_color=ACCENT_GREEN).pack(pady=(0, 40))
        
        # Nav Map
        options = [
            ("DASHBOARD", "⚡", self.open_dash),
            ("SMED OPTIMIZER", "🎯", self.open_smed),
            ("FLUX DIAGRAM", "⚛️", self.open_spaghetti),
            ("HILDEGARD 2.0", "🔥", self.open_hildegard)
        ]
        
        for name, icon, func in options:
            b = ctk.CTkButton(self.side, text=f"{icon}  {name}", font=("Segoe UI", 12, "bold"), fg_color="transparent", 
                              text_color=TEXT_P, anchor="w", height=55, hover_color=PANEL_BG, corner_radius=0, command=func)
            b.pack(fill="x")

        if self.u_role == "Ingeniero":
            b = ctk.CTkButton(self.side, text="🧪  ENGINEERING DOE", font=("Segoe UI", 12, "bold"), fg_color="transparent", 
                              text_color=TEXT_P, anchor="w", height=55, hover_color=PANEL_BG, corner_radius=0, command=self.open_doe)
            b.pack(fill="x")

        # Global Gauge (Lower Sidebar)
        g_box = ctk.CTkFrame(self.side, fg_color=PANEL_BG, corner_radius=20, height=250)
        g_box.pack(side="bottom", fill="x", padx=15, pady=30)
        ctk.CTkLabel(g_box, text="RENDIMIENTO OEE", font=("Segoe UI", 11, "bold"), text_color=TEXT_S).pack(pady=10)
        self.main_g = MatplotlibGauge(g_box, bg_color=PANEL_BG)

        # Content Port
        self.port = ctk.CTkFrame(self.app_b, fg_color="transparent")
        self.port.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        self.open_dash()

    def clear_frame(self, frame):
        for w in frame.winfo_children(): w.destroy()

    def show_module(self, module_name, module_class, *args):
        # Hide all
        for m in self.modules.values():
            m.pack_forget()
            
        # Create if not exists
        if module_name not in self.modules:
            self.modules[module_name] = module_class(self.port, *args)
            
        # Show specific
        mod = self.modules[module_name]
        mod.pack(fill="both", expand=True)
        return mod

    def open_dash(self):
        d = self.show_module("dash", DashboardModule, self.db, self.u_role)
        d.link_gauge(self.main_g)

    def open_smed(self):
        self.show_module("smed", SMEDModule)

    def open_spaghetti(self):
        uid = self.db.get_user_id(self.u_name)
        self.show_module("spaghetti", SpaghettiModule, self.db, uid)

    def open_doe(self):
        self.show_module("doe", DOEModule)

    def open_hildegard(self):
        self.show_module("hildegard", HildegardModule, self.db)

def main():
    app = EcolentesStunningOS()
    # Smooth Entry Effect (Simulated via initial update)
    app.update()
    app.attributes('-alpha', 0.98) # Stunning subtle transparency
    app.mainloop()

if __name__ == "__main__":
    main()
