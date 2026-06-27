from dataclasses import dataclass

# Creiamo il piccolo oggetto chiesto dal prof per i risultati
@dataclass
class Piazzamento:
    raceId: int
    driverId: int
    position: int

@dataclass
class Constructor:
    constructorId: int
    name: str
    nationality: str
    url: str

    # Questo si esegue in automatico quando crei l'oggetto. Nessun import al DAO!
    def __post_init__(self):
        self.risultati_per_anno = {}

    def __str__(self):
        return f"{self.name}"

    def __eq__(self, other):
        if isinstance(other, Constructor):
            return self.constructorId == other.constructorId
        return False

    def __hash__(self):
        return hash(self.constructorId)