import sys

from PsoConfig import PsoConfig
from PsoParticle import PsoParticle
from PsoState import PsoState

Vector = list[float]
PsoPopulation = list[PsoParticle]


class Pso:
    def __init__(self, config: PsoConfig):
        self.Config = config
        self.Population = self._initPopulation()
        self.State = PsoState(
            globalBestPosition=self.Population[0].LocalBestPosition,
            globalBestValue=-sys.float_info.max)

    def _initPopulation(self) -> PsoPopulation:
        population = []
        for n in range(self.Config.NoParticle):
            population.append(PsoParticle.GenerateInitial(
                noVariable=self.Config.NoVariables,
                minVal=self.Config.ParticleLowerBound,
                maxVal=self.Config.ParticleUpperBound))
        return population

    def Start(self):
        for k in range(self.Config.MaxIteration):
            # do stuff
            if self.State.NoStallIteration > self.Config.MaxStallIterations or \
                    self.State.GlobalBestValue > self.Config.TargetedValue:
                break


if __name__ == "__main__":
    # PSO Initialization
    psoConfig = PsoConfig(15)
    pso = Pso(psoConfig)
    pso.Start()
