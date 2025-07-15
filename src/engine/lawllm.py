
from transformers import AutoTokenizer
from vllm import LLM, SamplingParams
import torch
import os
from abc import abstractmethod
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from utils.register import register_class
from .base_engine import Engine
import time
import torch._dynamo


torch._dynamo.config.suppress_errors = True

@register_class(alias="Engine.lawllm")
class LawLLMEngine(Engine):
    _instance = None 

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            print("Creating new LawLLMEngine instance", flush=True)
            cls._instance = super(LawLLMEngine, cls).__new__(cls)
            cls._instance._initialized = False
        else:
            print("Reusing existing LawLLMEngine instance", flush=True)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        
        self.model_path = "/remote-home/zjia/LawLLM-Qwen2.5-7B"
        self.sampling_params = SamplingParams(temperature=0, max_tokens=16384)

        print("Loading LLM model...", flush=True)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.llm = LLM(
            model=self.model_path,
            tensor_parallel_size=torch.cuda.device_count(),  
            dtype=torch.float16,                            
            gpu_memory_utilization=0.9,               
            trust_remote_code=True,
            max_model_len=16384,                           
            enforce_eager=False                           
        )

        print(f"Initialized LLM with tensor parallel size: {torch.cuda.device_count()}", flush=True)

    def get_response(self, messages):
        retry = 0
        while retry < 5:
            try:
                prompt = self.tokenizer.apply_chat_template(
                    messages,
                    tokenize=False,
                    add_generation_prompt=True
                )
                input_tokens = self.tokenizer.encode(prompt)
                if len(input_tokens) > 16384:
                    print(f"Input too long: {len(input_tokens)} tokens (max 16384). Stopping dialogue.")
                    return None  
                outputs = self.llm.generate(prompt, self.sampling_params)
                
                for output in outputs:
                    generated_text = output.outputs[0].text
                    response = generated_text.strip()
                torch.cuda.empty_cache() 

                return response
            
            except Exception as e:
                print(f"Error occurred: {e}", flush=True)
                retry += 1
                time.sleep(10) 

        response = "Failed to generate response after multiple retries."
        return response