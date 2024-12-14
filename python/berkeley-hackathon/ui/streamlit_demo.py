from typing import Callable
import streamlit as st

import socket

def send_message(sock, message: str):
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
    sock = None
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((host, port))
        print(f"Connected to server at {host}:{port}")
        sock = client
    return sock
        # while True:
        #     message = input("You: ")
        #     send_message(client, message)
        #     if message.lower() == "exit":
        #         print("Connection closed.")
        #         break
        #     response = receive_message(client)
        #     print(f"Server: {response}")

# Socket connection setup (persistent for the session)
if "socket" not in st.session_state:
    st.session_state.socket = start_client()

def response_prompt(prompt: str):
    send_message(st.session_state.socket, prompt)
    return receive_message(st.session_state.socket)

def display_chat_history():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    for message in st.session_state.chat_history:
        msg = st.chat_message(message["role"])
        msg.write(message["message"])

def handle_chat(message_callback: Callable[[], str], role: str = "user"):
    message = ""
    # display an animation when waiting for the bot to respond here
    message_container = st.chat_message(role)
    with st.spinner("Bot is typing..."):
        message = message_callback()
    message_container.write(message)
    st.session_state.chat_history.append({"role": role, "message": message})

def handle_chat_str(message: str, role="user"):
    handle_chat(lambda: message, role)

st.title("Shopping Agent UI")

prompt = st.chat_input("Say something")

if prompt:
    display_chat_history()
    handle_chat_str(prompt)
    handle_chat(lambda: response_prompt(prompt), role="bot")


