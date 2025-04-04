import paho.mqtt.client as mqtt
import json
import random
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from group_4_data_generator import DataGenerator

class PublisherGUI:
    """
    A class to handle the MQTT publisher GUI.
    
    This class creates a GUI interface for publishing plant monitoring data,
    allowing configuration of data generation parameters and publishing settings.
    """
    
    def __init__(self, root):
        """Initialize the PublisherGUI with a Tkinter root window."""
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
        """Set up the GUI components and layout."""
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
        """
        Log a status message to the status text widget.
        
        Args:
            message (str): Message to log
        """
        self.status_text.insert(tk.END, f"{datetime.now().strftime('%H:%M:%S')} - {message}\n")
        self.status_text.see(tk.END)
        
    def start_publishing(self):
        """Start publishing data to the MQTT broker."""
        if not self.publishing:
            self.publishing = True
            self.client.connect(self.url, self.port)
            self.log_status(f"Connected to {self.url}:{self.port}")
            self.publish_loop()
            
    def stop_publishing(self):
        """Stop publishing data and disconnect from the MQTT broker."""
        if self.publishing:
            self.publishing = False
            self.client.disconnect()
            self.log_status("Disconnected from broker")
            
    def publish_loop(self):
        """
        Main publishing loop that generates and publishes data.
        
        This method:
        1. Generates new data using the DataGenerator
        2. Optionally simulates missed transmissions
        3. Optionally simulates wild data values
        4. Publishes the data to the MQTT broker
        5. Schedules the next publication
        """
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
    """Main function to create and run the publisher GUI."""
    root = tk.Tk()
    app = PublisherGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 