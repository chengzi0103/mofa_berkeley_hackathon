import socket

def send_message(sock, message):
    """Send an arbitrary-sized string over a socket."""
    message = message.encode('utf-8')  # Encode the string into bytes
    message_length = len(message)
    sock.sendall(f"{message_length:<10}".encode('utf-8'))  # Send header with fixed length
    sock.sendall(message)  # Send the actual message

def receive_message(sock):
    """Receive an arbitrary-sized string over a socket."""
    header = sock.recv(10).decode('utf-8')  # Read the 10-byte header
    if not header:
        return None
    message_length = int(header.strip())  # Get the message length from the header
    data = b""
    while len(data) < message_length:
        chunk = sock.recv(message_length - len(data))
        if not chunk:
            break
        data += chunk
    return data.decode('utf-8')  # Decode the bytes into a string

def start_client(host='localhost', port=12345):
    """Start the client to connect to the server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((host, port))
        print(f"Connected to server at {host}:{port}")
        while True:
            message = input("You: ")
            send_message(client, message)
            if message.lower() == "exit":
                print("Connection closed.")
                break
            response = receive_message(client)
            print(f"Server: {response}")

if __name__ == "__main__":
    start_client()
