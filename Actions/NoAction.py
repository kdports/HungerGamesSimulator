from __future__ import annotations
from typing import TYPE_CHECKING

from Actions.GameAction import GameAction
if TYPE_CHECKING:
    from Managers.objects.team import Team

# Most likely to happen if a team tried to fight a hiding team,
# but couldn't find them
class NoAction(GameAction):
    def __init__(self, team) -> None:
        self.team: Team = team
        self.sub_actions = []

    def do(self):
        pass