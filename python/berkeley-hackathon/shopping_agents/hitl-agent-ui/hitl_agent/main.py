import argparse
import json
import os
import ast
import sys

# import click
import pyarrow as pa
from dora import Node
from pycparser.c_ast import While

from mofa.utils.install_pkg.load_task_weaver_result import extract_important_content

RUNNER_CI = True if os.getenv("CI") == "true" else False

import socket

class Click:

    def __init__(self):
        self.msg = ""
        self.start_server()

    def echo(self, message):
        self.msg += message + "\n"

    def input(self, prompt: str, send=True):
        if send:
            Click.send_message(self.conn, self.msg)
        self.msg = ""
        return Click.receive_message(self.conn)
    
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

    def start_server(self, host='127.0.0.1', port=12345):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(5)  # Allow 5 connections to queue
        print(f"Server running on {host}:{port}...")
        self.server_socket = server_socket
        conn, addr = server_socket.accept()
        print(f"Connected by {addr}")
        self.conn = conn

click = Click()

def clean_string(input_string:str):
    return input_string.encode('utf-8', 'replace').decode('utf-8')
def send_task_and_receive_data(node):
    shopping_requirement_status = False
    shopping_planning_status = False
    while True:
        data = click.input(
            " Send You Task :  ",
            send=False
        )
        node.send_output("user_input", pa.array([clean_string(data)]))
        event = node.next(timeout=200)
        if event is not None:
            while True:
                if event is not None:

                    if shopping_requirement_status is False:
                        while True:
                            if event['id'] == "user_shopping_requirement_status":
                                node_results = json.loads(event['value'].to_pylist()[0])
                                results = node_results.get('node_results')
                                is_dataflow_end = node_results.get('dataflow_status', False)

                                if 'yes' in results or 'Yes' in results:
                                    click.echo("Please wait, we are generating a shopping plan.  /n")
                                    shopping_requirement_status = True
                                    break
                                else:
                                    click.echo(results)

                                    data = click.input(
                                        " Shopping Requirement Suggestions :  ",
                                    )
                                    node.send_output("user_input", pa.array([clean_string(data)]))
                            event = node.next(timeout=200)
                    if shopping_planning_status is False:
                        while True:

                            if event['id'] == "shopping_planning_status":
                                node_results = json.loads(event['value'].to_pylist()[0])
                                results = node_results.get('node_results')

                                if 'yes' in results or 'Yes' in results:
                                    click.echo("This is the final shopping assembly plan.")
                                    click.echo("results")

                                    click.echo("Please wait, we are go to web search .")
                                    shopping_planning_status = True
                                    break
                                else:
                                    click.echo(results)

                                    data = click.input(
                                        " Agent Shopping Plan Suggestions:  ",
                                    )
                                    node.send_output("user_input", pa.array([clean_string(data)]))
                            event = node.next(timeout=200)

                    node_results = json.loads(event['value'].to_pylist()[0])
                    results = node_results.get('node_results')
                    dataflow_end = node_results.get('dataflow_status', False)

                    if dataflow_end == False:
                        click.echo(f"{node_results.get('step_name', '')}: {results} ", )
                    else:
                        click.echo(f"{node_results.get('step_name', '')}: {results} :dataflow_status", )
                    sys.stdout.flush()
                    if dataflow_end:
                        break
                        # if results.get("post_list",None) is not None:
                        #     extract_important_content(results)
                        # else:
                        #     click.echo(f"{node_results.get('step_name','')}: {results} :dataflow_status",)
                    sys.stdout.flush()
                    event = node.next(timeout=200)
def main():

    # Handle dynamic nodes, ask for the name of the node in the dataflow, and the same values as the ENV variables.
    parser = argparse.ArgumentParser(description="Simple arrow sender")

    parser.add_argument(
        "--name",
        type=str,
        required=False,
        help="The name of the node in the dataflow.",
        default="hitl-agent",
    )
    parser.add_argument(
        "--data",
        type=str,
        required=False,
        help="Arrow Data as string.",
        default=None,
    )

    args = parser.parse_args()

    data = os.getenv("DATA", args.data)

    node = Node(
        args.name
    )  # provide the name to connect to the dataflow if dynamic node

    # if data is None and os.getenv("DORA_NODE_CONFIG") is None:
    send_task_and_receive_data(node)


if __name__ == "__main__":
    main()
