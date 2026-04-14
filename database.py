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
            
            # Hildegard 2.0 Logs Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS hildegard_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    temp REAL,
                    pressure REAL,
                    notes TEXT
                )
            ''')
            # Hildegard 2.0 Speed Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS hildegard_speed_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    speed REAL,
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

    def log_hildegard(self, temp, pressure, notes=""):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO hildegard_logs (timestamp, temp, pressure, notes) VALUES (?, ?, ?, ?)",
                           (datetime.now().isoformat(), temp, pressure, notes))
            conn.commit()

    def get_hildegard_logs(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM hildegard_logs ORDER BY id DESC")
            return cursor.fetchall()

    def update_hildegard_log(self, entry_id, temp, pressure):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE hildegard_logs SET temp = ?, pressure = ? WHERE id = ?", (temp, pressure, entry_id))
            conn.commit()

    def delete_hildegard_log(self, entry_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM hildegard_logs WHERE id = ?", (entry_id,))
            conn.commit()

    def clear_hildegard_logs(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM hildegard_logs")
            conn.commit()

    # Speed Logs
    def log_hildegard_speed(self, speed):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO hildegard_speed_logs (timestamp, speed) VALUES (?, ?)",
                           (datetime.now().isoformat(), speed))
            conn.commit()

    def get_hildegard_speed_logs(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM hildegard_speed_logs ORDER BY id DESC")
            return cursor.fetchall()

    def update_hildegard_speed(self, entry_id, speed):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE hildegard_speed_logs SET speed = ? WHERE id = ?", (speed, entry_id))
            conn.commit()

    def delete_hildegard_speed(self, entry_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM hildegard_speed_logs WHERE id = ?", (entry_id,))
            conn.commit()

    def clear_hildegard_speed_logs(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM hildegard_speed_logs")
            conn.commit()

    def get_full_history(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM production_cycles ORDER BY id DESC")
            return cursor.fetchall()
            
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
