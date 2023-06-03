from flask import Flask, jsonify, abort, make_response, flash, request, redirect, url_for, json, send_from_directory
from flask_restx import Api, Resource, fields
from flask_cors import CORS
import bjoern
from multiprocessing import Process
import configparser
from flask_compress import Compress
from Data.MODBUS import ModBus
from Data.Logger import logger


configfile = "config.ini"
config = configparser.ConfigParser()
config.read(configfile)

api_port = int(config["Blauberg"]["api_port"])
api_token = (config["Blauberg"]["api_token"])


authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    },
}

flask_app = Flask(__name__)
Compress(flask_app)
CORS(flask_app)

app = Api(app=flask_app, security='Bearer Auth', authorizations=authorizations)
logger.info("Starting Blauberg Home Assistant API")

alarms_ns = app.namespace('Alarms', description='Alarms APIs')
coils_ns = app.namespace('Coils', description='Coils APIs')
discrete_inputs_ns = app.namespace('DiscreteInputs', description='Discrete Inputs APIs')
input_registers_ns = app.namespace('InputRegisters', description='Input Registers APIs')
holding_registers_ns = app.namespace('HoldingRegisters', description='Holding Registers APIs')


def token_required(f):
    def decorated(*args, **kwargs):
        token = None
        print(request.headers)
        if 'X-API-KEY' in request.headers:
            token = request.headers['X-API-KEY']
        if not token:
            return {'message': 'Token is missing.'}, 401
        if token != api_token:
            return {'message': 'Wrong Token'}, 401
        print('TOKEN: {}'.format(token))
        return f(*args, **kwargs)
    return decorated


@alarms_ns.route("/")
class MainClass(Resource):
    @token_required
    @alarms_ns.doc(security='apikey')
    def get(self):
        alarms = ModBus.get_alarms()
        if len(alarms) == 0:
            abort(404)
        return alarms


@coils_ns.route("/")
class MainClass(Resource):
    @token_required
    @coils_ns.doc(security='apikey')
    def get(self):
        coils = ModBus.get_coils()
        if len(coils) == 0:
            abort(404)
        return coils


@discrete_inputs_ns.route("/")
class MainClass(Resource):
    @token_required
    @discrete_inputs_ns.doc(security='apikey')
    def get(self):
        discrete_inputs = ModBus.get_discrete_inputs()
        if len(discrete_inputs) == 0:
            abort(404)
        return discrete_inputs


@input_registers_ns.route("/")
class MainClass(Resource):
    @token_required
    @input_registers_ns.doc(security='apikey')
    def get(self):
        input_registers = ModBus.get_input_registers()
        if len(input_registers) == 0:
            abort(404)
        return input_registers


@holding_registers_ns.route("/")
class MainClass(Resource):
    @token_required
    @holding_registers_ns.doc(security='apikey')
    def get(self):
        holding_registers = ModBus.get_holding_registers()
        if len(holding_registers) == 0:
            abort(404)
        return holding_registers


if __name__ == '__main__':
    server = Process(target=bjoern.run(flask_app, "0.0.0.0", api_port))
    try:
        server.start()
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        server.terminate()
