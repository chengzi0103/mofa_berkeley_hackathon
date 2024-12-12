import json
import os
from dora import Node, DoraStatus
import pyarrow as pa
from mofa.kernel.utils.util import load_agent_config, load_dora_inputs_and_task, create_agent_output
from mofa.run.run_agent import run_dspy_agent, run_crewai_agent, run_dspy_or_crewai_agent
from mofa.utils.files.dir import get_relative_path
from mofa.utils.log.agent import record_agent_result_log


class Operator:
    def on_event(
        self,
        dora_event,
        send_output,
    ) -> DoraStatus:
        if dora_event["type"] == "INPUT":
            flag = dora_event["value"][0].as_py()[:3]
            text = dora_event["value"][0].as_py()[3:]
            # Normal task
            if flag[-1] in [' ', 'C']:
                task = dora_event["value"][0].as_py() + "analyse the text and provide a summary"
                yaml_file_path = get_relative_path(current_file=__file__, sibling_directory_name='configs', target_file_name='agent.yml')
                inputs = load_agent_config(yaml_file_path)
                inputs["task"] = task
                agent_result = run_dspy_or_crewai_agent(agent_config=inputs)
                record_agent_result_log(agent_config=inputs,
                                        agent_result={
                                            "1, "+ inputs.get('log_step_name', "Step_one"): {task:agent_result}})
                send_output("agent_comm", pa.array([create_agent_output(step_name='agent_response', output_data="CAC" + agent_result,dataflow_status=os.getenv('IS_DATAFLOW_END',True))]),dora_event['metadata'])
                print('agent_response:', agent_result)
            # Feedback task
            elif flag[-1] == '^':
                send_output("agent_response", pa.array([create_agent_output(step_name='agent_response', output_data='CA ' + 'task received: ' + text,dataflow_status=os.getenv('IS_DATAFLOW_END',True))]),dora_event['metadata'])

        return DoraStatus.CONTINUE