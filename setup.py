from setuptools import setup, find_namespace_packages
setup(
    name="blauberg-homeassistant",
    version="1.0.0",
    author="Dmitry Nikitin",
    author_email="dima@gracing.pro",
    description="Blauberg Ventilation Integration for Home Assistant",
    packages=find_namespace_packages(),
    setup_requires=[
        'wheel'],
    install_requires=[
        'wheel',
        'paho-mqtt',
        'pyModbusTCP',
        'flask==2.1.3',
        'flask_restx',
        'bjoern',
        'requests',
        'flask-httpauth',
        'flask_cors',
        'flask-compress',
        'werkzeug==2.1.2',
        'pyjwt'
    ]
)
