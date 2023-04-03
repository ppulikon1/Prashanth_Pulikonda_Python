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
        self.visited_rooms = set()
        



    def get_room(self):
        return self.map_data[self.current_room]

    def move_player(self, direction, player_state):
        next_room_id = self.map_data[self.current_room]['exits'].get(direction)
 

         
        next_room_index = next_room_id
        
        next_room = self.map_data[next_room_index]
        
        if next_room_index in self.visited_rooms:
            None
           # print("You have been here before.")
        else:
           # print(next_room['desc'])
            self.visited_rooms.add(next_room_index)

        self.current_room = next_room_index
        
        return True

    
    def get_exit_list(self, player_state):
        exit_list = "Exits: "
        room = self.get_room()
        if 'locked_doors' in room:
            for direction, destination in room['exits'].items():
                if direction in room['locked_doors']:
                    if direction in player_state.unlocked_doors:
                        exit_list += f"{direction} "
                    else:
                        exit_list += f"{direction} (locked), "
                else:
                    exit_list += f"{direction} "
        else:
            for direction, destination in room['exits'].items():
                exit_list += f"{direction} "
        return exit_list.rstrip()


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
            return "You're not carrying anything."
        else:
            items = sorted(self.inventory)  # sort the items alphabetically
            output = "Inventory:\n"
            for i, item in enumerate(items):
                if i == 0:
                    output += f"  {item}"
                else:
                    output += f"\n  {item}"
            return output        

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
        
                                                         
        if previous_room_name is not None and room['name'] == previous_room_name:
               None
        else:
            print("> " +room['name'])
            print("")
            print(room['desc'])
            # Print the available exits
            print("")
            if 'items' in room:
                if room['items']:
                    print("Items: " + ", ".join(room['items']))
                    print("")
            print(game_state.get_exit_list(player_state))
            print("")

        if room['name']== "A blue room":
            win = "flower"
            loose = "bomb"
            if win in player_state.inventory and loose not in player_state.inventory:
                print("Congrats you win the game")
                sys.exit(1)
            elif loose in player_state.inventory and win not in player_state.inventory:
                print("You loos the game better luck next time!")
                sys.exit(1)
            elif win and loose in player_state.inventory:
                print(f" Choose {win} or {loose} to drop it will decide your winning! so chooseWisely!")
            
        previous_room_name = room['name']
        game_state.set_previous_room(room) 
        # Get user input
        try:
            command = input("What would you like to do? ").lower()
        except EOFError:
            print("Use 'quit' to exit.")
        except KeyboardInterrupt:
            print("^CTraceback (most recent call last):")
            print("  ...")
            print("KeyboardInterrupt")
            sys.exit(0)
        # Process user input
        if command in ["quit","q","qu","qui"]:
            print("Goodbye!")
            sys.exit(0)
        elif command in ["help","h","he","hel"]:
            print(" You can run the following commands:\n   go...\n   get...\n   drop...\n   look\n   inventory\n   quit\n   help")
        
        elif command in ["look","l","loo","lo"]:
            print("> " +room['name'])
            print("")
            print(room['desc'])
            # Print the available exits
            print("")
            if 'items' in room:
                if room['items']:
                    print("Items: " + ", ".join(room['items']))
                    print("")
            print(game_state.get_exit_list(player_state))
            print("")
        elif command.startswith("go ") or command.startswith("go"):
            item = command[3:]
            if item in room['exits']:
                if game_state.move_player(item, player_state):
                    room = game_state.get_room()
                    print(f"You go {item}.\n")
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
                                    #if game_state.move_player(closest_match[0], player_state):
                                    room = game_state.get_room()
                                    mathcing = matches[0]
                                    print(f"You go {mathcing}.\n")
                                    game_state.move_player(mathcing,player_state)
                                    
                                    break
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
                            #print(f"You go {closest_match[0]}\n")
                            close = closest_match[0]
                            print(f"You go {close}.\n")
                            if 'lock' in room and room['lock'] == closest_match:
                                player_state.unlocked_doors[room['name']] = True
                    else :
                        print(f"There's no way to go '{item}'.")
                else:
                    print(f"There's no way to go '{item}'.")
##            try:
                
            #except KeyError:
                    #print("There was an error accessing the items in this room.")
                    
        #direction becomes verb
        elif not any(command.startswith(s) for s in ("g","go","inventory","i","in","inv","inve","inven","invent","invento","inventor","quit","q","qu","qui","look","l","loo","lo","help","h","he","hel","drop","d","dr","dro","get","ge")):
            item = command
            try:
                if item in room['exits']:
                    if game_state.move_player(item, player_state):
                        room = game_state.get_room()
                        print(f"You go {item}.\n")
                        if 'lock' in room  and room['lock'] == item:
                            player_state.unlocked_doors[room['name']] = True
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
                                            mathcing =matches[0]
                                            print(f"You go {mathcing}.\n")
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
                                close = closest_match[0]
                                print(f"You go {close}.\n")
                                if 'lock' in room and room['lock'] == closest_match:
                                    player_state.unlocked_doors[room['name']] = True
                        else :
                            print(f"There's no way to go '{item}'.")
                    else:
                        if not EOFError:
                                print(f"There's no way to go '{item}'.")
                        else :
                            print("Use 'quit' to exit.")
                        
            except KeyError:
                    print("There was an error accessing the items in this room.")
            
            
        elif command.startswith("get "):
            item = command[4:]
            if 'items' in room and item in room['items']:
                player_state.add_item(item)
                room['items'].remove(item)
                print(f"You pick up the {item}.")
            elif 'items' not in room:
                room['items'] = []
                print(f"There's no {item} anywhere.")
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
                                    sorted_matches = sorted(matches)
                                    match_string = ", ".join(sorted_matches[:-1]) + f", or the {matches[-1]}"
                                    match_string = match_string.replace(", or", " or")
                                    print(f"Did you want to get the {match_string}?")
                                    break
                                else :
                                    print(f"There's no {item} anywhere.")
                                    break
                            else :
                                print(f"There's no {item} anywhere.")
                                break
                                        
                elif len(closest_item)== 1:
                    if len(item) <= len(closest_item[0]):
                        player_state.add_item(closest_item[0])
                        room['items'].remove(closest_item[0])
                        print(f"You pick up the {closest_item[0]}.")
                    else:
                        print(f"There's no {item} anywhere.")
                else :
                    print(f"There's no {item} anywhere.")

            #try:
            
            #except KeyError:
                    #print("There was an error accessing the items in this room.")
    
        elif command.startswith("drop "):
            item = command[5:]
            try:
                if item in player_state.inventory:
                    player_state.remove_item(item)
                    if 'items' in room:
                        room['items'].append(item)
                    else:
                        room['items'] = [item]
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
                    print("You're not carrying anything.")
                else:
                    print(player_state.get_inventory())
            except KeyError:
                print("There was an error accessing your inventory.")
        else:
            print("Invalid command.")
start_game()
