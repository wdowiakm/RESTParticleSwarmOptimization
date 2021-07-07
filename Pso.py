import sys
import random
import logging
# import asyncio
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
                noVariable=self.Config.NoVariables,
                minVal=self.Config.ParticleLowerBound,
                maxVal=self.Config.ParticleUpperBound))
        return population

    def Start(self):
        # self._loopTask = asyncio.get_event_loop().create_task(self._psoLoop())
        self._loopTask = threading.Thread(target=self._psoLoop, name='pso loop')
        self._loopTask.daemon = True
        self._loopTask.start()

    def _psoLoop(self):
        log.info("Start PSO loop")
        for k in range(self.Config.MaxIteration):
            log.info(f"Iteration {k + 1}/{self.Config.MaxIteration}")
            log.info(f"Sending fitness function jos requests")
            for p in self.Population:
                p.SendFitFunJobRequest()

            log.info(f"Waiting for fitness function evaluation")
            while not all(self._iterationResults):
                # await asyncio.sleep(1000)
                sleep(1)
                log.debug(f"{len([x for x in self._iterationResults if x is not None])}/{self.Config.NoParticle} - "
                          f"fitness function calculated")
            self._iterationResults = [None] * self.Config.NoParticle
            self.State.CurrentIteration += 1
            self.State.GlobalBestValue = "awesome"
            log.debug("loop done")

    def _generateRandomVector(self, length, minVal, maxVal):
        r = []
        for k in range(length):
            r.append(random.uniform(minVal, maxVal))
        return r





    # def NextIter(self):
    #     if self.State.NoStallIteration > self.Config.MaxStallIterations or \
    #             self.State.GlobalBestValue > self.Config.TargetedValue:
    #         pass
    #     else:
    #         print(f"Calculate iteration n = {self.State.CurrentIteration} / {self.Config.MaxIteration}")
    #         self.State.CurrentIteration += 1
    #         self.NextIter()


if __name__ == "__main__":
    # PSO Initialization
    psoConfig = PsoConfig(15)
    pso = Pso(psoConfig)
    pso.Start()
