import sys
import json
import logging
import requests
import threading

from time import sleep
from datetime import datetime, timedelta

from .ParticleSwarmConfig import ParticleSwarmConfig
from .ParticleSwarmState import ParticleSwarmState
from .Particle import Particle


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

        self._iterationResults: Vector = [None] * self.Config.NoParticle
        self._loopTask: threading.Thread = None

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

    def StartLoop(self):
        if self.State.CurrentIteration == 0:
            self.State.CalculationStartingTime = datetime.now()
            self._loopTask = threading.Thread(target=self._psoInitialLoop, name='pso loop')
            self._loopTask.daemon = True
            self._loopTask.start()
        else:
            self._loopTask = threading.Thread(target=self._psoLoop, name='pso loop')
            self._loopTask.daemon = True
            self._loopTask.start()

    def SetFitnessFunctionResult(self, val: float, n: int):
        self._iterationResults[n] = val

    def _psoInitialLoop(self):
        self.State.CurrentIteration += 1
        log.info(f"Start PSO iteration {self.State.CurrentIteration}/{self.Config.MaxIteration}")

        log.info("Sending fitness function jos requests")
        for p in self.Population:
            p.SubmitFitnessFunctionJobRequest()

        log.info(f"Sending information for next iteration to {self.Config.PsoMainUrl}")
        self._sendRequestForNextIteration()

    def _psoLoop(self):
        self.State.CurrentIteration += 1
        log.info(f"Start PSO iteration {self.State.CurrentIteration}/{self.Config.MaxIteration}")

        log.info("Updating global solution")
        iterMaxVal = max(self._iterationResults)
        if iterMaxVal > self.State.GlobalBestValue:
            iterMaxIdx = self._iterationResults.index(iterMaxVal)
            deltaGlobalBest = abs(self.State.GlobalBestValue - iterMaxVal)
            self.State.GlobalBestValue = iterMaxVal
            self.State.GlobalBestPosition = self.Population[iterMaxIdx].CurrentPosition
            if deltaGlobalBest > self.Config.FitFunTolerance:
                self.State.NoStallIteration = 0
            else:
                self.State.NoStallIteration += 1
        else:
            self.State.NoStallIteration += 1

        self.State.HistGlobalBestValue.append(self.State.GlobalBestValue)

        log.info("Updating particle solution, position, velocity")
        n = 0
        for p in self.Population:
            # Updating particle best solution
            if self._iterationResults[n] is not None and self._iterationResults[n] > p.LocalBestValue:
                p.LocalBestValue = self._iterationResults[n]
                p.LocalBestPosition = p.CurrentPosition

            # Updating particle velocity
            p.UpdateVelocity(self.Config.WeightInertia,
                             self.Config.WeightSelf,
                             self.Config.WeightSocial,
                             self.State.GlobalBestPosition)
            # Updating particle position
            p.UpdatePosition(self.Config.ParticleLowerBound,
                             self.Config.ParticleUpperBound,
                             self.Config.LearningRate)
            n += 1

        self._iterationResults = [None] * self.Config.NoParticle

        log.info("PSO loop finished")
        if self.State.NoStallIteration > self.Config.MaxStallIterations or \
                self.State.GlobalBestValue > self.Config.TargetedValue or \
                self.State.CurrentIteration >= self.Config.MaxIteration:
            self.State.IsDone = True
            self.State.CalculationDuration = datetime.now() - self.State.CalculationStartingTime
        else:
            log.info(f"Sending information for next iteration to {self.Config.PsoMainUrl}")
            self._sendRequestForNextIteration()
            log.info("Sending fitness function jos requests")
            for p in self.Population:
                p.SubmitFitnessFunctionJobRequest()

    def _sendRequestForNextIteration(self):
        noRetries = 0
        waiting = True
        while waiting:
            try:
                requests.post(self.Config.PsoMainUrl, data=self.toJson(), headers={'content-type': 'application/json'})
                waiting = False
            except:
                noRetries += 1
                if noRetries > 100:
                    # If that happens whole algorithm will hangs (next PSO loop will not start)
                    raise Exception(f"Cannot start next iteration via endpoint {self.Config.PsoMainUrl}")
                logging.error(f"Cannot start next iteration via endpoint {self.Config.PsoMainUrl} - retry... ({noRetries})")
                sleep(1)

    def toJson(self, indent: int = None):
        conversionCopy = self.__dict__.copy()
        conversionCopy.pop('_loopTask')
        conversionCopy.pop('_iterationResults')
        if indent is None:
            return json.dumps(conversionCopy, default=lambda o: o.__dict__ if not isinstance(o, datetime) else o.isoformat())
        return json.dumps(conversionCopy, default=lambda o: o.__dict__, indent=indent)

    def __repr__(self):
        return self.toJson()

    @property
    def NoFitnessFunctionJobDone(self):
        return len([x for x in self._iterationResults if x is not None])


if __name__ == '__main__':
    psoConfig = ParticleSwarmConfig(3)
    pso = ParticleSwarmStateless(psoConfig)
    pso.State.CalculationStartingTime = datetime.now()
    print(pso.toJson(indent=3))
