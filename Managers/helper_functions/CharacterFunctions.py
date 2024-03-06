from typing import List
from Managers.objects.character import Character
from Managers.objects.strategies import Strategy
from Managers.objects.team import Team
from Registries.CharacterRegistry import CharacterRegistry
from utilities import static_random

'''
More positive = better for team1
'''
def CompareTeams(team1: Team, team2: Team):
    team1_sum = 0
    team2_sum = 0

    for char1_nid in team1.members():
        char1 = CharacterRegistry.GetCharacter(char1_nid)
        team1_sum += GetCharacterCombatRating(char1)

    for char2_nid in team2.members():
        char2 = CharacterRegistry.GetCharacter(char2_nid)
        team2_sum += GetCharacterCombatRating(char2)

    return team1_sum - team2_sum

def ResolveCharacterEnteringTeam(char: Character, team: Team):
    num_friends = 0
    for other_char in team.members():
        if other_char in char.get_alliances():
            num_friends += 1

    if num_friends == 0:
        return False
    elif num_friends == len(team):
        team.add_player(char.nid)
        return True
    else:
        # 0 < friends in team < team size
        BASE_CHANCE = 30
        STRATEGY_INCREMENT = 10
        majority_bonus = 35 if num_friends > len(team) // 2 else 0
        join_team_chance = BASE_CHANCE + (char.get_strategy(Strategy.Friendly) * STRATEGY_INCREMENT) + majority_bonus
        if join_team_chance > static_random.get_randint(0, 99):
            team.add_player(char.nid)
            return True
    return False

def MakeSinglePersonTeam(char_nid: str):
    team = Team([char_nid])
    return team

def GetCharacterCombatRating(char: Character) -> int:
    return char.combat_bonus()