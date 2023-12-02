from Managers.NewGameManager import NewGameManager

class GameManager():
    def NewGame(self):
        new_game = NewGameManager()
        new_game.NewGameController()

if __name__ == "__main__":
    game_manager = GameManager()
    while True:
        task = input("Welcome to the Hunger Games Simulator.\nType and enter N to create a new game, or L to load a game.")
        if task.capitalize() == "N":
            game_manager.NewGame()
        elif task.capitalize() == "L":
            pass
        else:
            print("Invalid entry. Please try again.\n")