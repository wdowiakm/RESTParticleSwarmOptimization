import json
from typing import Union
from datetime import datetime, timedelta

Vector = list[float]


class ParticleSwarmState:
    def __init__(self,
                 GlobalBestPosition: Vector,
                 GlobalBestValue: float,
                 CurrentIteration: int = 0,
                 NoStallIteration: int = 0,
                 HistGlobalBestValue: Vector = None,
                 IsDone: bool = False,
                 CalculationStartingTime: Union[str, datetime] = None,
                 CalculationDuration: Union[str, timedelta] = None):

        self.GlobalBestPosition = GlobalBestPosition
        self.GlobalBestValue = GlobalBestValue
        self.CurrentIteration = CurrentIteration
        self.NoStallIteration = NoStallIteration

        if HistGlobalBestValue is None:
            self.HistGlobalBestValue = []
        else:
            self.HistGlobalBestValue = HistGlobalBestValue

        if CalculationStartingTime is not None:
            if isinstance(CalculationStartingTime, str):
                self.CalculationStartingTime = datetime.fromisoformat(CalculationStartingTime)
            elif isinstance(CalculationStartingTime, datetime):
                self.CalculationStartingTime = CalculationStartingTime
        else:
            self.CalculationStartingTime = CalculationStartingTime

        if CalculationDuration is not None:
            if isinstance(CalculationDuration, str):
                t = datetime.strptime(CalculationDuration, "%H:%M:%S")
                self.CalculationDuration = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
            elif isinstance(CalculationDuration, timedelta):
                self.CalculationDuration = CalculationDuration
        else:
            self.CalculationDuration = CalculationDuration

        self.IsDone = IsDone

    def toJson(self, indent: int = None):
        conversionCopy = self.__dict__.copy()
        conversionCopy["CalculationStartingTime"] = self.CalculationStartingTime.isoformat()
        if self.CalculationDuration is not None:
            conversionCopy["CalculationDuration"] = str(self.CalculationDuration)
        if indent is None:
            return json.dumps(conversionCopy, default=lambda o: o.__dict__)
        return json.dumps(conversionCopy, default=lambda o: o.__dict__, indent=indent)

    def __repr__(self):
        return self.toJson()


if __name__ == '__main__':
    psoState = ParticleSwarmState(GlobalBestPosition=[0, 1, 2],
                                  GlobalBestValue=1.23,
                                  CalculationStartingTime=datetime.now().isoformat(),
                                  CalculationDuration=timedelta(hours=2))

    print(psoState.toJson(indent=3))
