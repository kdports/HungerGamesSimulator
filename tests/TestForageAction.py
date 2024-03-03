import unittest

from Actions.ForageAction import ForageAction

from Managers.objects.character import Character
from Managers.objects.item import Item
from Managers.objects.team import Team
from Registries.CharacterRegistry import CharacterRegistry

def has_an_item(char: Character):
    return len(char.weapons) > 0 or len(char.food) > 0 or len(char.medicine) > 0

def has_no_item(char: Character):
    return len(char.weapons) == 0 and len(char.food) == 0 and len(char.medicine) == 0

class ForageActionUnitTests(unittest.TestCase):
    def setUp(self):
        self.all_items = [Item("Sword", "Sword", combat_mod=2, hands_needed=1), \
                     Item("BandAid", "BandAid", is_medicine=True), \
                     Item("Bread", "Bread", is_food=True)]
    
    # Checks that a single team member will always be given
    # the reward if the search succeeds
    def test_single_member_team_success(self):
        CharacterRegistry.Clear()
        guaranteed_success = 100
        CharacterRegistry.AddCharacter(Character("Bob", "Bob", {"Survival Skill": guaranteed_success}))
        team = Team(["Bob"])
        action = ForageAction(team, self.all_items)
        action.do()

        bob = CharacterRegistry.GetCharacter("Bob")
        self.assertTrue(has_an_item(bob))

    # Test that a search can fail
    def test_single_member_team_failure(self):
        CharacterRegistry.Clear()
        guaranteed_fail = -100
        CharacterRegistry.AddCharacter(Character("Bob", "Bob", {"Survival Skill": guaranteed_fail}))
        team = Team(["Bob"])
        action = ForageAction(team, self.all_items)
        action.do()

        bob = CharacterRegistry.GetCharacter("Bob")
        self.assertTrue(has_no_item(bob))

if __name__ == '__main__':
    unittest.main()