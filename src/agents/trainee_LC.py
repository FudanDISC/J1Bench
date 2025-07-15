from .base_agent import Agent
from utils.register import register_class, registry
from collections import defaultdict
import re
import jsonlines
import json

@register_class(alias="Agent.Trainee.ConsultBase")
class Trainee_consult(Agent):
    def __init__(self, engine=None, trainee_info=None, name="A"):
        self.name = name
        self.trainee_greetings = "您好，我是您的法律顾问，请问有什么可以帮助您的？"
        self.engine = engine
        
        def default_value_factory():
            return [("system", self.system_prompt)]
        self.memories = defaultdict(default_value_factory)
    
    @staticmethod
    def add_parser_args(parser):
        pass
    
    def get_response(self, messages):
        response = self.engine.get_response(messages)
        return response

    def memorize(self, message, case_id):
        self.memories[case_id].append(message)
    
    def forget(self, case_id=None):
        def default_value_factory():
            return [("system", self.system_prompt)]
        if case_id is None:
            self.memories.pop(case_id)
        else:
            self.memories = defaultdict(default_value_factory)
            
    def speak(self, content, case_id, save_to_memory=True):
        memories = self.memories[case_id]

        messages = [{"role": memory[0], "content": memory[1]} for memory in memories]
        messages.append({"role": "user", "content": content})

        response = self.get_response(messages)

        self.memorize(("user", content), case_id)
        self.memorize(("assistant", response), case_id)

        return response
    

@register_class(alias="Agent.Trainee.LC_GPT")
class GPTTrainee_consult(Trainee_consult):
    def __init__(self, args=None, trainee_info=None, name="A"):
        engine = registry.get_class("Engine.GPT4o_1120")(
            openai_api_key=args.trainee_openai_api_key,
            openai_api_base=args.trainee_openai_api_base,
            openai_model_name=args.trainee_openai_model_name,
            temperature=args.trainee_temperature,
            max_tokens=args.trainee_max_tokens
        )
            
        with open("/root/J1Bench/src/agents/profiles.json", "r", encoding="utf-8") as f:
            profiles = json.load(f)
        
        
        
        if args.scenario == "J1Bench.Scenario.LC":
            system_prompt = ''
            profile = profiles["trainee_LC"]
            for p in profile:
                system_prompt += p + '\n'
            if system_prompt.endswith('\n'):
                system_prompt = system_prompt[:-1]
            self.system_prompt = system_prompt
        
        super(GPTTrainee_consult, self).__init__(engine, trainee_info, name)
    
    @staticmethod
    def add_parser_args(parser):
        parser.add_argument('--trainee_openai_api_key', type=str, help='API key for OpenAI')
        parser.add_argument('--trainee_openai_api_base', type=str, help='API base for OpenAI')
        parser.add_argument('--trainee_openai_model_name', type=str, help='API model name for OpenAI')
        parser.add_argument('--trainee_temperature', type=float, default=0, help='temperature')
        parser.add_argument('--trainee_max_tokens', type=int, default=16384, help='max tokens')

    def get_response(self, messages):
        response = self.engine.get_response(messages, flag=0)
        return response

    def speak(self, content, case_id, save_to_memory=True):
        memories = self.memories[case_id]

        messages = [{"role": memory[0], "content": memory[1]} for memory in memories]
        messages.append({"role": "user", "content": content})

        response = self.get_response(messages)

        self.memorize(("user", content), case_id)
        self.memorize(("assistant", response), case_id)

        return response


@register_class(alias="Agent.Trainee.LC_Qwen3_14B")
class Qwen3_14BTrainee_consult(Trainee_consult):
    def __init__(self, args=None, trainee_info=None, name="A"):
        engine = registry.get_class("Engine.qwen3_14B")()
            
        with open("/root/J1Bench/src/agents/profiles.json", "r", encoding="utf-8") as f:
            profiles = json.load(f)
        
        
        
        if args.scenario == "J1Bench.Scenario.LC":
            system_prompt = ''
            profile = profiles["trainee_LC"]
            for p in profile:
                system_prompt += p + '\n'
            if system_prompt.endswith('\n'):
                system_prompt = system_prompt[:-1]
            self.system_prompt = system_prompt
        
        super(Qwen3_14BTrainee_consult, self).__init__(engine, trainee_info, name)
    
    @staticmethod
    def add_parser_args(parser):
        parser.add_argument('--trainee_temperature', type=float, default=0, help='temperature')
        parser.add_argument('--trainee_max_tokens', type=int, default=16384, help='max tokens')
        parser.add_argument('--trainee_top_p', type=float, default=1, help='top p')
        parser.add_argument('--trainee_frequency_penalty', type=float, default=0, help='frequency penalty')
        parser.add_argument('--trainee_presence_penalty', type=float, default=0, help='presence penalty')

    def get_response(self, messages):
        response = self.engine.get_response(messages)
        return response

    def speak(self, content, case_id, save_to_memory=True):
        memories = self.memories[case_id]

        messages = [{"role": memory[0], "content": memory[1]} for memory in memories]
        messages.append({"role": "user", "content": content})

        response = self.get_response(messages)

        self.memorize(("user", content), case_id)
        self.memorize(("assistant", response), case_id)

        return response

@register_class(alias="Agent.Trainee.LC_Gemma12B")
class Gemma12BTrainee_consult(Trainee_consult):
    def __init__(self, args=None, trainee_info=None, name="A"):
        engine = registry.get_class("Engine.Gemma12B")()
            
        with open("/root/J1Bench/src/agents/profiles.json", "r", encoding="utf-8") as f:
            profiles = json.load(f)
        
        
        
        if args.scenario == "J1Bench.Scenario.LC":
            system_prompt = ''
            profile = profiles["trainee_LC"]
            for p in profile:
                system_prompt += p + '\n'
            if system_prompt.endswith('\n'):
                system_prompt = system_prompt[:-1]
            self.system_prompt = system_prompt
        
        super(Gemma12BTrainee_consult, self).__init__(engine, trainee_info, name)
    
    @staticmethod
    def add_parser_args(parser):
        parser.add_argument('--trainee_temperature', type=float, default=0, help='temperature')
        parser.add_argument('--trainee_max_tokens', type=int, default=16384, help='max tokens')
        parser.add_argument('--trainee_top_p', type=float, default=1, help='top p')
        parser.add_argument('--trainee_frequency_penalty', type=float, default=0, help='frequency penalty')
        parser.add_argument('--trainee_presence_penalty', type=float, default=0, help='presence penalty')

    def get_response(self, messages):
        response = self.engine.get_response(messages)
        return response

    def speak(self, content, case_id, save_to_memory=True):
        memories = self.memories[case_id]

        messages = [{"role": memory[0], "content": memory[1]} for memory in memories]
        messages.append({"role": "user", "content": content})

        response = self.get_response(messages)

        self.memorize(("user", content), case_id)
        self.memorize(("assistant", response), case_id)
        return response


@register_class(alias="Agent.Trainee.LC_Qwen3_32B")
class Qwen3_32BTrainee_consult(Trainee_consult):
    def __init__(self, args=None, trainee_info=None, name="A"):
        engine = registry.get_class("Engine.qwen3_32B")()
            
        with open("/root/J1Bench/src/agents/profiles.json", "r", encoding="utf-8") as f:
            profiles = json.load(f)
        
        
        
        if args.scenario == "J1Bench.Scenario.LC":
            system_prompt = ''
            profile = profiles["trainee_LC"]
            for p in profile:
                system_prompt += p + '\n'
            if system_prompt.endswith('\n'):
                system_prompt = system_prompt[:-1]
            self.system_prompt = system_prompt
        
        super(Qwen3_32BTrainee_consult, self).__init__(engine, trainee_info, name)
    
    @staticmethod
    def add_parser_args(parser):
        parser.add_argument('--trainee_temperature', type=float, default=0, help='temperature')
        parser.add_argument('--trainee_max_tokens', type=int, default=16384, help='max tokens')
        parser.add_argument('--trainee_top_p', type=float, default=1, help='top p')
        parser.add_argument('--trainee_frequency_penalty', type=float, default=0, help='frequency penalty')
        parser.add_argument('--trainee_presence_penalty', type=float, default=0, help='presence penalty')

    def get_response(self, messages):
        response = self.engine.get_response(messages)
        return response

    def speak(self, content, case_id, save_to_memory=True):
        memories = self.memories[case_id]

        messages = [{"role": memory[0], "content": memory[1]} for memory in memories]
        messages.append({"role": "user", "content": content})

        response = self.get_response(messages)

        self.memorize(("user", content), case_id)
        self.memorize(("assistant", response), case_id)
        return response

@register_class(alias="Agent.Trainee.LC_GLM9B")
class GLM9BTrainee_consult(Trainee_consult):
    def __init__(self, args=None, trainee_info=None, name="A"):
        engine = registry.get_class("Engine.GLM9B")()
            
        with open("/root/J1Bench/src/agents/profiles.json", "r", encoding="utf-8") as f:
            profiles = json.load(f)
        
        
        
        if args.scenario == "J1Bench.Scenario.LC":
            system_prompt = ''
            profile = profiles["trainee_LC"]
            for p in profile:
                system_prompt += p + '\n'
            if system_prompt.endswith('\n'):
                system_prompt = system_prompt[:-1]
            self.system_prompt = system_prompt
        
        super(GLM9BTrainee_consult, self).__init__(engine, trainee_info, name)
    
    @staticmethod
    def add_parser_args(parser):
        parser.add_argument('--trainee_temperature', type=float, default=0, help='temperature')
        parser.add_argument('--trainee_max_tokens', type=int, default=16384, help='max tokens')
        parser.add_argument('--trainee_top_p', type=float, default=1, help='top p')
        parser.add_argument('--trainee_frequency_penalty', type=float, default=0, help='frequency penalty')
        parser.add_argument('--trainee_presence_penalty', type=float, default=0, help='presence penalty')

    def get_response(self, messages):
        response = self.engine.get_response(messages)
        return response

    def speak(self, content, case_id, save_to_memory=True):
        memories = self.memories[case_id]

        messages = [{"role": memory[0], "content": memory[1]} for memory in memories]
        messages.append({"role": "user", "content": content})

        response = self.get_response(messages)

        self.memorize(("user", content), case_id)
        self.memorize(("assistant", response), case_id)

        return response
    
        
    
@register_class(alias="Agent.Trainee.LC_Deepseekv3")
class Deepseekv3Trainee_consult(Trainee_consult):
    def __init__(self, args=None, trainee_info=None, name="A"):
        engine = registry.get_class("Engine.deepseekv3")(
            openai_api_key=args.trainee_openai_api_key,
            openai_api_base=args.trainee_openai_api_base,
            openai_model_name=args.trainee_openai_model_name,
            temperature=args.trainee_temperature,
            max_tokens=args.trainee_max_tokens
        )
            
        with open("/root/J1Bench/src/agents/profiles.json", "r", encoding="utf-8") as f:
            profiles = json.load(f)
        
        
        
        if args.scenario == "J1Bench.Scenario.LC":
            system_prompt = ''
            profile = profiles["trainee_LC"]
            for p in profile:
                system_prompt += p + '\n'
            if system_prompt.endswith('\n'):
                system_prompt = system_prompt[:-1]
            self.system_prompt = system_prompt
        
        super(Deepseekv3Trainee_consult, self).__init__(engine, trainee_info, name)
    
    @staticmethod
    def add_parser_args(parser):
        parser.add_argument('--trainee_openai_api_key', type=str, help='API key for OpenAI')
        parser.add_argument('--trainee_openai_api_base', type=str, help='API base for OpenAI')
        parser.add_argument('--trainee_openai_model_name', type=str, help='API model name for OpenAI')
        parser.add_argument('--trainee_temperature', type=float, default=0, help='temperature')
        parser.add_argument('--trainee_max_tokens', type=int, default=16384, help='max tokens')

    def get_response(self, messages):
        response = self.engine.get_response(messages, flag=0)
        return response

    def speak(self, content, case_id, save_to_memory=True):
        memories = self.memories[case_id]

        messages = [{"role": memory[0], "content": memory[1]} for memory in memories]
        messages.append({"role": "user", "content": content})

        response = self.get_response(messages)

        self.memorize(("user", content), case_id)
        self.memorize(("assistant", response), case_id)

        return response
    

 

@register_class(alias="Agent.Trainee.LC_LLaMa3_3")
class LLaMa3_3Trainee_consult(Trainee_consult):
    def __init__(self, args=None, trainee_info=None, name="A"):
        engine = registry.get_class("Engine.LLaMa3_3")()
            
        with open("/root/J1Bench/src/agents/profiles.json", "r", encoding="utf-8") as f:
            profiles = json.load(f)
        
        
        
        if args.scenario == "J1Bench.Scenario.LC":
            system_prompt = ''
            profile = profiles["trainee_LC"]
            for p in profile:
                system_prompt += p + '\n'
            if system_prompt.endswith('\n'):
                system_prompt = system_prompt[:-1]
            self.system_prompt = system_prompt
        
        super(LLaMa3_3Trainee_consult, self).__init__(engine, trainee_info, name)
    
    @staticmethod
    def add_parser_args(parser):
        parser.add_argument('--trainee_temperature', type=float, default=0, help='temperature')
        parser.add_argument('--trainee_max_tokens', type=int, default=16384, help='max tokens')
        parser.add_argument('--trainee_top_p', type=float, default=1, help='top p')
        parser.add_argument('--trainee_frequency_penalty', type=float, default=0, help='frequency penalty')
        parser.add_argument('--trainee_presence_penalty', type=float, default=0, help='presence penalty')

    def get_response(self, messages):
        response = self.engine.get_response(messages)
        return response

    def speak(self, content, case_id, save_to_memory=True):
        memories = self.memories[case_id]

        messages = [{"role": memory[0], "content": memory[1]} for memory in memories]
        messages.append({"role": "user", "content": content})

        response = self.get_response(messages)

        self.memorize(("user", content), case_id)
        self.memorize(("assistant", response), case_id)

        return response



@register_class(alias="Agent.Trainee.LC_InternLM3")
class InternLM3Trainee_consult(Trainee_consult):
    def __init__(self, args=None, trainee_info=None, name="A"):
        engine = registry.get_class("Engine.InternLM3")()
            
        with open("/root/J1Bench/src/agents/profiles.json", "r", encoding="utf-8") as f:
            profiles = json.load(f)
        
        
        
        if args.scenario == "J1Bench.Scenario.LC":
            system_prompt = ''
            profile = profiles["trainee_LC"]
            for p in profile:
                system_prompt += p + '\n'
            if system_prompt.endswith('\n'):
                system_prompt = system_prompt[:-1]
            self.system_prompt = system_prompt
        
        super(InternLM3Trainee_consult, self).__init__(engine, trainee_info, name)
    
    @staticmethod
    def add_parser_args(parser):
        parser.add_argument('--trainee_temperature', type=float, default=0, help='temperature')
        parser.add_argument('--trainee_max_tokens', type=int, default=16384, help='max tokens')
        parser.add_argument('--trainee_top_p', type=float, default=1, help='top p')
        parser.add_argument('--trainee_frequency_penalty', type=float, default=0, help='frequency penalty')
        parser.add_argument('--trainee_presence_penalty', type=float, default=0, help='presence penalty')

    def get_response(self, messages):
        response = self.engine.get_response(messages)
        return response

    def speak(self, content, case_id, save_to_memory=True):
        memories = self.memories[case_id]

        messages = [{"role": memory[0], "content": memory[1]} for memory in memories]
        messages.append({"role": "user", "content": content})

        response = self.get_response(messages)

        self.memorize(("user", content), case_id)
        self.memorize(("assistant", response), case_id)

        return response


    
    
    
@register_class(alias="Agent.Trainee.LC_Ministral8B")
class Ministral8BTrainee_consult(Trainee_consult):
    def __init__(self, args=None, trainee_info=None, name="A"):
        engine = registry.get_class("Engine.Ministral8B")()
            
        with open("/root/J1Bench/src/agents/profiles.json", "r", encoding="utf-8") as f:
            profiles = json.load(f)
        
        
        
        if args.scenario == "J1Bench.Scenario.LC":
            system_prompt = ''
            profile = profiles["trainee_LC"]
            for p in profile:
                system_prompt += p + '\n'
            if system_prompt.endswith('\n'):
                system_prompt = system_prompt[:-1]
            self.system_prompt = system_prompt
        
        super(Ministral8BTrainee_consult, self).__init__(engine, trainee_info, name)
    
    @staticmethod
    def add_parser_args(parser):
        parser.add_argument('--trainee_temperature', type=float, default=0, help='temperature')
        parser.add_argument('--trainee_max_tokens', type=int, default=16384, help='max tokens')
        parser.add_argument('--trainee_top_p', type=float, default=1, help='top p')
        parser.add_argument('--trainee_frequency_penalty', type=float, default=0, help='frequency penalty')
        parser.add_argument('--trainee_presence_penalty', type=float, default=0, help='presence penalty')

    def get_response(self, messages):
        response = self.engine.get_response(messages)
        return response

    def speak(self, content, case_id, save_to_memory=True):
        memories = self.memories[case_id]

        messages = [{"role": memory[0], "content": memory[1]} for memory in memories]
        messages.append({"role": "user", "content": content})

        response = self.get_response(messages)

        self.memorize(("user", content), case_id)
        self.memorize(("assistant", response), case_id)

        return response
    
    
@register_class(alias="Agent.Trainee.LC_Chatlaw2")
class Chatlaw2Trainee_consult(Trainee_consult):
    def __init__(self, args=None, trainee_info=None, name="A"):
        engine = registry.get_class("Engine.Chatlaw2")()
            
        with open("/root/J1Bench/src/agents/profiles.json", "r", encoding="utf-8") as f:
            profiles = json.load(f)
        
        
        
        if args.scenario == "J1Bench.Scenario.LC":
            system_prompt = ''
            profile = profiles["trainee_LC"]
            for p in profile:
                system_prompt += p + '\n'
            if system_prompt.endswith('\n'):
                system_prompt = system_prompt[:-1]
            self.system_prompt = system_prompt
        
        super(Chatlaw2Trainee_consult, self).__init__(engine, trainee_info, name)
    
    @staticmethod
    def add_parser_args(parser):
        parser.add_argument('--trainee_temperature', type=float, default=0, help='temperature')
        parser.add_argument('--trainee_max_tokens', type=int, default=16384, help='max tokens')
        parser.add_argument('--trainee_top_p', type=float, default=1, help='top p')
        parser.add_argument('--trainee_frequency_penalty', type=float, default=0, help='frequency penalty')
        parser.add_argument('--trainee_presence_penalty', type=float, default=0, help='presence penalty')

    def get_response(self, messages):
        response = self.engine.get_response(messages)
        return response

    def speak(self, content, case_id, save_to_memory=True):
        memories = self.memories[case_id]

        messages = [{"role": memory[0], "content": memory[1]} for memory in memories]
        messages.append({"role": "user", "content": content})

        response = self.get_response(messages)

        self.memorize(("user", content), case_id)
        self.memorize(("assistant", response), case_id)

        return response
    
    
@register_class(alias="Agent.Trainee.LC_LawLLM")
class LawLLMTrainee_consult(Trainee_consult):
    def __init__(self, args=None, trainee_info=None, name="A"):
        engine = registry.get_class("Engine.lawllm")()
            
        with open("/root/J1Bench/src/agents/profiles.json", "r", encoding="utf-8") as f:
            profiles = json.load(f)
        
        
        
        if args.scenario == "J1Bench.Scenario.LC":
            system_prompt = ''
            profile = profiles["trainee_LC"]
            for p in profile:
                system_prompt += p + '\n'
            if system_prompt.endswith('\n'):
                system_prompt = system_prompt[:-1]
            self.system_prompt = system_prompt
        
        super(LawLLMTrainee_consult, self).__init__(engine, trainee_info, name)
    
    @staticmethod
    def add_parser_args(parser):
        parser.add_argument('--trainee_temperature', type=float, default=0, help='temperature')
        parser.add_argument('--trainee_max_tokens', type=int, default=16384, help='max tokens')
        parser.add_argument('--trainee_top_p', type=float, default=1, help='top p')
        parser.add_argument('--trainee_frequency_penalty', type=float, default=0, help='frequency penalty')
        parser.add_argument('--trainee_presence_penalty', type=float, default=0, help='presence penalty')

    def get_response(self, messages):
        response = self.engine.get_response(messages)
        return response

    def speak(self, content, case_id, save_to_memory=True):
        memories = self.memories[case_id]

        messages = [{"role": memory[0], "content": memory[1]} for memory in memories]
        messages.append({"role": "user", "content": content})

        response = self.get_response(messages)

        self.memorize(("user", content), case_id)
        self.memorize(("assistant", response), case_id)

        return response