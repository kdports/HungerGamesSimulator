from utilities import static_random

class Team():
    def __init__(self, players) -> None:
        # List of character nids
        self.players: list = players

    def add_player(self, nid):
        if nid not in self.players:
            self.players.append(nid)

    def remove_player(self, nid):
        self.players.remove(nid)

    def get_random_player(self):
        idx = static_random.get_randint(0, len(self.players) - 1)
        return self.players[idx]

    def __contains__(self, item):
        return item in self.players
    
    def __len__(self):
        return self.players.__len__()