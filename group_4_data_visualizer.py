import tkinter as tk
from typing import Any
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DataVisualizer:
    """
    A class to handle the visualization of plant monitoring data.
    
    This class creates and updates real-time plots showing environmental conditions
    and plant health metrics over time.
    """
    
    def __init__(self, root):
        """Initialize the DataVisualizer with a Tkinter root window."""
        self.root = root
        self.data_history: list[dict[str, Any]] = []
        self.max_history = 100  # Maximum number of data points to keep
        
        # Create figure for plots
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(10, 8))
        self.fig.tight_layout(pad=3.0)
        
        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def update_plots(self, data: dict[str, Any]):
        """
        Update the plots with new data.
        
        Args:
            data (dict): New plant monitoring data to visualize
        """
        # Add new data to history
        self.data_history.append(data)
        if len(self.data_history) > self.max_history:
            self.data_history.pop(0)
            
        # Clear previous plots
        self.ax1.clear()
        self.ax2.clear()
        
        # Prepare data for plotting
        timestamps = [d['timestamp'] for d in self.data_history]
        temps = [d['environmental_conditions']['temperature_c'] for d in self.data_history]
        humidities = [d['environmental_conditions']['humidity_pct'] for d in self.data_history]
        health_scores = [d['health_score'] for d in self.data_history]
        
        # Plot temperature and humidity
        self.ax1.plot(timestamps, temps, 'r-', label='Temperature (°C)')
        self.ax1.plot(timestamps, humidities, 'b-', label='Humidity (%)')
        self.ax1.set_title('Environmental Conditions')
        self.ax1.set_ylabel('Value')
        self.ax1.legend()
        self.ax1.grid(True)
        
        # Plot health score
        self.ax2.plot(timestamps, health_scores, 'g-', label='Health Score')
        self.ax2.set_title('Plant Health Score')
        self.ax2.set_ylabel('Score')
        self.ax2.set_ylim(0, 100)
        self.ax2.legend()
        self.ax2.grid(True)
        
        # Rotate x-axis labels for better readability
        for ax in [self.ax1, self.ax2]:
            ax.tick_params(axis='x', rotation=45)
        
        # Update canvas
        self.canvas.draw()