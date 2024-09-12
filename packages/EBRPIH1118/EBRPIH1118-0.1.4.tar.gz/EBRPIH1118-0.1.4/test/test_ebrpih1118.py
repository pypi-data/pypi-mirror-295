import unittest
from unittest.mock import patch, MagicMock
from EBRPIH1118_intf.ebrpih1118 import HwType, HwDirection, RelayActions, DoActions, DiStates, EBRPIH1118

class TestEBRPIH1118(unittest.TestCase):
    
    def test_hw_type_enum(self):
        self.assertEqual(HwType.Relay, 0)
        self.assertEqual(HwType.DO, 1)
        self.assertEqual(HwType.DI, 2)
        self.assertEqual(HwType.AI, 3)
        self.assertEqual(HwType.W1_SENSOR, 4)

    def test_hw_direction_enum(self):
        self.assertEqual(HwDirection.INPUT, 0)
        self.assertEqual(HwDirection.OUTPUT, 1)

    def test_relay_actions_enum(self):
        self.assertEqual(RelayActions.OFF, 0)
        self.assertEqual(RelayActions.ON, 1)

    def test_do_actions_enum(self):
        self.assertEqual(DoActions.Deactivated, 0)
        self.assertEqual(DoActions.Activated, 1)

    def test_di_states_enum(self):
        self.assertEqual(DiStates.Grounded, 0)
        self.assertEqual(DiStates.High, 1)
    
    @patch('EBRPIH1118_intf.ebrpih1118.IO')
    @patch('EBRPIH1118_intf.ebrpih1118.spidev.SpiDev')
    def test_gpio_setup(self, mock_spi, mock_gpio):
        # Mock the GPIO and SPI setup
        mock_gpio.BCM = MagicMock()
        mock_gpio.OUT = MagicMock()
        mock_gpio.IN = MagicMock()
        mock_gpio.LOW = MagicMock()
        mock_gpio.PUD_OFF = MagicMock()

        board = EBRPIH1118()
        mock_gpio.setmode.assert_called_once_with(mock_gpio.BCM)
        self.assertEqual(mock_gpio.setwarnings.call_count, 1)

    @patch('EBRPIH1118_intf.ebrpih1118.IO.output')
    def test_energize_relay(self, mock_output):
        board = EBRPIH1118()
        self.assertTrue(board.energize_relay(1))
        mock_output.assert_called_once_with(17, True)  # 17 is GPIO pin for relay 1
        
        self.assertFalse(board.energize_relay(10))  # Invalid relay number

    @patch('EBRPIH1118_intf.ebrpih1118.IO.output')
    def test_relay_on(self, mock_output):
        board = EBRPIH1118()
        
        # Test valid relay on
        result = board.relay_on(1)
        self.assertTrue(result[0])  # Success
        mock_output.assert_called_once_with(17, True)
        
        # Test invalid relay on
        result = board.relay_on(10)
        self.assertFalse(result[0])  # Fail due to invalid relay number
        self.assertIn("Invalid relay number", result[1])  # Error message


if __name__ == '__main__':
    unittest.main()
