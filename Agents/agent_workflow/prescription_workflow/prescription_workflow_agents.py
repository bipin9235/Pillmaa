import json

import autogen_core
from Agents.agent_workflow.base_agent.base_agent import BaseAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from .prescription_workflow_agents_prompt import Prompt
from Agents.agent_workflow.common_agent.json_validator_agent import json_validator_agent
from Agents.pydantic_models.prescription_extractor_model import PrescriptionModel
import asyncio
from autogen_agentchat.ui import Console
from pydantic import ValidationError
from autogen_agentchat.teams import RoundRobinGroupChat,SelectorGroupChat,Swarm
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.messages import StructuredMessage
from autogen_agentchat.messages import TextMessage,MultiModalMessage



base_agent_obj=BaseAgent()
prompt_obj=Prompt()

def fetch_drug()->list:
    """Fetch the matching drug_names list from database to confirm it's existing and a valid medicine."""
    with open('/workspaces/Pillmaa/Agents/agent_workflow/prescription_workflow/prescription.json','r') as file:
        raw=json.load(file)
        data=json.loads(raw)
        #print(data)

    #print(type(data))
    drug_names = [medicine["drug_name"] for medicine in data["medicines"]]

    #print(drug_names)
    import sqlite3

    # # Your extracted list
    # drug_names = ["Cefixime", "Paracetamol", "Vitamin C"]

    # Connect to your SQLite database
    conn = sqlite3.connect("pharma.db")
    cursor = conn.cursor()

    existing_names = []

    for name in drug_names:
        # Use LIKE for partial matching
        cursor.execute("SELECT medicine_name FROM drugs WHERE medicine_name LIKE ?", (f"%{name}%",))
        results = cursor.fetchall()
        existing_names.extend([row[0] for row in results])

    conn.close()

    print("Matched drug names in DB:", existing_names)
    return existing_names

def validate_and_write_json(input:str|dict)->str:
    """Write the output to file. This function validate if input is valid json or not."""
    try:
        decoder = json.JSONDecoder()
        input = str(input).replace("'", '"')
        obj, idx = decoder.raw_decode(input)
        user = PrescriptionModel(**obj)
        print("Found JSON & Validated with its' PydanticModel", obj)
        with open("/workspaces/Pillmaa/Agents/agent_workflow/prescription_workflow/prescription.json", "w") as f:
            f.write(user.model_dump_json(indent=4))
    except Exception as e:
        print('Error occured!',e)
    return obj

# with open('/workspaces/Pillmaa/Agents/agent_workflow/prescription_workflow/prescription.json','r') as file:
#         #raw=json.load(file)
#         data=json.load(file)
#         #print(data)
# validate_and_write_json(data)


input_validator_agent=base_agent_obj.create_assistant_agent('input_validator_agent',prompt_obj.input_validator_agent_prompt,description='Handles input prescription validating')

prescription_extractor_agent=base_agent_obj.create_assistant_agent('prescription_extractor_agent',prompt_obj.prescription_extractor_agent_prompt,description='Handles generating json of prescribed medicines.',reflect_on_tool_use=True,output_content_type=PrescriptionModel)

final_output_validator_agent=base_agent_obj.create_assistant_agent('final_output_validator_agent',prompt_obj.final_output_validator_agent_prompt,reflect_on_tool_use=True,description='Handles validating final json prescrition with database.')


# valid_content="""
#     Dr. Kavita Sharma, MBBS, MD (General Medicine)
#     Reg. No: MCI/DL/2025/67890
#     Lotus Care Clinic, New Delhi
#     Phone: +91-9812345678
#     Patient: Rohan Mehta
#     Age/Gender: 45 / Male
#     Date: 22/11/2025

#     Rx:
#     - Cefixime 200 mg 
#     - Paracetamol 500 mg – Oral, one tablet every 6 hours as needed for fever (max 4 tablets/day)
#     - Vitamin C 1000 mg – Oral, once daily for 10 days

#     Diagnosis: Upper respiratory tract infection
#     Advice: Drink plenty of fluids, rest, avoid cold exposure
#     Follow-up: Review after 1 week
#     Signature:
#     Dr. Kavita Sharma
#     """
# invalid_content="""
#     Dr. Arvind Patel, MBBS
#     Green Valley Clinic, Pune
#     Phone: +91-9876543210
#     Patient: Sneha
#     Age/Gender: 29 / Female
#     Date: 22/11/2025

#     Rx:
#     (No medicine details provided — only patient and doctor info)
#     """

# async def teams_run(input_content):
#     task=TextMessage(content=input_content,source='User')
#     cancellation_token=CancellationToken()
#     termination_condition=TextMentionTermination('DONE') or TextMentionTermination('INVALID')
    
#     teams=SelectorGroupChat(
#         participants=[input_validator_agent,prescription_extractor_agent,final_output_validator_agent],
#         termination_condition=termination_condition,
#         custom_message_types=[StructuredMessage[PrescriptionModel]],
#         model_client=BaseAgent.create_model_client(),
#         selector_prompt="""
#         Final goal is to validate input doctors prescription, extract drug/prescription and validate it with existing drugs in database. Select the most appropriate agent to handel the task.
#         {roles}
        
#         Current conversation context:
#         {history}

#         Select one agent from {participants} to handle the task.
#         A valid json prescrition always starts with input validation, medicine/drug details extraction and final json validation.
#             """
#     )

#     await Console(teams.run_stream(task=task,cancellation_token=cancellation_token))
#     # response=result.messages[-1].content
#     # prescription: PrescriptionModel = response
#     # json_output = prescription.model_dump_json(indent=2)
#     # print('Final Response',json_output)
#     # with open('output.json','w') as file:
#     #     json.dump(json_output,file)
#     await teams.reset()

# #asyncio.run(teams_run(valid_content))

async def workflow(input_content,path=None):
    print('----------------User Input---------------------')
    if isinstance(input_content,autogen_core._image.Image):
        task=MultiModalMessage(content=[input_content],source='user')
    else:
        task=TextMessage(content=input_content,source='user')
        print(input_content)
    if path is None:
        path='/workspaces/Pillmaa/Agents/agent_workflow/prescription_workflow/tests/Prescriptions/prescription.json'
    else:
        path=path+'_output.json'
    input_valid_flag=None
    result1=None
    json_written_flag=False
    while True:
        if input_valid_flag==None:
            result1=await input_validator_agent.run(task=task,cancellation_token=CancellationToken())
            result1=result1.messages[-1].content
            print('----------------Input Validator---------------------')
            print(result1)
            #input_validator_agent.on_reset()
        
        if not 'INVALID' in result1 or input_valid_flag:
            input_valid_flag=True
            result2=await prescription_extractor_agent.run(task=task,cancellation_token=CancellationToken())
            response=result2.messages[-1].content
            prescription: PrescriptionModel = response
            #prescription_extractor_agent.on_reset()
            json_output = prescription.model_dump_json(indent=4)
            with open(path, "w") as f:
                f.write(json_output)
            json_written_flag=True
            print('----------------Prescription Extracter---------------------')
            print(json_output)
        else:
            with open(path, "w") as f:
                json.dump({"input":"Invalid"},f)
            print('Input Invalid')
            return 'Input Invalid'
        if json_written_flag:
            result3=await final_output_validator_agent.run(task=task,cancellation_token=CancellationToken())
            response=result3.messages[-1].content
            #final_output_validator_agent.on_reset()
            print('----------------Final Output Validator---------------------')
            print(response)
            if 'DONE' in response.upper():
                print('Final result generated')
                return 'Done'
            else:
                json_written_flag=False
                continue
# asyncio.run(workflow(invalid_content))
        

        





    
