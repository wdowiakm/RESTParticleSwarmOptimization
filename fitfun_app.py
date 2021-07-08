from flask import Flask, request, jsonify
from time import sleep
import requests
import logging
import json
import os
import math

from PsoParticle import PsoParticle

SYS_APP_HOST = os.getenv('SYS_APP_HOST', 'localhost')
SYS_APP_PORT = os.getenv('SYS_APP_PORT', 35200)
PSO_MAIN_URL = os.getenv('PSO_MAIN_URL', 'http://localhost:35100/fitFunRes')

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)

global n
n = 0

@app.route('/')
def state():
    global n
    return f"Hello from simple fitness function calculator. \n I calculated fitness function {n} times"

@app.route('/calcFitFun', methods=['POST'])
def calc_fit_fun():
    particle = PsoParticle(**request.json)
    logging.info(f'Got particle info: {particle.toJson()}')
    x = particle.CurrentPosition[0]
    y = particle.CurrentPosition[1]
    fitFunRes = math.sin(x*20)+math.sin(y*15)-2*math.pow(x-0.45, 2)-2*math.pow(y-0.45, 2)+1.0679

    msg = json.dumps({"ParticleId": particle.ParticleId,
                      "Value": fitFunRes})

    waiting = True
    while waiting:
        try:
            result = requests.post(PSO_MAIN_URL, data=msg, headers={'content-type': 'application/json'})
            waiting = False
        except:
            sleep(1)

    if result.status_code == 200:
        response = jsonify(success=True)
        global n
        n += 1
    else:
        response = jsonify(success=False)
        response.status_code = 500

    return response


if __name__ == '__main__':
    app.run(host=SYS_APP_HOST, port=SYS_APP_PORT)
