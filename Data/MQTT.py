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
    paho.mqtt.publish.single(topic, value, hostname=mqtt_host, port=mqtt_port, auth=mqtt_auth, qos=2)


def publish_retained(topic, value):
    paho.mqtt.publish.single(topic, value, hostname=mqtt_host, port=mqtt_port, auth=mqtt_auth, qos=1, retain=True)


def publish_many(msgs):
    paho.mqtt.publish.multiple(msgs, hostname=mqtt_host, port=mqtt_port, auth=mqtt_auth)
