from flask import Flask, request, render_template
import logging

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
    xData = [1, 2, 3, 4]
    yData = [1, 2, 1, 3]
    return render_template('example2d.html', xData=xData, yData=yData)


@app.route('/FitFunRes')
def fit_fun_res():
    particle = int(request.args.get('particle'))
    pso._iterationResults[particle] = particle+1
    msg = f"""
    <HTML>
    <HEAD>
        <title>PSO</title>
    </HEAD>
    <BODY>
        <p>Loop state:</p>
        <p>{pso._loopTask.is_alive()}</p>
        <p>Iteration state</p>
        <p>{pso._iterationResults}</p>
        <p>PSO current iter</p>
        <p>{pso.State.CurrentIteration}</p>
        <p>PSO Global best</p>
        <p>{pso.State.GlobalBestValue}</p>
    </BODY>
    <HTML>
    """
    return msg


if __name__ == '__main__':
    psoConfig = PsoConfig(noVariables=15,
                          noParticle=2,
                          maxIteration=3)
    pso = Pso(psoConfig)
    pso.Start()

    app.run()
