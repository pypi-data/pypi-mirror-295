from gai.lib.common.generators_utils import chat_string_to_list
from gai.lib.common.logging import getLogger
logger = getLogger(__name__)

import os
from gai.lib.common.utils import get_gai_config, get_gai_url
from dotenv import load_dotenv
load_dotenv()
from gai.ttt.client.completions import Completions

class TTTClient:

    # config is either a string path or a component config
    def __init__(self, config=None):
        if config is str or config is None:
            self.config=get_gai_config(file_path=config)
            self.config = self.config["clients"]["ttt-gai"]
            self.url = get_gai_url("ttt")
        else:
            self.config = config
            self.url = config["url"]
            # override the environment variable for Completion to use
            os.environ["TTT_URL"] = self.url

        from openai import OpenAI
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))
        self.client = Completions.PatchOpenAI(client, override_url=self.url)

    def __call__(self, 
                 messages:str|list, 
                 stream:bool=True, 
                 max_new_tokens:int=None, 
                 max_tokens:int=None, 
                 temperature:float=None, 
                 top_p:float=None, 
                 top_k:float=None,
                 json_schema:dict=None,
                 tools:list=None,
                 tool_choice:str=None,
                 stop_conditions:list=None,
                 timeout:float=None):

        if isinstance(messages, str):
            messages = chat_string_to_list(messages)

        response = self.client.chat.completions.create(model="exllamav2-mistral7b",
                    messages=messages,
                    stream=stream,
                    max_new_tokens=max_new_tokens,
                    temperature=temperature,
                    top_p=top_p,
                    top_k=top_k,
                    json_schema=json_schema,
                    tools=tools,
                    tool_choice=tool_choice,
                    stop_conditions=stop_conditions,
                    timeout=timeout)
        if stream:
            def streamer():
                for chunk in response:
                    yield chunk
            return streamer()
        return response

