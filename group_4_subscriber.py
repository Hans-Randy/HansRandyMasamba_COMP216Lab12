import paho.mqtt.client as mqtt
import json
import tkinter as tk
from tkinter import ttk
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from typing import Dict, Any, List

class DataVisualizer:
    def __init__(self, root):
        self.root = root
        self.data_history: List[Dict[str, Any]] = []
        self.max_history = 100  # Maximum number of data points to keep
        
        # Create figure for plots
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(10, 8))
        self.fig.tight_layout(pad=3.0)
        
        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def update_plots(self, data: Dict[str, Any]):
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

class SubscriberGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Plant Monitoring Subscriber")
        
        # MQTT settings
        self.url = 'localhost'
        self.port = 1883
        self.topic = "group_4/plant_monitoring"
        
        # Create MQTT client
        self.client = mqtt.Client(client_id='subscriber_gui', callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_message = self.on_message
        
        # Create visualizer
        self.visualizer = DataVisualizer(root)
        
        # Create status frame
        self.status_frame = ttk.LabelFrame(root, text="Status", padding="10")
        self.status_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Status text
        self.status_text = tk.Text(self.status_frame, height=10, width=50)
        self.status_text.pack(padx=5, pady=5)
        
        # Connect to broker
        self.connect_to_broker()
        
    def connect_to_broker(self):
        try:
            self.client.connect(self.url, self.port)
            self.client.subscribe(self.topic)
            self.client.loop_start()
            self.log_status(f"Connected to {self.url}:{self.port}")
            self.log_status(f"Subscribed to topic: {self.topic}")
        except Exception as e:
            self.log_status(f"Connection error: {e}")
            
    def on_message(self, client, userdata, msg):
        try:
            # Decode message
            payload = msg.payload.decode()
            data = json.loads(payload)
            
            # Log received data
            self.log_status(f"Received (ID: {data['id']}): {data['plant_type']} - {data['growth_stage']} - Health: {data['health_score']}/100")
            
            # Update visualizations
            self.visualizer.update_plots(data)
            
        except Exception as e:
            self.log_status(f"Error processing message: {e}")
            
    def log_status(self, message):
        self.status_text.insert(tk.END, f"{datetime.now().strftime('%H:%M:%S')} - {message}\n")
        self.status_text.see(tk.END)
        
    def on_closing(self):
        self.client.loop_stop()
        self.client.disconnect()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = SubscriberGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main() 