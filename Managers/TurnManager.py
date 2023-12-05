from typing import List, Dict
from Managers.objects.character import Character
from Managers.objects.item import Item
from Managers.objects.team import Team
from utilities import static_random

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

    def IsCharacterInTeam(self, char_nid):
        for team in self.teams:
            if char_nid in team:
                return True
        return False

    def BuildAlliances(self):
        for char in self.characters:
            # You can't be in multiple teams
            if self.IsCharacterInTeam(char):
                continue

            # Needs to be seriously reworked/TODO
            desired_allies = char.get_alliances()
            confirmed_allies = []
            for prospective_ally in desired_allies:
                if char.nid in prospective_ally.get_alliances():
                    confirmed_allies.append(prospective_ally.nid)

    def KillCharacter(self, nid):
        for team in self.teams:
            team.remove_player(nid)
        self.PurgeEmptyTeams()

    def PurgeEmptyTeams(self):
        for team in self.teams:
            if len(team) == 0:
                self.teams.remove(team)