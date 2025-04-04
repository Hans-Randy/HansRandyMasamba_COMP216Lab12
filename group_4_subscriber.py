import paho.mqtt.client as mqtt
import json
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from group_4_data_visualizer import DataVisualizer
class SubscriberGUI:
    """
    A class to handle the MQTT subscriber GUI.
    
    This class creates a GUI interface for subscribing to plant monitoring data,
    displaying status information, and managing the MQTT connection.
    """
    
    def __init__(self, root):
        """Initialize the SubscriberGUI with a Tkinter root window."""
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
        """Connect to the MQTT broker and subscribe to the topic."""
        try:
            self.client.connect(self.url, self.port)
            self.client.subscribe(self.topic)
            self.client.loop_start()
            self.log_status(f"Connected to {self.url}:{self.port}")
            self.log_status(f"Subscribed to topic: {self.topic}")
        except Exception as e:
            self.log_status(f"Connection error: {e}")
            
    def on_message(self, client, userdata, msg):
        """
        Handle incoming MQTT messages.
        """
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
        """
        Log a status message to the status text widget.
        
        Args:
            message (str): Message to log
        """
        self.status_text.insert(tk.END, f"{datetime.now().strftime('%H:%M:%S')} - {message}\n")
        self.status_text.see(tk.END)
        
    def on_closing(self):
        """Handle window closing event by stopping MQTT client and destroying window."""
        self.client.loop_stop()
        self.client.disconnect()
        self.root.destroy()

def main():
    """Main function to create and run the subscriber GUI."""
    root = tk.Tk()
    app = SubscriberGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main() 