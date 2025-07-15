from .base_agent import Agent
from utils.register import registry, register_class
import json

@register_class(alias="Agent.Procurator.criminalPredictionBase")
class Procurator_criminalPrediction(Agent):
    def __init__(self, engine=None, procurator_info=None, name="B"):
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
        messages.append({"role": "user", "content": f"<Procurator> {content}"})

        response = self.engine.get_response(messages)
        
        if save_to_memory:
            self.memorize(("user", f"<Procurator> {content}"))
            self.memorize(("assistant", response))
        
        return response
    
@register_class(alias="Agent.Procurator.GPT_CR")
class GPTProcurator_criminalPrediction(Agent):
    def __init__(self, args, procurator_info=None, name="B"):
        engine = registry.get_class("Engine.GPT4o_1120")(
            openai_api_key=args.procurator_openai_api_key,
            openai_api_base=args.procurator_openai_api_base,
            openai_model_name=args.procurator_openai_model_name,
            temperature=args.procurator_temperature,
            max_tokens=args.procurator_max_tokens
        )
        
        #编写profile
        id = procurator_info['id']
        defendant_info = procurator_info['defendant']['personal_information']
        procurator = procurator_info['procurator']
        
        with open("/root/J1Bench/src/agents/profiles.json", "r", encoding="utf-8") as f:
            profiles = json.load(f)
            
        if args.scenario == "J1Bench.Scenario.CR":
            profile = profiles['procurator_CR']
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
                elif '{accusation}' in p:
                    system_prompt += p.format(accusation = procurator['charges']) + '\n'
                elif '{opinion}' in p:
                    system_prompt += p.format(opinion = procurator['opinion']) + '\n'
                elif '{evidences}' in p:
                    system_prompt += p.format(evidences = procurator['evidence']) + '\n\n'
                elif '{' not in p:
                    system_prompt += p + '\n'
            if system_prompt.endswith('\n'):
                system_prompt = system_prompt[:-1]
            self.system_prompt = system_prompt
            
        super(GPTProcurator_criminalPrediction, self).__init__(engine)
        self.id = id
    
    @staticmethod
    def add_parser_args(parser):
        parser.add_argument('--procurator_openai_api_key', type=str, help='API key for OpenAI')
        parser.add_argument('--procurator_openai_api_base', type=str, help='API base for OpenAI')
        parser.add_argument('--procurator_openai_model_name', type=str, help='API model name for OpenAI')
        parser.add_argument('--procurator_temperature', type=float, default=0, help='temperature')
        parser.add_argument('--procurator_max_tokens', type=int, default=4096, help='max tokens')
    
    def speak(self, content, save_to_memory = True):
        messages = [{"role": memory[0], "content": memory[1]} for memory in self.memories]
        messages.append({"role": "user", "content": f"{content}"})

        response = self.engine.get_response(messages, flag =0)
        
        if save_to_memory:
            self.memorize(("user", f"{content}"))
            self.memorize(("assistant", response))
        
        return response
    


@register_class(alias="Agent.Procurator.Qwen3_32B_CR")
class Qwen3_32BProcurator_criminalPrediction(Agent):
    def __init__(self, args, procurator_info=None, name="B"):
        engine = registry.get_class("Engine.qwen3_32B")()
        
        #编写profile
        id = procurator_info['id']
        defendant_info = procurator_info['defendant']['personal_information']
        procurator = procurator_info['procurator']
        
        with open("/root/J1Bench/src/agents/profiles.json", "r", encoding="utf-8") as f:
            profiles = json.load(f)
            
        if args.scenario == "J1Bench.Scenario.CR":
            profile = profiles['procurator_CR']
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
                elif '{accusation}' in p:
                    system_prompt += p.format(accusation = procurator['charges']) + '\n'
                elif '{opinion}' in p:
                    system_prompt += p.format(opinion = procurator['opinion']) + '\n'
                elif '{evidences}' in p:
                    system_prompt += p.format(evidences = procurator['evidence']) + '\n\n'
                elif '{' not in p:
                    system_prompt += p + '\n'
            if system_prompt.endswith('\n'):
                system_prompt = system_prompt[:-1]
            self.system_prompt = system_prompt
            
        super(Qwen3_32BProcurator_criminalPrediction, self).__init__(engine)
        self.id = id
    
    @staticmethod
    def add_parser_args(parser):
        parser.add_argument('--procurator_temperature', type=float, default=0, help='temperature')
        parser.add_argument('--procurator_max_tokens', type=int, default=4096, help='max tokens')
        parser.add_argument('--procurator_top_p', type=float, default=1, help='top p')
        parser.add_argument('--procurator_frequency_penalty', type=float, default=0, help='frequency penalty')
        parser.add_argument('--procurator_presence_penalty', type=float, default=0, help='presence penalty')
    
    def speak(self, content, save_to_memory = True):
        messages = [{"role": memory[0], "content": memory[1]} for memory in self.memories]
        messages.append({"role": "user", "content": f"{content}"})

        response = self.engine.get_response(messages)
        
        if save_to_memory:
            self.memorize(("user", f"{content}"))
            self.memorize(("assistant", response))
        
        return response