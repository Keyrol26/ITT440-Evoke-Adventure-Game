import socket
import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading

SERVER = "127.0.0.1"
PORT = 65432
ADDRESS = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)

def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            text_area.insert(tk.END, message + "\n")
            text_area.yview(tk.END)
            if "Goodbye" in message:
                # Extract title from the message
                title = message.split(":")[-1].strip()
                # Show a message box with goodbye message and title
                messagebox.showinfo("Game Over", f"{message}\nYour Title: {title}")
                client.close()
                root.quit()
                break
            elif "Enter a number" in message:
                show_number_buttons()
            else:
                hide_number_buttons()
        except Exception as e:
            print(f"Connection lost. Error: {e}")
            client.close()
            break
			
def show_number_buttons():
    number_frame.pack()

def hide_number_buttons():
    number_frame.pack_forget()

def send_command(command):
    client.send(command.encode("utf-8"))

def send_name():
    player_name = name_entry.get()
    if player_name:
        send_command(player_name)
        name_entry.delete(0, tk.END)
        name_frame.pack_forget()
        game_frame.pack()

def create_ui():
    global text_area, name_entry, name_frame, game_frame, number_frame, root

    root = tk.Tk()
    root.title("Evoke Adventure Game")

    name_frame = tk.Frame(root)
    name_frame.pack()

    name_label = tk.Label(name_frame, text="Enter your name:")
    name_label.pack(side=tk.LEFT, padx=5, pady=5)

    name_entry = tk.Entry(name_frame)
    name_entry.pack(side=tk.LEFT, padx=5, pady=5)

    name_button = tk.Button(name_frame, text="Start", command=send_name)
    name_button.pack(side=tk.LEFT, padx=5, pady=5)

    game_frame = tk.Frame(root)

    text_area = scrolledtext.ScrolledText(game_frame, wrap=tk.WORD, width=50, height=20)
    text_area.pack(pady=10)

    button_frame = tk.Frame(game_frame)
    button_frame.pack()

    btn_look = tk.Button(button_frame, text="Look", command=lambda: send_command("look"))
    btn_look.grid(row=0, column=0, padx=5, pady=5)

    btn_collect = tk.Button(button_frame, text="Collect", command=lambda: send_command("collect"))
    btn_collect.grid(row=0, column=1, padx=5, pady=5)

    btn_inventory = tk.Button(button_frame, text="Inventory", command=lambda: send_command("inventory"))
    btn_inventory.grid(row=0, column=2, padx=5, pady=5)

    btn_north = tk.Button(button_frame, text="North", command=lambda: send_command("north"))
    btn_north.grid(row=1, column=1, padx=5, pady=5)

    btn_west = tk.Button(button_frame, text="West", command=lambda: send_command("west"))
    btn_west.grid(row=2, column=0, padx=5, pady=5)

    btn_south = tk.Button(button_frame, text="South", command=lambda: send_command("south"))
    btn_south.grid(row=2, column=1, padx=5, pady=5)

    btn_east = tk.Button(button_frame, text="East", command=lambda: send_command("east"))
    btn_east.grid(row=2, column=2, padx=5, pady=5)

    btn_quit = tk.Button(button_frame, text="Quit", command=lambda: send_command("quit"))
    btn_quit.grid(row=3, column=1, padx=5, pady=5)

    number_frame = tk.Frame(game_frame)

    number_buttons = []
    for num in range(1, 6):
        btn_num = tk.Button(number_frame, text=str(num), command=lambda n=num: send_command(str(n)))
        btn_num.grid(row=0, column=num-1, padx=5, pady=5)
        number_buttons.append(btn_num)

    number_frame.pack()

    game_frame.pack()

    threading.Thread(target=receive_messages, daemon=True).start()
    
    root.mainloop()

if __name__ == "__main__":
    create_ui()
