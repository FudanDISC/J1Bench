from transformers import AutoTokenizer
from vllm import LLM, SamplingParams
from abc import abstractmethod
import time
import torch
from .base_engine import Engine
from utils.register import register_class, registry


@register_class(alias="Engine.Gemma12B")
class Gemma12BEngine(Engine):
    _instance = None 

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            print("Creating new Gemma12BEngine instance", flush=True)
            cls._instance = super(Gemma12BEngine, cls).__new__(cls)
            cls._instance._initialized = False
        else:
            print("Reusing existing Gemma12BEngine instance", flush=True)
        return cls._instance
    
    def __init__(self): 
        if self._initialized:
            return
        self._initialized = True
        
        self.model_path = "/tmp/gemma12B/gemma-3-12b-it"
        self.sampling_params = SamplingParams(
            temperature=0,
            max_tokens=16384,
        )
        
        print("Loading LLM model with vLLM...", flush=True)
        self.llm = LLM(
            model=self.model_path,
            tensor_parallel_size=torch.cuda.device_count(),
            dtype=torch.bfloat16,
            gpu_memory_utilization=0.9,
            trust_remote_code=True,
        )
        
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        print(f"Initialized vLLM engine with tensor parallel size: {torch.cuda.device_count()}", flush=True)
        
    def _format_messages(self, messages):
        """将消息格式化为vLLM需要的输入格式"""
        formatted = []
        for msg in messages:
            role = "user" if msg["role"] == "system" else msg["role"]
            content = msg["content"]
            if isinstance(content, list):
                text = next(item["text"] for item in content if item["type"] == "text")
            else:
                text = content
            formatted.append({"role": role, "content": text})
        return formatted
    
    def get_response(self, messages):
        retry = 0
        while retry < 5:
            try:
                formatted_messages = self._format_messages(messages)
                
                if formatted_messages[1]['role'] == 'user':
                    formatted_messages[1]['content'] = 'system: ' + formatted_messages[0]['content'] + '\n user: ' + formatted_messages[1]['content']
                    del formatted_messages[0]
                
                prompt = self.tokenizer.apply_chat_template(
                    formatted_messages,
                    add_generation_prompt=True,
                    tokenize=False
                )
                
                outputs = self.llm.generate(
                    prompts=[prompt],
                    sampling_params=self.sampling_params
                )
                
                generated_text = outputs[0].outputs[0].text
                return generated_text.strip()
                
            except Exception as e:
                print(f"Error occurred: {e}")
                retry += 1
                time.sleep(10)
                if retry >= 5:
                    raise RuntimeError("Failed after 5 retries")
        return None