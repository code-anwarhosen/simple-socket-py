import socket
import threading

def handle_client(client_socket, client_address):
    # Receive and broadcast messages from the client
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            print(f"[{client_address}] : ", data)
            broadcast(data, client_socket)
        except ConnectionResetError:
            break
    
    # Client has disconnected
    print("Client", client_address, "disconnected")
    client_socket.close()

def broadcast(message, sender_socket):
    # Send the message to all connected clients except the sender
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode())
            except socket.error:
                # Client connection broken
                client.close()
                remove_client(client)

def remove_client(client_socket):
    # Remove the client from the list of clients
    if client_socket in clients:
        clients.remove(client_socket)

# Create a server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the server address and port
server_address = ('localhost', 1234)

# Bind the server socket to the server address and port
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(5)
print("Server is listening for connections...")

# List to store connected clients
clients = []

# Accept and handle incoming connections
while True:
    client_socket, client_address = server_socket.accept()
    clients.append(client_socket)
    print("Connected to client:", client_address)

    # Start a new thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()

    if input() == "stop":
        break

# Close all client sockets
for client_socket in clients:
    client_socket.close()

# Close the server socket
server_socket.close()