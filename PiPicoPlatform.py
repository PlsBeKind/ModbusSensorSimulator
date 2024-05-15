from machine import Pin
from umodbus.serial import ModbusRTU
import uselect
import sys
# pin here

class PiPicoPlatform():
    def __init__(
        self,
        modbus_slave_addr: int,
        modbus_uart_id: int,
        modbus_tx_pin: int,
        modbus_rx_pin: int,
        modbus_ctrl_pin: int,
    ):
        self._modbus_client = ModbusRTU(
            addr=modbus_slave_addr,
            pins=(modbus_tx_pin, modbus_rx_pin),
            uart_id=modbus_uart_id,
            ctrl_pin=modbus_ctrl_pin,
        )

    def setup_registers(self, register_definitions):
        self._modbus_client.setup_registers(register_definitions)

    def set_coil(self, register: int, value: int):
        self._modbus_client.set_coil(register, value)

    def set_hreg(self, register: int, value: int):
        self._modbus_client.set_hreg(register, value)

    def set_ist(self, register: int, value: bool):
        self._modbus_client.set_ist(register, value)

    def set_ireg(self, register: int, value: int):
        self._modbus_client.set_ireg(register, value)

    def get_coil(self, register: int):
        return self._modbus_client.get_coil(register)

    def get_hreg(self, register: int):
        return self._modbus_client.get_hreg(register)

    def get_ist(self, register: int):
        return self._modbus_client.get_ist(register)

    def get_ireg(self, register: int):
        return self._modbus_client.get_ireg(register)

    def set_gpio(self, pin: int, mode: int):
        if(mode == 1):
            ChangedPin = Pin(int(pin), Pin.OUT)
            ChangedPin.high()
            print(f"Set pin {ChangedPin} to high")
        elif(mode == 0):
            ChangedPin = Pin(int(pin), Pin.OUT)
            ChangedPin.low()
            print(f"Set pin {ChangedPin} to low")
        elif(mode == -1):
            ChangedPin = Pin(int(pin), Pin.IN)
            print(f"Set pin {ChangedPin} to resistance")
        else:
            print("Error: Invalid mode")

    def process(self):
        self._modbus_client.process()

    def check_input(self): #optimally, returns list[str] 
        upoll = uselect.poll()
        upoll.register(sys.stdin, uselect.POLLIN)

        if upoll.poll(0):
            return sys.stdin.readline().split()
        else:
            return None 
