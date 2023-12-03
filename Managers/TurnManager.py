from typing import List
from Managers.objects.character import Character
from Managers.objects.team import Team

class TurnManager():
    def __init__(self) -> None:
        self.board = []
        self.characters: List[Character] = {}
        self.teams: List[Team] = []
        # TODO: self.modifiers

    def LoadJSONData(self, data: dict):
        self.board = data.get("board", [])
        self.characters = data["characters"]
        self.BuildAlliances()

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

            desired_allies = char.get_alliances()
            confirmed_allies = []
            for prospective_ally in desired_allies:
                if char.nid in prospective_ally.get_alliances():
                    confirmed_allies.append(prospective_ally.nid)