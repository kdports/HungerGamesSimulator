
from enum import Enum
from utilities import static_random

class LimbHealthState(Enum):
    HEALTHY = 0
    INJURED = 1
    DISABLED = 2

class Body:
    def __init__(self) -> None:
        self.body_dict = {
            "head": LimbHealthState.HEALTHY.value,
            "torso": LimbHealthState.HEALTHY.value,
            "left arm": LimbHealthState.HEALTHY.value,
            "right arm": LimbHealthState.HEALTHY.value,
            "legs": LimbHealthState.HEALTHY.value
        }
        self.body_parts = ["head", "torso", "left arm", "right arm", "legs"]

    def get_random_part(self):
        return self.body_parts[static_random.get_randint(0, len(self.body_parts) - 1)]
    
    def parts(self):
        return self.body_dict

