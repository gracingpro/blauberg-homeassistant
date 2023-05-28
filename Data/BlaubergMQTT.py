import json
import configparser


configfile = "config.ini"
config = configparser.ConfigParser()
config.read(configfile)

mqtt_topic = config["MQTT"]["topic"]
homeassistant_topic = config["MQTT"]["homeassistant_topic"]

node_id = mqtt_topic

device = {
        "identifiers": [node_id],
        "name": "Blauberg",
        "model": "Blauberg",
        "manufacturer": "Blauberg"
    }


def entity_to_hass(entity, payload):
    output = []
    config_js = {}
    topic_sensor = f"{homeassistant_topic}/sensor/{node_id}/{entity}/config"
    topic_switch = f"{homeassistant_topic}/switch/{node_id}/{entity}/config"
    topic_select = f"{homeassistant_topic}/select/{node_id}/{entity}/config"
    topic_state = f"{node_id}/{entity}/state"
    config_template = {
        "name": entity,
        "enabled_by_default": True,
        "unique_id": f"{node_id}_{entity}",
        "state_topic": topic_state,
        "json_attributes_topic": topic_state,
        "value_template": "{{ value_json.value }}",
        "device": device
    }
    if 'unit' in payload and payload["unit"] is not None:
        config_template["unit_of_measurement"] = payload["unit"]
    if 'icon' in payload and payload["icon"] is not None:
        config_template["icon"] = payload["icon"]
    if 'control' in payload and payload["control"] is not None:
        config_template["command_topic"] = f"{node_id}/{entity}/set"
        for key in payload["control"]:
            config_template[key] = payload["control"][key]
        if "payload_on" in config_template:
            config_js = {'topic': topic_switch, 'payload': json.dumps(config_template), 'qos': 1, 'retain': True}
        elif "options" in config_template:
            config_js = {'topic': topic_select, 'payload': json.dumps(config_template), 'qos': 1, 'retain': True}
    else:
        config_js = {'topic': topic_sensor, 'payload': json.dumps(config_template), 'qos': 1, 'retain': True}
    message = {'topic': topic_state, 'payload': json.dumps(payload), 'qos': 1, 'retain': False}
    output.append(config_js)
    output.append(message)
    return output
