"""
ElectronBits 2020
This module handles commands sent to the EBIOXP0919-4I4O board 
from a Raspberry Pi, which sits on EBRPIH1118 board. 
To read input status and energize/de-energize power relays.
It uses smbus/smbus2 module to connect to the board. 
"""

try:
    import smbus as smbus
except Exception as e:
    try:
        import smbus2 as smbus
    except:
        raise ImportError("There is no smbus/smbus2 module available on your system. Please install smbus/smbus2 module for Python3.")

from enum import IntEnum

class RelayState(IntEnum):
    OFF = 0
    ON = 1

class Colors:
    color_codes = {
        'HEADER' : '\033[95m',
        'OKBLUE' : '\033[94m',
        'OKGREEN' : '\033[92m',
        'WARNING' : '\033[93m',
        'FAIL' : '\033[91m',
        'ENDC' : '\033[0m',
        'BOLD' : '\033[1m',
        'UNDERLINE' : '\033[4m',
    }

    @classmethod
    def colored_text(cls, text: str, color_code: str) -> str:
        color = cls.color_codes.get(color_code)
        if color is not None:
            return color + text + cls.color_codes['ENDC']
        else:
            return text


class EBIOXP0919:
    RD_REGISTER = 0x00 
    WR_REGISTER = 0x01
    CFG_REGISTER = 0x03
    CFG_VALUE = 0xf0
    
    def __init__(self, chip_address=0x3f):
        self.chip_address = chip_address
        self.bus = self.get_bus()
        
        if not self.is_already_init():
            print(Colors.colored_text("Initializing Board...", 'UNDERLINE'))
            self.init_board()

    @staticmethod
    def get_bus() -> smbus.SMBus:
        "Returns smbus.SMBus object"
        try:
            return smbus.SMBus(1)
        except Exception as e:
            raise Exception(Colors.colored_text(str(e), 'FAIL'))

    def cleanup(self):
        self.bus.close()
        print(Colors.colored_text("Clean up Done.", 'OKGREEN'))

    def is_already_init(self) -> bool:
        ret = self.read_from_board(self.CFG_REGISTER)
        return ret == self.CFG_VALUE

    def init_board(self):
        try:
            self.bus.write_byte_data(self.chip_address, self.CFG_REGISTER, 0xf0)
            self.bus.write_byte_data(self.chip_address, self.WR_REGISTER, 0x0)
        except OSError as e:
            raise Exception(Colors.colored_text(str(e), 'FAIL'))

    def read_from_board(self, target_reg):
        "Reads target register value which can be either config register or read register"
        return self.bus.read_byte_data(self.chip_address, target_reg)

    def read_input_state(self, input_number):
        expected_values = {1: 0x1, 2: 0x2, 3: 0x4, 4: 0x8}
        ret = self.read_from_board(self.RD_REGISTER) >> 4
        return (ret & expected_values[input_number]) >> (input_number - 1)

    def relay_handler(self, relay_number, state: RelayState):
        former_relays_status = self.read_from_board(self.RD_REGISTER) & 0xf
        if state == RelayState.OFF:
            new_relays_status = former_relays_status & (0xf ^ (1 << relay_number - 1))
        elif state == RelayState.ON:
            new_relays_status = former_relays_status | (1 << relay_number - 1)
        self.bus.write_byte_data(self.chip_address, self.WR_REGISTER, new_relays_status)

    def toggle_relay(self, relay_number, state: RelayState):
        if relay_number in (1, 2, 3, 4):
            self.relay_handler(relay_number, state)
        else:
            print(Colors.colored_text("Invalid Relay number.", 'FAIL'))

    def get_input_state(self, input_number):
        if input_number in (1, 2, 3, 4):
            return self.read_input_state(input_number)
        else:
            raise ValueError(Colors.colored_text("Invalid digital input number.", 'FAIL'))


# Example usage:
if __name__ == "__main__":
    board = EBIOXP0919(chip_address=0x3f)

    # Example to toggle relay 1 ON
    board.toggle_relay(1, RelayState.ON)

    # Example to read digital input 2
    input_state = board.get_input_state(2)
    print(f"Digital Input 2 State: {input_state}")

    # Cleanup when done
    board.cleanup()
