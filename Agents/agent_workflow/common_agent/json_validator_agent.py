from Agents.agent_workflow.base_agent.base_agent import BaseAgent
from Agents.agent_workflow.common_agent.common_agents_prompt import Prompt

base_agent_obj=BaseAgent()
prompt_obj=Prompt()

json_validator_agent=base_agent_obj.create_assistant_agent(name='json_validator_agent',system_message=prompt_obj.json_validator_agent_prompt)


"""
async def test_json_validator(response):
    decoder = json.JSONDecoder()
    try:
        obj, idx = decoder.raw_decode(response)
        response=obj
        medicines=PrescriptionExtractor(**obj)
        print(f'VALID or ```VALID``` Json & data, {response}')
    except (json.JSONDecodeError,ValidationError) as e:
        print(f'ERROR or ```ERROR``` Invalid Json or Data, {e}')

asyncio.run(test_json_validator(response))
"""