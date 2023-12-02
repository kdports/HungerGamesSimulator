from ast import List
from Managers.objects.character import Character


class TurnManager():
    def __init__(self) -> None:
        self.board = []
        self.characters: List[Character] = {}
        self.teams = []
        # TODO: self.modifiers

    def LoadJSONData(self, data: dict):
        self.board = data.get("board", [])
        self.characters = data["characters"]
        self.BuildAlliances()

    def BuildAlliances(self):
        for char in self.characters:
            desired_allies = char.get_alliances()
            confirmed_allies = []
            for prospective_ally in desired_allies:
                if char.nid in prospective_ally.get_alliances():
                    confirmed_allies.append(prospective_ally.nid)