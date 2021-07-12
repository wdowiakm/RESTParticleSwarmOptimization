import json
from datetime import datetime, timedelta

Vector = list[float]


class ParticleSwarmState:
    def __init__(self,
                 GlobalBestPosition: Vector,
                 GlobalBestValue: float,
                 CurrentIteration: int = 1,
                 NoStallIteration: int = 0,
                 HistGlobalBestValue: Vector = None,
                 IsDone: bool = False,
                 CalculationStartingTime: datetime = None,
                 CalculationDuration: timedelta = None):

        self.GlobalBestPosition = GlobalBestPosition
        self.GlobalBestValue = GlobalBestValue
        self.CurrentIteration = CurrentIteration
        self.NoStallIteration = NoStallIteration

        if HistGlobalBestValue is None:
            self.HistGlobalBestValue = []
        else:
            self.HistGlobalBestValue = HistGlobalBestValue

        self.CalculationStartingTime = CalculationStartingTime
        self.CalculationDuration = CalculationDuration
        self.IsDone = IsDone

    def toJson(self, indent: int = None):
        if indent is None:
            return json.dumps(self.__dict__, default=lambda o: o.__dict__)
        return json.dumps(self.__dict__, default=lambda o: o.__dict__, indent=indent)

    def __repr__(self):
        return self.toJson()
