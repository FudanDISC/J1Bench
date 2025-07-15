from .base_agent import Agent
from utils.register import registry, register_class
import json

@register_class(alias="Agent.Lawyer.criminalPredictionBase")
class Lawyer_criminalPrediction(Agent):
    def __init__(self, engine=None, lawyer_info=None, name="B"):
        self.name = name
        self.engine = engine
        
    @staticmethod
    def add_parser_args(parser):
        pass
    
    def get_response(self, messages):
        response = self.engine.get_response(messages)
        return response
    
    def speak(self, content, save_to_memory = True):
        messages = [{"role": memory[0], "content": memory[1]} for memory in self.memories]
        messages.append({"role": "user", "content": f"<Lawyer> {content}"})

        response = self.engine.get_response(messages)
        
        if save_to_memory:
            self.memorize(("user", f"<Lawyer> {content}"))
            self.memorize(("assistant", response))
        
        return response
    
@register_class(alias="Agent.Lawyer.GPT_CR")
class GPTLawyer_criminalPrediction(Agent):
    def __init__(self, args, lawyer_info=None, name="B"):
        engine = registry.get_class("Engine.GPT4o_1120")(
            openai_api_key=args.lawyer_openai_api_key,
            openai_api_base=args.lawyer_openai_api_base,
            openai_model_name=args.lawyer_openai_model_name,
            temperature=args.lawyer_temperature,
            max_tokens=args.lawyer_max_tokens
        )
        
        #编写profile
        id = lawyer_info['id']
        defendant_info = lawyer_info['defendant']['personal_information']
        lawyer_defence = lawyer_info['lawyer']
        
        with open("/root/J1Bench/src/agents/profiles.json", "r", encoding="utf-8") as f:
            profiles = json.load(f)
            
        if args.scenario == "J1Bench.Scenario.CR":
            profile = profiles['lawyer_CR']
            system_prompt = ''
            
            for p in profile:
                if '{defendant_name}' in p:
                    system_prompt += p.format(defendant_name = defendant_info['name']) + '\n'
                elif '{defendant_sex}' in p:
                    system_prompt += p.format(defendant_sex = defendant_info['sex']) + '\n'
                elif '{defendant_birth}' in p:
                    system_prompt += p.format(defendant_birth = defendant_info['birth_date']) + '\n'
                elif '{defendant_ethnicity}' in p:
                    system_prompt += p.format(defendant_ethnicity = defendant_info['ethnicity']) + '\n'
                elif '{defendant_address}' in p:
                    system_prompt += p.format(defendant_address = defendant_info['address']) + '\n'
                elif '{occupation}' in p:
                    system_prompt += p.format(occupation = defendant_info['occupation']) + '\n'
                elif '{education}' in p:
                    system_prompt += p.format(education = defendant_info['education']) + '\n'
                elif '{status}' in p:
                    system_prompt += p.format(status = defendant_info['status']) + '\n'
                elif '{defence}' in p:
                    system_prompt += p.format(defence = lawyer_defence) + '\n\n'
                elif '{' not in p:
                    system_prompt += p + '\n'
            if system_prompt.endswith('\n'):
                system_prompt = system_prompt[:-1]
            self.system_prompt = system_prompt
            
        super(GPTLawyer_criminalPrediction, self).__init__(engine)
        self.id = id
    
    @staticmethod
    def add_parser_args(parser):
        parser.add_argument('--lawyer_openai_api_key', type=str, help='API key for OpenAI')
        parser.add_argument('--lawyer_openai_api_base', type=str, help='API base for OpenAI')
        parser.add_argument('--lawyer_openai_model_name', type=str, help='API model name for OpenAI')
        parser.add_argument('--lawyer_temperature', type=float, default=0, help='temperature')
        parser.add_argument('--lawyer_max_tokens', type=int, default=4096, help='max tokens')
    
    def speak(self, content, save_to_memory = True):
        messages = [{"role": memory[0], "content": memory[1]} for memory in self.memories]
        messages.append({"role": "user", "content": f"{content}"})

        response = self.engine.get_response(messages, flag =0)
        
        if save_to_memory:
            self.memorize(("user", f"{content}"))
            self.memorize(("assistant", response))
        
        return response


    
@register_class(alias="Agent.Lawyer.Qwen3_32B_CR")
class Qwen3_32BLawyer_criminalPrediction(Agent):
    def __init__(self, args, lawyer_info=None, name="B"):
        engine = registry.get_class("Engine.qwen3_32B")()
        
        #编写profile
        id = lawyer_info['id']
        defendant_info = lawyer_info['defendant']['personal_information']
        lawyer_defence = lawyer_info['lawyer']
        
        with open("/root/J1Bench/src/agents/profiles.json", "r", encoding="utf-8") as f:
            profiles = json.load(f)
            
        if args.scenario == "J1Bench.Scenario.CR":
            profile = profiles['lawyer_CR']
            system_prompt = ''
            
            for p in profile:
                if '{defendant_name}' in p:
                    system_prompt += p.format(defendant_name = defendant_info['name']) + '\n'
                elif '{defendant_sex}' in p:
                    system_prompt += p.format(defendant_sex = defendant_info['sex']) + '\n'
                elif '{defendant_birth}' in p:
                    system_prompt += p.format(defendant_birth = defendant_info['birth_date']) + '\n'
                elif '{defendant_ethnicity}' in p:
                    system_prompt += p.format(defendant_ethnicity = defendant_info['ethnicity']) + '\n'
                elif '{defendant_address}' in p:
                    system_prompt += p.format(defendant_address = defendant_info['address']) + '\n'
                elif '{occupation}' in p:
                    system_prompt += p.format(occupation = defendant_info['occupation']) + '\n'
                elif '{education}' in p:
                    system_prompt += p.format(education = defendant_info['education']) + '\n'
                elif '{status}' in p:
                    system_prompt += p.format(status = defendant_info['status']) + '\n'
                elif '{defence}' in p:
                    system_prompt += p.format(defence = lawyer_defence) + '\n\n'
                elif '{' not in p:
                    system_prompt += p + '\n'
            if system_prompt.endswith('\n'):
                system_prompt = system_prompt[:-1]
            self.system_prompt = system_prompt
            
        super(Qwen3_32BLawyer_criminalPrediction, self).__init__(engine)
        self.id = id
    
    @staticmethod
    def add_parser_args(parser):
        parser.add_argument('--lawyer_temperature', type=float, default=0, help='temperature')
        parser.add_argument('--lawyer_max_tokens', type=int, default=4096, help='max tokens')
        parser.add_argument('--lawyer_top_p', type=float, default=1, help='top p')
        parser.add_argument('--lawyer_frequency_penalty', type=float, default=0, help='frequency penalty')
        parser.add_argument('--lawyer_presence_penalty', type=float, default=0, help='presence penalty')
    
    def speak(self, content, save_to_memory = True):
        messages = [{"role": memory[0], "content": memory[1]} for memory in self.memories]
        messages.append({"role": "user", "content": f"{content}"})

        response = self.engine.get_response(messages)
        
        if save_to_memory:
            self.memorize(("user", f"{content}"))
            self.memorize(("assistant", response))
        
        return response