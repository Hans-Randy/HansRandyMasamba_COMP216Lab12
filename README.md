# Plant Monitoring IoT System

This project implements an IoT system for monitoring plant growth conditions using MQTT protocol. It consists of a publisher that generates and sends plant monitoring data, and a subscriber that receives and visualizes the data.

## Prerequisites

- Python 3.6.5 or later
- Eclipse Mosquitto MQTT broker
- Required Python packages (install using `pip install -r requirements.txt`)

## Setup

1. Install the Eclipse Mosquitto MQTT broker:

   - Windows: Download and install from https://mosquitto.org/download/
   - Linux: `sudo apt-get install mosquitto`
   - macOS: `brew install mosquitto`

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the System

1. Start the Mosquitto broker:

   - Windows: The broker should start automatically as a service
   - Linux/macOS: `mosquitto`

2. Run the publisher:

   ```bash
   python group_4_publisher.py
   ```

3. Run the subscriber:
   ```bash
   python group_4_subscriber.py
   ```

## Features

### Publisher

- Generates random plant monitoring data
- Configurable parameters:
  - Base temperature
  - Base humidity
  - Publish interval
- Simulates real-world conditions:
  - Missed transmissions (1 in 100)
  - Wild data values (1 in 200)

### Subscriber

- Real-time data visualization:
  - Temperature and humidity trends
  - Plant health score
- Text-based status updates
- Automatic reconnection to broker

## Project Structure

- `group_4_publisher.py`: Publisher application with GUI
- `group_4_subscriber.py`: Subscriber application with visualization
- `requirements.txt`: Python dependencies
- `README.md`: This file

## Notes

- The system uses the MQTT topic "group_4/plant_monitoring"
- Default broker settings: localhost:1883
- Data is transmitted in JSON format
