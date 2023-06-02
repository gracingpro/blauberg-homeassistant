from pyModbusTCP.client import ModbusClient
from References.Descriptions.InputRegisters import input_registers as description_input_registers
from References.Descriptions.HoldingRegisters import holding_registers as description_holding_registers
from References.Descriptions.Coils import coils as description_coils
from References.Descriptions.DiscreteInputs import discrete_inputs as description_discrete_inputs
from References.Descriptions.Alarms import alarms as description_alarms
from References.Variables.InputRegisters import input_registers as variables_input_registers
from References.Variables.HoldingRegisters import holding_registers as variables_holding_registers
from References.Variables.Coils import coils as variables_coils
from References.Variables.DiscreteInputs import discrete_inputs as variables_discrete_inputs
from References.Variables.Alarms import alarms as variables_alarms
from References.Units.InputRegisters import input_registers as units_input_registers
from References.Units.HoldingRegisters import holding_registers as units_holding_registers
from References.Controls.Coils import coils as control_coils
from References.Controls.HoldingRegisters import holding_registers as control_holding_registers
from References.Aliases.HoldingRegisters import holding_registers as aliases_holding_registers
from References.Aliases.InputRegisters import input_registers as aliases_input_registers
from References.Icons.HoldingRegisters import holding_registers as icons_holding_registers
from References.Icons.InputRegisters import input_registers as icons_input_registers
from Data.Vars import get_description, get_by_name, replace_options, get_key_from_value
import configparser

configfile = "config.ini"
config = configparser.ConfigParser()
config.read(configfile)
# TCP auto connect on first modbus request
c = ModbusClient(host=config["Vent"]["ip"], port=502, auto_open=True, auto_close=True)


class ModBus:
    @staticmethod
    def get_coils():
        output = {}
        coils = c.read_coils(0, 25)
        coils_len = len(coils)
        for coil in range(coils_len):
            output[get_description(variables_coils, coil)] = {"value": coils[coil],
                                                              "description": get_description(description_coils, coil),
                                                              "unit": None,
                                                              "control": get_description(control_coils, coil)}
        return output

    @staticmethod
    def get_discrete_inputs():
        output = {}
        discrete_inputs = c.read_discrete_inputs(0, 19)
        discrete_inputs_len = len(discrete_inputs)
        for discrete_input in range(discrete_inputs_len):
            output[get_description(variables_discrete_inputs, discrete_input)] = {
                "value": discrete_inputs[discrete_input],
                "description": get_description(
                    description_discrete_inputs, discrete_input),
                "unit": None}
        return output

    @staticmethod
    def get_alarms():
        output = {}
        alarms = c.read_discrete_inputs(19, 44)
        alarms_len = len(alarms)
        for alarm in range(alarms_len):
            description = get_description(description_alarms, alarm)
            output[get_description(variables_alarms, alarm)] = {"value": alarms[alarm],
                                                                "description": description,
                                                                "unit": None,
                                                                "icon": "mdi:alarm-light"}
        return output

    @staticmethod
    def get_input_registers():
        output = {}
        input_registers = c.read_input_registers(0, 51)
        input_registers_len = len(input_registers)
        for input_register in range(input_registers_len):
            unit = get_description(units_input_registers, input_register)
            if unit == "°C":
                if int(input_registers[input_register] / 10) > 6000:
                    value = float((input_registers[input_register] - 65540) / 10)
                else:
                    value = float(input_registers[input_register] / 10)
            elif unit == "h":
                hours = (input_registers[input_register] >> 8) & 0xFF
                minutes = input_registers[input_register] & 0xFF
                days = input_registers[input_register + 1]
                value = int((days * 24) + hours + (minutes / 60))
            else:
                value = input_registers[input_register]
            if value not in (32768, 3276.8):
                if input_register not in (26, 28, 30, 35, 36):
                    aliases = get_description(aliases_input_registers, input_register)
                    icon = get_description(icons_input_registers, input_register)
                    description = get_description(description_input_registers, input_register)
                    if aliases is not None:
                        value = aliases.get(str(value))
                    output[get_description(variables_input_registers, input_register)] = {"value": value,
                                                                                          "description": description,
                                                                                          "unit": unit,
                                                                                          "icon": icon}
        return output

    @staticmethod
    def get_holding_registers():
        output = {}
        holding_registers = c.read_holding_registers(0, 45)
        holding_registers_len = len(holding_registers)
        for holding_register in range(holding_registers_len):
            unit = get_description(units_holding_registers, holding_register)
            if unit == "°C" and holding_register != 44:
                value = float(holding_registers[holding_register] / 10)
            else:
                value = holding_registers[holding_register]
            if value not in (32768, 3276.8):
                if holding_register not in range(27, 37):
                    controls = get_description(control_holding_registers, holding_register)
                    aliases = get_description(aliases_holding_registers, holding_register)
                    description = get_description(description_holding_registers, holding_register)
                    icon = get_description(icons_holding_registers, holding_register)
                    if aliases is not None:
                        value = aliases.get(str(value))
                    if aliases is not None and controls is not None:
                        control = replace_options(controls, aliases)
                    else:
                        control = controls
                    output[get_description(variables_holding_registers, holding_register)] = {"value": value,
                                                                                              "description": description,
                                                                                              "unit": unit,
                                                                                              "control": control,
                                                                                              "icon": icon}
        return output

    @staticmethod
    def post_holding_registers(key, value):
        address = get_by_name(variables_holding_registers, key)
        aliases = get_description(aliases_holding_registers, address)
        if aliases is not None:
            value = get_key_from_value(aliases, value)
        c.write_single_register(address, int(value))
        return True

    @staticmethod
    def post_coils(key, value):
        address = get_by_name(variables_coils, key)
        c.write_single_coil(address, bool(value))
        return True
