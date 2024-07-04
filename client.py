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


if __name__ == "__main__":
    create_ui()
