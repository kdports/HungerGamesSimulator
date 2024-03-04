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
        bob.body['legs'] = 1
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