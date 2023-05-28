import time
import configparser
from Data.MODBUS import ModBus
from Data.BlaubergMQTT import entity_to_hass
from Data.MQTT import publish_many

configfile = "config.ini"
config = configparser.ConfigParser()
config.read(configfile)


def vent_monitor():
    input_registers = ModBus.get_input_registers()
    alarms = ModBus.get_alarms()
    coils = ModBus.get_coils()
    discrete_inputs = ModBus.get_discrete_inputs()
    holding_registers = ModBus.get_holding_registers()
    out_list = []
    for input_register in input_registers:
        out = entity_to_hass(input_register, input_registers[input_register])
        for x in out:
            out_list.append(x)
    for alarm in alarms:
        out = entity_to_hass(alarm, alarms[alarm])
        for x in out:
            out_list.append(x)
    for coil in coils:
        out = entity_to_hass(coil, coils[coil])
        for x in out:
            out_list.append(x)
    for discrete_input in discrete_inputs:
        out = entity_to_hass(discrete_input, discrete_inputs[discrete_input])
        for x in out:
            out_list.append(x)
    for holding_register in holding_registers:
        out = entity_to_hass(holding_register, holding_registers[holding_register])
        for x in out:
            out_list.append(x)
    publish_many(out_list)
    print('Published {} messages'.format(len(out_list)))


while 1 > 0:
    try:
        vent_monitor()
    except:
        pass
    time.sleep(config.getint("MQTT", "scrape_interval"))
