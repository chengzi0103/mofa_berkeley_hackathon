import argparse
import json
import os
import ast
import sys

import click
import pyarrow as pa
from dora import Node
from mofa.utils.install_pkg.load_task_weaver_result import extract_important_content

RUNNER_CI = True if os.getenv("CI") == "true" else False




def clean_string(input_string:str):
    return input_string.encode('utf-8', 'replace').decode('utf-8')
def send_task_and_receive_data(node):
    while True:
        data = input(
            " Send You Task :  ",
        )
        node.send_output("data", pa.array([clean_string(data)]))
        event = node.next(timeout=200)
        if event is not None:
            while True:
                if event is not None:
                    node_results = json.loads(event['value'].to_pylist()[0])
                    results = node_results.get('node_results')
                    is_dataflow_end = node_results.get('dataflow_status', False)
                    if is_dataflow_end == False:
                        try:
                            results_dict = json.loads(results)
                            if results_dict.get("post_list",None) is not None:
                                extract_important_content(results_dict)
                            else:
                                click.echo(f"{node_results.get('step_name','')}: {results} ",)
                        except:
                            click.echo(f"{node_results.get('step_name','')}: {results} ",)

                        # if results.get("post_list",None) is not None:
                        #     extract_important_content(results)
                        # else:
                        #     click.echo(f"{node_results.get('step_name','')}: {results} ",)
                    else:
                        try:
                            results_dict = json.loads(results)
                            if results_dict.get("post_list", None) is not None:
                                extract_important_content(results_dict)
                                click.echo(":dataflow_status")
                            else:
                                click.echo(f"{node_results.get('step_name', '')}: {results} :dataflow_status", )
                        except Exception:
                            click.echo(f"{node_results.get('step_name', '')}: {results} :dataflow_status", )
                        # if results.get("post_list",None) is not None:
                        #     extract_important_content(results)
                        # else:
                        #     click.echo(f"{node_results.get('step_name','')}: {results} :dataflow_status",)
                    sys.stdout.flush()
                    if is_dataflow_end:
                        feedback = input("Do you want to give feedback? (y/n) ")
                        if feedback.lower() == "y":
                            feedback_text = input("Enter your feedback: ")
                            node.send_output("feedback", pa.array([clean_string(feedback_text)]))
                        else:
                            break
                    event = node.next(timeout=200)
def main():

    # Handle dynamic nodes, ask for the name of the node in the dataflow, and the same values as the ENV variables.
    parser = argparse.ArgumentParser(description="Simple arrow sender")

    parser.add_argument(
        "--name",
        type=str,
        required=False,
        help="The name of the node in the dataflow.",
        default="terminal-input",
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

    if data is None and os.getenv("DORA_NODE_CONFIG") is None:
        send_task_and_receive_data(node)


if __name__ == "__main__":
    main()
