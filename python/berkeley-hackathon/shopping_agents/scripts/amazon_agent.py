import json
import os
from dora import Node, DoraStatus
import pyarrow as pa
from mofa.utils.ai.conn import create_openai_client
from mofa.kernel.utils.util import load_agent_config, create_agent_output, load_node_result
from core.web_search.amazon import amazon_crawler_with_selenium
from core.web_search.util import shopping_html_structure
from dotenv import load_dotenv
class Operator:
    def __init__(self):
        self.task = None


    def on_event(
            self,
            dora_event,
            send_output,
    ) -> DoraStatus:
        if dora_event["type"] == "INPUT":
            if dora_event['id'] == 'web_search_task':
                all_results = []
                self.task = json.loads(load_node_result(dora_event["value"][0].as_py()))
                llm_client = create_openai_client()
                print('-------: ',self.task)
                web_search_tasks = list(self.task.values())
                for web_search_text in web_search_tasks:
                    html_context = amazon_crawler_with_selenium(web_search_text)
                    web_result = shopping_html_structure(llm_client=llm_client,html_content=html_context,search_text=web_search_text)
                    all_results.append(web_result)
                print(" shopping_result  :  ",all_results)
                send_output("amazon_shopping_result", pa.array([create_agent_output(step_name='shopping_result',
                                                                               output_data=all_results,
                                                                               dataflow_status=os.getenv(
                                                                                   'IS_DATAFLOW_END', True))]),
                            dora_event['metadata'])

        return DoraStatus.CONTINUE