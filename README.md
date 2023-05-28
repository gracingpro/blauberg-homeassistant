# Blauberg Ventilation Integration for Home Assistant
[![MIT license][license-badge]][license-url]
[![Python][python-badge]][python-url]
[![Docker][docker-badge]][docker-url]

This repository provides an integration service for the Blauberg ventilation system with Home Assistant, specifically designed for the Blauberg Modbus S21 controller. It scrapes the counters from the S21 controller via Modbus, and publishes metrics to MQTT on separate topics, while also publishing configuration profiles for Home Assistant. The service is developed in Python and is suitable for use with Docker.

## Blauberg Series Supported

The following Blauberg Ventilation series are compatible with this service, provided they use the Modbus S21 controller:

- Serie KOMFORT


## Features

- Scrapes counters from the S21 controller via Modbus.
- Publishes metrics to MQTT separate topics, each of them having a predefined description, icon, and measure units.
- Publishes configuration profiles for Home Assistant.
- Enables control of the Blauberg ventilation system through switches and selects in Home Assistant.

The service also provides an API with read-only access to the following data types from the Blauberg ventilation system:

- Alarms
- Coils
- Discrete Inputs
- Input Registers
- Holding Registers

Note: The API does not provide methods to control these data types. It is designed only for retrieving their current state.

## Prerequisites

- Docker

## Installation

Create a directory for the project and create a `config.ini` file inside it:

```bash
mkdir blauberg-homeassistant
cd blauberg-homeassistant
touch config.ini
```

Create a `docker-compose.yml` file inside the directory:

```bash
touch docker-compose.yml
```

Copy the following content into the `docker-compose.yml` file:

```yaml
version: "2"
services:
  blauberg-homeassistant:
    image: gracingpro/blauberg-homeassistant:latest
    container_name: blauberg-homeassistant
    network_mode: bridge
    extra_hosts:
      - "host.docker.internal:host-gateway"
    ports:
      - "8006:8006"
    volumes:
      - ./config.ini:/opt/blauberg/config.ini
    restart: always
```

Copy the following content into the `config.ini` file:

```ini
[Vent]
ip = 192.168.0.251

[MQTT]
user = mqtt_user
topic = Blauberg
homeassistant_topic = homeassistant
password = mqtt_password
host = host.docker.internal
port = 1883
scrape_interval = 15

[Blauberg]
api_token = 123
api_port = 8006
```

Here is a description of each section and the individual properties:

- `[Vent]`
  - `ip`: This is the IP address of the Blauberg ventilation unit.

- `[MQTT]`
  - `user`: The username for authentication with the MQTT broker.
  - `topic`: The main topic under which the service will publish messages.
  - `homeassistant_topic`: The topic that the Home Assistant listens to for the configuration of the Blauberg component.
  - `password`: The password for authentication with the MQTT broker.
  - `host`: The IP address of the MQTT broker.
  - `port`: The port on which the MQTT broker is running.
  - `scrape_interval`: The interval, in seconds, at which the service will scrape data from the Blauberg ventilation unit and publish it to the MQTT broker.

- `[Blauberg]`
  - `api_token`: The API token to authenticate with the Blauberg API.
  - `api_port`: The port on which the Blauberg API is running.

This configuration file is essential for the operation of the service. Without it, the application wouldn't know how to connect to the ventilation unit, the MQTT broker, or the Blauberg API. Always ensure that this file is correctly configured before running the application.

## Usage

To start the service, run the following command:

```bash
docker-compose up -d
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Versioning and Changelog
Blauberg Ventilation Integration for Home Assistant follows semantic versioning. Check out the [Change Log](CHANGELOG.md) for information on the latest updates and improvements.


## Licensing

Blauberg Ventilation Integration for Home Assistant is licensed under [MIT License](https://opensource.org/license/mit/). For more details, see the [License file](LICENSE.md).



[license-url]: LICENSE.md
[license-badge]: https://img.shields.io/github/license/exness/mock-xhr-request.svg
[python-badge]: https://img.shields.io/badge/python-3.11%2B-blue.svg
[python-url]: https://www.python.org/downloads/release/python-3110/
[docker-badge]: https://img.shields.io/badge/docker-20.10.8-blue.svg
[docker-url]: https://www.docker.com/
