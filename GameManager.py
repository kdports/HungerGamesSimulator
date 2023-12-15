from Managers.NewGameManager import NewGameManager
from Managers import TurnManager

class GameManager():
    def NewGame(self):
        new_game = NewGameManager()
        new_game.NewGameController()

if __name__ == "__main__":
    game_manager = GameManager()
    while True:
        task = input("Welcome to the Hunger Games Simulator.\nType and enter N to create a new game, or L to load a game: ")
        if task.upper() == "N":
            game_manager.NewGame()
        elif task.upper() == "L":
            turn_manager = TurnManager.make_turn_manager()
            pass
        else:
            print("Invalid entry. Please try again.\n")