class Team():
    def __init__(self, players) -> None:
        # List of character nids
        self.players: list = players

    def add_player(self, nid):
        if nid not in self.players:
            self.players.append(nid)

    def remove_player(self, nid):
        self.players.remove(nid)

    def __contains__(self, item):
        return item in self.players