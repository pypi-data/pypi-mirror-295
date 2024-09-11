# EBIOXP0919

![EBIOXP0919](https://raw.githubusercontent.com/electronbits/Py_EBIOXP0919/main/io_4i4o_2.jpg)

This is a Python package to interface with the EBIOXP0910-4I4O board, it is designed to be easily integrated with [EBRPIH1118](https://www.electronbits.com/product/raspberry-pi-base/) and RaspberryPi.

## Features

- Read input status
- Control relays
- Easy to use and integrate with other projects


# Setting Up I2C on Raspberry Pi

## Step 1: Enable I2C Interface

Before interacting with I2C devices, the I2C interface needs to be enabled on your Linux Machine. e.g. Raspberry Pi.
You can install `EBIOXP0919` using pip. Ensure you have the necessary Python libraries for GPIO and I2C communication.

1. Open the Raspberry Pi configuration tool:

   ```bash
   sudo raspi-config
   ```
2. Navigate to Interface Options using the arrow keys and select I2C.
3. Choose Yes to enable the I2C interface.
4. Exit the tool and reboot your Raspberry Pi:
    ```bash
    sudo reboot
    ```
## Step 2: Install I2C Tools
After enabling I2C, you'll need to install i2c-tools to scan and interact with I2C devices.

1. Update your package list:
    ```bash
    sudo apt update
    ```
2. Install the I2C tools package:
    ```bash
    sudo apt install -y i2c-tools
    ```
## Step 3: Verify I2C is Enabled
After rebooting, verify that the I2C kernel module is loaded.

1. Check if I2C modules are loaded by running:
    ```bash
    lsmod | grep i2c
    ```
You should see something like i2c_bcm2835 or i2c_dev listed. If they are not present, you may need to manually load the modules:
```bash
sudo modprobe i2c-bcm2835
sudo modprobe i2c-dev
```
## Step 4: Identify I2C Bus Number
To find which I2C bus your Raspberry Pi is using, check the /dev directory.

1. List available I2C buses:
    ```bash
    ls /dev/i2c-*
    ```
    You should see something like /dev/i2c-1 (or /dev/i2c-0 depending on your Raspberry Pi model). Most modern Raspberry Pi boards use /dev/i2c-1.
## Step 5: Scan for I2C Devices
Now that everything is set up, you can scan the I2C bus to detect any connected devices.

1. Run the following command to scan the I2C bus (assuming your bus is i2c-1):
    ```bash
    sudo i2cdetect -y 1
    ```
2. The output will display a grid, showing the I2C addresses of any detected devices:
    ```bash
    0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
    00: -- -- -- -- -- -- -- --
    10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    50: -- -- -- -- -- -- -- -- 3f -- -- -- -- -- -- --
    60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    70: -- -- -- -- -- -- -- --
    ```
    Any value shown (like 3f in the above example) is the hexadecimal address of a detected I2C device.
    
    If you see no addresses, check your wiring and make sure the device is powered on.


## Installation

```bash
pip install EBIOXP0919
```
# Usage
## Importing the Package
from EBRPIH1118_intf import ebrpih1118

# Example usage
```python
from EBIOXP0919_intf import ebioxp0919

board = ebioxp0919.EBIOXP0919(chip_address=0x3f)

# Example to toggle relay 1 ON
board.toggle_relay(1, ebioxp0919.RelayState.ON)

# Example to read digital input 2
input_state = board.get_input_state(2)
print(f"Digital Input 2 State: {input_state}")

# Cleanup when done
board.cleanup()
```



# Steps to Contribute
Fork the repository.
Create a new branch for your feature or bug fix.
Make your changes.
Submit a pull request to the main repository.

# License
This project is licensed under the MIT License - see the LICENSE file for details.

# Acknowledgments
 - This package uses the `smbus` library for I2C communication.

# More Information

For more details, visit our website: [www.electronbits.com](https://www.electronbits.com)

