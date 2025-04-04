import random
from datetime import datetime
from typing import Any

class DataGenerator:
    """
    A class to generate simulated plant monitoring data.
    
    This class creates realistic plant monitoring data including metrics like height,
    leaf count, environmental conditions, and soil data. The data can be customized
    with base temperature and humidity values.
    """
    
    def __init__(self):
        """Initialize the DataGenerator with default values and lists."""
        self.start_id = 111  # Starting ID for generated records
        self.researchers = ["Dr. Smith", "Dr. Garcia", "Dr. Lee", "Dr. Patel"]
        self.plant_types = ["Tomato", "Cucumber", "Basil", "Lettuce"]
        self.growth_stages = ["Seedling", "Vegetative", "Flowering", "Fruiting"]
        
    def create_data(self, base_temp: float = 23.0, base_humidity: float = 65.0) -> dict[str, Any]:
        """
        Generate a new set of plant monitoring data.
        
        Args:
            base_temp (float): Base temperature in Celsius around which to generate data
            base_humidity (float): Base humidity percentage around which to generate data
            
        Returns:
            dict: A dictionary containing the generated plant monitoring data
        """
        # Generate data with realistic variations around the base values
        data = {
            'id': self.start_id,
            'researcher': random.choice(self.researchers),
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'plant_metrics': {
                'height_cm': round(random.gauss(45, 8), 1),  # Average height 45cm with 8cm standard deviation
                'leaf_count': round(random.gauss(24, 6)),    # Average 24 leaves with 6 standard deviation
                'stem_diameter_mm': round(random.gauss(8.5, 1.2), 2)  # Average 8.5mm with 1.2mm standard deviation
            },
            'environmental_conditions': {
                'temperature_c': round(random.gauss(base_temp, 2), 1),  # Temperature varies around base_temp
                'humidity_pct': round(random.gauss(base_humidity, 10)),  # Humidity varies around base_humidity
                'light_intensity_lux': round(random.gauss(15000, 3000))  # Average 15000 lux with 3000 standard deviation
            },
            'soil_data': {
                'moisture_pct': round(random.gauss(70, 8)),  # Average 70% moisture with 8% standard deviation
                'ph_level': round(random.gauss(6.5, 0.4), 1),  # Average pH 6.5 with 0.4 standard deviation
                'nutrient_index': round(random.gauss(450, 80))  # Average 450 with 80 standard deviation
            },
            'plant_type': random.choice(self.plant_types),
            'growth_stage': random.choice(self.growth_stages),
            'health_score': round(random.gauss(85, 12))  # Average health score 85 with 12 standard deviation
        }
        self.start_id += 1  # Increment ID for next data point
        return data