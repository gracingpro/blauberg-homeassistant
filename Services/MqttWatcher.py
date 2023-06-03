import paho.mqtt.client as mqtt
import time
import configparser
from Data.MODBUS import ModBus
from Data.BlaubergMQTT import entity_to_hass
from Data.MQTT import publish_many
import ast
from Data.Logger import logger

configfile = "config.ini"
config = configparser.ConfigParser()
config.read(configfile)

mqtt_host = (config["MQTT"]["host"])
mqtt_user = (config["MQTT"]["user"])
mqtt_password = (config["MQTT"]["password"])
mqtt_port = int((config["MQTT"]["port"]))
mqtt_topic = (config["MQTT"]["topic"])


def on_connect(client, userdata, flags, rc):
    client.subscribe(str(userdata['topic']) + "/+/set")


def on_message(client, userdata, message):
    logger.info("MQTT Watcher: on message")
    logger.info("MQTT Watcher: message received {}".format(str(message.payload.decode("utf-8"))))
    logger.info("MQTT Watcher: message topic={}".format(message.topic))
    logger.info("MQTT Watcher: message qos={}".format(message.qos))
    logger.info("MQTT Watcher: message retain flag={}".format(message.retain))
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
    except Exception as e:
        logger.error("MQTT Watcher: {}".format(e))
        pass


########################################
def instance(gateway):
    logger.info("MQTT Watcher: creating new instance")
    instance_name = 'MqttWatcher-' + gateway['topic']
    client = mqtt.Client(instance_name)  # create new instance
    client.user_data_set(gateway)
    client.username_pw_set(mqtt_user, mqtt_password)
    client.on_message = on_message_try  # attach function to callback
    client.on_connect = on_connect
    client.connect(host=mqtt_host, port=mqtt_port)  # connect to broker
    client.loop_forever()  # start the loop


if __name__ == "__main__":
    processes = []
    while True:
        try:
            instance({'topic': mqtt_topic})
            break
        except Exception as e:
            logger.error("MQTT Watcher: {}".format(e))
            time.sleep(5)
            pass
