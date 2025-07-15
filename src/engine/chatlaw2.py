from transformers import AutoTokenizer, AutoModel, AutoModelForCausalLM
from abc import abstractmethod
import time
from .base_engine import Engine
from utils.register import register_class, registry
import torch


@register_class(alias="Engine.Chatlaw2")
class Chatlaw2Engine(Engine):
    _instance = None  # 单例实例

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            print("Creating new Chatlaw2Engine instance", flush=True)
            cls._instance = super(Chatlaw2Engine, cls).__new__(cls)
            cls._instance._initialized = False
        else:
            print("Reusing existing Chatlaw2Engine instance", flush=True)
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        
        self.model_path = "/tmp/chatlaw2/ChatLaw2_plain_7B"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path, trust_remote_code=True)
        self.model = AutoModel.from_pretrained(self.model_path, trust_remote_code=True).half().cuda()

        print(f"Initialized LLM with tensor parallel size: {torch.cuda.device_count()}", flush=True)
        
    def get_response(self, messages):
        retry = 0
        while retry < 5:
            try:
                tokenized_chat = self.tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True, return_tensors="pt").cuda()
                generated_ids = self.model.generate(tokenized_chat, max_new_tokens=16348, temperature=0.0).cuda()
                generated_ids = [
                    output_ids[len(input_ids):] for input_ids, output_ids in zip(tokenized_chat, generated_ids)
                ]
                prompt = self.tokenizer.batch_decode(tokenized_chat)[0]
                response = self.tokenizer.batch_decode(generated_ids)[0]

                return response
            except Exception as e:
                print(f"Error occurred: {e}")
                retry += 1
                time.sleep(10)