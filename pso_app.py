import sys

from flask import Flask, request, jsonify, render_template
import os
import logging

from Pso import Pso
from PsoConfig import PsoConfig

SYS_APP_HOST = os.getenv('SYS_APP_HOST', 'localhost')
SYS_APP_PORT = os.getenv('SYS_APP_PORT', 35100)
FITFUN_URL = os.getenv('FITFUN_URL', 'http://localhost:35200/calcFitFun')
NOVARIABLES = os.getenv('NOVARIABLES', 2)
NOPARTICLE = os.getenv('NOPARTICLE', 25)
MAXITERATION = os.getenv('MAXITERATION', 50)
TARGETEDVALUE = os.getenv('TARGETEDVALUE', sys.float_info.max)
FITFUNTOLERANCE = os.getenv('FITFUNTOLERANCE', 1e-6)
MAXSTALLITERATIONS = os.getenv('MAXSTALLITERATIONS', 20)
WEIGHTSELF = os.getenv('WEIGHTSELF', 1.49)
WEIGHTSOCIAL = os.getenv('WEIGHTSOCIAL', 1.49)
WEIGHTINERTIA = os.getenv('WEIGHTINERTIA', 0.99)
LEARNINGRATE = os.getenv('LEARNINGRATE', 0.1)
PARTICLELOWERBOUND = os.getenv('PARTICLELOWERBOUND', [0])
PARTICLEUPPERBOUND = os.getenv('PARTICLEUPPERBOUND', [1])

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)


@app.route('/')
def state():
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


@app.route('/fitFunRes', methods=['POST'])
def fit_fun_res():
    particleId = request.json["ParticleId"]
    fitFunRes = request.json["Value"]

    pso.SetFitFunRes(fitFunRes, particleId)

    response = jsonify(success=True)
    return response


if __name__ == '__main__':
    # PSO Initialization
    psoConfig = PsoConfig(noVariables=int(NOVARIABLES),
                          noParticle=int(NOPARTICLE),
                          maxIteration=int(MAXITERATION),
                          targetedValue=float(TARGETEDVALUE),
                          fitFunTolerance=float(FITFUNTOLERANCE),
                          maxStallIterations=int(MAXSTALLITERATIONS),
                          weightSelf=float(WEIGHTSELF),
                          weightSocial=float(WEIGHTSOCIAL),
                          weightInertia=float(WEIGHTINERTIA),
                          learningRate=float(LEARNINGRATE),
                          particleLowerBound=PARTICLELOWERBOUND,
                          particleUpperBound=PARTICLEUPPERBOUND,
                          fitFunUrl=FITFUN_URL)
    pso = Pso(psoConfig)
    pso.Start()

    # Start Flask app
    app.run(host=SYS_APP_HOST, port=SYS_APP_PORT)
