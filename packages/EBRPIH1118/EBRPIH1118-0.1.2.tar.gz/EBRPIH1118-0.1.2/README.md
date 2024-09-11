# EBRPIH1118

`EBRPIH1118` is a Python package designed to facilitate the control of hardware resources such as relays, digital inputs (DI), digital outputs (DO), analog inputs (AI), and temperature sensors on a Raspberry Pi. This package provides a convenient API to interact with GPIO pins and SPI devices, making it easy to develop automation applications on the Raspberry Pi.

## Features

- **Relay Control**: Easily manage relays connected to the Raspberry Pi GPIO pins.
- **Digital Input/Output**: Read from and write to digital input/output pins.
- **Analog Input**: Read analog sensor data using SPI interface.
- **Temperature Sensor Integration**: Read data from 1-wire temperature sensors.
- **Flexible Hardware Management**: Abstract hardware interaction with a clean, easy-to-use API.

## Installation

You can install `EBRPIH1118` using pip. Ensure you have the necessary Python libraries for GPIO and SPI communication.

### Prerequisites

Before installing `EBRPIH1118`, ensure that your Raspberry Pi is set up with the following libraries:

```bash
sudo apt-get update
sudo apt-get install python3-pip python3-rpi.gpio python3-spidev
```

# Installing the Package
```bash
pip install EBRPIH1118
```

# Usage
## Importing the Package
from EBRPIH1118_intf import ebrpih1118

# Example usage
```python
from EBRPIH1118_intf import ebrpih1118

# Initialize GPIO and SPI
hardware_manager = ebrpih1118.EBRPIH1118()

# Example: Turn on relay #1
hardware_manager.energize_relay(relay_number=1)

# Example: Read an analog input from channel 1 to 4 (SPI)
analog_value = hardware_manager.read_ai_channels(channels="1,2,3,4")
print(f"Analog Input Values: {analog_value}")

# Cleanup after operations
hardware_manager.cleanup()
```



# Steps to Contribute
Fork the repository.
Create a new branch for your feature or bug fix.
Make your changes.
Submit a pull request to the main repository.

# License
This project is licensed under the MIT License - see the LICENSE file for details.

# Acknowledgments
 - This package uses the RPi.GPIO library for GPIO control.
 - It also uses the spidev library for SPI communication.

# More Information

For more details, visit our website: [www.electronbits.com](https://www.electronbits.com)