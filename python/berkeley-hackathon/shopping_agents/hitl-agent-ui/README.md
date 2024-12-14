# Hitl Agent

This is the Hitl Agent for the Berkeley Hackathon.

## Running the agent

To run the agent, you can use the following command in the terminal:

```bash
git clone https://github.com/chengzi0103/mofa_berkeley_hackathon
cd mofa_berkeley_hackathon/python/berkeley-hackathon/shopping_agents
dora up
dora build shopping_dataflow.yml
dora start shopping_dataflow.ymlshopping_dataflow.yml
```

Open a new terminal and run the following command to start the agent:

```bash
hitl-agent
```

And the last step is to start the agent using the `streamlit` command in the terminal.

```bash
cd mofa_berkeley_hackathon/python/berkeley-hackathon/ui
streamlit run socket_client.py
```
