import paho.mqtt.client as mqtt
import time
import json
import random
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from typing import Any

class DataGenerator:
    def __init__(self):
        self.start_id = 111
        self.researchers = ["Dr. Smith", "Dr. Garcia", "Dr. Lee", "Dr. Patel"]
        self.plant_types = ["Tomato", "Cucumber", "Basil", "Lettuce"]
        self.growth_stages = ["Seedling", "Vegetative", "Flowering", "Fruiting"]
        
    def create_data(self, base_temp: float = 23.0, base_humidity: float = 65.0) -> dict[str, Any]:
        """Generate plant monitoring data with configurable base values"""
        data = {
            'id': self.start_id,
            'researcher': random.choice(self.researchers),
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'plant_metrics': {
                'height_cm': round(random.gauss(45, 8), 1),
                'leaf_count': round(random.gauss(24, 6)),
                'stem_diameter_mm': round(random.gauss(8.5, 1.2), 2)
            },
            'environmental_conditions': {
                'temperature_c': round(random.gauss(base_temp, 2), 1),
                'humidity_pct': round(random.gauss(base_humidity, 10)),
                'light_intensity_lux': round(random.gauss(15000, 3000))
            },
            'soil_data': {
                'moisture_pct': round(random.gauss(70, 8)),
                'ph_level': round(random.gauss(6.5, 0.4), 1),
                'nutrient_index': round(random.gauss(450, 80))
            },
            'plant_type': random.choice(self.plant_types),
            'growth_stage': random.choice(self.growth_stages),
            'health_score': round(random.gauss(85, 12))
        }
        self.start_id += 1
        return data

class PublisherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Plant Monitoring Publisher")
        
        # MQTT settings
        self.url = 'localhost'
        self.port = 1883
        self.topic = "group_4/plant_monitoring"
        
        # Create MQTT client
        self.client = mqtt.Client(client_id='publisher_gui', callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
        
        # Data generator
        self.data_generator = DataGenerator()
        
        # GUI variables
        self.publishing = False
        self.base_temp = tk.DoubleVar(value=23.0)
        self.base_humidity = tk.DoubleVar(value=65.0)
        self.publish_interval = tk.DoubleVar(value=3.0)
        self.missed_transmissions = tk.BooleanVar(value=True)
        self.wild_data = tk.BooleanVar(value=False)
        
        self.setup_gui()
        
    def setup_gui(self):
        # Control frame
        control_frame = ttk.LabelFrame(self.root, text="Controls", padding="10")
        control_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Parameters frame
        param_frame = ttk.LabelFrame(self.root, text="Parameters", padding="10")
        param_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        # Status frame
        status_frame = ttk.LabelFrame(self.root, text="Status", padding="10")
        status_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        
        # Controls
        ttk.Button(control_frame, text="Start Publishing", command=self.start_publishing).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(control_frame, text="Stop Publishing", command=self.stop_publishing).grid(row=0, column=1, padx=5, pady=5)
        
        # Parameters
        ttk.Label(param_frame, text="Base Temperature (°C):").grid(row=0, column=0, padx=5, pady=5)
        ttk.Scale(param_frame, from_=15, to=30, variable=self.base_temp, orient="horizontal").grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(param_frame, text="Base Humidity (%):").grid(row=1, column=0, padx=5, pady=5)
        ttk.Scale(param_frame, from_=30, to=90, variable=self.base_humidity, orient="horizontal").grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(param_frame, text="Publish Interval (s):").grid(row=2, column=0, padx=5, pady=5)
        ttk.Scale(param_frame, from_=1, to=10, variable=self.publish_interval, orient="horizontal").grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Checkbutton(param_frame, text="Enable Missed Transmissions", variable=self.missed_transmissions).grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        ttk.Checkbutton(param_frame, text="Enable Wild Data", variable=self.wild_data).grid(row=4, column=0, columnspan=2, padx=5, pady=5)
        
        # Status
        self.status_text = tk.Text(status_frame, height=10, width=50)
        self.status_text.grid(row=0, column=0, padx=5, pady=5)
        
    def log_status(self, message):
        self.status_text.insert(tk.END, f"{datetime.now().strftime('%H:%M:%S')} - {message}\n")
        self.status_text.see(tk.END)
        
    def start_publishing(self):
        if not self.publishing:
            self.publishing = True
            self.client.connect(self.url, self.port)
            self.log_status(f"Connected to {self.url}:{self.port}")
            self.publish_loop()
            
    def stop_publishing(self):
        if self.publishing:
            self.publishing = False
            self.client.disconnect()
            self.log_status("Disconnected from broker")
            
    def publish_loop(self):
        if not self.publishing:
            return
            
        try:
            # Generate data
            data = self.data_generator.create_data(
                base_temp=self.base_temp.get(),
                base_humidity=self.base_humidity.get()
            )
            
            # Simulate missed transmissions (1 in 100)
            if self.missed_transmissions.get() and random.random() < 0.01:
                self.log_status(f"Simulated missed transmission (ID: {data['id']})")
            else:
                # Simulate wild data (1 in 200)
                if self.wild_data.get() and random.random() < 0.005:
                    data['environmental_conditions']['temperature_c'] = random.uniform(-10, 50)
                    data['environmental_conditions']['humidity_pct'] = random.uniform(0, 200)
                    self.log_status(f"Published WILD data (ID: {data['id']})")
                
                # Publish the data
                payload = json.dumps(data)
                self.client.publish(self.topic, payload)
                self.log_status(f"Published (ID: {data['id']}): {data['plant_type']} - {data['growth_stage']} - Health: {data['health_score']}/100")
            
        except Exception as e:
            self.log_status(f"Error: {e}")
            
        # Schedule next transmission
        self.root.after(int(self.publish_interval.get() * 1000), self.publish_loop)

def main():
    root = tk.Tk()
    app = PublisherGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 