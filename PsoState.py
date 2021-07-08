Vector = list[float]


class PsoState:
    def __init__(self, globalBestPosition: Vector,
                 globalBestValue: float,
                 currentIteration: int = 1,
                 noStallIteration: int = 0,
                 histGlobalBestValue: Vector = None):

        self.GlobalBestPosition = globalBestPosition
        self.GlobalBestValue = globalBestValue
        self.CurrentIteration = currentIteration
        self.NoStallIteration = noStallIteration
        if histGlobalBestValue is not None:
            self.HistGlobalBestValue = histGlobalBestValue
        else:
            self.HistGlobalBestValue = []
