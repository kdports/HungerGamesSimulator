import unittest

from Actions.HideAction import HideAction

from Managers.objects.character import Character
from Managers.objects.item import Item
from Managers.objects.team import Team
from Registries.CharacterRegistry import CharacterRegistry

class HealActionUnitTests(unittest.TestCase):
    def setUp(self):
        self.healing_item = Item("Scalpel", "Scalpel", is_medicine=True)

    # Test that a solo team can successfully heal
    def test_solo_team_heal_success(self):
        CharacterRegistry.Clear()
        guaranteed_success = 100
        CharacterRegistry.AddCharacter(Character("Bob", "Bob", {"Medical Skill": guaranteed_success}))
        CharacterRegistry.GetCharacter("Bob").get_injured()
        CharacterRegistry.GetCharacter("Bob").give_item(self.healing_item)
        team = Team(["Bob"])

        self.assertFalse(CharacterRegistry.GetCharacter("Bob").is_healthy())

        action = HideAction(team)
        action.do()

        self.assertTrue(CharacterRegistry.GetCharacter("Bob").is_healthy())

    # Test that a solo team can fail to heal
    def test_solo_team_heal_fail(self):
        CharacterRegistry.Clear()
        guaranteed_fail = -100
        CharacterRegistry.AddCharacter(Character("Bob", "Bob", {"Medical Skill": guaranteed_fail}))
        CharacterRegistry.GetCharacter("Bob").get_injured()
        CharacterRegistry.GetCharacter("Bob").give_item(self.healing_item)
        team = Team(["Bob"])

        self.assertFalse(CharacterRegistry.GetCharacter("Bob").is_healthy())

        action = HideAction(team)
        action.do()

        self.assertFalse(CharacterRegistry.GetCharacter("Bob").is_healthy())

    # Test that a successful heal decrements a healing item from inventory
    def test_solo_team_heal_success_decrement_item(self):
        CharacterRegistry.Clear()
        guaranteed_success = 100
        CharacterRegistry.AddCharacter(Character("Bob", "Bob", {"Medical Skill": guaranteed_success}))
        CharacterRegistry.GetCharacter("Bob").get_injured()
        CharacterRegistry.GetCharacter("Bob").give_item(self.healing_item)
        team = Team(["Bob"])

        action = HideAction(team)
        action.do()

        self.assertTrue(len(CharacterRegistry.GetCharacter("Bob").medicine) == 0)

    # Test that a failed heal decrements a healing item from inventory
    def test_solo_team_heal_fail_decrement_item(self):
        CharacterRegistry.Clear()
        guaranteed_fail = -100
        CharacterRegistry.AddCharacter(Character("Bob", "Bob", {"Medical Skill": guaranteed_fail}))
        CharacterRegistry.GetCharacter("Bob").get_injured()
        CharacterRegistry.GetCharacter("Bob").give_item(self.healing_item)
        team = Team(["Bob"])

        action = HideAction(team)
        action.do()

        self.assertTrue(len(CharacterRegistry.GetCharacter("Bob").medicine) == 0)

    # If no one is injured, the item should not be used
    def test_status_quo_if_no_valid_targets(self):
        CharacterRegistry.Clear()
        guaranteed_success = 100
        CharacterRegistry.AddCharacter(Character("Bob", "Bob", {"Medical Skill": guaranteed_success}))
        CharacterRegistry.GetCharacter("Bob").give_item(self.healing_item)
        team = Team(["Bob"])

        action = HideAction(team)
        action.do()

        self.assertTrue(len(CharacterRegistry.GetCharacter("Bob").medicine) == 1)

    # Test that nothing happens w/o a healing item
    def test_solo_team_heal_no_item(self):
        CharacterRegistry.Clear()
        guaranteed_success = 100
        CharacterRegistry.AddCharacter(Character("Bob", "Bob", {"Medical Skill": guaranteed_success}))
        CharacterRegistry.GetCharacter("Bob").get_injured()
        team = Team(["Bob"])

        self.assertFalse(CharacterRegistry.GetCharacter("Bob").is_healthy())

        action = HideAction(team)
        action.do()

        self.assertFalse(CharacterRegistry.GetCharacter("Bob").is_healthy())

    # Test that the highest medical skill will be used
    def test_team_heal_use_highest(self):
        CharacterRegistry.Clear()
        guaranteed_success = 100
        CharacterRegistry.AddCharacter(Character("Bob", "Bob", {"Medical Skill": guaranteed_success}))
        CharacterRegistry.GetCharacter("Bob").get_injured()
        CharacterRegistry.GetCharacter("Bob").give_item(self.healing_item)

        guaranteed_fail = -100
        CharacterRegistry.AddCharacter(Character("Jane", "Jane", {"Medical Skill": guaranteed_fail}))
        team = Team(["Bob", "Jane"])

        self.assertFalse(CharacterRegistry.GetCharacter("Bob").is_healthy())

        action = HideAction(team)
        action.do()

        self.assertTrue(CharacterRegistry.GetCharacter("Bob").is_healthy())

    # Test that only one person is healed per action
    def test_team_heal_one_target(self):
        CharacterRegistry.Clear()
        guaranteed_success = 100
        CharacterRegistry.AddCharacter(Character("Bob", "Bob", {"Medical Skill": guaranteed_success}))
        CharacterRegistry.GetCharacter("Bob").get_injured()
        CharacterRegistry.GetCharacter("Bob").give_item(self.healing_item)

        CharacterRegistry.AddCharacter(Character("Jane", "Jane", {"Medical Skill": guaranteed_success}))
        CharacterRegistry.GetCharacter("Jane").get_injured()
        team = Team(["Bob", "Jane"])

        self.assertFalse(CharacterRegistry.GetCharacter("Bob").is_healthy())

        action = HideAction(team)
        action.do()

        self.assertTrue(not CharacterRegistry.GetCharacter("Bob").is_healthy() or not CharacterRegistry.GetCharacter("Jane").is_healthy())

if __name__ == '__main__':
    unittest.main()