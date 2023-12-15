from typing import List, Dict
from Managers.objects.character import Character
from Managers.objects.item import Item
from Managers.objects.team import Team
from utilities import static_random
from helper_functions import CharacterFunctions

class TurnManager():
    def __init__(self) -> None:
        self.board = []
        self.characters: Dict[str, Character] = {}
        self.items: Dict[str, Item] = {}
        self.teams: List[Team] = []
        self.seed = 0
        # TODO: self.modifiers

    def LoadJSONData(self, data: dict):
        self.board = data.get("board", [])
        self.characters = self.LoadCharacterData(data["characters"])
        self.items = self.LoadItemData(data["items"])

        self.seed = data.get("seed", 0)
        static_random.set_seed(self.seed)
        self.BuildAlliances()

    def LoadCharacterData(self, char_data: dict):
        char_dict = {}
        for char_nid in char_data.keys():
            new_character = Character()
            new_character.load_json_object(char_data[char_nid])
            char_dict[new_character.nid] = new_character
        return char_dict

    def LoadItemData(self, item_data: dict):
        item_dict = {}
        for item_nid in item_data.keys():
            new_item = Item()
            new_item.load_json_object(item_data[item_nid])
            item_dict[new_item.nid] = new_item
        return item_dict

    def IsCharacterInTeam(self, char_nid):
        for team in self.teams:
            if char_nid in team and len(team) > 1:
                return True
        return False

    def GetCharacter(self, char_nid):
        return self.characters[char_nid]

    def CalculateTrueAllies(self):
        for char_nid in self.characters:
            char = self.GetCharacter(char_nid)
            true_allies = []
            for prospective_ally_nid in char.get_alliances():
                if char.nid in self.characters[prospective_ally_nid].get_alliances():
                    true_allies.append(prospective_ally_nid)
            char.set_alliances(true_allies)

    def BuildAlliances(self):
        self.CalculateTrueAllies()

        for char_nid in self.characters:
            char = self.GetCharacter(char_nid)
            # You can't be in multiple teams
            if self.IsCharacterInTeam(char):
                continue

            for team in self.teams:
                if CharacterFunctions.ResolveCharacterEnteringTeam(char):
                    team.add_player(char_nid)
                    break
            self.PurgeEmptyTeams()

    def KillCharacter(self, nid):
        for team in self.teams:
            team.remove_player(nid)
        self.PurgeEmptyTeams()

    def PurgeEmptyTeams(self):
        for team in self.teams:
            if len(team) == 0:
                self.teams.remove(team)

turn = TurnManager()