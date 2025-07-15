


from transformers import AutoTokenizer, AutoModelForCausalLM
from vllm import LLM, SamplingParams
import torch
import os
from abc import abstractmethod
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))

parent_dir = os.path.dirname(current_dir)

sys.path.append(parent_dir)

from utils.register import register_class
from utils.utils_func import vllm_api_url
from .base_engine import Engine
import time
import torch._dynamo
import json
from openai import OpenAI
from requests.exceptions import ConnectionError, Timeout, RequestException
import os




torch._dynamo.config.suppress_errors = True

@register_class(alias="Engine.qwen3_32B")
class qwen3_32BEngine(Engine):
    _instance = None 

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            print("Creating new qwen3_32BEngine instance", flush=True)
            cls._instance = super(qwen3_32BEngine, cls).__new__(cls)
            cls._instance._initialized = False
        else:
            print("Reusing existing qwen3_32BEngine instance", flush=True)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        
        self.model_path = "Qwen3-32B"
        self.api_key = vllm_api_url['api_key']
        self.base_url = vllm_api_url['base_url']
        
        self.client = OpenAI(
            api_key = self.api_key,
            base_url = self.base_url
        )
       
    def get_response(self, messages):
        max_retries = 3
        for attempt in range(max_retries):
            try:
                chat_completion = self.client.chat.completions.create(
                    messages=messages,
                    model="Qwen3-32B",
                    max_tokens=None,
                    temperature=0.0
                    )

                response = chat_completion.choices[0].message.content
                return response
            
            except (ConnectionError, Timeout) as e:
                print(f"Network error occurred: {e}. Retrying {attempt + 1}/{max_retries}...")
                if attempt == max_retries - 1:
                    raise
                
            except RequestException as e:
                print(f"An error occurred: {e}.")
                raise 
            
            except Exception as e:
                print(e)
                
        return "Unable to get a response after several attempts."
