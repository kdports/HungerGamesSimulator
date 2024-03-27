from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Managers.objects.team import Team

class GameAction():
    def __init__(self, team) -> None:
        self.team: Team = team
        self.sub_actions = []

    def do(self):
        pass