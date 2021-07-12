import sys
import json
import logging
import threading
from time import sleep
from datetime import datetime, timedelta

from ParticleSwarmConfig import ParticleSwarmConfig
from ParticleSwarmState import ParticleSwarmState
from Particle import Particle


Vector = list[float]
ListDict = list[dict]
SwarmPopulation = list[Particle]

log = logging.getLogger("ParticleSwarm")
log.setLevel(logging.DEBUG)


class ParticleSwarmStateless:
    def __init__(self,
                 Config: ParticleSwarmConfig,
                 Population: SwarmPopulation = None,
                 State: ParticleSwarmState = None):

        if isinstance(Config, dict):
            self.Config = ParticleSwarmConfig(**Config)
        else:
            self.Config = Config

        if Population is None:
            self.Population = self._initPopulation()
        elif all(isinstance(x, dict) for x in Population):
            self.Population = []
            for particle in Population:
                self.Population.append(Particle(**particle))
        else:
            self.Population = Population

        if State is None:
            self.State = ParticleSwarmState(
                GlobalBestPosition=self.Population[0].LocalBestPosition,
                GlobalBestValue=-sys.float_info.max)
        elif isinstance(State, dict):
            self.State = ParticleSwarmState(**State)
        else:
            self.State = State

        self._iterationResults = [None] * self.Config.NoParticle

    def _initPopulation(self) -> SwarmPopulation:
        population = []
        for n in range(self.Config.NoParticle):
            population.append(Particle.GenerateInitial(
                particleId=n,
                noVariable=self.Config.NoVariables,
                minVal=self.Config.ParticleLowerBound,
                maxVal=self.Config.ParticleUpperBound,
                fitFunUrl=self.Config.FitFunUrl))
        return population

    def Start(self):
        pass

    def SetFitFunRes(self, val: float, n: int):
        pass

    def _psoLoop(self):
        pass

    def toJson(self, indent: int = None):
        if indent is None:
            return json.dumps(self.__dict__, default=lambda o: o.__dict__)
        return json.dumps(self.__dict__, default=lambda o: o.__dict__, indent=indent)

    def __repr__(self):
        return self.toJson()


if __name__ == '__main__':
    psoConfig = ParticleSwarmConfig(3)
    pso = ParticleSwarmStateless(psoConfig)
    print(pso.toJson(indent=3))
