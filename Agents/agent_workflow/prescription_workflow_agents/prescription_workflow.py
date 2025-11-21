from demo import name
from agent_workflow.base_agent.base_agent import BaseAssistantAgent
print(type(BaseAssistantAgent))
print(name)

# from agent_workflow.base_agent.base_agent import BaseAssistantAgent
# from autogen_agentchat.messages import TextMessage
# from autogen_core import CancellationToken
# import asyncio


# input_validator_agent=BaseAssistantAgent(name='input_validator_agent',system_message='You are helpful assistant.')
# prescription_extracter_agent=BaseAssistantAgent(name='prescription_extracter_agent',system_message='You are helpful assistant.')

# async def observe_agent_run()->None:
#     task=TextMessage(content='What is name of capital and official language of India? and what is current whether of that city?',source='User')
#     cancellation_token=CancellationToken()
#     result=await input_validator_agent.on_messages(messages=[task],cancellation_token=cancellation_token)
#     print(result.inner_messages)
#     print('\n\n\n')
#     print(result.chat_message)
# asyncio.run(observe_agent_run())
