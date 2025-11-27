import json

import autogen_core
from Agents.agent_workflow.base_agent.base_agent import BaseAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from .schedular_workflow_agents_prompt import Prompt
from Agents.pydantic_models.schedular_model import Prescription
import asyncio
from autogen_agentchat.ui import Console
from autogen_agentchat.messages import TextMessage



base_agent_obj=BaseAgent()
prompt_obj=Prompt()


schedular_agent=base_agent_obj.create_assistant_agent('schedular_agent',prompt_obj.schedular_agent_prompt,output_content_type=Prescription)

async def main(input_json:str)->None:
    #task=TextMessage(content=str(input_json),sources="User")
    termination=TextMentionTermination('TERMINATE')
    await Console(schedular_agent.run_stream(task=str(input_json),cancellation_token=CancellationToken()))



path=f'/workspaces/Pillmaa/Agents/agent_workflow/prescription_workflow/tests/Prescriptions/Valid_text/2_output.json'
with open(file=path,mode='r') as file:
    data=json.load(file)
    print(type(data))
    #print(data)
asyncio.run(main(str(data)))



#activate env: source .venv/bin/activate
#to run this file: python -m Agents.agent_workflow.schedular_workflow.schedular_workflow_agents





    
