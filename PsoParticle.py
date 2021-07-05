import sys
import random

Vector = list[float]


class PsoParticle():
    def __init__(self,
                 currentPosition: Vector = None,
                 currentVelocity: Vector = None,
                 localBestPosition: Vector = None,
                 localBestValue: float = None):

        self.CurrentPosition = currentPosition
        self.CurrentVelocity = currentVelocity
        self.LocalBestPosition = localBestPosition
        self.LocalBestValue = localBestValue

    @classmethod
    def GenerateInitial(cls, noVariable: int, minVal: Vector, maxVal: Vector) -> 'PsoParticle':
        x = []
        v = []

        if len(minVal) == 1:
            for k in range(noVariable):
                x.append(random.uniform(minVal[0], maxVal[0]))
                v.append(random.uniform(minVal[0], maxVal[0]))

        else:
            for k in range(noVariable):
                x.append(random.uniform(minVal[k], maxVal[k]))
                v.append(random.uniform(minVal[0], maxVal[0]))

        return PsoParticle(x, v, x, -sys.float_info.max)
