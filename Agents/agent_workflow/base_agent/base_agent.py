from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.models.ollama import OllamaChatCompletionClient
import os
from dotenv import load_dotenv
load_dotenv()
api_key=os.getenv('OPENAI_API_KEY')


class BaseAgent:
    def __init__(self):
        self.model_client=BaseAgent.create_model_client()
  
    def create_assistant_agent(self,name,system_message,**kwargs)->AssistantAgent:
        return AssistantAgent(
            name=name,
            system_message=system_message,
            model_client=self.model_client,
            **kwargs)
    @classmethod
    def create_model_client(cls):
        model_client = OpenAIChatCompletionClient(
            base_url='https://openrouter.ai/api/v1',
            model='nvidia/nemotron-nano-12b-v2-vl:free',
            api_key=api_key,
            model_info={"family": "nvidia", "name": "nemotron-nano-12b-v2-vl", "provider": "OpenRouter","vision":True,"function_calling":True,"json_output":True,"structured_output":True})
        return model_client
    # @classmethod
    # def create_model_client(cls):
    #     model_client = OllamaChatCompletionClient(
    #         base_url="http://127.0.0.1:11434",
    #         model='qwen3-4b',
    #         model_info={"family": "qwen", "name": "qwen3-4b", "provider": "OpenRouter","vision":True,"function_calling":True,"json_output":True,"structured_output":True})
    #     return model_client


# other_parms={"reflect_on_tool_use":True}
# obj=BaseAssitantAgent(name='demo',system_message='Yor are helpful assistant',**other_parms)
