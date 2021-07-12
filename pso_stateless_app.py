import os
import sys
import logging

from flask import Flask, request, jsonify, render_template

from ParticleSwarmStateless import ParticleSwarmStateless
from ParticleSwarmConfig import ParticleSwarmConfig

SYS_APP_HOST = os.getenv('SYS_APP_HOST', 'localhost')
SYS_APP_PORT = os.getenv('SYS_APP_PORT', 35100)

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)


@app.route('/')
def state():
    global pso
    if pso is None:
        return "Particle swarm optimization have not yet stared!"

    currIter = pso.State.CurrentIteration
    maxIter = pso.Config.MaxIteration
    isDone = str(pso.State.IsDone)
    startingTime = str(pso.State.CalculationStartingTime)
    calculationTime = str(pso.State.CalculationDuration if pso.State.CalculationDuration else "-")
    noParticlesDone = len([x for x in pso._iterationResults if x is not None])
    noParticles = pso.Config.NoParticle
    gBestVal = pso.State.GlobalBestValue
    if pso.State.HistGlobalBestValue is not None:
        convX = list(range(0, len(pso.State.HistGlobalBestValue)))
        convY = pso.State.HistGlobalBestValue
    else:
        convX = 0
        convY = 0
    gBestX = pso.State.GlobalBestPosition[0]
    gBestY = pso.State.GlobalBestPosition[1]
    particleX = []
    particleY = []
    for p in pso.Population:
        particleX.append(p.CurrentPosition[0])
        particleY.append(p.CurrentPosition[1])

    return render_template('example2d.html',
                           currIter=currIter, maxIter=maxIter,
                           noParticlesDone=noParticlesDone, noParticles=noParticles,
                           convX=convX, convY=convY,
                           isDone=isDone, startingTime=startingTime, calculationTime=calculationTime,
                           particleX=particleX, particleY=particleY,
                           gBestVal=gBestVal, gBestX=gBestX, gBestY=gBestY)


@app.route('/config', methods=['POST'])
def config():
    global pso
    try:
        psoConfig = ParticleSwarmConfig(**request.json)
        logging.info(f"Received PSO config: {psoConfig.toJson()}")
        if pso is None:
            logging.debug("pso is none")
        else:
            logging.debug("pso is not none")
        return jsonify(success=True)
    except:
        logging.error("Unable to map request json to ParticleSwarmConfig")
        response = jsonify(success=False)
        response.status_code = 400
        return response


@app.route('/psoIteration', methods=['POST'])
def psoIteration():
    global pso
    try:
        pso = ParticleSwarmStateless(**request.json)
        logging.info(f"Received PSO iteration information: {pso.toJson()}")
        return jsonify(success=True)
    except:
        logging.error("Unable to map request json to ParticleSwarmStateless")
        response = jsonify(success=False)
        response.status_code = 400
        return response


@app.route('/fitnessFunctionResult', methods=['POST'])
def fitnessFunctionResult():
    return "ok"


if __name__ == '__main__':
    global pso
    pso = None
    app.run(host=SYS_APP_HOST, port=SYS_APP_PORT)
