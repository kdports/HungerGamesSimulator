from typing import List
from Managers.objects.character import Character
from Managers.objects.skills import Skill
from Managers.objects.strategies import Strategy
from Registries.CharacterRegistry import CharacterRegistry 
from utilities import static_random

class Team():
    def __init__(self, players: List[str]) -> None:
        # List of character nids
        self.players: List[str] = players
        self.action_decided = False
        self.action = None

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
            char = CharacterRegistry.GetCharacter(char_nid)
            if char.get_strategy(Strategy.Commanding) > highest_leadership:
                leader = char
            elif char.get_strategy(Strategy.Commanding) == highest_leadership and static_random.fiftyfifty():
                leader = char
        return leader.get_strategy(Strategy.Aggressive)

    def get_escape_capability(self):
        escape_bonus = 0
        for char_nid in self.players:
            char = CharacterRegistry.GetCharacter(char_nid)
            if char.injury_multiplier() == 1:
                escape_bonus += char.get_skill(Skill.SurvivalSkill)
        escape_bonus /= len(self.players)
        return escape_bonus
    
    def get_pursuit_capability(self):
        pursuit_bonus = 0
        for char_nid in self.players:
            char = CharacterRegistry.GetCharacter(char_nid)
            if char.injury_multiplier() == 1:
                pursuit_bonus += char.get_skill(Skill.EnduranceSkill)
        pursuit_bonus /= len(self.players)
        return pursuit_bonus
    
    def get_highest_survival_skill(self) -> int:
        highest_survival = 0
        for char_nid in self.players:
            char = CharacterRegistry.GetCharacter(char_nid)
            med = char.get_skill(Skill.SurvivalSkill)
            if med > highest_survival:
                highest_survival = med
        return highest_survival

    def get_highest_medical_skill(self) -> int:
        highest_med = 0
        for char in self.players:
            med = CharacterRegistry.GetCharacter(char).get_skill(Skill.MedicalSkill)
            if med > highest_med:
                highest_med = med
        return highest_med
    
    def members(self):
        return self.players

    def save(self):
        return self.players
    
    def any_injuries(self) -> bool:
        return any([not CharacterRegistry.GetCharacter(char_nid).is_healthy() for char_nid in self.players])

    def decide_action(self, potential_targets: list):
        if self.action_decided:
            return
        if len(potential_targets) > 0:
            BASE_COMBAT_CHANCE = 33
            INCREMENT = 9
            HIGH_AGGRESSION = 7
            aggression = self.get_team_aggression() if len(potential_targets) > 2 else HIGH_AGGRESSION
            combat_chance = BASE_COMBAT_CHANCE + (INCREMENT * aggression)
            hide_chance = (100 - combat_chance) // 2 if self.any_injuries() else 0
            forage_chance = 100 - combat_chance - hide_chance
        else:
            combat_chance = 0
            hide_chance = 50 if self.any_injuries() else 0
            forage_chance = 100 - combat_chance - hide_chance