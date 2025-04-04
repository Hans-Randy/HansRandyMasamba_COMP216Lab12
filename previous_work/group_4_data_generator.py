import matplotlib.pyplot as plt
import random
import math

class DataGenerator:
    """
    A class to generate pseudo-random data that simulates sensor readings.
    """

    def __init__(self, base_min: float = 18, base_max: float = 21, squiggle_std: float = 0.1, peak_mean: float = 20, peak_std: float = 1, peak_frequency: int = 50, sin_delta: float = 0.1, seed: int = 48):
        """
        Initializes the DataGenerator with customizable parameters.

        Args:
            base_min: The minimum value of the base range.
            base_max: The maximum value of the base range.
            squiggle_std: Standard deviation for the squiggle (noise).
            peak_mean: Mean value around which peaks will occur.
            peak_std: Standard deviation for the peak heights.
            peak_frequency:  Determines how often peaks occur.  Higher value = less frequent.
            sin_delta: Determines how fast the sine pattern complete 1 cycle.
            seed: Seed for the random number generator.
        """
        self.base_min = base_min
        self.base_max = base_max
        self.squiggle_std = squiggle_std
        self.peak_mean = peak_mean
        self.peak_std = peak_std
        self.peak_frequency = peak_frequency
        self._base_value = (base_min + base_max) / 2  # Initialize a base value for pattern generation.
        self._sin_seed = 0
        self._sin_delta = sin_delta
        random.seed(seed)

    def _generate_normalized_value(self) -> float:
        """
        Generates a normalized random value between 0 and 1 using a combination of techniques.

        Returns:
            A normalized random value.
        """
        # Generate a uniform random value between 0 and 1
        uniform_value = random.random()

        # Generate a Gaussian (normal) random value with mean 0.5 and standard deviation 0.15
        gaussian_value = random.gauss(0.5, 0.15)
        
        # Ensure the Gaussian value is within the range [0, 1]
        gaussian_value = max(0, min(1, gaussian_value))

        # Generate a sine-pattern based random value in the range of 0 to 1
        pattern_value_sine = (math.sin(self._sin_seed) / 2 + 0.5) * 0.9 + 0.1 * (random.random())
        self._sin_seed += self._sin_delta

        # Combine the three values with specified weights
        combined_value = 0.4 * uniform_value + 0.3 * gaussian_value + 0.3 * pattern_value_sine

        return combined_value

    @property
    def value(self) -> float:
        """
        Returns a random value within the specified range, incorporating squiggles and peaks.

        Returns:
            A random value within the defined range.
        """
        # Calculate the base range
        base_range = self.base_max - self.base_min

        # Generate a normalized random value
        random_value = self._generate_normalized_value()

        # Calculate the base value within the range
        y = base_range * random_value + self.base_min

        # Add Gaussian noise (squiggle)
        y += random.gauss(0, self.squiggle_std)

        # # Occasionally add a peak value
        if random.randint(0, self.peak_frequency) == 0:
            y += random.gauss(self.peak_mean - y, self.peak_std)

        # Clamp the value to ensure it stays within the specified range
        y = max(self.base_min, min(self.base_max, y))

        return y

def main() -> None:
    data_generator = DataGenerator(base_min=18, base_max=22, squiggle_std=0.2, peak_mean=23, peak_std=0.8, peak_frequency=60, sin_delta=0.1, seed=42)

    # num_points = 500
    num_points = 500
    data_points = [data_generator.value for _ in range(num_points)]

    plt.figure(figsize=(12, 6))
    plt.plot(data_points, color='blue', linestyle='-', linewidth=1)
    # plt.title('Simulated Temperature Data')
    plt.title('Simulated Temperature Data')
    plt.xlabel('Time')
    plt.ylabel('Temperature (°C)')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()