import asyncio
from Agents.agent_workflow.prescription_workflow.prescription_workflow_agents import workflow,invalid_content
from .valid_prescriptions import valid_content
from .invalid_prescriptions import invalid_contents

#print(invalid_contents)

asyncio.run(workflow(valid_content))
