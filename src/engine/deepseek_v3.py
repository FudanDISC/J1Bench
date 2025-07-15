import os
import openai
from openai import OpenAI
from utils.register import register_class
from .base_engine import Engine
import time
import re

def remove_think_blocks(text):
    cleaned_text = re.sub(r'<think>.*?</think>\n*', '', text, flags=re.DOTALL)
    return cleaned_text

@register_class(alias="Engine.deepseekv3")
class DeepseekEngine(Engine):
    def __init__(
        self, 
        openai_api_key, openai_api_base=None, openai_model_name="deepseek-chat", 
        temperature=0.0, max_tokens=16384
        ):
        openai_api_key = openai_api_key if openai_api_key is not None else os.environ.get("OPENAI_API_KEY")
        assert openai_api_key is not None, "openai_api_key is required" #方便调试直接找到问题根源
        openai_api_base = openai_api_base if openai_api_base is not None else os.environ.get("OPENAI_API_BASE")
        
        self.model_path = "deepseek-v3-0324"
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        if openai_api_base is not None:
            self.client = OpenAI(
                api_key=openai_api_key,
                base_url='https://api.ai-gaochao.cn/v1'
            )
        else:
            self.client = OpenAI(
                api_key=openai_api_key
            )
            
    def get_response(self, messages, flag=1):
        while True:
            try:
                model_path = self.model_path
                i = 0
                while i < 10:
                    try:
                        response = self.client.chat.completions.create(
                            model=model_path,
                            messages=messages,
                            temperature=self.temperature,
                            max_tokens=self.max_tokens
                        )
                        break
                    except openai.BadRequestError:
                        time.sleep(10)
                        i += 1
                    except openai.RateLimitError:
                        time.sleep(60)
                        i += 1
                    except Exception as e:
                        print(e)
                        i += 1
                        time.sleep(10)
                        continue
                return remove_think_blocks(response.choices[0].message.content)

            except:
                time.sleep(600)