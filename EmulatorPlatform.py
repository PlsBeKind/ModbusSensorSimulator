from HAL9000 import HAL
import logging
logger = logging.getLogger(__name__)

class EmulatorPlatform(HAL):
    def __init__(self):
        super().__init__()
 
    def process(self):
        logger.debug("Processing...")

    def set_gpio(self, pin: int, mode: int):
        logger.debug(f"Set pin {pin} to {mode}")
        if(mode == 0): #low
            Pin(int)

    def setup_registers(self, registers): 
        self.registers = registers
        logger.info("Registers set up!")
 
    def check_input(self) -> list[str]:
        input_str = input("Input: ").split()
        return input_str
    
    # ModbusRTU register    
    def _validate_register_type(self, reg_type: str):
        if reg_type not in self.registers:
            raise ValueError(f"Register type '{reg_type}' not found")

    def _validate_register(self, reg_type: str, reg_name: str):
        self._validate_register_type(reg_type)
        if reg_name not in self.registers[reg_type]:
            raise ValueError(f"Register '{reg_name}' not found in {reg_type}")
    
    def get_register(self, reg_type: str, register: int): 
        self._validate_register_type(reg_type)
        for reg_name, reg_info in self.registers[reg_type].items():
            if reg_info["register"] == register:
                return reg_info["val"]
        raise ValueError(f"Register '{register}' not found in {reg_type}")

    def set_register(self, reg_type: str, register: int, value):
        self._validate_register_type(reg_type)
        for reg_name, reg_info in self.registers[reg_type].items():
            if reg_info["register"] == register:
                reg_info["val"] = value
                return
        raise ValueError(f"Register '{register}' not found in {reg_type}")

    def set_coil(self, register: int, value: int):
        self.set_register("COILS", register, value)
        logger.debug(f"Setting COIL {register} to {value}")

    def set_hreg(self, register: int, value: int):
        self.set_register("HREGS", register, value)
        logger.debug(f"Setting HREG {register} to {value}")

    def set_ist(self, register: int, value: int):
        self.set_register("ISTS", register, bool(value))
        logger.debug(f"Setting IST {register} to {value}")

    def set_ireg(self, register: int, value: int):
        self.set_register("IREGS", register, value)
        logger.debug(f"Setting IREG {register} to {value}")

    def get_coil(self, register: int):
        logger.debug(f"Getting COIL value from register {register}")
        return self.get_register("COILS", register)

    def get_hreg(self, register: int) -> int:
        logger.debug(f"Getting HREG value from register {register}")
        return self.get_register("HREGS", register)

    def get_ist(self, register: int) -> bool:
        logger.debug(f"Getting IST value from register {register}")
        return self.get_register("ISTS", register)

    def get_ireg(self, register: int) -> int:
        logger.debug(f"Getting IREG value from register {register}")
        return self.get_register("IREGS", register)
        
#TODO remove
class Pin:
    IN = 0
    OUT = 1
    PULL_UP = 2
    IRQ_FALLING = 3
    
    def __init__(self, *argv, **kwargs) -> None: ...
    def high(self):
        logger.info("Pin has been set to high!")
    
    def low(self):
        logger.info("Pin has been set to low!")
 