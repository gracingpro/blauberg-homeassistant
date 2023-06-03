import paho.mqtt.client as mqtt
import paho.mqtt.publish
import configparser

configfile = "config.ini"
config = configparser.ConfigParser()
config.read(configfile)

mqtt_host = (config["MQTT"]["host"])
mqtt_user = (config["MQTT"]["user"])
mqtt_password = (config["MQTT"]["password"])
mqtt_port = int((config["MQTT"]["port"]))
mqtt_auth = { 'username': mqtt_user, 'password': mqtt_password }


def publish(topic, value):
    try:
        paho.mqtt.publish.single(topic, value, hostname=mqtt_host, port=mqtt_port, auth=mqtt_auth, qos=2)
    except Exception as e:
        return e


def publish_retained(topic, value):
    try:
        paho.mqtt.publish.single(topic, value, hostname=mqtt_host, port=mqtt_port, auth=mqtt_auth, qos=1, retain=True)
    except Exception as e:
        return e


def publish_many(msgs):
    try:
        paho.mqtt.publish.multiple(msgs, hostname=mqtt_host, port=mqtt_port, auth=mqtt_auth)
    except Exception as e:
        return e
