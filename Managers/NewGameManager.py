import os
import glob
import json
import time
from typing import List

from Managers.objects.character import Character

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

        current_dirname = os.path.dirname(__file__)
        relative_dir = "games/" + nid.lower() + "/" + nid.lower() + "_turn0.json"
        game_file = os.path.join(current_dirname, relative_dir)
        with open(game_file, "w") as outfile:
            outfile.write(game_dict)
        time.sleep(2)
        print("Configuration Complete!\n\nGame data has been written to " + relative_dir + ".\nMay the odds be ever in your favor!")

    def AssignGameName(self):
        nid = input("Choose a new name for your game: ")
        nid = "".join(nid.split())
        nid = nid.isalnum()
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
            character_nid = input("Please enter a character's unique name.\nWe will search your directory and subdirectories for their information.\nType Done to end character entry.\n")
            if character_nid.capitalize() == "DONE":
                if len(character_list) > 0:
                    print("Character entry finished. Proceeding...")
                    finished = 1
                else:
                    print("You have yet to enter any characters.\nYou must enter at least one character.")
                    continue

            current_dirname = os.path.dirname(__file__)
            matching_files = glob.glob("*" + character_nid + "_character_sheet.json", recursive=True)
            if len(matching_files) == 0:
                print("\nWe couldn't find any files with that character's unique name.\nPlease try again.\n")
                continue

            char = self.LoadCharacter(matching_files[0])
            if char is not None:
                character_list.append(char)

        character_dict = {}
        for char in character_list:
            character_dict[char.nid] = char.save()
        return character_dict