from utilities import static_random

class CombatManager():
    def __init__(self, team1, team2) -> None:
        self.team1 = team1
        self.team2 = team2

    '''
    Best of three system. Three rolls are made and compared against each other. 
    Each person on a team makes an individual roll. Highest team roll is taken
    All a bit placeholder
    '''
    def solve_combat(self):
        team1_wins = 0
        team2_wins = 0

        min_rolls_to_win = 2

        while team1_wins < min_rolls_to_win or team2_wins < min_rolls_to_win:
            # TODO: Check for desire/ability to disengage

            team1_rolls = [static_random.get_combat() + char.combat_bonus() for char in self.team1]
            team1_best = max(team1_rolls)

            team2_rolls = [static_random.get_combat() + char.combat_bonus() for char in self.team2]
            team2_best = max(team2_rolls)

            if team1_best > team2_best:
                team1_wins += 1
            elif team1_best < team2_best:
                team2_wins += 1

        if team1_wins > team2_wins:
            winner = self.team1
            loser = self.team2
        else:
            winner = self.team2
            loser = self.team1

        self.combat_over(winner, loser)

    def combat_over(self, winner, loser):
        # Write text here
        pass
