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

def start_server(host='127.0.0.1', port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)  # Allow 5 connections to queue
    print(f"Server running on {host}:{port}...")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connection established with {addr}")
        try:
            while True:
                client_message = receive_message(conn)
                if client_message.lower() == 'exit':
                    print("Client disconnected.")
                    break
                print(f"Client: {client_message}")

                # Get server input from the console
                server_response = input("You: ")
                send_message(conn, server_response)

                if server_response.lower() == 'exit':
                    print("Closing connection...")
                    break
        finally:
            conn.close()
            server_socket.close()

if __name__ == "__main__":
    start_server()
