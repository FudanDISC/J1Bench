from .base_agent import Agent
from utils.register import registry, register_class
import json

@register_class(alias="Agent.Specific_character.GenerationBase")
class Specific_character_generation(Agent):
    def __init__(self, engine=None, specific_character_info=None, name="B"):
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
        messages.append({"role": "user", "content": f"<Specific_character> {content}"})

        response = self.engine.get_response(messages)
        
        if save_to_memory:
            self.memorize(("user", f"<Specific_character> {content}"))
            self.memorize(("assistant", response))
        
        return response
    
    
@register_class(alias="Agent.Specific_character.GPT_DD")
class GPTSpecific_character_generation(Agent):
    def __init__(self, args, specific_character_info=None, name="B"):
        engine = registry.get_class("Engine.GPT4o_1120")(
            openai_api_key=args.specific_character_openai_api_key,
            openai_api_base=args.specific_character_openai_api_base,
            openai_model_name=args.specific_character_openai_model_name,
            temperature=args.specific_character_temperature,
            max_tokens=args.specific_character_max_tokens
        )
        
        id = specific_character_info['id']
        plaintiff_info = specific_character_info['specific_characters']['plaintiff']
        defendant_info = specific_character_info['specific_characters']['defendant']
        evidence = specific_character_info['evidence']
        defence = specific_character_info['statement_of_defence']
        
        with open("/root/J1Bench/src/agents/profiles.json", "r", encoding="utf-8") as f:
            profiles = json.load(f)
            
        if args.scenario == "J1Bench.Scenario.DD":
            profile = profiles["specific_character_DD"]
            system_prompt = ''
            
            if "gender" in plaintiff_info.keys():
                if "gender" in defendant_info.keys():
                    for p in profile:
                        if '{plaintiff_name}' in p:
                            system_prompt += p.format(plaintiff_name = plaintiff_info['name']) + '\n'
                        elif '{plaintiff_sex}' in p:
                            system_prompt += p.format(plaintiff_sex = plaintiff_info["gender"]) + '\n'
                        elif '{plaintiff_birth}' in p:
                            system_prompt += p.format(plaintiff_birth = plaintiff_info['birth_date']) + '\n'
                        elif '{plaintiff_nation}' in p:
                            system_prompt += p.format(plaintiff_nation = plaintiff_info['ethnicity']) + '\n'
                        elif '{plaintiff_address}' in p:
                            system_prompt += p.format(plaintiff_address = plaintiff_info['address']) + '\n'
                        elif '{defendant_name}' in p:
                            system_prompt += p.format(defendant_name = defendant_info['name']) + '\n'
                        elif '{defendant_sex}' in p:
                            system_prompt += p.format(defendant_sex = defendant_info["gender"]) + '\n'
                        elif '{defendant_birth}' in p:
                            system_prompt += p.format(defendant_birth = defendant_info['birth_date']) + '\n'
                        elif '{defendant_nation}' in p:
                            system_prompt += p.format(defendant_nation = defendant_info['ethnicity']) + '\n'
                        elif '{defendant_address}' in p:
                            system_prompt += p.format(defendant_address = defendant_info['address']) + '\n'
                        elif '{defence}' in p:
                            system_prompt += p.format(defence = defence) + '\n'
                        elif '{evidences}' in p:
                            count = 1
                            for e in evidence:
                                evi = evidence[e]['evidence']
                                system_prompt += f'{count}. {evi}\n'
                                count += 1
                            if len(evidence) == 0:
                                system_prompt += '无\n'
                        elif '{style}' in p:
                            system_prompt += p.format(style = defendant_info['behavioral_style']) + '\n\n'
                        elif '{' not in p:
                            system_prompt += p + '\n'
                else:
                    for p in profile:
                        if '{plaintiff_name}' in p:
                            system_prompt += p.format(plaintiff_name = plaintiff_info['name']) + '\n'
                        elif '{plaintiff_sex}' in p:
                            system_prompt += p.format(plaintiff_sex = plaintiff_info["gender"]) + '\n'
                        elif '{plaintiff_birth}' in p:
                            system_prompt += p.format(plaintiff_birth = plaintiff_info['birth_date']) + '\n'
                        elif '{plaintiff_nation}' in p:
                            system_prompt += p.format(plaintiff_nation = plaintiff_info['ethnicity']) + '\n'
                        elif '{plaintiff_address}' in p:
                            system_prompt += p.format(plaintiff_address = plaintiff_info['address']) + '\n'
                        elif '{defendant_company_name}' in p:
                            system_prompt += p.format(defendant_company_name = defendant_info['name']) + '\n'
                        elif '{defendant_company_legal_person}' in p:
                            system_prompt += p.format(defendant_company_legal_person = defendant_info['representative']) + '\n'
                        elif '{defendant_company_address}' in p:
                            system_prompt += p.format(defendant_company_address = defendant_info['address']) + '\n'
                        elif '{defence}' in p:
                            system_prompt += p.format(defence = defence) + '\n'
                        elif '{evidences}' in p:
                            count = 1
                            for e in evidence:
                                evi = evidence[e]['evidence']
                                system_prompt += f'{count}. {evi}\n'
                                count += 1
                            if len(evidence) == 0:
                                system_prompt += '无\n'
                        elif '{style}' in p:
                            system_prompt += p.format(style = defendant_info['behavioral_style']) + '\n\n'
                        elif '{' not in p:
                            system_prompt += p + '\n'
            else:
                if "gender" in defendant_info.keys():
                    for p in profile:
                        if '{plaintiff_company_name}' in p:
                            system_prompt += p.format(plaintiff_company_name = plaintiff_info['name']) + '\n'
                        elif '{plaintiff_company_legal_person}' in p:
                            system_prompt += p.format(plaintiff_company_legal_person = plaintiff_info['representative']) + '\n'
                        elif '{plaintiff_company_address}' in p:
                            system_prompt += p.format(plaintiff_company_address = plaintiff_info['address']) + '\n'
                        elif '{defendant_name}' in p:
                            system_prompt += p.format(defendant_name = defendant_info['name']) + '\n'
                        elif '{defendant_sex}' in p:
                            system_prompt += p.format(defendant_sex = defendant_info["gender"]) + '\n'
                        elif '{defendant_birth}' in p:
                            system_prompt += p.format(defendant_birth = defendant_info['birth_date']) + '\n'
                        elif '{defendant_nation}' in p:
                            system_prompt += p.format(defendant_nation = defendant_info['ethnicity']) + '\n'
                        elif '{defendant_address}' in p:
                            system_prompt += p.format(defendant_address = defendant_info['address']) + '\n'
                        elif '{defence}' in p:
                            system_prompt += p.format(defence = defence) + '\n'
                        elif '{evidences}' in p:
                            count = 1
                            for e in evidence:
                                evi = evidence[e]['evidence']
                                system_prompt += f'{count}. {evi}\n'
                                count += 1
                            if len(evidence) == 0:
                                system_prompt += '无\n'
                        elif '{style}' in p:
                            system_prompt += p.format(style = defendant_info['behavioral_style']) + '\n\n'
                        elif '{' not in p:
                            system_prompt += p + '\n'
                else:
                    for p in profile:
                        if '{plaintiff_company_name}' in p:
                            system_prompt += p.format(plaintiff_company_name = plaintiff_info['name']) + '\n'
                        elif '{plaintiff_company_legal_person}' in p:
                            system_prompt += p.format(plaintiff_company_legal_person = plaintiff_info['representative']) + '\n'
                        elif '{plaintiff_company_address}' in p:
                            system_prompt += p.format(plaintiff_company_address = plaintiff_info['address']) + '\n'
                        elif '{defendant_company_name}' in p:
                            system_prompt += p.format(defendant_company_name = defendant_info['name']) + '\n'
                        elif '{defendant_company_legal_person}' in p:
                            system_prompt += p.format(defendant_company_legal_person = defendant_info['representative']) + '\n'
                        elif '{defendant_company_address}' in p:
                            system_prompt += p.format(defendant_company_address = defendant_info['address']) + '\n'
                        elif '{defence}' in p:
                            system_prompt += p.format(defence = defence) + '\n'
                        elif '{evidences}' in p:
                            count = 1
                            for e in evidence:
                                evi = evidence[e]['evidence']
                                system_prompt += f'{count}. {evi}\n'
                                count += 1
                            if len(evidence) == 0:
                                system_prompt += '无\n'
                        elif '{style}' in p:
                            system_prompt += p.format(style = defendant_info['behavioral_style']) + '\n\n'
                        elif '{' not in p:
                            system_prompt += p + '\n'
            
            if system_prompt.endswith('\n'):
                system_prompt = system_prompt[:-1]
            self.system_prompt = system_prompt
            
        super(GPTSpecific_character_generation, self).__init__(engine)
        self.id = id
        self.specific_character_greetings = "您好，我想要起草一份答辩状。"
        
    @staticmethod
    def add_parser_args(parser):
        parser.add_argument('--specific_character_openai_api_key', type=str, help='API key for OpenAI')
        parser.add_argument('--specific_character_openai_api_base', type=str, help='API base for OpenAI')
        parser.add_argument('--specific_character_openai_model_name', type=str, help='API model name for OpenAI')
        parser.add_argument('--specific_character_temperature', type=float, default=0, help='temperature')
        parser.add_argument('--specific_character_max_tokens', type=int, default=4096, help='max tokens')

    def speak(self, content, save_to_memory = True):
        messages = [{"role": memory[0], "content": memory[1]} for memory in self.memories]
        messages.append({"role": "user", "content": f"{content}"})

        response = self.engine.get_response(messages, flag =0)
        
        if save_to_memory:
            self.memorize(("user", f"{content}"))
            self.memorize(("assistant", response))
        
        return response


@register_class(alias="Agent.Specific_character.Qwen332B_DD")
class Qwen332BSpecific_character_generation(Agent):
    def __init__(self, args, specific_character_info=None, name="B"):
        engine = registry.get_class("Engine.qwen3_32B")()
        
        id = specific_character_info['id']
        plaintiff_info = specific_character_info['specific_characters']['plaintiff']
        defendant_info = specific_character_info['specific_characters']['defendant']
        evidence = specific_character_info['evidence']
        defence = specific_character_info['statement_of_defence']
        
        with open("/root/J1Bench/src/agents/profiles.json", "r", encoding="utf-8") as f:
            profiles = json.load(f)
            
        if args.scenario == "J1Bench.Scenario.DD":
            profile = profiles["specific_character_DD"]
            system_prompt = ''
            
            if "gender" in plaintiff_info.keys():
                if "gender" in defendant_info.keys():
                    for p in profile:
                        if '{plaintiff_name}' in p:
                            system_prompt += p.format(plaintiff_name = plaintiff_info['name']) + '\n'
                        elif '{plaintiff_sex}' in p:
                            system_prompt += p.format(plaintiff_sex = plaintiff_info["gender"]) + '\n'
                        elif '{plaintiff_birth}' in p:
                            system_prompt += p.format(plaintiff_birth = plaintiff_info['birth_date']) + '\n'
                        elif '{plaintiff_nation}' in p:
                            system_prompt += p.format(plaintiff_nation = plaintiff_info['ethnicity']) + '\n'
                        elif '{plaintiff_address}' in p:
                            system_prompt += p.format(plaintiff_address = plaintiff_info['address']) + '\n'
                        elif '{defendant_name}' in p:
                            system_prompt += p.format(defendant_name = defendant_info['name']) + '\n'
                        elif '{defendant_sex}' in p:
                            system_prompt += p.format(defendant_sex = defendant_info["gender"]) + '\n'
                        elif '{defendant_birth}' in p:
                            system_prompt += p.format(defendant_birth = defendant_info['birth_date']) + '\n'
                        elif '{defendant_nation}' in p:
                            system_prompt += p.format(defendant_nation = defendant_info['ethnicity']) + '\n'
                        elif '{defendant_address}' in p:
                            system_prompt += p.format(defendant_address = defendant_info['address']) + '\n'
                        elif '{defence}' in p:
                            system_prompt += p.format(defence = defence) + '\n'
                        elif '{evidences}' in p:
                            count = 1
                            for e in evidence:
                                evi = evidence[e]['evidence']
                                system_prompt += f'{count}. {evi}\n'
                                count += 1
                            if len(evidence) == 0:
                                system_prompt += '无\n'
                        elif '{style}' in p:
                            system_prompt += p.format(style = defendant_info['behavioral_style']) + '\n\n'
                        elif '{' not in p:
                            system_prompt += p + '\n'
                else:
                    for p in profile:
                        if '{plaintiff_name}' in p:
                            system_prompt += p.format(plaintiff_name = plaintiff_info['name']) + '\n'
                        elif '{plaintiff_sex}' in p:
                            system_prompt += p.format(plaintiff_sex = plaintiff_info["gender"]) + '\n'
                        elif '{plaintiff_birth}' in p:
                            system_prompt += p.format(plaintiff_birth = plaintiff_info['birth_date']) + '\n'
                        elif '{plaintiff_nation}' in p:
                            system_prompt += p.format(plaintiff_nation = plaintiff_info['ethnicity']) + '\n'
                        elif '{plaintiff_address}' in p:
                            system_prompt += p.format(plaintiff_address = plaintiff_info['address']) + '\n'
                        elif '{defendant_company_name}' in p:
                            system_prompt += p.format(defendant_company_name = defendant_info['name']) + '\n'
                        elif '{defendant_company_legal_person}' in p:
                            system_prompt += p.format(defendant_company_legal_person = defendant_info['representative']) + '\n'
                        elif '{defendant_company_address}' in p:
                            system_prompt += p.format(defendant_company_address = defendant_info['address']) + '\n'
                        elif '{defence}' in p:
                            system_prompt += p.format(defence = defence) + '\n'
                        elif '{evidences}' in p:
                            count = 1
                            for e in evidence:
                                evi = evidence[e]['evidence']
                                system_prompt += f'{count}. {evi}\n'
                                count += 1
                            if len(evidence) == 0:
                                system_prompt += '无\n'
                        elif '{style}' in p:
                            system_prompt += p.format(style = defendant_info['behavioral_style']) + '\n\n'
                        elif '{' not in p:
                            system_prompt += p + '\n'
            else:
                if "gender" in defendant_info.keys():
                    for p in profile:
                        if '{plaintiff_company_name}' in p:
                            system_prompt += p.format(plaintiff_company_name = plaintiff_info['name']) + '\n'
                        elif '{plaintiff_company_legal_person}' in p:
                            system_prompt += p.format(plaintiff_company_legal_person = plaintiff_info['representative']) + '\n'
                        elif '{plaintiff_company_address}' in p:
                            system_prompt += p.format(plaintiff_company_address = plaintiff_info['address']) + '\n'
                        elif '{defendant_name}' in p:
                            system_prompt += p.format(defendant_name = defendant_info['name']) + '\n'
                        elif '{defendant_sex}' in p:
                            system_prompt += p.format(defendant_sex = defendant_info["gender"]) + '\n'
                        elif '{defendant_birth}' in p:
                            system_prompt += p.format(defendant_birth = defendant_info['birth_date']) + '\n'
                        elif '{defendant_nation}' in p:
                            system_prompt += p.format(defendant_nation = defendant_info['ethnicity']) + '\n'
                        elif '{defendant_address}' in p:
                            system_prompt += p.format(defendant_address = defendant_info['address']) + '\n'
                        elif '{defence}' in p:
                            system_prompt += p.format(defence = defence) + '\n'
                        elif '{evidences}' in p:
                            count = 1
                            for e in evidence:
                                evi = evidence[e]['evidence']
                                system_prompt += f'{count}. {evi}\n'
                                count += 1
                            if len(evidence) == 0:
                                system_prompt += '无\n'
                        elif '{style}' in p:
                            system_prompt += p.format(style = defendant_info['behavioral_style']) + '\n\n'
                        elif '{' not in p:
                            system_prompt += p + '\n'
                else:
                    for p in profile:
                        if '{plaintiff_company_name}' in p:
                            system_prompt += p.format(plaintiff_company_name = plaintiff_info['name']) + '\n'
                        elif '{plaintiff_company_legal_person}' in p:
                            system_prompt += p.format(plaintiff_company_legal_person = plaintiff_info['representative']) + '\n'
                        elif '{plaintiff_company_address}' in p:
                            system_prompt += p.format(plaintiff_company_address = plaintiff_info['address']) + '\n'
                        elif '{defendant_company_name}' in p:
                            system_prompt += p.format(defendant_company_name = defendant_info['name']) + '\n'
                        elif '{defendant_company_legal_person}' in p:
                            system_prompt += p.format(defendant_company_legal_person = defendant_info['representative']) + '\n'
                        elif '{defendant_company_address}' in p:
                            system_prompt += p.format(defendant_company_address = defendant_info['address']) + '\n'
                        elif '{defence}' in p:
                            system_prompt += p.format(defence = defence) + '\n'
                        elif '{evidences}' in p:
                            count = 1
                            for e in evidence:
                                evi = evidence[e]['evidence']
                                system_prompt += f'{count}. {evi}\n'
                                count += 1
                            if len(evidence) == 0:
                                system_prompt += '无\n'
                        elif '{style}' in p:
                            system_prompt += p.format(style = defendant_info['behavioral_style']) + '\n\n'
                        elif '{' not in p:
                            system_prompt += p + '\n'
            
            if system_prompt.endswith('\n'):
                system_prompt = system_prompt[:-1]
            self.system_prompt = system_prompt
            
        super(Qwen332BSpecific_character_generation, self).__init__(engine)
        self.id = id
        self.specific_character_greetings = "您好，我想要起草一份答辩状。"
        
    @staticmethod
    def add_parser_args(parser):
        parser.add_argument('--specific_character_temperature', type=float, default=0, help='temperature')
        parser.add_argument('--specific_character_max_tokens', type=int, default=4096, help='max tokens')
        parser.add_argument('--specific_character_top_p', type=float, default=1, help='top p')
        parser.add_argument('--specific_character_frequency_penalty', type=float, default=0, help='frequency penalty')
        parser.add_argument('--specific_character_presence_penalty', type=float, default=0, help='presence penalty')

    def speak(self, content, save_to_memory = True):
        messages = [{"role": memory[0], "content": memory[1]} for memory in self.memories]
        messages.append({"role": "user", "content": f"{content}"})

        response = self.engine.get_response(messages)
        
        if save_to_memory:
            self.memorize(("user", f"{content}"))
            self.memorize(("assistant", response))
        
        return response
    