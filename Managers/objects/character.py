from enum import Enum
import json

class LimbHealthState(Enum):
    HEALTHY = 0
    INJURED = 1
    DISABLED = 2

class HungerState(Enum):
    FULL = 0,
    HUNGRY = 1,
    MALNOURISHED = 2,
    STARVING = 3,
    DEAD = 4

class Character:
    def __init__(self) -> None:
        self.nid = ""
        self.name = ""
        self.skills = {}
        self.alliances = []
        self.strategies = {}

        self.dead = False

        self.reset_body()

        self.weapons = []
        self.medicine = []
        self.food = []

        self.position = None

        self.hunger_state = HungerState.FULL

    def reset_body(self):
        self.body = {
            "head": LimbHealthState.HEALTHY,
            "torso": LimbHealthState.HEALTHY,
            "left arm": LimbHealthState.HEALTHY,
            "right arm": LimbHealthState.HEALTHY,
            "legs": LimbHealthState.HEALTHY
        }

    def get_skill(self, skill_name):
        return self.skills.get(skill_name, 0)

    def get_strategy(self, strategy_name):
        return self.strategies.get(strategy_name, 0)
    
    def get_alliances(self):
        return self.alliances
    
    def increment_hunger_state(self):
        # Will wrap around if increments off last value - should be handled in the game manager though
        self.hunger_state = (self.hunger_state.value + 1) % len(HungerState)

    def load_json_file(self, file_name):
        with open(file_name, 'r') as openfile:
            character_json = json.load(openfile)
            self.load_json_object(character_json)
            
    def load_json_object(self, json_obj):
        self.nid = json_obj["nid"]
        self.name = json_obj["name"]
        self.position = json_obj.get("position", None)
        self.skills = json_obj.get("skills", {})
        self.alliances = json_obj.get("alliances", [])
        self.strategies = json_obj.get("strategies", {})

    def save(self):
        save_dict = {
            "nid": self.nid,
            "name": self.name,
            "position": self.position,
            "skills": self.skills,
            "alliances": self.alliances,
            "strategies": self.strategies
        }
        return save_dict
    
    # TODO - Factor in items/injuries
    def combat_bonus(self):
        return 0