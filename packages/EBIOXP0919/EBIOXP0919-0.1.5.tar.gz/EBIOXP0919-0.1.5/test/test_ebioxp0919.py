import unittest
from unittest.mock import patch, MagicMock
from EBIOXP0919_intf.ebioxp0919 import RelayState, Colors, EBIOXP0919

class TestEBIOXP0919(unittest.TestCase):
    
    def test_relay_state_enum(self):
        self.assertEqual(RelayState.OFF, 0)
        self.assertEqual(RelayState.ON, 1)

    def test_colored_text(self):
        self.assertEqual(Colors.colored_text("Test", "OKGREEN"), "\033[92mTest\033[0m")
        self.assertEqual(Colors.colored_text("Test", "UNKNOWN"), "Test")  # When color is not found
    
    @patch('EBIOXP0919_intf.ebioxp0919.smbus.SMBus')
    def test_get_bus(self, mock_smbus):
        # Test successful bus return
        mock_smbus.return_value = MagicMock()
        bus = EBIOXP0919.get_bus()
        self.assertIsNotNone(bus)
    
    @patch('EBIOXP0919_intf.ebioxp0919.EBIOXP0919.is_already_init')
    @patch('EBIOXP0919_intf.ebioxp0919.EBIOXP0919.get_bus')
    def test_init_board(self, mock_get_bus, mock_is_already_init):
        # Set up mock behavior
        mock_get_bus.return_value = MagicMock()
        mock_is_already_init.return_value = False
        
        # Create an instance of EBIOXP0919
        board = EBIOXP0919()
        mock_get_bus.assert_called_once()
        mock_is_already_init.assert_called_once()

    @patch('EBIOXP0919_intf.ebioxp0919.smbus.SMBus')
    def test_cleanup(self, mock_smbus):
        # Set up mock bus
        mock_bus = MagicMock()
        mock_smbus.return_value = mock_bus
        
        # Create instance and call cleanup
        board = EBIOXP0919()
        board.cleanup()
        mock_bus.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
