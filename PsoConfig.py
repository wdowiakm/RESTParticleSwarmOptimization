import sys

Vector = list[float]


class PsoConfig:
    def __init__(self, noVariables: int,
                 noParticle: int = None,
                 maxIteration: int = None,
                 targetedValue: float = sys.float_info.max,
                 fitFunTolerance: float = 1e-6,
                 maxStallIterations: int = 20,
                 weightSelf: float = 1.49,
                 weightSocial: float = 1.49,
                 learningRate: float = 0.1,
                 particleLowerBound: Vector = None,
                 particleUpperBound: Vector = None):

        if noParticle is not None:
            self.NoParticle = noParticle
        else:
            self.NoParticle = min([100, 10*noVariables])

        if maxIteration is not None:
            self.MaxIteration = maxIteration
        else:
            self.MaxIteration = 200*noVariables

        self.NoVariables = noVariables
        self.TargetedValue = targetedValue
        self.FitFunTolerance = fitFunTolerance
        self.MaxStallIterations = maxStallIterations
        self.WeightSelf = weightSelf
        self.WeightSocial = weightSocial
        self.LearningRate = learningRate
        self.ParticleLowerBound = particleLowerBound
        self.ParticleUpperBound = particleUpperBound

