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
    }
}

def place_gold_in_rooms(rooms):
    candidate_rooms = [room for room in rooms.keys() if room != "start"]
    rooms_with_gold = random.sample(candidate_rooms, 2)
    for room in rooms_with_gold:
        gold_amount = random.randint(10, 50)
        rooms[room]["gold"] = gold_amount

place_gold_in_rooms(rooms)
def main():
    print("Server is listening...")
    while True:
        client, addr = server.accept()
        print(f"Connected with {addr}")
        client_thread = threading.Thread(target=handle_client, args=(client,))
        client_thread.start()

if __name__ == "__main__":
    main()