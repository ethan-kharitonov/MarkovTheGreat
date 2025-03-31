from dataclasses import dataclass
from typing import List


@dataclass
class State:
    health_vector: List[str]
    location_vector: List[int]

    def is_disease_free(self):
        return all(health != 'I' for health in self.health_vector)




