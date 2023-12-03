from typing import List
from Managers.objects.character import Character
from Managers.objects.team import Team
from utilities import static_random

class TurnManager():
    def __init__(self) -> None:
        self.board = []
        self.characters: List[Character] = {}
        self.teams: List[Team] = []
        self.seed = 0
        # TODO: self.modifiers

    def LoadJSONData(self, data: dict):
        self.board = data.get("board", [])
        self.characters = data["characters"]

        self.seed = data.get("seed", 0)
        static_random.set_seed(self.seed)
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