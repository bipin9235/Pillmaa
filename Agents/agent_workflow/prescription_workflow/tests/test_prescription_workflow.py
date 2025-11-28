import asyncio
from Agents.agent_workflow.prescription_workflow.prescription_workflow_agents import workflow
from autogen_core import Image as AGImage
from PIL import Image
from io import BytesIO

# to run: python -m Agents.agent_workflow.prescription_workflow.tests.test_prescription_workflow

#valid_path=f'/workspaces/Pillmaa/Agents/agent_workflow/prescription_workflow/tests/Prescriptions/Valid_text/{i}'
#invalid_input_path=f'/workspaces/Pillmaa/Agents/agent_workflow/prescription_workflow/tests/Prescriptions/invalid_text/{i}'
#valid_images=f'/workspaces/Pillmaa/Agents/agent_workflow/prescription_workflow/tests/Prescriptions/Valid_image/{i}'

for i in range(1,6):
    path=f'C:/Users/bipikuma/OneDrive - Capgemini/Documents/Learnings/GenAI/Pillmaa/Agents/agent_workflow/prescription_workflow/tests/Prescriptions/Valid_text/{i}'
    with open(file=path+'.txt',mode='r') as file:
        content=file.read()
        asyncio.run(workflow(input_content=content,path=path))

# for i in range(7,8):
#     path=f'/workspaces/Pillmaa/Agents/agent_workflow/prescription_workflow/tests/Prescriptions/Valid_image/{i}'
#     pil_image = Image.open(path+'.png')
#     ag_image=AGImage(pil_image)
#     #print(pil_image)

#     asyncio.run(workflow(input_content=ag_image,path=path))


"""
Feedback to be implemented:
1. include "duration" field in output josn(pydanticModel)
2. remove drug category field from output json(pydanticModel)
3. dose/no. of capsule/ml or anything to be captured in output json(pydanticModel)
"""

import os
current_dir = os.getcwd()

print("Current Working Directory:", current_dir)
