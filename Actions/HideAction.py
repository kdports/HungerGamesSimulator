from __future__ import annotations
from typing import TYPE_CHECKING, List
from Actions.GameAction import GameAction

from Managers.objects.skills import Skill
from Registries.CharacterRegistry import CharacterRegistry
from utilities import static_random

if TYPE_CHECKING:
    from Managers.objects.team import Team
    from Managers.objects.character import Character


class HideAction(GameAction):
    def __init__(self, team) -> None:
        self.team: Team = team

    def get_injured_teammates(self) -> List[Character]:
        injured_teammates = []
        for char_nid in self.team.members():
            char = CharacterRegistry.GetCharacter(char_nid)
            if not char.is_healthy():
                injured_teammates.append(char)
        return injured_teammates
    
    def get_num_healing_items(self) -> int:
        healing_items = 0
        for char_nid in self.team.members():
            char = CharacterRegistry.GetCharacter(char_nid)
            healing_items += len(char.medicine)
        return healing_items
    
    def remove_random_healing_item(self):
        for char_nid in self.team.members():
            char = CharacterRegistry.GetCharacter(char_nid)
            if char.medicine:
                char.medicine.pop()
                return

    def apply_healing(self):
        injured_teammates = self.get_injured_teammates()
        num_healing_items = self.get_num_healing_items()
        while num_healing_items > 0 and injured_teammates:
            BASE_HEAL_CHANCE = 30
            INCREMENT = 30
            heal_chance = BASE_HEAL_CHANCE + (INCREMENT * self.team.get_highest_medical_skill())

            if static_random.get_randint(0, 99) < heal_chance:
                static_random.shuffle(injured_teammates)[0].heal()

            self.remove_random_healing_item()
            num_healing_items -= 1

    def do(self):
        self.apply_healing()
            
        