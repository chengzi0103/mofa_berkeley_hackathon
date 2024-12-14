import socket
import time
from typing import Callable
import streamlit as st

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

def response_prompt(prompt: str):
    send_message(st.session_state.sock, prompt)
    return receive_message(st.session_state.sock)

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

def cleanup_socket():
    """Cleanup the socket connection."""
    if "sock" in st.session_state and st.session_state.sock:
        try:
            send_message(st.session_state.sock, "exit")  # Notify the server
            st.session_state.sock.close()
        except Exception as e:
            st.warning(f"Error while closing socket: {e}")
        finally:
            del st.session_state.sock
            st.session_state.connected = False
            st.warning("Disconnected from the server.")

# This function will initialize the connection and clean up if session is reloaded
def check_connection():
    if "connected" not in st.session_state:
        st.session_state.connected = False
        st.session_state.sock = None
    # If page is refreshed and there's an active connection, disconnect it
    if not st.session_state.get("_is_fresh", False):
        st.session_state["_is_fresh"] = True
        cleanup_socket()

def main():
    st.title("Shopping Agent UI")
    server_ip = "127.0.0.1"
    server_port = 12345

    check_connection()

    if "connected" not in st.session_state:
        st.session_state.connected = False

    if not st.session_state.connected:
        try:
            st.session_state.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            st.session_state.sock.connect((server_ip, server_port))
            st.session_state.connected = True
        except Exception as e:
            st.error(f"Connection failed: {e}")

    if st.session_state.connected:
        prompt = st.chat_input("Say something")

        if prompt:
            display_chat_history()
            handle_chat_str(prompt)
            handle_chat(lambda: response_prompt(prompt), role="bot")
    else:
        st.error("Please ensure that the server is running and try again.")


if __name__ == "__main__":
    try:
        main()
    except:
        cleanup_socket()
