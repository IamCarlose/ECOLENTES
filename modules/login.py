import customtkinter as ctk
from PIL import Image
from app_config import *
import os
import tkinter as tk

class AbstractArtPanel(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.canvas = tk.Canvas(self, bg=PANEL_BG, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=20, pady=20)
        self.bind("<Configure>", self.draw_art)
        self.after(500, self.draw_art) # Increased delay to ensure window is ready
        self.canvas.bind("<Map>", self.draw_art) # Redraw when mapped (visible)

    def draw_art(self, event=None):
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w < 10 or h < 10: return
        
        # 1. Background Grid (Tech vibe)
        for i in range(0, w, 30):
            self.canvas.create_line(i, 0, i, h, fill="#F8FAFC", width=1)
        for i in range(0, h, 30):
            self.canvas.create_line(0, i, w, i, fill="#F8FAFC", width=1)

        # 2. Dynamic Industrial Curves (Flow)
        self.canvas.create_oval(-50, h*0.2, w*0.6, h*1.2, outline=LIME_MINT, width=40)
        self.canvas.create_oval(w*0.4, -h*0.2, w+50, h*0.8, outline="#F1F5F9", width=30)
        
        # 3. Geometric Eco-Intersections
        # Main Hexagon Glass Effect
        pts = [w*0.5, h*0.2, w*0.8, h*0.35, w*0.8, h*0.65, w*0.5, h*0.8, w*0.2, h*0.65, w*0.2, h*0.35]
        self.canvas.create_polygon(pts, fill="", outline=ACCENT_GREEN, width=2, dash=(10,5))
        
        # 4. Floating Industrial Nodes
        nodes = [(w*0.3, h*0.4), (w*0.7, h*0.5), (w*0.4, h*0.7), (w*0.6, h*0.2)]
        for nx, ny in nodes:
            self.canvas.create_oval(nx-15, ny-15, nx+15, ny+15, fill=PANEL_BG, outline=ACCENT_BLUE, width=3)
            self.canvas.create_oval(nx-5, ny-5, nx+5, ny+5, fill=ACCENT_BLUE, outline="")

        # 5. Connected Threads (Spaghetti hint)
        self.canvas.create_line(w*0.3, h*0.4, w*0.7, h*0.5, fill=ACCENT_BLUE, width=1)
        self.canvas.create_line(w*0.7, h*0.5, w*0.4, h*0.7, fill=ACCENT_BLUE, width=1)

        # 6. Organic Accents (Leaf shapes)
        for i in range(3):
            x, y = w * (0.1 + i*0.4), h * 0.9
            self.canvas.create_arc(x, y-100, x+100, y, start=30, extent=120, fill=LIME_MINT, outline=ACCENT_GREEN, style="chord")

class LoginModule(ctk.CTkFrame):
    def __init__(self, master, on_login_success, db_manager, **kwargs):
        super().__init__(master, fg_color=BG_MAIN, **kwargs)
        self.on_success = on_login_success
        self.db = db_manager
        self.mode = "login" # 'login' or 'register'
        
        self.grid_columnconfigure((0, 2), weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # --- LEFT PANEL: ARTISTIC DECO ---
        self.left_art = AbstractArtPanel(self)
        self.left_art.grid(row=0, column=0, padx=40, pady=100, sticky="nsew")

        # --- CENTRAL CARD: AUTHENTICATION ---
        self.card = ctk.CTkFrame(self, fg_color=PANEL_BG, corner_radius=35, border_width=1, border_color="#E2E8F0")
        self.card.grid(row=0, column=1, pady=80, padx=20, sticky="nsew")
        self.build_auth_ui()

        # --- RIGHT PANEL: ARTISTIC DECO ---
        self.right_art = AbstractArtPanel(self)
        self.right_art.grid(row=0, column=2, padx=40, pady=100, sticky="nsew")

    def build_auth_ui(self):
        for widget in self.card.winfo_children(): widget.destroy()
        
        # Logo
        if os.path.exists(LOGO_IMG):
            logo_pil = Image.open(LOGO_IMG)
            self.logo_img = ctk.CTkImage(logo_pil, size=(140, 140))
            ctk.CTkLabel(self.card, image=self.logo_img, text="").pack(pady=(50, 10))

        title = "INICIAR SESIÓN" if self.mode == "login" else "CREAR CUENTA"
        ctk.CTkLabel(self.card, text=title, font=("Segoe UI", 28, "bold"), text_color=TEXT_P).pack()
        
        # Premium Branding Title
        ctk.CTkLabel(self.card, text="ECOLENTES", font=("Segoe UI", 48, "bold"), text_color=ACCENT_BLUE).pack(pady=(10, 0))
        ctk.CTkLabel(self.card, text="INDUSTRIAL OS PRO", font=("Segoe UI", 12, "bold"), text_color=TEXT_S).pack(pady=(0, 30))

        # Form
        self.u_entry = ctk.CTkEntry(self.card, placeholder_text="Usuario", width=350, height=50, fg_color=BG_MAIN, border_color="#E2E8F0")
        self.u_entry.pack(pady=10)
        
        self.p_entry = ctk.CTkEntry(self.card, placeholder_text="Contraseña", show="*", width=350, height=50, fg_color=BG_MAIN, border_color="#E2E8F0")
        self.p_entry.pack(pady=10)

        self.role_m = ctk.CTkOptionMenu(self.card, values=["Operario", "Ingeniero"], fg_color=ACCENT_BLUE, button_color=ACCENT_BLUE, width=350, height=45)
        self.role_m.pack(pady=20)

        btn_text = "ACCEDER AL TERMINAL" if self.mode == "login" else "REGISTRAR USUARIO"
        btn_color = ACCENT_GREEN if self.mode == "login" else ACCENT_BLUE
        
        self.action_b = ctk.CTkButton(self.card, text=btn_text, font=("Segoe UI", 14, "bold"), fg_color=btn_color, text_color=PANEL_BG, width=350, height=55, command=self.handle_action)
        self.action_b.pack(pady=10)

        # Toggle Link
        toggle_text = "¿No tienes cuenta? Regístrate" if self.mode == "login" else "Ya tengo cuenta, iniciar sesión"
        self.toggle_btn = ctk.CTkButton(self.card, text=toggle_text, font=("Segoe UI", 11), fg_color="transparent", text_color=TEXT_S, hover_color=BG_MAIN, command=self.toggle_mode)
        self.toggle_btn.pack(pady=20)

        self.msg = ctk.CTkLabel(self.card, text="", font=("Segoe UI", 11))
        self.msg.pack()

    def toggle_mode(self):
        self.mode = "register" if self.mode == "login" else "login"
        self.build_auth_ui()

    def handle_action(self):
        user = self.u_entry.get()
        pwd = self.p_entry.get()
        role = self.role_m.get()
        
        if not user or not pwd:
            self.msg.configure(text="Complete todos los campos", text_color=DANGER_P)
            return

        if self.mode == "login":
            auth_role = self.db.authenticate(user, pwd)
            if auth_role:
                self.on_success(user, auth_role)
            else:
                self.msg.configure(text="Credenciales incorrectas", text_color=DANGER_P)
        else:
            success = self.db.register_user(user, pwd, role)
            if success:
                self.msg.configure(text="✓ Registro exitoso! Inicie sesión", text_color=ACCENT_GREEN)
                self.mode = "login"
                self.after(2000, self.build_auth_ui)
            else:
                self.msg.configure(text="El usuario ya existe", text_color=DANGER_P)
