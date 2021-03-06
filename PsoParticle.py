import logging
import sys
import random
import requests
import json
from time import sleep

Vector = list[float]


class PsoParticle:
    def __init__(self,
                 ParticleId: int,
                 CurrentPosition: Vector = None,
                 CurrentVelocity: Vector = None,
                 LocalBestPosition: Vector = None,
                 LocalBestValue: float = None,
                 FitFunUrl: str = ""):

        self.ParticleId = ParticleId
        self.CurrentPosition = CurrentPosition
        self.CurrentVelocity = CurrentVelocity
        self.LocalBestPosition = LocalBestPosition
        self.LocalBestValue = LocalBestValue
        self.FitFunUrl = FitFunUrl

    def SendFitFunJobRequest(self):
        noRetries = 0
        waiting = True
        while waiting:
            try:
                result = requests.post(self.FitFunUrl, data=self.toJson(), headers={'content-type': 'application/json'})
                waiting = False
            except:
                if noRetries > 100:
                    raise Exception(f"Cannot reach fitness function app {self.FitFunUrl}")
                logging.error(f"Cannot reach fitness function app {self.FitFunUrl} - retry... ({noRetries})")
                sleep(1)

    def UpdateVelocity(self, weightInertia, weightSelf, weightSocial, globalBestPosition):
        noVariables = len(self.CurrentPosition)
        vInertia = [0] * noVariables
        vPersonal = [0] * noVariables
        vSocial = [0] * noVariables
        v = [0] * noVariables
        for k in range(noVariables):
            vInertia[k] = weightInertia * self.CurrentVelocity[k]
            vPersonal[k] = weightSelf * random.uniform(0, 2) * (self.LocalBestPosition[k] - self.CurrentPosition[k])
            vSocial[k] = weightSocial * random.uniform(0, 2) * (globalBestPosition[k] - self.CurrentPosition[k])
            v[k] = vInertia[k] + vPersonal[k] + vSocial[k]
        self.CurrentVelocity = v

    def UpdatePosition(self, particleLowerBound, particleUpperBound, learningRate):
        isUniformLowerBound = len(particleLowerBound) == 1
        isUniformUpperBound = len(particleUpperBound) == 1
        noVariables = len(self.CurrentPosition)
        newPos = [0] * noVariables
        for k in range(noVariables):
            x = self.CurrentPosition[k] + learningRate * self.CurrentVelocity[k]

            if isUniformLowerBound:
                if x < particleLowerBound[0]:
                    x = particleLowerBound[0]
            else:
                if x < particleLowerBound[k]:
                    x = particleLowerBound[k]

            if isUniformUpperBound:
                if x > particleUpperBound[0]:
                    x = particleUpperBound[0]
            else:
                if x > particleUpperBound[k]:
                    x = particleUpperBound[k]

            newPos[k] = x
        self.CurrentPosition = newPos

    def toJson(self):
        return json.dumps(self.__dict__, default=lambda o: o.__dict__)

    @classmethod
    def GenerateInitial(cls, particleId, noVariable: int, minVal: Vector, maxVal: Vector, fitFunUrl: str) -> 'PsoParticle':
        x = []
        v = []

        if len(minVal) == 1:
            for k in range(noVariable):
                x.append(random.uniform(minVal[0], maxVal[0]))
                v.append(random.uniform(minVal[0], maxVal[0])*0.1)

        else:
            for k in range(noVariable):
                x.append(random.uniform(minVal[k], maxVal[k]))
                v.append(random.uniform(minVal[k], maxVal[k])*0.1)

        return PsoParticle(particleId, x, v, x, -sys.float_info.max, fitFunUrl)
