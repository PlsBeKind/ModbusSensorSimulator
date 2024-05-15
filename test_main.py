import unittest
from unittest.mock import patch
import main

class TestMain(unittest.TestCase):
    def test_setModbusValueType(self):
        with patch("builtins.print") as print_mock:
            with patch("main.platform") as platform_mock:
                # COIL
                main.setModbusValueType(["1", "0", "2", "1"])
                platform_mock.set_coil.assert_called_once_with(2, 1)
                print_mock.assert_any_call("Successfully written value 1 to COIL 2")
                
                # HREG
                platform_mock.reset_mock()
                main.setModbusValueType(["1", "1", "4", "10"])
                platform_mock.set_hreg.assert_called_once_with(4, 10)
                print_mock.assert_any_call("Successfully written value 10 to HREG 4")

                # IST
                platform_mock.reset_mock()
                main.setModbusValueType(["1", "2", "6", "1"])
                platform_mock.set_ist.assert_called_once_with(6, True)
                print_mock.assert_any_call("Successfully written value 1 to IST 6")

                # IREG
                platform_mock.reset_mock()
                main.setModbusValueType(["1", "3", "8", "20"])
                platform_mock.set_ireg.assert_called_once_with(8, 20)
                print_mock.assert_any_call("Successfully written value 20 to IREG 8")

                # invalid type
                platform_mock.reset_mock()
                main.setModbusValueType(["1", "4", "2", "10"])
                platform_mock.set_hreg.assert_not_called()
                print_mock.assert_any_call("<0: coil, 1: hreg, 2: ist, 3: ireg>")

    def test_readModbusValue(self):
        with patch("builtins.print") as print_mock:
            with patch("main.platform") as platform_mock:
                platform_mock.get_coil.return_value = 1
                platform_mock.get_hreg.return_value = 20
                platform_mock.get_ist.return_value = True
                platform_mock.get_ireg.return_value = 40

                # COIL
                main.readModbusValue(["2", "0", "2"])
                platform_mock.get_coil.assert_called_once_with(2)
                print_mock.assert_any_call("COIL value in register 2: 1")

                # HREG
                platform_mock.reset_mock()
                main.readModbusValue(["2", "1", "4"])
                platform_mock.get_hreg.assert_called_once_with(4)
                print_mock.assert_any_call("HREG value in register 4: 20")

                # IST
                platform_mock.reset_mock()
                main.readModbusValue(["2", "2", "6"])
                platform_mock.get_ist.assert_called_once_with(6)
                print_mock.assert_any_call("IST value in register 6: True")

                # IREG
                platform_mock.reset_mock()
                main.readModbusValue(["2", "3", "8"])
                platform_mock.get_ireg.assert_called_once_with(8)
                print_mock.assert_any_call("IREG value in register 8: 40")

                # invalid type
                platform_mock.reset_mock()
                main.readModbusValue(["2", "4", "2"])
                platform_mock.get_hreg.assert_not_called()
                print_mock.assert_any_call("<0: coil, 1: hreg, 2: ist, 3: ireg>")

    # if input can't be casted to integer
    def test_checkCommand_invalid_int(self):
        with patch("builtins.print") as print_mock:
            main.checkCommand(["w", "a"])
            print_mock.assert_any_call("Error, invalid int. Input: ['w', 'a']")

    def test_checkCommand_invalid_command(self):
        with patch("builtins.print") as print_mock:
            main.checkCommand(["99", "some", "invalid", "command"])
            print_mock.assert_any_call("Error, invalid command. Input: 99")
 
if __name__ == "__main__":
    unittest.main()
