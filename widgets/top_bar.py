import customtkinter as ctk
from PIL import Image
from app_config import *
import os
import sys

class TopBar(ctk.CTkFrame):
    def __init__(self, master, user_name, on_logout, **kwargs):
        # Slightly transparent effect simulated by PANEL_BG
        super().__init__(master, fg_color=PANEL_BG, height=50, corner_radius=0, **kwargs)
        self.on_logout = on_logout
        
        # Logo Icon
        if os.path.exists(LOGO_IMG):
            logo_pil = Image.open(LOGO_IMG)
            self.logo_img = ctk.CTkImage(logo_pil, size=(80, 40))
            self.logo_icon = ctk.CTkLabel(self, image=self.logo_img, text="")
            self.logo_icon.pack(side="left", padx=(25, 10))
            self.logo_lbl = ctk.CTkLabel(self, text="ECOLENS APP", font=("Segoe UI", 12, "bold"), text_color=ACCENT_GREEN)
            self.logo_lbl.pack(side="left")
        else:
            self.logo_lbl = ctk.CTkLabel(self, text="ECOLENS APP", font=("Segoe UI", 12, "bold"), text_color=ACCENT_GREEN)
            self.logo_lbl.pack(side="left", padx=25)
        
        # User Badge
        self.user_lbl = ctk.CTkLabel(self, text=f"OPERADOR: {user_name.upper()}", font=("Segoe UI", 10), text_color=TEXT_S)
        self.user_lbl.pack(side="left", padx=20)
        
        # Navigation Actions
        self.btn_exit = ctk.CTkButton(self, text="SALIR", width=80, height=30, fg_color="transparent", border_width=1, border_color=DANGER_P, text_color=DANGER_P, hover_color=DANGER_P, command=self.shutdown)
        self.btn_exit.pack(side="right", padx=10)
        
        self.btn_off = ctk.CTkButton(self, text="CERRAR SESIÓN", width=120, height=30, fg_color=ACCENT_GREEN, text_color=BG_MAIN, font=("Segoe UI", 10, "bold"), command=on_logout)
        self.btn_off.pack(side="right", padx=10)

    def shutdown(self):
        sys.exit()
