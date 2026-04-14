import tkinter as tk
import customtkinter as ctk
from app_config import *
import math
import time
from tkinter import messagebox

class SpaghettiModule(ctk.CTkFrame):
    def __init__(self, master, db_manager, user_id, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.db = db_manager
        self.user_id = user_id
        
        self.nodes = [] 
        self.edges = [] 
        self.paths = [] 
        self.selected_node = None
        self.linking_mode = False
        self.drawing_mode = False
        self.current_path = []
        self.temp_line = None
        self.undo_stack = []
        self.redo_stack = []
        
        # --- UI LAYOUT (GRID for Absolute Stability) ---
        self.grid_columnconfigure(0, weight=1) # Canvas
        self.grid_columnconfigure(1, weight=0) # Sidebar
        self.grid_rowconfigure(0, weight=1)
        
        # 1. Main Canvas Area
        self.c_frame = ctk.CTkFrame(self, fg_color=PANEL_BG, corner_radius=25, border_width=1, border_color="#E2E8F0")
        self.c_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.canvas_container = ctk.CTkFrame(self.c_frame, fg_color="transparent")
        self.canvas_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Using CTKScrollbar for better theme integration
        self.h_scroll = ctk.CTkScrollbar(self.canvas_container, orientation="horizontal")
        self.h_scroll.pack(side="bottom", fill="x")
        self.v_scroll = ctk.CTkScrollbar(self.canvas_container, orientation="vertical")
        self.v_scroll.pack(side="right", fill="y")
        
        self.canvas = tk.Canvas(self.canvas_container, bg="#F8FAFC", highlightthickness=0, # Light gray bg to see it
                               scrollregion=(0,0,5000,3500),
                               xscrollcommand=self.h_scroll.set,
                               yscrollcommand=self.v_scroll.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        
        self.h_scroll.configure(command=self.canvas.xview)
        self.v_scroll.configure(command=self.canvas.yview)

        # 2. Control Panel (Sidebar)
        self.ctrl = ctk.CTkFrame(self, fg_color=PANEL_BG, corner_radius=25, border_width=1, border_color="#E2E8F0", width=280)
        self.ctrl.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.ctrl.pack_propagate(False) # Keep fixed width
        
        ctk.CTkLabel(self.ctrl, text="DIAGRAMA DE FLUJO", font=("Segoe UI", 16, "bold"), text_color=TEXT_P).pack(pady=(20, 10))
        ctk.CTkLabel(self.ctrl, text="— Industrial v4.8 —", font=("Segoe UI", 9), text_color=ACCENT_BLUE).pack(pady=(0, 20))
        
        self.name_ent = ctk.CTkEntry(self.ctrl, placeholder_text="Nombre Estación", width=200)
        self.name_ent.pack(pady=10)
        
        self.shape_var = ctk.StringVar(value="Cuadrado")
        self.shape_m = ctk.CTkOptionMenu(self.ctrl, values=["Cuadrado", "Círculo", "Hexágono", "Diamante"], variable=self.shape_var, width=200)
        self.shape_m.pack(pady=10)
        
        self.col_var = ctk.StringVar(value="Verde")
        self.col_m = ctk.CTkOptionMenu(self.ctrl, values=["Verde", "Azul", "Naranja", "Gris", "Rojo"], variable=self.col_var, width=200)
        self.col_m.pack(pady=10)
        
        ctk.CTkButton(self.ctrl, text="+ AÑADIR NODO", fg_color=ACCENT_GREEN, text_color=BG_MAIN, font=("Segoe UI", 11, "bold"), height=40, command=self.add_new_node).pack(pady=20)
        
        self.btn_link = ctk.CTkButton(self.ctrl, text="🔗 CONECTAR", fg_color=ACCENT_STEEL, height=35, command=self.toggle_link_mode)
        self.btn_link.pack(pady=5)
        
        self.btn_draw = ctk.CTkButton(self.ctrl, text="✏️ DIBUJO LIBRE", fg_color=ACCENT_STEEL, height=35, command=self.toggle_draw_mode)
        self.btn_draw.pack(pady=5)
        
        ctk.CTkButton(self.ctrl, text="💾 GUARDAR", fg_color=ACCENT_BLUE, height=45, command=self.save_to_db).pack(pady=20)
        
        self.btn_undo = ctk.CTkButton(self.ctrl, text="↩", width=90, fg_color="#475569", command=self.undo)
        self.btn_undo.pack(side="left", padx=(40, 5), pady=10)
        
        self.btn_redo = ctk.CTkButton(self.ctrl, text="↪", width=90, fg_color="#475569", command=self.redo)
        self.btn_redo.pack(side="left", padx=5, pady=10)
        
        # Mouse Events
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.canvas.bind("<Motion>", self.on_mouse_move)

        self.draw_grid()
        self.load_from_db()

    def draw_grid(self):
        self.canvas.delete("grid")
        for i in range(0, 5000, 100):
            self.canvas.create_line(i, 0, i, 3500, fill="#E2E8F0", width=1, tags="grid")
            self.canvas.create_line(0, i, 5000, i, fill="#E2E8F0", width=1, tags="grid")
        self.canvas.tag_lower("grid")

    def add_new_node(self):
        name = self.name_ent.get() or f"EST-{len(self.nodes)+1}"
        tag = f"n_{len(self.nodes)}_{int(time.time()%1000)}"
        self.save_state()
        self.create_node_gfx(tag, 200, 200, name, self.shape_var.get(), self.col_var.get())
        self.nodes.append({'id': tag, 'name': name, 'x': 200, 'y': 200, 'shape': self.shape_var.get(), 'color': self.col_var.get()})
        self.name_ent.delete(0, 'end')

    def create_node_gfx(self, tag, x, y, name, shape, col_name):
        cols = {"Verde": ACCENT_GREEN, "Azul": ACCENT_BLUE, "Naranja": "#F59E0B", "Gris": ACCENT_STEEL, "Rojo": DANGER_P}
        color = cols.get(col_name, ACCENT_GREEN)
        
        if shape == "Círculo":
            self.canvas.create_oval(x-40, y-40, x+40, y+40, fill=PANEL_BG, outline=color, width=2, tags=(tag, "obj"))
        else:
            self.canvas.create_rectangle(x-40, y-40, x+40, y+40, fill=PANEL_BG, outline=color, width=2, tags=(tag, "obj"))
            
        self.canvas.create_text(x, y, text=name[:8], fill=color, font=("Segoe UI", 10, "bold"), tags=(tag, "obj", "txt"))
        self.canvas.create_text(x, y+55, text=name, fill=TEXT_P, font=("Segoe UI", 9, "bold"), tags=(tag, "obj", "lbl"))
        
        self.canvas.tag_bind(tag, "<Button-1>", lambda e, t=tag: self.on_click(e, t))
        self.canvas.tag_bind(tag, "<B1-Motion>", lambda e, t=tag: self.on_drag(e, t))

    def on_canvas_click(self, event):
        cx, cy = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        if self.drawing_mode:
            target = self.find_near(cx, cy)
            sx, sy = (target['x'], target['y']) if target else (cx, cy)
            self.current_path = [sx, sy]
            col = {"Verde": ACCENT_GREEN, "Azul": ACCENT_BLUE, "Naranja": "#F59E0B", "Gris": ACCENT_STEEL, "Rojo": DANGER_P}.get(self.col_var.get(), ACCENT_BLUE)
            self.temp_line = self.canvas.create_line(sx, sy, sx, sy, fill=col, width=3, smooth=True, tags=("path", "current"))
        else:
            self.selected_node = None

    def on_canvas_drag(self, event):
        if self.drawing_mode and self.temp_line:
            cx, cy = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
            self.current_path.extend([cx, cy])
            self.canvas.coords(self.temp_line, *self.current_path)

    def on_canvas_release(self, event):
        if self.drawing_mode and self.temp_line:
            self.save_state()
            cx, cy = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
            target = self.find_near(cx, cy)
            if target:
                self.current_path[-2:] = [target['x'], target['y']]
                self.canvas.coords(self.temp_line, *self.current_path)
            
            p_data = {'coords': list(self.current_path), 'color': self.canvas.itemcget(self.temp_line, "fill"), 'id': self.temp_line}
            self.paths.append(p_data)
            self.temp_line = None
            self.current_path = []

    def on_click(self, event, tag):
        if self.linking_mode:
            if not self.selected_node:
                self.selected_node = tag
            elif self.selected_node != tag:
                self.create_edge(self.selected_node, tag)
                self.selected_node = None
                self.toggle_link_mode()
        else:
            self.selected_node = tag
            self._sx, self._sy = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)

    def on_drag(self, event, tag):
        if self.linking_mode: return
        cx, cy = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        dx, dy = cx - self._sx, cy - self._sy
        self.canvas.move(tag, dx, dy)
        self._sx, self._sy = cx, cy
        for n in self.nodes:
            if n['id'] == tag:
                n['x'] += dx; n['y'] += dy; break
        self.update_edges()

    def create_edge(self, t1, t2):
        self.save_state()
        n1 = next(n for n in self.nodes if n['id'] == t1)
        n2 = next(n for n in self.nodes if n['id'] == t2)
        lid = self.canvas.create_line(n1['x'], n1['y'], n2['x'], n2['y'], fill=ACCENT_STEEL, width=2, arrow=tk.LAST, tags="edge")
        self.canvas.tag_lower(lid)
        self.edges.append({'from': t1, 'to': t2, 'line': lid})

    def update_edges(self):
        for e in self.edges:
            n1 = next(n for n in self.nodes if n['id'] == e['from'])
            n2 = next(n for n in self.nodes if n['id'] == e['to'])
            self.canvas.coords(e['line'], n1['x'], n1['y'], n2['x'], n2['y'])

    def find_near(self, x, y):
        for n in self.nodes:
            if math.sqrt((x-n['x'])**2 + (y-n['y'])**2) < 50: return n
        return None

    def save_state(self):
        self.undo_stack.append({'nodes': [n.copy() for n in self.nodes], 'edges': [e.copy() for e in self.edges], 'paths': [p.copy() for p in self.paths]})
        self.redo_stack = []

    def undo(self):
        if self.undo_stack:
            self.redo_stack.append({'nodes': [n.copy() for n in self.nodes], 'edges': [e.copy() for e in self.edges], 'paths': [p.copy() for p in self.paths]})
            self.restore(self.undo_stack.pop())

    def redo(self):
        if self.redo_stack:
            self.undo_stack.append({'nodes': [n.copy() for n in self.nodes], 'edges': [e.copy() for e in self.edges], 'paths': [p.copy() for p in self.paths]})
            self.restore(self.redo_stack.pop())

    def restore(self, state):
        self.canvas.delete("obj", "txt", "lbl", "path", "edge")
        self.nodes, self.edges, self.paths = [], [], []
        for n in state['nodes']:
            self.create_node_gfx(n['id'], n['x'], n['y'], n['name'], n['shape'], n['color'])
            self.nodes.append(n)
        for e in state['edges']:
            self.create_edge(e['from'], e['to'])
        for p in state['paths']:
            lid = self.canvas.create_line(*p['coords'], fill=p['color'], width=3, smooth=True, tags="path")
            p['id'] = lid; self.paths.append(p)

    def load_from_db(self):
        nodes, edges, paths = self.db.load_spaghetti(self.user_id)
        for n in nodes:
            tag = f"n_{len(self.nodes)}_{int(time.time()%1000)}"
            self.create_node_gfx(tag, n[1], n[2], n[0], n[3], n[4])
            self.nodes.append({'id': tag, 'name': n[0], 'x': n[1], 'y': n[2], 'shape': n[3], 'color': n[4]})
        for f, t in edges:
            if f < len(self.nodes) and t < len(self.nodes):
                self.create_edge(self.nodes[f]['id'], self.nodes[t]['id'])
        for p_str, col in paths:
            coords = list(map(float, p_str.split(",")))
            lid = self.canvas.create_line(*coords, fill=col, width=3, smooth=True, tags="path")
            self.paths.append({'coords': coords, 'color': col, 'id': lid})

    def save_to_db(self):
        node_map = {n['id']: i for i, n in enumerate(self.nodes)}
        db_edges = [{'from': node_map[e['from']], 'to': node_map[e['to']]} for e in self.edges]
        self.db.save_spaghetti(self.user_id, self.nodes, db_edges, self.paths)

    def toggle_link_mode(self):
        self.linking_mode = not self.linking_mode
        self.drawing_mode = False
        self.btn_link.configure(fg_color=ACCENT_BLUE if self.linking_mode else ACCENT_STEEL)
        self.btn_draw.configure(fg_color=ACCENT_STEEL)

    def toggle_draw_mode(self):
        self.drawing_mode = not self.drawing_mode
        self.linking_mode = False
        self.btn_draw.configure(fg_color=ACCENT_BLUE if self.drawing_mode else ACCENT_STEEL)
        self.btn_link.configure(fg_color=ACCENT_STEEL)

    def on_mouse_move(self, event):
        if self.linking_mode and self.selected_node:
            cx, cy = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
            n = next(node for node in self.nodes if node['id'] == self.selected_node)
            if self.temp_line: self.canvas.coords(self.temp_line, n['x'], n['y'], cx, cy)
            else: self.temp_line = self.canvas.create_line(n['x'], n['y'], cx, cy, fill=ACCENT_BLUE, dash=(5,5))
