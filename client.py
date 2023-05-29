import socket
import threading

def receive_messages(client_socket):
    # Receive and print messages from the server
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            print("[!] : ", data)
        except ConnectionResetError:
            break

# Create a client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the server address and port
server_address = ('localhost', 1234)

# Connect to the server
client_socket.connect(server_address)
print("Connected to the server.")

# Start a new thread to receive messages from the server
receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
receive_thread.start()

# Send messages to the server
while True:
    message = input()
    if message == 'quit':
        break
    client_socket.send(message.encode())

# Clean up the socket
client_socket.close()
