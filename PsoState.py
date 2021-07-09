from datetime import datetime, timedelta

Vector = list[float]


class PsoState:
    def __init__(self, GlobalBestPosition: Vector,
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
        if HistGlobalBestValue is not None:
            self.HistGlobalBestValue = HistGlobalBestValue
        else:
            self.HistGlobalBestValue = []
        self.CalculationStartingTime = CalculationStartingTime
        self.CalculationDuration = CalculationDuration
        self.IsDone = IsDone
