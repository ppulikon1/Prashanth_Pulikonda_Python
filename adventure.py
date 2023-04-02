import json
import sys
from difflib import get_close_matches

class GameState:
    def __init__(self, map_file):
        try:
            with open(map_file, 'r') as f:
                self.map_data = json.load(f)
        except FileNotFoundError:
            print(f"Error: file '{map_file}' not found.")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"Error: file '{map_file}' contains invalid JSON.")
            sys.exit(1)
        self.current_room = 0
        self.previous_room = None
        if "win_condition" in self.map_data:
            self.win_condition = self.map_data["win_condition"]
        else:
            self.win_condition = None


    def get_room(self):
        return self.map_data['rooms'][self.current_room]

    def move_player(self, direction, player_state):
        next_room_id = self.get_room()['exits'].get(direction)
        if next_room_id is None:
            print(f"Error: Invalid direction '{direction}'.")
            return False
        next_room = self.map_data['rooms'][next_room_id]
        if direction in self.get_room()['locked_doors']:
            required_item = self.get_room()['locked_doors'][direction]
            if required_item in player_state.inventory:
                player_state.remove_item(required_item)
                print(f"You unlock the {direction} door with {required_item}.")
                player_state.unlocked_doors[direction] = next_room_id
            elif direction in player_state.unlocked_doors and player_state.unlocked_doors[direction] == next_room_id:
               pass  # door is already unlocked
            else:
                print(f"The {direction} door is locked and you don't have the required a {required_item} to unlock it.")
                return False
    
        self.previous_room = self.current_room
        self.current_room = next_room_id
        return True

    
    def get_exit_list(self, player_state):
        exit_list = "Exits: "
        room = self.get_room()
        if 'locked_doors' in room:
            for direction, destination in room['exits'].items():
                if direction in room['locked_doors']:
                    if direction in player_state.unlocked_doors:
                        exit_list += f"{direction} ({destination}), "
                    else:
                        exit_list += f"{direction} (locked), "
                else:
                    exit_list += f"{direction} ({destination}), "
        else:
            for direction, destination in room['exits'].items():
                exit_list += f"{direction} ({destination}), "
        return exit_list[:-2]

    def set_previous_room(self, room):
        self.previous_room = room['name'] # or room['id'] if you want to use the room ID
    def get_previous_room(self):
        return self.previous_room

class PlayerState:
    def __init__(self):
        self.inventory = []
        self.unlocked_doors = {}

    def add_item(self, item):
        self.inventory.append(item)

    def remove_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)

    def get_inventory(self):
        if len(self.inventory) == 0:
            return "You have no items."
        else:
            items = sorted(self.inventory)  # sort the items alphabetically
            output = "Inventory:\n"
            for i, item in enumerate(items):
                if i == 0:
                    output += f"  {item}"
                else:
                    output += f"\n  {item}"
            return output        
    def unlock_door(self, direction, required_item):
        if required_item in self.inventory:
            self.remove_item(required_item)
            self.unlocked_doors[direction] = self.current_room['exits'][direction]
            print(f"You unlock the {direction} door.")
            return True
        else:
            print(f"You don't have the required item to unlock the {direction} door.")
            return False

# Check if the user provided the filename of the map as an argument
if len(sys.argv) != 2:
    print("Usage: python3 adventure.py <map_file>")
    sys.exit(1)


player_state = PlayerState()
game_state = GameState(sys.argv[1])

def start_game():
    player_state = PlayerState()
    previous_room_name = None
    command = ""
    #game loop
    while True:
        # Print the current room's description
        
        room = game_state.get_room()
        if room is not None and "win_condition" in game_state.map_data and (game_state.win_condition["item"] in player_state.inventory) and (room["name"] == game_state.win_condition["room"]):
            items = game_state.win_condition["item"]
            print(f"Congratulations, you have won the game by fighting with boss with {items}!")
            break
        elif room is not None and "win_condition" in game_state.map_data and(game_state.win_condition["item"] not in player_state.inventory) and (room["name"] == game_state.win_condition["room"]):
            print("Better Luck Next time , you loose the game!")
            items = game_state.win_condition["item"]
            print(f"You loose game because you don't have {items} to fought with Boss" )
            break
                                                                              
        if previous_room_name is not None and room['name'] == previous_room_name:
               None
        else:
            print("> " +room['name']+"\n")
            print(room['desc'])
            # Print the available exits
            print("")
            print(game_state.get_exit_list(player_state))
            if 'items' in room:
                if room['items']:
                    print("")
                    print("Items in the room: " + ", ".join(room['items']))
        previous_room_name = room['name']
        game_state.set_previous_room(room) 
        # Get user input
        try:
            command = input("\nWhat would you like to do? ").lower()
            print("")
        except EOFError:
            print("Use 'quit' to exit.")
        except KeyboardInterrupt:
            print("\nProgram interrupted by user.")
            print("Thanks for playing!")
            sys.exit(0)
        # Process user input
        if command in ["quit","q","qu","qui"]:
            print("Thanks for playing!")
            sys.exit(0)
        elif command in ["help","h","he","hel"]:
            print(" We can run the following commands : \n Go... \n Get... \n Drop... \n Inventory \n Look \n Quit \n.......................")
        
        elif command in ["look","l","loo","lo"]:
            print(room['name'])
            print(room['desc'])
            # Print the available exits
            print("")
            print(game_state.get_exit_list(player_state))
            if 'items' in room:
                if room['items']:
                    print("")
                    print("Items in the room: " + ", ".join(room['items']))
        elif command.startswith("go ") or command.startswith("go"):
            item = command[3:]
            try:
                if item in room['exits']:
                    if game_state.move_player(item, player_state):
                        room = game_state.get_room()
                        if 'lock' in room  and room['lock'] == item:
                            player_state.unlocked_doors[room['name']] = True
                            
                elif len(item)==0:
                    print("Sorry, you need to 'go' somewhere.")
                else :
                    closest_match = get_close_matches(item, room['exits'].keys(), n=5, cutoff=0.1)
                    if len(closest_match) > 1:
                        match_found = False
                        while True:
                            if len(closest_match) > 1:
                                matches = [match for match in closest_match if all(char in match for char in item)]
                                if len(item) <= len(closest_match[0]):
                                    if len(matches) == 1:
                                        if game_state.move_player(closest_match[0], player_state):
                                            room = game_state.get_room()
                                            if 'lock' in room and room['lock'] == closest_match[0]:
                                                player_state.unlocked_doors[room['name']] = True
                                        break
                                    elif len(matches) > 1:
                                        print(f"Did you want to go {' or '.join(matches)}?")
                                        break
                                    else :
                                        print(f"There's no way to go'{item}'.")
                                        break
                                else:
                                    print(f"There's no way to go '{item}'.")
                                    break
                            else:
                                print(f"There's no way to go '{item}'.")
                    elif len(closest_match)== 1 :
                        if len(item) <= len(closest_match[0]):
                            if game_state.move_player(closest_match[0], player_state):
                                room = game_state.get_room()
                                if 'lock' in room and room['lock'] == closest_match:
                                    player_state.unlocked_doors[room['name']] = True
                        else :
                            print(f"There's no way to go '{item}'.")
                    else:
                        print(f"There's no way to go '{item}'.")
            except KeyError:
                    print("There was an error accessing the items in this room.")
                    
        #direction becomes verb
        elif not any(command.startswith(s) for s in ("g","go","inventory","i","in","inv","inve","inven","invent","invento","inventor","quit","q","qu","qui","look","l","loo","lo","help","h","he","hel")):
            item = command
            try:
                if item in room['exits']:
                    if game_state.move_player(item, player_state):
                        room = game_state.get_room()
                        if 'lock' in room  and room['lock'] == item:
                            player_state.unlocked_doors[room['name']] = True
                            
                elif len(item)==0:
                    print("Sorry, you need to 'go' somewhere.")
                else :
                    closest_match = get_close_matches(item, room['exits'].keys(), n=5, cutoff=0.1)
                    if len(closest_match) > 1:
                        match_found = False
                        while True:
                            if len(closest_match) > 1:
                                matches = [match for match in closest_match if all(char in match for char in item)]
                                if len(item) <= len(closest_match[0]):
                                    if len(matches) == 1:
                                        if game_state.move_player(closest_match[0], player_state):
                                            room = game_state.get_room()
                                            if 'lock' in room and room['lock'] == closest_match[0]:
                                                player_state.unlocked_doors[room['name']] = True
                                        break
                                    elif len(matches) > 1:
                                        print(f"Did you want to go {' or '.join(matches)}?")
                                        break
                                    else :
                                        print(f"There's no way to go'{item}'.")
                                        break
                                else:
                                    print(f"There's no way to go '{item}'.")
                                    break
                            else:
                                print(f"There's no way to go '{item}'.")
                    elif len(closest_match)== 1 :
                        if len(item) <= len(closest_match[0]):
                            if game_state.move_player(closest_match[0], player_state):
                                room = game_state.get_room()
                                if 'lock' in room and room['lock'] == closest_match:
                                    player_state.unlocked_doors[room['name']] = True
                        else :
                            print(f"There's no way to go '{item}'.")
                    else:
                        print(f"There's no way to go '{item}'.")
            except KeyError:
                    print("There was an error accessing the items in this room.")
            
            
        elif command.startswith("get "):
            item = command[4:]
            try:
                if item in room['items']:
                    player_state.add_item(item)
                    room['items'].remove(item)
                    print(f"You pick up the {item}.") 
                elif len(item)==0:
                    print("Sorry, you need to 'get' something.")
                else :
                    closest_item = get_close_matches(item, room['items'], n=5, cutoff=0.1)
                    if len(closest_item) > 1:
                        item_found = False
                        while True:
                            if len(closest_item) > 1:
                                matches = [match for match in closest_item if all(char in match for char in item)]
                                if len(item) <= len(closest_item[0]):
                                    if len(matches) == 1:
                                        player_state.add_item(closest_item[0])
                                        room['items'].remove(closest_item[0])
                                        print(f"You pick up the {closest_item[0]}.")
                                        break
                                    elif len(matches) > 1:
                                        print(f"Did you want to go {' or '.join(matches)}?")
                                        break
                                    else :
                                        print(f"There's no '{item}' anywhere.")
                                        break
                                else :
                                    print(f"There's no '{item}' anywhere.")
                                    break
                                        
                    elif len(closest_item)== 1:
                        if len(item) <= len(closest_item[0]):
                            player_state.add_item(closest_item[0])
                            room['items'].remove(closest_item[0])
                            print(f"You pick up the {closest_item[0]}.")
                        else:
                            print(f"There's no '{item}' anywhere.")
            except KeyError:
                    print("There was an error accessing the items in this room.")
    
        elif command.startswith("drop "):
            item = command[5:]
            try:
                if item in player_state.inventory:
                    player_state.remove_item(item)
                    room['items'].append(item)
                    print(f"You drop the {item}.")
                else:
                    print("You do not have that item.")
            except KeyError:
                print("There was an error accessing your inventory.")
        elif command in ["inventory","i","in","inv","inve","inven","invent","invento","inventor"]:
            item = command[5:]
            try:
                inventory = player_state.get_inventory()
                if len(inventory) == 0:
                    print("You do not have any items in inventory")
                else:
                    print(player_state.get_inventory())
            except KeyError:
                print("There was an error accessing your inventory.")
        else:
            print("Invalid command.")

#menu for game
def Menu():
    command = None
    print("Main Menu")
    print(" Start \n Help \n Quit \n")
    try:
        command = input("Select one Option? ").lower()
    except EOFError:
        print("Use 'quit' to exit.")
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
        print("Thanks for playing!")
        sys.exit(0)
    if command in ["start","s","st","sta","star"]:
        print("")
        start_game()
    elif command in ["quit","q","qu","qui"]:
        print("Thanks for playing!")
    elif command in ["help","h","he","hel"]:
        print(" We can run the following commands : \n Go... \n Get... \n Drop... \n Inventory \n Look \n Quit \n....................... ")
        Menu()
    else:
        Menu()


Menu()
