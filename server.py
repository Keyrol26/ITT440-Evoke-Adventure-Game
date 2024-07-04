import socket
import random
import threading

SERVER = "127.0.0.1"
PORT = 65432
ADDRESS = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)
server.listen()

rooms = {
    "start": {
        "description": "You are in a starting room. There is a door to the north.",
        "north": "hall"
    },
    "hall": {
        "description": "You are in a hall. There are doors to the south, east, and west.",
        "south": "start",
        "east": "kitchen",
        "west": "library"
    },
    "kitchen": {
        "description": "You are in a kitchen. There is a door to the west.",
        "west": "hall"
    },
    "library": {
        "description": "You are in a library. There are doors to the north, east, and the treasure room to the west.",
        "north": "garden",
        "east": "hall",
        "west": "treasure_room"
    },
    "garden": {
        "description": "You are in a beautiful garden. There is a door to the south.",
        "south": "library"
    },
    "treasure_room": {
        "description": "You are in a room filled with treasure! There is a question to answer.",
        "question": "How many genders are there in this world? Enter a number.",
        "answer": "2",
        "diamond_collected": "not yet"
    }
}

def place_gold_in_rooms(rooms):
    candidate_rooms = [room for room in rooms.keys() if room != "start"]
    rooms_with_gold = random.sample(candidate_rooms, 2)
    for room in rooms_with_gold:
        gold_amount = random.randint(10, 50)
        rooms[room]["gold"] = gold_amount

place_gold_in_rooms(rooms)

def get_title(gold, diamond_collected):
    if diamond_collected == "collected":
        if gold >= 100:
            return "Diamond Collector and Master Treasure Hunter"
        elif gold >= 50:
            return "Diamond Collector and Expert Adventurer"
        elif gold >= 20:
            return "Diamond Collector and Novice Explorer"
        else:
            return "Diamond Collector and Beginner"
    else:
        if gold >= 100:
            return "Master Treasure Hunter"
        elif gold >= 50:
            return "Expert Adventurer"
        elif gold >= 20:
            return "Novice Explorer"
        else:
            return "Beginner"

def handle_client(client):
    current_room = "start"
    inventory = {"gold": 0, "diamond_collected": "not yet"}

    def send_message(message):
        client.send(message.encode("utf-8"))

    def receive_message():
        return client.recv(1024).decode("utf-8").strip().lower()

    intro_message = """
    ******************************
    *    Welcome to EVOKE        *
    *    Adventure Game!         *
    ******************************
    
    Objective:
    Explore the rooms and collect as much gold as possible.
    Find the treasure room and answer the question to collect a diamond!
    
    Commands:
    - look: Check your surroundings
    - collect: Collect rewards in the room
    - inventory: Check your inventory
    - north, south, east, west: Move between rooms
    - quit: Exit the game
    
    ******************************
    """
    send_message(intro_message)
    send_message("What's your name?")
    player_name = receive_message().title()

    send_message(f"Hello, {player_name}! Click buttons to navigate or type 'quit' to exit.\n")

    while True:
        command = receive_message()
        print(f"Received command: {command}")

        if command == "look":
            room_desc = rooms[current_room]["description"]
            if "gold" in rooms[current_room]:
                room_desc += f" You see {rooms[current_room]['gold']} gold coins here."
            if current_room == "treasure_room" and rooms["treasure_room"]["diamond_collected"] == "not yet":
                room_desc += " There is a diamond here."
            send_message(room_desc)

        elif command == "collect":
            if current_room == "treasure_room" and rooms["treasure_room"]["diamond_collected"] == "not yet":
                send_message(rooms["treasure_room"]["question"])
                answer = receive_message()
                if answer.strip() == rooms["treasure_room"]["answer"]:
                    inventory["diamond_collected"] = "collected"
                    rooms["treasure_room"]["diamond_collected"] = "collected"
                    send_message("Correct answer! You collected a diamond!")
                else:
                    send_message("Incorrect answer. The diamond remains in the room.")
            elif "gold" in rooms[current_room]:
                gold_amount = rooms[current_room].pop("gold")
                inventory["gold"] += gold_amount
                send_message(f"You collected {gold_amount} gold coins! Your inventory: {inventory}")
            else:
                send_message("There is nothing to collect in this room.")

        elif command == "inventory":
            send_message(f"Your inventory: {inventory}")

        elif command in ["north", "south", "east", "west"]:
            if command in rooms[current_room]:
                current_room = rooms[current_room][command]
                send_message(f"You moved {command}. {rooms[current_room]['description']}")
            else:
                send_message("You can't go that way.")

        elif command == "quit":
            total_gold = inventory.get("gold", 0)
            title = get_title(total_gold, inventory["diamond_collected"])
            send_message(f"Thank you for playing, {player_name}! This is your total gold collected: {total_gold}. You earned the title: {title}. Goodbye!")
            break

        else:
            send_message("Invalid command. Try 'look', 'north', 'south', 'east', 'west', 'collect', or 'quit'.")

    client.close()

def main():
    print("Server is listening...")
    while True:
        client, addr = server.accept()
        print(f"Connected with {addr}")
        client_thread = threading.Thread(target=handle_client, args=(client,))
        client_thread.start()

if __name__ == "__main__":
    main()