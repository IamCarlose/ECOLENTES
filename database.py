import sqlite3
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_name="ecolentes.db"):
        self.db_path = os.path.join(os.getcwd(), db_name)
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Spaghetti Paths Table (Freehand)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS spaghetti_paths (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    coords TEXT,
                    color TEXT
                )
            ''')
            # Users Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT,
                    role TEXT
                )
            ''')
            # Production Cycles Table (Enhanced)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS production_cycles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    duration REAL,
                    operator TEXT,
                    status TEXT,
                    material_kg REAL DEFAULT 0,
                    ambient_temp REAL DEFAULT 0,
                    reject_count INTEGER DEFAULT 0
                )
            ''')
            
            # Safe Migration for existing databases
            try:
                cursor.execute("ALTER TABLE production_cycles ADD COLUMN material_kg REAL DEFAULT 0")
            except sqlite3.OperationalError: pass
            try:
                cursor.execute("ALTER TABLE production_cycles ADD COLUMN ambient_temp REAL DEFAULT 0")
            except sqlite3.OperationalError: pass
            try:
                cursor.execute("ALTER TABLE production_cycles ADD COLUMN reject_count INTEGER DEFAULT 0")
            except sqlite3.OperationalError: pass
            # SMED Tasks Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS smed_tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_name TEXT,
                    task_type TEXT,
                    duration REAL,
                    improvement_notes TEXT
                )
            ''')
            # DOE Results Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS doe_experiments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    factor_a REAL,
                    factor_b REAL,
                    result REAL,
                    timestamp TEXT
                )
            ''')
            
            # Spaghetti Diagram Storage
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS spaghetti_nodes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    name TEXT,
                    x REAL,
                    y REAL,
                    shape TEXT,
                    color TEXT
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS spaghetti_edges (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    node_from_id INTEGER,
                    node_to_id INTEGER
                )
            ''')
            
            
            # Hildegard Modular Tables
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS hildegard_temp_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    temp REAL,
                    notes TEXT
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS hildegard_pressure_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    pressure REAL,
                    notes TEXT
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS hildegard_rpm_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    rpm REAL,
                    notes TEXT
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS hildegard_diameter_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    diameter REAL,
                    length_m REAL,
                    notes TEXT
                )
            ''')
            
            # Default Admin
            cursor.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)", 
                           ("admin", "admin123", "Ingeniero"))
            conn.commit()

    def log_cycle(self, duration, operator, status, material=0, temp=0, rejects=0):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO production_cycles 
                (timestamp, duration, operator, status, material_kg, ambient_temp, reject_count) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (datetime.now().isoformat(), duration, operator, status, material, temp, rejects))
            conn.commit()

    # --- HILDEGARD MODULAR LOGS ---
    def log_temp(self, temp, notes=""):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO hildegard_temp_logs (timestamp, temp, notes) VALUES (?, ?, ?)",
                           (datetime.now().isoformat(), temp, notes))
            conn.commit()

    def get_temp_logs(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM hildegard_temp_logs ORDER BY id DESC")
            return cursor.fetchall()

    def update_temp_log(self, entry_id, temp):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE hildegard_temp_logs SET temp = ? WHERE id = ?", (temp, entry_id))
            conn.commit()

    def delete_temp_log(self, entry_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM hildegard_temp_logs WHERE id = ?", (entry_id,))
            conn.commit()

    def log_pressure(self, pressure, notes=""):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO hildegard_pressure_logs (timestamp, pressure, notes) VALUES (?, ?, ?)",
                           (datetime.now().isoformat(), pressure, notes))
            conn.commit()

    def get_pressure_logs(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM hildegard_pressure_logs ORDER BY id DESC")
            return cursor.fetchall()

    def update_pressure_log(self, entry_id, pressure):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE hildegard_pressure_logs SET pressure = ? WHERE id = ?", (pressure, entry_id))
            conn.commit()

    def delete_pressure_log(self, entry_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM hildegard_pressure_logs WHERE id = ?", (entry_id,))
            conn.commit()

    def log_rpm(self, rpm, notes=""):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO hildegard_rpm_logs (timestamp, rpm, notes) VALUES (?, ?, ?)",
                           (datetime.now().isoformat(), rpm, notes))
            conn.commit()

    def get_rpm_logs(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM hildegard_rpm_logs ORDER BY id DESC")
            return cursor.fetchall()

    def update_rpm_log(self, entry_id, rpm):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE hildegard_rpm_logs SET rpm = ? WHERE id = ?", (rpm, entry_id))
            conn.commit()

    def delete_rpm_log(self, entry_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM hildegard_rpm_logs WHERE id = ?", (entry_id,))
            conn.commit()

    def log_diameter(self, diameter, length_m, notes=""):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO hildegard_diameter_logs (timestamp, diameter, length_m, notes) VALUES (?, ?, ?, ?)",
                           (datetime.now().isoformat(), diameter, length_m, notes))
            conn.commit()

    def get_diameter_logs(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM hildegard_diameter_logs ORDER BY id DESC")
            return cursor.fetchall()

    def update_diameter_log(self, entry_id, diameter, length_m):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE hildegard_diameter_logs SET diameter = ?, length_m = ? WHERE id = ?", (diameter, length_m, entry_id))
            conn.commit()

    def delete_diameter_log(self, entry_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM hildegard_diameter_logs WHERE id = ?", (entry_id,))
            conn.commit()

    def clear_modular_logs(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM hildegard_temp_logs")
            cursor.execute("DELETE FROM hildegard_pressure_logs")
            cursor.execute("DELETE FROM hildegard_rpm_logs")
            cursor.execute("DELETE FROM hildegard_diameter_logs")
            conn.commit()

    def get_full_history(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM production_cycles ORDER BY id DESC")
            return cursor.fetchall()
            
    def update_latest_cycle_defects(self, defects):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE production_cycles SET reject_count = ? WHERE id = (SELECT MAX(id) FROM production_cycles)", (defects,))
            conn.commit()

    def update_cycle(self, cid, operator, duration, defects):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE production_cycles SET operator = ?, duration = ?, reject_count = ? WHERE id = ?", (operator, duration, defects, cid))
            conn.commit()

    def delete_cycle(self, cid):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM production_cycles WHERE id = ?", (cid,))
            conn.commit()

    def clear_all_cycles(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM production_cycles")
            conn.commit()

            
    def get_doe_data(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM doe_experiments ORDER BY id DESC")
            return cursor.fetchall()

    def get_smed_data(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM smed_tasks")
            return cursor.fetchall()

    def get_last_cycles(self, limit=10):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT duration FROM production_cycles ORDER BY id DESC LIMIT ?", (limit,))
            return [row[0] for row in cursor.fetchall()]

    def authenticate(self, username, password):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT role FROM users WHERE username = ? AND password = ?", (username, password))
            result = cursor.fetchone()
            return result[0] if result else None

    def register_user(self, username, password, role):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                               (username, password, role))
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False # Username already exists

    def get_user_id(self, username):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            res = cursor.fetchone()
            return res[0] if res else None

    # Diagram Methods
    def save_spaghetti(self, user_id, nodes, edges, paths=[]):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM spaghetti_nodes WHERE user_id = ?", (user_id,))
            cursor.execute("DELETE FROM spaghetti_edges WHERE user_id = ?", (user_id,))
            cursor.execute("DELETE FROM spaghetti_paths WHERE user_id = ?", (user_id,))
            for n in nodes:
                cursor.execute("INSERT INTO spaghetti_nodes (user_id, name, x, y, shape, color) VALUES (?,?,?,?,?,?)",
                               (user_id, n['name'], n['x'], n['y'], n['shape'], n['color']))
            for e in edges:
                cursor.execute("INSERT INTO spaghetti_edges (user_id, node_from_id, node_to_id) VALUES (?,?,?)",
                               (user_id, e['from'], e['to']))
            for p in paths:
                cursor.execute("INSERT INTO spaghetti_paths (user_id, coords, color) VALUES (?,?,?)",
                               (user_id, ",".join(map(str, p['coords'])), p['color']))
            conn.commit()

    def load_spaghetti(self, user_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name, x, y, shape, color FROM spaghetti_nodes WHERE user_id = ?", (user_id,))
            nodes = cursor.fetchall()
            cursor.execute("SELECT node_from_id, node_to_id FROM spaghetti_edges WHERE user_id = ?", (user_id,))
            edges = cursor.fetchall()
            cursor.execute("SELECT coords, color FROM spaghetti_paths WHERE user_id = ?", (user_id,))
            paths = cursor.fetchall()
            return nodes, edges, paths
