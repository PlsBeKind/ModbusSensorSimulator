### Project Overview
Simulator for sensors.
Modbus values can be entered and read with the help of commands.
GPIO pins can be set to a value of high, low or resistance.

#### Command syntax
1. **setModbusValueType (command 1)**:
    - Sets the value of a Modbus register.
    - Syntax: `1 <RegisterType> <RegisterAddress> <Value>`
    - Example: `1 1 4 6`
        - `1`: Command for setting a Modbus value
        - `1`: Register type (0: Coil, 1: Hreg, 2: Actual, 3: Ireg)
        - 4`: Address of the register
        - `6`: Value to be written to the register

2. **readModbusValue (command 2)**:
    - Reads the value of a Modbus register.
    - Syntax: `2 <RegisterType> <RegisterAddress>`
    - Example: `2 0 5`
        - `2`: Command for reading a Modbus value
        - `0`: Register type (0: Coil, 1: Hreg, 2: Actual, 3: Ireg)
        - `5`: Address of the register

3. **setGPIO (command 3)**:
    - Sets the state of a GPIO pin.
    - Syntax: `3 <PinNumber> <State>`
    - Example: `3 16 1`
        - `3`: Command for setting a GPIO pin
        - `16`: Number of the GPIO pin
        - `1`: State of the GPIO pin (1: High, 0: Low, -1: Resistance)

4. **stop (command 42)**:
    - Terminates the script.
    - Syntax: `42`
    - Example: `42`
        - `42`: Command to end the script

## Additional information:
    If the terminal is empty when the script is started, the script is probably asking for a slaveID (use_Emulator False only)

### Configuration
    The application can be executed either in emulator mode or in real mode by setting the variable `use_Emulator' to True or False

    : Start the script with `python main.py`
    : Start the tests with `python -m unittest test_main.py`
    : Start the coverage report with `coverage run main.py` and create html tables with `coverage html`