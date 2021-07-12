import sys
import json

Vector = list[float]


class ParticleSwarmConfig:
    def __init__(self,
                 NoVariables: int,
                 NoParticle: int = None,
                 MaxIteration: int = None,
                 TargetedValue: float = sys.float_info.max,
                 FitFunTolerance: float = 1e-6,
                 MaxStallIterations: int = 20,
                 WeightSelf: float = 1.49,
                 WeightSocial: float = 1.49,
                 WeightInertia: float = 0.99,
                 LearningRate: float = 0.1,
                 ParticleLowerBound: Vector = None,
                 ParticleUpperBound: Vector = None,
                 FitFunUrl: str = "",
                 PsoMainUrl: str = ""):

        if NoParticle is not None:
            self.NoParticle = NoParticle
        else:
            self.NoParticle = min([100, 10*NoVariables])

        if MaxIteration is not None:
            self.MaxIteration = MaxIteration
        else:
            self.MaxIteration = 200*NoVariables

        self.NoVariables = NoVariables
        self.TargetedValue = TargetedValue
        self.FitFunTolerance = FitFunTolerance
        self.MaxStallIterations = MaxStallIterations
        self.WeightSelf = WeightSelf
        self.WeightSocial = WeightSocial
        self.WeightInertia = WeightInertia
        self.LearningRate = LearningRate

        if ParticleLowerBound is not None:
            self.ParticleLowerBound = ParticleLowerBound
        else:
            self.ParticleLowerBound = [0]

        if ParticleUpperBound is not None:
            self.ParticleUpperBound = ParticleUpperBound
        else:
            self.ParticleUpperBound = [1]

        self.FitFunUrl = FitFunUrl
        self.PsoMainUrl = PsoMainUrl

    def toJson(self, indent: int = None):
        if indent is None:
            return json.dumps(self.__dict__, default=lambda o: o.__dict__)
        return json.dumps(self.__dict__, default=lambda o: o.__dict__, indent=indent)

    def __repr__(self):
        return self.toJson()


if __name__ == '__main__':
    psoConfig = ParticleSwarmConfig(3)
    print(psoConfig.toJson(indent=3))
