use_emulator = True

if use_emulator:
    from EmulatorPlatform import EmulatorPlatform, Pin
    platform = EmulatorPlatform()
else:
    from umodbus.serial import ModbusRTU    # https://github.com/brainelectronics/micropython-modbus
    from machine import Pin
    import sys
    import uselect
    import time
    from PiPicoPlatform import PiPicoPlatform

    # pin definitions
    DriverIn = Pin(0)
    ReceiveOut = Pin(1)
    Control = 2
    SlaveID = 0 

    def askForSlaveAddress():
        global SlaveID
        if(SlaveID == 0):
            ID = input("Please enter the slave address you want to give this device: ")
        try:
            SlaveID = int(ID)
            print("This device was given the SlaveID ", SlaveID)
        except:
            ID = input("Please enter the slave address you want to give this device: ")
    askForSlaveAddress()

    platform = PiPicoPlatform(
        modbus_slave_addr = SlaveID,
        modbus_tx_pin = DriverIn,
        modbus_rx_pin = ReceiveOut,
        modbus_uart_id = 0,
        modbus_ctrl_pin = Control
    )
 
    def buttonHandler(pin):
        print("Button press received")
        closeProgram()

    button = Pin(28, Pin.IN, Pin.PULL_UP)        
    button.irq(trigger = Pin.IRQ_FALLING, handler = buttonHandler)

shouldClose = False

IntEnum = object

def onCallback(reg_type, address, val):
    print(f"Callback function on register {address} called")

register_definitions = {
    "COILS": {
        "COIL": {
            "register": 2,
            "len": 1,
            "val": 1,
            "unit": "unit"
        }
    },
    "HREGS": {
        "HREG": {
            "register": 4,
            "len": 1, 
            "val": 2,
            "unit": "unit",
            "on_get_cb": onCallback
        }
    },
    "ISTS": {
        "IST": {
            "register": 6,
            "len": 1,
            "val": 3,
            "unit": "unit"
        }
    },
    "IREGS": {
        "IREG": {
            "register": 8,
            "len": 1,
            "val": 4,
            "unit": "unit"
        }
    }
}

platform.setup_registers(register_definitions)

class Commands(IntEnum):
    setModbusValueType = 1
    readModbusValue = 2
    setGPIO = 3
    stop = 42   # crashes the script but it does the job
                # easy fix but like... why?

shouldClose = False

# 1 (setModbusValueType) 0 <0: coil, 1: hreg, 2: ist, 3: ireg> 93 (registerName)) 5 (value)
def setModbusValueType(arguments):
    if len(arguments) != 4:
        print("setModbusValueType <RegisterName> <Value>") 
        return

    type = int(arguments[1])
    register = int(arguments[2])
    value = int(arguments[3])

    try:
        if type == 0: #coil
            platform.set_coil(register, value)
            print(f"Successfully written value {value} to COIL {register}")
        elif type == 1: #hreg
            platform.set_hreg(register, value)
            print(f"Successfully written value {value} to HREG {register}")
        elif type == 2: #ist
            platform.set_ist(register, bool(value))
            print(f"Successfully written value {value} to IST {register}")
        elif type == 3: #ireg
            platform.set_ireg(register, value)
            print(f"Successfully written value {value} to IREG {register}")
        else:
            print("<0: coil, 1: hreg, 2: ist, 3: ireg>")
    except Exception as e:
        print(f"Failed writing to register {register}: {e}")

# 2 (readModbusValue) <0: coil, 1:hreg, 2: ist, 3:ireg> 93 (register)
def readModbusValue(argument):
    if len(argument) != 3:
        print("readModbusValue <type> <address>")
        return

    type = int(argument[1])
    register = int(argument[2])

    try:
        if type == 0: #coil
            print(f"COIL value in register {register}: {platform.get_coil(register)}")
        elif type == 1: #hreg
            print(f"HREG value in register {register}: {platform.get_hreg(register)}")
        elif type == 2: #ist
            print(f"IST value in register {register}: {platform.get_ist(register)}")
        elif type == 3: #ireg
            print(f"IREG value in register {register}: {platform.get_ireg(register)}")
        else:
            print("<0: coil, 1: hreg, 2: ist, 3: ireg>")
    except Exception as e:
        print(f"Failed reading from register {register}: ", e)
         
# 3 16 1
# setGPIO GPIO16 high
def setGPIO(arguments):
    if len(arguments) != 3:
        print("setGPIO <Pin> <1:high / 0:low>")
        return

    try:
        ChangedPin = Pin(int(arguments[1]), Pin.OUT)
        mode = int(arguments[2])
        platform.set_gpio(ChangedPin, mode)
        print(f"Set pin {ChangedPin} to {mode}")
    except Exception as e:
        print(f"Error: {e}")
        # dont make an extra Pin object in EmulatorPlatform

def closeProgram():
    global shouldClose
    shouldClose = True
    print("Stopping tasks!")
    time.sleep(2)

def checkCommand(Input):
    try:
        number = int(Input[0])
    except:
        print(f"Error, invalid int. Input: " + str(Input))
        return

    if number == Commands.setModbusValueType:
        setModbusValueType(Input)
    elif number == Commands.readModbusValue:
        readModbusValue(Input)
    elif number == Commands.setGPIO:
        setGPIO(Input)
    elif number == Commands.stop:
        closeProgram()
    else: 
        print(f"Error, invalid command. Input: {number}")

if __name__ == "__main__":
    while shouldClose == False:
        userInput = platform.check_input()
        if userInput:  
            checkCommand(userInput)
        else:
            platform.process() # doesnt work in Emulator Mode but that doesn't really matter as we won't be processing clients

        '''
        command = input("---------------------------------------------\n"
                    + "(Int) <EnumCommand> <Value1> <Value2>\n"
                    + "setModbusValueType = 1 <register> <value>\n"
                    + "readModbusValue    = 2\n"
                    + "setGPIO            = 3 <pin> <1: high / 0:low>\n"
                    + ":").split()
        '''
    