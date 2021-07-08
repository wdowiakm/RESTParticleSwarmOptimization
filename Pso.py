import sys
import logging
import threading
from time import sleep


from PsoConfig import PsoConfig
from PsoParticle import PsoParticle
from PsoState import PsoState

Vector = list[float]
PsoPopulation = list[PsoParticle]

log = logging.getLogger("PSO")
log.setLevel(logging.DEBUG)


class Pso:
    def __init__(self, config: PsoConfig):
        self.Config = config
        self.Population = self._initPopulation()
        self.State = PsoState(
            globalBestPosition=self.Population[0].LocalBestPosition,
            globalBestValue=-sys.float_info.max)
        self._loopTask = None
        self._iterationResults = [None] * config.NoParticle

    def _initPopulation(self) -> PsoPopulation:
        population = []
        for n in range(self.Config.NoParticle):
            population.append(PsoParticle.GenerateInitial(
                particleId=n,
                noVariable=self.Config.NoVariables,
                minVal=self.Config.ParticleLowerBound,
                maxVal=self.Config.ParticleUpperBound,
                fitFunUrl=self.Config.FitFunUrl))
        return population

    def Start(self):
        self._loopTask = threading.Thread(target=self._psoLoop, name='pso loop')
        self._loopTask.daemon = True
        self._loopTask.start()

    def SetFitFunRes(self, val: float, n: int):
        self._iterationResults[n] = val

    def _psoLoop(self):
        log.info("Start PSO loop")
        for k in range(self.Config.MaxIteration):
            log.info(f"Iteration {k + 1}/{self.Config.MaxIteration}")
            log.info("Sending fitness function jos requests")
            for p in self.Population:
                p.SendFitFunJobRequest()

            log.info("Waiting for fitness function evaluation")
            while not all(self._iterationResults):
                sleep(0.1)
                log.debug(f"{len([x for x in self._iterationResults if x is not None])}/{self.Config.NoParticle} - "
                          f"fitness function calculated")

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

            if self.State.NoStallIteration > self.Config.MaxStallIterations or \
                    self.State.GlobalBestValue > self.Config.TargetedValue:
                break

            self._iterationResults = [None] * self.Config.NoParticle
            self.State.CurrentIteration += 1
