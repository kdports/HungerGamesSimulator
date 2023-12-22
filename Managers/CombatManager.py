from Managers.objects.combatoutput import CombatOutput
from Managers.objects.skills import Skill
from Managers.objects.team import Team
from utilities import static_random
from helper_functions import CharacterFunctions

class CombatManager():
    def __init__(self, team1, team2) -> None:
        self.team1 = team1
        self.team2 = team2
        self.outcome = CombatOutput()

    def escape_success_chance(self, escaping_team, pursuing_team):
        base_chance = 50 # %
        for char in escaping_team:
            # 1 is injured, 2 is disabled
            if char.body["legs"] > 0:
                base_chance = base_chance//2
        for char in pursuing_team:
            if char.body["legs"] > 0:
                base_chance = base_chance*2
        return base_chance

    '''
    Higher means more likely to decide to continue combat
    '''
    def fight_desire(self, ally_team: Team, enemy_team: Team):
        BASE_CHANCE = 50
        INCREMENT = 16
        # Positive is good for ally team
        relative_str = CharacterFunctions.CompareTeams(ally_team, enemy_team)
        # Compute aggressiveness
        ally_aggression = ally_team.get_team_aggression()

        fight_desire = BASE_CHANCE
        fight_desire += INCREMENT * relative_str
        fight_desire += INCREMENT * ally_aggression

        return fight_desire
    
    def check_team_retreat(self, team1, team2):
        team1_try_flee = False
        team2_try_flee = False
        if self.fight_desire(team1, team2) < static_random.get_randint(0, 99):
            team1_try_flee = True
        if self.fight_desire(team2, team1) < static_random.get_randint(0, 99):
            team2_try_flee = True
        return team1_try_flee, team2_try_flee
    
    def check_successful_escape(self, fleeing: Team, pursuing: Team):
        flight_chance = 15
        pursue_chance = 10

        flight_chance += fleeing.get_escape_capability()
        pursue_chance += pursuing.get_pursuit_capability()
        return (flight_chance - pursue_chance) > static_random.get_randint(0, 99)

    '''
    Best of three system. Three rolls are made and compared against each other. 
    Each person on a team makes an individual roll. Highest team roll is taken
    All a bit placeholder
    '''
    def solve_combat(self) -> CombatOutput:
        team1_wins = 0
        team2_wins = 0

        min_rolls_to_win = 2

        while team1_wins < min_rolls_to_win or team2_wins < min_rolls_to_win:
            
            team1_try_flee, team2_try_flee = self.check_team_retreat(self.team1, self.team2)
            if team1_try_flee and team2_try_flee:
                return self.combat_inconclusive(self.team1, self.team2)
            elif (team1_try_flee and self.check_successful_escape(self.team1, self.team2)) or \
                    (team2_try_flee and self.check_successful_escape(self.team2, self.team1)):
                return self.combat_inconclusive(self.team1, self.team2)

            team1_rolls = [static_random.get_combat() + char.combat_bonus() for char in self.team1]
            team1_best = max(team1_rolls)

            team2_rolls = [static_random.get_combat() + char.combat_bonus() for char in self.team2]
            team2_best = max(team2_rolls)

            if team1_best > team2_best:
                team1_wins += 1
                self.calculate_injuries(self.team2)
            elif team1_best < team2_best:
                team2_wins += 1
                self.calculate_injuries(self.team1)

        if team1_wins > team2_wins:
            winner = self.team1
            loser = self.team2
        else:
            winner = self.team2
            loser = self.team1

        # If we reach this point, there has been a winner and loser
        return self.combat_decided(winner, loser)

    def calculate_injuries(self, team):
        BASE_INJURY_CHANCE = 30
        for char in team:
            avg_combat_survival = (char.get_skill(Skill.CombatSkill) + char.get_skill(Skill.SurvivalSkill)) // 2
            if static_random.get_randint(0, 99) < \
                    BASE_INJURY_CHANCE / (avg_combat_survival + 1):
                char.get_injured()
                self.outcome.add_injury(char, static_random.shuffle(team.players)[0])

    def combat_decided(self, winner, loser) -> CombatOutput:
        for char in loser:
            BASE_FINAL_ESCAPE_CHANCE = 5
            if static_random.get_randint(0, 99) < BASE_FINAL_ESCAPE_CHANCE * char.get_skill(Skill.SurvivalSkill):
                # They manage to escape in the last moment
                self.outcome.add_escape(char)
            else:
                # They die
                killer = static_random.shuffle(winner.players)[0]
                self.outcome.add_death(char, killer)
        return self.outcome

    def combat_inconclusive(self, team1, team2) -> CombatOutput:
        return self.outcome