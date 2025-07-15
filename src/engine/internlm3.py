import transformers
import torch
from abc import abstractmethod
from .base_engine import Engine
from utils.register import register_class, registry

from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import AutoTokenizer
from vllm import LLM, SamplingParams
import torch,time


@register_class(alias="Engine.InternLM3")
class InternLM3Engine(Engine):
    _instance = None 
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            print("Creating new InternLM3Engine instance", flush=True)
            cls._instance = super(InternLM3Engine, cls).__new__(cls)
            cls._instance._initialized = False
        else:
            print("Reusing existing InternLM3Engine instance", flush=True)
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        
        self.model_path = "/tmp/Mistral-7B-Instruct-v0.3/Mistral-7B-Instruct-v0.3"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.sampling_params = SamplingParams(temperature=0, max_tokens=16384)
        self.llm = LLM(
            model = self.model_path, 
            dtype = torch.float16, 
            gpu_memory_utilization = 0.9, 
            max_model_len=16384
            )
        print(f"Initialized LLM with tensor parallel size: {torch.cuda.device_count()}", flush=True)

    def get_response(self, messages):
        retry = 0
        
        while retry < 5:
            try:
                text = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
                input_tokens = self.tokenizer.encode(text)
                outputs = self.llm.generate([text], self.sampling_params)
                for output in outputs:
                    generated_text = output.outputs[0].text
                    response = generated_text
                return response
            except Exception as e:
                print(f"Error occurred: {e}")
                retry += 1
                time.sleep(10)