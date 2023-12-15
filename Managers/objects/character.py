from enum import Enum
import json

from Managers.objects.item import Item
from Managers.objects.skills import Skill
from Managers.objects.strategies import Strategy

'''
Currently Implemented Strategies:
Friendly
Trustworthy
Aggressive
Commanding
'''

'''
Currently Implemented Skills:
Combat Skill
Medical Skill
Survival Skill
Endurance Skill
'''

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

        self.left_hand_weapon: Item = None
        self.right_hand_weapon: Item = None

    def reset_body(self):
        self.body = {
            "head": LimbHealthState.HEALTHY,
            "torso": LimbHealthState.HEALTHY,
            "left arm": LimbHealthState.HEALTHY,
            "right arm": LimbHealthState.HEALTHY,
            "legs": LimbHealthState.HEALTHY
        }

    def get_skill(self, skill: Skill):
        return self.skills.get(skill.value, 0)

    def get_strategy(self, strategy: Strategy):
        return self.strategies.get(strategy.value, 0)
    
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
    
    '''
    Outta get called whenever someone gets an item
    '''
    def equip_item(self, item: Item):
        if not self.left_hand_weapon or self.left_hand_weapon.get_combat_modifier() < item.get_combat_modifier():
            self.left_hand_weapon = item
            return
        if not self.right_hand_weapon or self.right_hand_weapon.get_combat_modifier() < item.get_combat_modifier():
            self.right_hand_weapon = item
            return
    
    def combat_bonus(self):
        combat_skill = self.skills.get(Skill.CombatSkill, 0)
        combat_skill += self.left_hand_weapon.get_combat_modifier()
        combat_skill += self.right_hand_weapon.get_combat_modifier()
        combat_skill *= self.injury_multiplier()
        return combat_skill
    
    def injury_multiplier_inverter(self, limb_state: LimbHealthState):
        INJURED_EFFECT = 0.66
        DISABLED_EFFECT = 0.33
        if limb_state == LimbHealthState.HEALTHY:
            return 1
        elif limb_state == LimbHealthState.INJURED:
            return INJURED_EFFECT
        return DISABLED_EFFECT
    
    def hunger_combat_multiplier(self, hunger_state: HungerState):
        MULTIPLIER = 1/3
        return max(1 - (max(self.endurance_hunger_effect(hunger_state) - 1, 0) * MULTIPLIER), 0)
    
    def endurance_hunger_effect(self, hunger_state: HungerState) -> HungerState:
        return max(0, hunger_state - self.get_skill(Skill.EnduranceSkill))

    '''
    Injuries decrease
    Hunger decreases
    '''
    def injury_multiplier(self):
        multiplier = 1
        for limb in self.body:
            multiplier *= self.injury_multiplier_inverter(limb)
        multiplier *= self.hunger_combat_multiplier(self.hunger_state)
        return multiplier
        