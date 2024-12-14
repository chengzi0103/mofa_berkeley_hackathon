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

agents = {
    "A": "to_term",
    "B": "to_agent",
    "C": "to_agent_2"
}
agent_names = {
    v: k for k, v in agents.items()
}

def clean_string(input_string:str):
    return input_string.encode('utf-8', 'replace').decode('utf-8')
def send_task_and_receive_data(node):
    while True:
        data = input(
            " Send You Task :  ",
        )
        node.send_output("data", pa.array(["AB " + clean_string(data)]))
        event = node.next(timeout=200)
        if event is not None:
            from_agent = ""
            return_agent = ""
            answer = ""
            while True:
                if event is not None:
                    node_results = json.loads(event['value'].to_pylist()[0])
                    results = node_results.get('node_results')
                    is_dataflow_end = node_results.get('dataflow_status', False)
                    current_from_agent = node_results.get('step_name','')
                    
                    if is_dataflow_end == False:
                        try:
                            results_dict = json.loads(results)
                            if results_dict.get("post_list",None) is not None:
                                extract_important_content(results_dict)
                            else:
                                if current_from_agent == "agent_comm":
                                    results = str(results)
                                    from_agent = agents[results[0]]
                                    return_agent = agents[results[-1]] if results[-1] in agents else ""
                                    results = results[3:]
                                    answer = results
                                    click.echo(f"{from_agent}: {results} ",)
                                else:
                                    click.echo(f"{current_from_agent}: {results} ",)
                        except:
                            if current_from_agent == "agent_comm":
                                results = str(results)
                                from_agent = agents[results[0]]
                                return_agent = agents[results[-1]] if results[-1] in agents else ""
                                results = results[3:]
                                answer = results
                                click.echo(f"{from_agent}: {results} ",)
                            else:
                                click.echo(f"{current_from_agent}: {results} ",)

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
                                # click.echo(f"{current_from_agent}: {results} :dataflow_status", )
                                if current_from_agent == "agent_comm":
                                    results = str(results)
                                    from_agent = agents[results[0]]
                                    return_agent = agents[results[-1]] if results[-1] in agents else ""
                                    results = results[3:]
                                    answer = results
                                    click.echo(f"{from_agent}: {results} :dataflow_status", )
                                else:
                                    click.echo(f"{current_from_agent}: {results} :dataflow_status", )
                        except Exception:
                            # click.echo(f"{current_from_agent}: {results} :dataflow_status", )
                            if current_from_agent == "agent_comm":
                                results = str(results)
                                from_agent = agents[results[0]]
                                return_agent = agents[results[-1]] if results[-1] in agents else ""
                                results = results[3:]
                                answer = results
                                click.echo(f"{from_agent}: {results} :dataflow_status", )
                            else:
                                click.echo(f"{current_from_agent}: {results} :dataflow_status", )
                        # if results.get("post_list",None) is not None:
                        #     extract_important_content(results)
                        # else:
                        #     click.echo(f"{node_results.get('step_name','')}: {results} :dataflow_status",)
                    sys.stdout.flush()
                    if is_dataflow_end:
                        feedback = input("Do you want to give feedback? (y/n) ")
                        if feedback.lower() == "y":
                            feedback_text = input("Enter your feedback: ")
                            feedback_text = clean_string('The original question was: ' + data + 'The original answer was: ' + answer + '. My feedback is: ' + feedback_text + '. Returning to the original question, give me a new answer according to my feedback.')
                            if from_agent != "":
                                from_target_agent = agent_names[from_agent]
                                if return_agent != "":
                                    return_target_agent = agent_names[return_agent]
                                    data_sent = "A"+return_target_agent+return_target_agent+feedback_text
                                    node.send_output("data", pa.array([clean_string(data_sent)]))
                                    return_agent = ""
                                    from_agent = ""
                                else:
                                    data_sent = "A"+from_target_agent+from_target_agent+feedback_text
                                    node.send_output("data", pa.array([clean_string()]))
                                    from_agent = ""
                        else:
                            if from_agent != "":
                                target_agent = agent_names[from_agent]
                                node.send_output("data", pa.array([clean_string("A"+target_agent+'^'+feedback_text)]))
                                from_agent = ""
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
