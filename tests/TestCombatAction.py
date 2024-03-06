import unittest
from Actions.CombatAction import CombatAction

from Managers.objects.character import Character
from Managers.objects.item import Item
from Managers.objects.team import Team
from Registries.CharacterRegistry import CharacterRegistry

class CombatActionUnitTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_escape_chance(self):
        CharacterRegistry.Clear()

        # Bob will be injured
        bob = Character("Bob", "Bob")
        bob.body.parts()['legs'] = 1
        CharacterRegistry.AddCharacter(bob)
        bob_team = Team([bob.nid])

        jane = Character("Jane", "Jane")
        CharacterRegistry.AddCharacter(jane)
        jane_team = Team([jane.nid])

        action = CombatAction(bob_team, jane_team)

        base_value = action.escape_success_chance(jane_team, jane_team)
        # Someone with broken legs should have a harder time escaping
        self.assertTrue(action.escape_success_chance(bob_team, jane_team) < base_value)
        # Someone with broken legs should have a harder time pursuing
        self.assertTrue(action.escape_success_chance(jane_team, bob_team) > base_value)

    def test_fight_desire(self):
        CharacterRegistry.Clear()

        # Bob is aggressive
        bob = Character("Bob", "Bob", strategies={"Aggressive": 4})
        CharacterRegistry.AddCharacter(bob)
        bob_team = Team([bob.nid])

        jane = Character("Jane", "Jane", strategies={"Aggressive": -4})
        CharacterRegistry.AddCharacter(jane)
        jane_team = Team([jane.nid])

        john = Character("John", "John")
        CharacterRegistry.AddCharacter(john)
        john_team = Team([john.nid])

        action = CombatAction(bob_team, jane_team)

        base_value = action.fight_desire(john_team, john_team)
        # More aggressive teams should continue to fight
        self.assertTrue(action.fight_desire(bob_team, jane_team) > base_value)
        # Less aggressive teams should not want to fight
        self.assertTrue(action.fight_desire(jane_team, bob_team) < base_value)

    def test_check_team_retreat(self):
        CharacterRegistry.Clear()
        bob = Character("Bob", "Bob", strategies={"Aggressive": 4})
        CharacterRegistry.AddCharacter(bob)
        bob_team = Team([bob.nid])

        jane = Character("Jane", "Jane", strategies={"Aggressive": -4})
        CharacterRegistry.AddCharacter(jane)
        jane_team = Team([jane.nid])

        action = CombatAction(bob_team, jane_team)

        retreat_choices = action.check_team_retreat(bob_team, jane_team)
        self.assertTrue(retreat_choices[0] == False and retreat_choices[1] == True)

    def test_injury_avoided(self):
        CharacterRegistry.Clear()
        # Makes sure that an injury roll can fail
        # These skill numbers are impossible - they're just to skew the roll
        guaranteed_no_injury = -100
        bob = Character("Bob", "Bob", skills={"Survival Skill": guaranteed_no_injury})
        CharacterRegistry.AddCharacter(bob)
        bob_team = Team([bob.nid])

        action = CombatAction(bob_team, bob_team)
        action.calculate_injuries(bob_team)
        self.assertTrue(bob.is_healthy())

    def test_injury_taken(self):
        CharacterRegistry.Clear()
        # Makes sure that an injury roll can fail
        # These skill numbers are impossible - they're just to skew the roll
        guaranteed_injury = 0.000001
        bob = Character("Bob", "Bob", skills={"Survival Skill": guaranteed_injury})
        CharacterRegistry.AddCharacter(bob)
        bob_team = Team([bob.nid])

        action = CombatAction(bob_team, bob_team)
        action.calculate_injuries(bob_team)
        self.assertFalse(bob.is_healthy())