import json
from openai import OpenAI
from requests.exceptions import ConnectionError, Timeout, RequestException
import os

# Set vllm serve api and url
vllm_api_url = {
    'base_url': "http://localhost:8888/v1",
    "api_key": "EMPTY"
}

# Set OpenAI api and url
api_key = 'YOUR_API_KEY'
api_base = 'YOUR_API_BASE'

os.environ['OPENAI_API_KEY'] = api_key
os.environ['OPENAI_API_BASE'] = api_base

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def load_jsonl(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))
    return data

def save_json(data, save_path):
    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def get_completion(prompt, history, flag):
    client = OpenAI(api_key=api_key,
                    base_url=api_base)
    max_retries = 3
    for attempt in range(max_retries):
        try:
            SYSTEM_PROMPT = """你是一个得力的助手。"""
            messages = []
            messages.append({'role': 'system', "content": SYSTEM_PROMPT})
            if history != []:
                for h in history:
                    messages.append({'role':'user',"content":h[0]})
                    messages.append({'role':'assistant',"content":h[1]})
            else:
                messages.append({'role':'user',"content":prompt})
        
            if flag == 1:
                chat_completion = client.chat.completions.create(
                    messages=messages,
                    model="gpt-4o-2024-08-06",
                    response_format={"type": "json_object"},
                    max_tokens=4096,
                    temperature=0
                    )
            else:
                chat_completion = client.chat.completions.create(
                    messages=messages,
                    model="gpt-4o-2024-08-06",
                    max_tokens=4096,
                    temperature=0
                    )
            
            response = chat_completion.choices[0].message.content
            history.append((prompt, response))
            return response, history
        
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