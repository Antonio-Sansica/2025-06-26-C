from dataclasses import dataclass

@dataclass
class Result:
    resultId: int
    raceId: int
    driverId: int
    constructorId: int
    number: int
    grid:int
    position: int
    positionText: str
    positionOrder: int
    points: int
    laps: int
    time: str
    milliseconds: int
    fastestLap: int
    rank: int
    fastestLapTime: str
    fastestLapSpeed: str
    statusId: int


    def __str__(self):
        return f"{self.resultId}"

    def __eq__(self, other):
        if isinstance(other, Result):
            return self.resultId == other.resultId
        return False

    def __hash__(self):
        return hash(self.resultId)