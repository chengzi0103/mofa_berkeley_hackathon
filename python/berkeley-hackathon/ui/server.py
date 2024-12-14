import socket

def send_message(conn, message):
    """Send an arbitrary-sized string over a socket connection."""
    message = message.encode('utf-8')  # Encode the string into bytes
    message_length = len(message)
    conn.sendall(f"{message_length:<10}".encode('utf-8'))  # Send header with fixed length
    conn.sendall(message)  # Send the actual message

def receive_message(conn):
    """Receive an arbitrary-sized string over a socket connection."""
    header = conn.recv(10).decode('utf-8')  # Read the 10-byte header
    if not header:
        return None
    message_length = int(header.strip())  # Get the message length from the header
    data = b""
    while len(data) < message_length:
        chunk = conn.recv(message_length - len(data))
        if not chunk:
            break
        data += chunk
    return data.decode('utf-8')  # Decode the bytes into a string

def start_server(host='localhost', port=12345):
    """Start the server to handle client connections."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((host, port))
        server.listen(1)
        print(f"Server is listening on {host}:{port}")
        
        conn, addr = server.accept()
        with conn:
            print(f"Connection established with {addr}")
            while True:
                message = receive_message(conn)
                if not message or message.lower() == "exit":
                    print("Connection closed by client.")
                    break
                print(f"Client: {message}")
                response = input("You: ")
                send_message(conn, response)

if __name__ == "__main__":
    start_server()
