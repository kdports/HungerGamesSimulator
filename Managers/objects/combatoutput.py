from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Managers.objects.character import Character

'''
Lame dataclass just to keep things obvious
'''
class Result():
    def __init__(self, victim=None, attacker=None, body_part=None) -> None:
        self.victim: Character = victim
        self.attacker: Character = attacker
        self.body_part: str = body_part

'''
This is all essentially a wrapper around info_dict member var
I decided to define the class in order to reduce developer error
'''
class CombatOutput():
    def __init__(self) -> None:
        # Deaths and Injuries are both lists of Result classes
        # Escaped is just a list of characters
        # That's awful. I'm awful.
        # This is actually so fucked, 
        # I just can't be bothered to think of a better way to do this
        self.info_dict = {"Deaths": [],
                          "Injuries": [],
                          "Escaped": []}

    def save(self):
        return self.info_dict
    
    def load(self, info_dict):
        self.info_dict = info_dict

    def add_death(self, victim: Character, attacker: Character):
        result = Result(victim, attacker)
        self.info_dict["Deaths"].append(result)

    def add_injury(self, victim: Character, attacker: Character, body_part: str):
        result = Result(victim, attacker, body_part)
        self.info_dict["Injuries"].append(result)

    def add_escape(self, escapee: Character):
        self.info_dict["Escaped"].append(escapee)