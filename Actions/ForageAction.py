from __future__ import annotations
from Actions.GameAction import GameAction
from Managers.objects.strategies import Strategy
from Registries.CharacterRegistry import CharacterRegistry
from utilities import static_random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Managers.objects.team import Team
    from Managers.objects.item import Item


class ForageAction(GameAction):
    def __init__(self, team: Team, available_items: list) -> None:
        super().__init__(team)
        # The list of all items that could be pulled.
        self.available_items = available_items

    def get_random_item(self) -> Item:
        static_random.shuffle(self.available_items)
        if self.available_items:
            return self.available_items[0]
        return None

    # Chance of each individual player to get the item
    def individual_weight(self, p: str):
        char = CharacterRegistry.GetCharacter(p)
        return char.get_strategy(Strategy.Friendly) + char.get_strategy(Strategy.Commanding)

    def forage(self):
        BASE_FIND_CHANCE = 30
        INCREMENT = 30
        find_chance = BASE_FIND_CHANCE + (INCREMENT * self.team.get_highest_survival_skill())

        if static_random.get_randint(0, 99) < find_chance:
            item = self.get_random_item()
            players = self.team.players.copy()
            players.sort(reverse=True, key=self.individual_weight)
            for p in players:
                char = CharacterRegistry.GetCharacter(p)
                if item.hands_needed > 0 and char.wants_to_equip(item):
                    char.equip_item(item)
                    return
                else:
                    char.give_item(item)

    def do(self):
        self.forage()