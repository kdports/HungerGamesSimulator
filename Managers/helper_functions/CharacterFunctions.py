from typing import List
from Managers.objects.character import Character
from Managers.objects.team import Team
from utilities import static_random

'''
More positive = better for team1
'''
def CompareTeams(team1: Team, team2: Team):
    team1_sum = 0
    team2_sum = 0

    for char1 in team1:
        team1_sum += GetCharacterCombatRating(char1)

    for char2 in team2:
        team2_sum += GetCharacterCombatRating(char2)

    return team1_sum - team2_sum

def GetCharacterCombatRating(char: Character) -> int:
    return char.combat_bonus()