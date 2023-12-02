import os
import glob
import json
import re
import time
from typing import List

from Managers.objects.character import Character
from pathlib import Path

class NewGameManager():
    def NewGameController(self):
        nid = self.AssignGameName()
        character_dict = self.NewGameAddCharacters()
        # Load items: TODO
        # Generate map: TODO

        print("Setup complete! Now saving...")
        game_dict = {
            "nid": nid,
            "characters": character_dict
        }

        current_dirname = os.getcwd()
        self.MakeGameFolder(nid)
        relative_dir = os.path.join("games", nid.lower(), nid.lower() + "_turn0.json")
        game_file = os.path.join(current_dirname, relative_dir)
        with open(game_file, "w") as outfile:
            outfile.write(json.dumps(game_dict))
        time.sleep(2)
        print("Configuration Complete!\n\nGame data has been written to " + relative_dir + ".\nMay the odds be ever in your favor!")

    def MakeGameFolder(self, nid):
        current_dirname = os.getcwd()
        game_folder = os.path.join(current_dirname, "games")
        if not os.path.exists(game_folder):
            os.makedirs(game_folder)
        new_game_dir = os.path.join(game_folder, nid.lower())
        if not os.path.exists(new_game_dir):
            os.makedirs(new_game_dir)
        else:
            print("Folder with Character NID already exists!\n")
            return False
        return True

    def AssignGameName(self):
        nid = input("Choose a new name for your game: ")
        nid = "".join(nid.split())
        nid = re.sub(r"[/\\?%*:|\"<>\x7F\x00-\x1F]", "-", nid)
        return nid

    def LoadCharacter(self, file_name):
        try:
            new_character = Character()
            with open(file_name, 'r') as character_file:
                character_json = json.load(character_file)
                new_character.load_json_object(character_json)
            return new_character
        except:
            print("An error occurred while loading your character.\nPlease ensure your character has a name and nid.\n")
        return None

    def NewGameAddCharacters(self):
        finished = 0
        character_list: List[Character] = []

        print("It is time to select tributes.\n")
        while not finished:
            character_nid = input("Please enter a character's unique name.\nWe will search your directory and subdirectories for their information.\nType Done to end character entry.\n").strip()
            if character_nid.upper() == "DONE":
                if len(character_list) > 0:
                    print("Character entry finished. Proceeding...")
                    finished = 1
                    continue
                else:
                    print("You have yet to enter any characters.\nYou must enter at least one character.")
                    continue

            current_dirname = os.getcwd()
            try:
                file = next(Path(current_dirname).rglob(character_nid + "_character_sheet.json"))
            except StopIteration:
                print("We couldn't find any files with that character's unique name.\nPlease try again.\n")
                continue

            char = self.LoadCharacter(file)
            if char is not None:
                character_list.append(char)
                print("Character loaded successfully!\n")

        character_dict = {}
        for char in character_list:
            character_dict[char.nid] = char.save()
        return character_dict