from flask import Flask, request, jsonify, render_template
import logging
import math

from Pso import Pso
from PsoConfig import PsoConfig
from PsoParticle import PsoParticle
from PsoState import PsoState

# PSO Initialization

logging.basicConfig(level=logging.DEBUG)
# app = Quart(__name__)
app = Flask(__name__)


@app.route('/')
def state():
    currIter = pso.State.CurrentIteration
    maxIter = pso.Config.MaxIteration
    noParticlesDone = len([x for x in pso._iterationResults if x is not None])
    noParticles = pso.Config.NoParticle
    gBestVal = pso.State.GlobalBestValue
    if pso.State.HistGlobalBestValue is not None:
        convX = list(range(1, len(pso.State.HistGlobalBestValue)))
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
                           particleX=particleX, particleY=particleY,
                           gBestVal=gBestVal, gBestX=gBestX, gBestY=gBestY)


@app.route('/FitFunRes', methods=['POST'])
def fit_fun_res():
    particle = PsoParticle(**request.json)
    logging.info(f'Got fitness function result for particle: {particle}')
    x = particle.CurrentPosition[0]
    y = particle.CurrentPosition[1]
    fitFunRes = math.sin(x*20)+math.sin(y*15)-2*math.pow(x-0.45, 2)-2*math.pow(y-0.45, 2)+1.0679

    pso.SetFitFunRes(fitFunRes, particle.ParticleId)

    response = jsonify(success=True)
    return response


if __name__ == '__main__':
    psoConfig = PsoConfig(noVariables=2,
                          noParticle=15,
                          maxIteration=100)
    pso = Pso(psoConfig)
    pso.Start()

    app.run()
