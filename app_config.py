import customtkinter as ctk
import os

# --- LIGHT INDUSTRIAL PALETTE ---
BG_MAIN = "#F1F5F9"      # Light Slate Gray
PANEL_BG = "#FFFFFF"     # Pure White Card
ACCENT_GREEN = "#10B981" # Emerald Flow
ACCENT_BLUE = "#3B82F6"  # Cobalt Professional
ACCENT_STEEL = "#475569" # Steel Blue Gray
TEXT_P = "#0F172A"       # Deep Slate Blue-Black
TEXT_S = "#334155"       # Darker Slate for better visibility (was #64748B)
DANGER_P = "#EF4444"     # Alert Red
LIME_MINT = "#D1FAE5"    # Mint Highlight
ACCENT_GOLD = "#F59E0B"  # Industrial Gold (Warning)

# --- ASSETS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_IMG = os.path.join(BASE_DIR, "logo_clean.png")

# --- BUSINESS LOGIC ---
STANDARD_TIME = 15.0
ANDON_THRESHOLD = 1.25 # 25% extra for bold alerts

def setup_branding_theme():
    ctk.set_appearance_mode("Light")
    ctk.set_default_color_theme("blue") # Standard CTK blue for widgets
