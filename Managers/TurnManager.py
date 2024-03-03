from typing import List, Dict
from Managers.objects.character import Character
from Managers.objects.item import Item
from Registries.CharacterRegistry import CharacterRegistry
from Registries.ItemRegistry import ItemRegistry
from utilities import static_random
from Managers.helper_functions import CharacterFunctions

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Managers.objects.team import Team
    from Managers.objects.combatoutput import CombatOutput

class TurnManager():
    def __init__(self) -> None:
        self.board = []
        self.teams: List[Team] = []
        self.seed = 0
        self.combats: List[CombatOutput] = []
        # TODO: Make this actually do something
        self.modifiers = []

    # Step 1 of turn
    def StartTurn(self, data: dict):
        self.LoadJSONData(data)
        static_random.set_seed(self.seed)
        self.BuildAlliances()
        self.MakeSinglePersonTeams()

    # Step 2 of turn
    def RandomizeTeamActionOrder(self):
        self.teams = static_random.shuffle(self.teams)

    def LoadJSONData(self, data: dict):
        self.board = data.get("board", [])
        self.LoadCharacterData(data["characters"])
        self.LoadItemData(data["items"])
        self.teams = data.get("teams", [])
        self.seed = data.get("seed", 0)

        # We don't load combat outputs from last turn because we don't care

    def SaveJSONData(self):
        data = {}
        data["board"] = self.board
        data["characters"] = [CharacterRegistry.GetCharacter(ch).save() for ch in CharacterRegistry.characters]
        data["items"] = [ItemRegistry.GetItem(i).save() for i in ItemRegistry.items]
        data["teams"] = [t.save() for t in self.teams]
        data["seed"] = self.seed
        data["combats"] = [c.save() for c in self.combats]
        return data

    def LoadCharacterData(self, char_data: dict):
        # Loads into the CharacterRegistry holder
        for char_nid in char_data.keys():
            new_character = Character()
            new_character.load_json_object(char_data[char_nid])
            CharacterRegistry.AddCharacter(new_character)

    def LoadItemData(self, item_data: dict):
        for item_nid in item_data.keys():
            new_item = Item()
            new_item.load_json_object(item_data[item_nid])
            ItemRegistry.AddItem(new_item)

    def IsCharacterInTeam(self, char_nid):
        for team in self.teams:
            if char_nid in team:
                return True
        return False

    def GetCharacter(self, char_nid):
        return CharacterRegistry.GetCharacter(char_nid)

    def CalculateTrueAllies(self):
        for char_nid in CharacterRegistry.characters:
            char = self.GetCharacter(char_nid)
            true_allies = []
            for prospective_ally_nid in char.get_alliances():
                if char.nid in CharacterRegistry.characters[prospective_ally_nid].get_alliances():
                    true_allies.append(prospective_ally_nid)
            char.set_alliances(true_allies)

    def BuildAlliances(self):
        self.CalculateTrueAllies()

        for char_nid in CharacterRegistry.characters:
            char = self.GetCharacter(char_nid)
            # You can't be in multiple teams
            if self.IsCharacterInTeam(char_nid):
                continue

            for team in self.teams:
                if CharacterFunctions.ResolveCharacterEnteringTeam(char):
                    team.add_player(char_nid)
                    break
            self.PurgeEmptyTeams()

    def MakeSinglePersonTeams(self):
        for char_nid in CharacterRegistry.characters:
            if not self.IsCharacterInTeam(char_nid):
                self.teams.append(CharacterFunctions.MakeSinglePersonTeam(char_nid))

    def KillCharacter(self, nid):
        for team in self.teams:
            team.remove_player(nid)
        self.PurgeEmptyTeams()

    def PurgeEmptyTeams(self):
        for team in self.teams:
            if len(team) == 0:
                self.teams.remove(team)

    def RemainingPlayers(self):
        return len(CharacterRegistry.characters)

turn = TurnManager()

def make_turn_manager():
    global turn
    return turn