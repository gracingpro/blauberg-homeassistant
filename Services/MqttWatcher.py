import paho.mqtt.client as mqtt
import time
import json
import configparser
from Data.MODBUS import ModBus
from Data.BlaubergMQTT import entity_to_hass
from Data.MQTT import publish_many
import ast

configfile = "config.ini"
config = configparser.ConfigParser()
config.read(configfile)

mqtt_host = (config["MQTT"]["host"])
mqtt_user = (config["MQTT"]["user"])
mqtt_password = (config["MQTT"]["password"])
mqtt_port = int((config["MQTT"]["port"]))
mqtt_topic = (config["MQTT"]["topic"])


def on_connect(client, userdata, flags, rc):
    print("on connect")
    print(userdata['topic'])
    client.subscribe(str(userdata['topic']) + "/+/set")


def on_message(client, userdata, message):
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    print("message qos=", message.qos)
    print("message retain flag=", message.retain)
    topic = message.topic
    key = topic.split("/")[1]
    value = str(message.payload.decode("utf-8"))
    if key[0:2] == "CL":
        ModBus.post_coils(key, ast.literal_eval(value))
        coils = ModBus.get_coils()
        message = entity_to_hass(key, coils[key])
        publish_many(message)
    elif key[0:2] == "HR":
        try:
            value = int(value)
        except:
            value = str(value)
        ModBus.post_holding_registers(key, value)
        holding_registers = ModBus.get_holding_registers()
        message = entity_to_hass(key, holding_registers[key])
        publish_many(message)


def on_message_try(client, userdata, message):
    try:
        on_message(client, userdata, message)
    except:
        pass


########################################
def instance(gateway):
    print("creating new instance")
    instance_name = 'MqttWatcher-' + gateway['topic']
    client = mqtt.Client(instance_name)  # create new instance
    client.user_data_set(gateway)
    client.username_pw_set(mqtt_user, mqtt_password)
    client.on_message = on_message_try  # attach function to callback
    client.on_connect = on_connect
    print("connecting to broker")
    client.connect(host=mqtt_host, port=mqtt_port)  # connect to broker
    client.loop_forever()  # start the loop


if __name__ == "__main__":
    processes = []
    instance({'topic': mqtt_topic})
