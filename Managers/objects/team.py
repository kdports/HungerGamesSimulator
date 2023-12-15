from typing import List
from Managers.objects.character import Character
from Managers.objects.skills import Skill
from Managers.objects.strategies import Strategy
from Managers.TurnManager import turn
from utilities import static_random

class Team():
    def __init__(self, players) -> None:
        # List of character nids
        self.players: List[str] = players

    def add_player(self, nid: str):
        if nid not in self.players:
            self.players.append(nid)

    def remove_player(self, nid):
        self.players.remove(nid)

    def get_random_player(self):
        idx = static_random.get_randint(0, len(self.players) - 1)
        return self.players[idx]

    def __contains__(self, item):
        return item in self.players
    
    def __len__(self):
        return self.players.__len__()

    def get_team_aggression(self):
        highest_leadership = -99
        leader: Character = None
        for char_nid in self.players:
            char = turn.GetCharacter(char_nid)
            if char.get_strategy(Strategy.Commanding) > highest_leadership:
                leader = char
            elif char.get_strategy(Strategy.Commanding) == highest_leadership and static_random.fiftyfifty():
                leader = char
        return leader.get_strategy(Strategy.Aggressive)

    def get_escape_capability(self):
        INCREMENT = 4
        escape_bonus = 0
        for char_nid in self.players:
            char = turn.GetCharacter(char_nid)
            if char.injury_multiplier() == 1:
                escape_bonus += char.get_skill(Skill.SurvivalSkill)
        escape_bonus /= len(self.players)
        return escape_bonus
    
    def get_pursuit_capability(self):
        INCREMENT = 4
        pursuit_bonus = 0
        for char_nid in self.players:
            char = turn.GetCharacter(char_nid)
            if char.injury_multiplier() == 1:
                pursuit_bonus += char.get_skill(Skill.EnduranceSkill)
        pursuit_bonus /= len(self.players)
        return pursuit_bonus