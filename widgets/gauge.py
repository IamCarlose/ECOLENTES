import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class MatplotlibGauge:
    def __init__(self, master, bg_color="#1E293B"):
        self.master = master
        self.bg_color = bg_color
        
        # Transparent figure
        self.fig, self.ax = plt.subplots(figsize=(4, 2), subplot_kw={'projection': 'polar'})
        self.fig.patch.set_alpha(0)
        self.ax.set_facecolor("none")
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self.canvas.get_tk_widget().configure(bg=bg_color, highlightthickness=0)
        
        self.draw_gauge(0)

    def draw_gauge(self, value):
        self.ax.clear()
        self.ax.set_theta_zero_location("W")
        self.ax.set_theta_direction(-1)
        self.ax.set_thetamax(180)
        
        # Color bar
        # Create a gradient effect
        colors = plt.cm.RdYlGn(np.linspace(0, 1, 100))
        for i in range(100):
            interval = np.pi / 100
            self.ax.barh(0, interval, left=i*interval, height=0.4, color=colors[i], align='edge', alpha=0.3)
            
        # Needle (Solid value bar)
        val_color = "#10B981" if value > 75 else "#F59E0B" if value > 50 else "#EF4444"
        self.ax.barh(0.1, (value/100)*np.pi, left=0, height=0.3, color=val_color, align='edge')
        
        # Needle pointer
        angle = (value/100)*np.pi
        self.ax.annotate('', xy=(angle, 0.4), xytext=(angle, 0),
                     arrowprops=dict(arrowstyle='-|>,head_width=0.5,head_length=1', color='white', lw=2))
        
        self.ax.set_axis_off()
        self.ax.text(np.pi/2, -0.4, f"{value}%", ha='center', va='center', 
                     fontsize=24, color='white', fontweight='bold', fontfamily='Arial')
        self.canvas.draw()

    def update_value(self, value):
        self.draw_gauge(value)
