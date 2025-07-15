from .base_agent import Agent
from utils.register import registry, register_class
import json

@register_class(alias="Agent.Plaintiff.civilPredictionBase")
class Plaintiff_civilPrediction(Agent):
    def __init__(self, engine=None, plaintiff_info=None, name="B"):
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
        messages.append({"role": "user", "content": f"<Plaintiff> {content}"})

        response = self.engine.get_response(messages)
        
        if save_to_memory:
            self.memorize(("user", f"<Plaintiff> {content}"))
            self.memorize(("assistant", response))
        
        return response
    

@register_class(alias="Agent.Plaintiff.GPT_CI")
class GPTPlaintiff_civilPrediction(Agent):
    def __init__(self, args, plaintiff_info=None, name="B"):
        engine = registry.get_class("Engine.GPT4o_1120")(
            openai_api_key=args.plaintiff_openai_api_key,
            openai_api_base=args.plaintiff_openai_api_base,
            openai_model_name=args.plaintiff_openai_model_name,
            temperature=args.plaintiff_temperature,
            max_tokens=args.plaintiff_max_tokens
        )
        
        #编写profile
        id = plaintiff_info['id']
        plaintiff = plaintiff_info['specific_characters']['plaintiff']
        defendant = plaintiff_info['specific_characters']['defendant']
        plaintiff_claim = plaintiff_info['plaintiff_claim']
        plaintiff_case_details = plaintiff_info['plaintiff_case_details']
        plaintiff_evidence = plaintiff_info['evidence']['plaintiff_evidence']
        defendant_evidence = plaintiff_info['evidence']['defendant_evidence']
        other_statement = plaintiff_info['other_statement']['plaintiff']['plaintiff_1']
        if other_statement == '':
            other_statement = '无'
        
        with open("/root/J1Bench/src/agents/profiles.json", "r", encoding="utf-8") as f:
            profiles = json.load(f)
            
        if args.scenario == "J1Bench.Scenario.CI":
            profile = profiles['plaintiff_CI']
            system_prompt = ''
            
            if "gender" in plaintiff.keys():
                if "gender" in defendant.keys():
                    for p in profile:
                        if '{plaintiff_name}' in p:
                            system_prompt += p.format(plaintiff_name = plaintiff['name']) + '\n'
                        elif '{plaintiff_sex}' in p:
                            system_prompt += p.format(plaintiff_sex = plaintiff['gender']) + '\n'
                        elif '{plaintiff_birth}' in p:
                            system_prompt += p.format(plaintiff_birth = plaintiff['birth_date']) + '\n'
                        elif '{plaintiff_nation}' in p:
                            system_prompt += p.format(plaintiff_nation = plaintiff['ethnicity']) + '\n'
                        elif '{plaintiff_address}' in p:
                            system_prompt += p.format(plaintiff_address = plaintiff['address']) + '\n'
                        elif '{defendant_name}' in p:
                            system_prompt += p.format(defendant_name = defendant['name']) + '\n'
                        elif '{defendant_sex}' in p:
                            system_prompt += p.format(defendant_sex = defendant['gender']) + '\n'
                        elif '{defendant_birth}' in p:
                            system_prompt += p.format(defendant_birth = defendant['birth_date']) + '\n'
                        elif '{defendant_nation}' in p:
                            system_prompt += p.format(defendant_nation = defendant['ethnicity']) + '\n'
                        elif '{defendant_address}' in p:
                            system_prompt += p.format(defendant_address = defendant['address']) + '\n'
                        elif '{case_details}' in p:
                            system_prompt += p.format(case_details = plaintiff_case_details) + '\n'
                        elif '{claims}' in p:
                            count = 1
                            for claim in plaintiff_claim:
                                system_prompt += f'{count}. {claim}\n'
                                count += 1
                        elif '{evidences}' in p:
                            count = 1
                            if len(list(plaintiff_evidence.keys())) >= 1:
                                for e in plaintiff_evidence.keys():
                                    evi = plaintiff_evidence[e]['evidence']
                                    system_prompt += f'{count}. {evi}\n'
                                    count += 1
                            else:
                                system_prompt += '无\n'
                        elif '{refute}' in p:
                            count = 1
                            if len(list(defendant_evidence.keys())) >= 1:
                                for e in defendant_evidence.keys():
                                    evi = defendant_evidence[e]['evidence']
                                    ref = defendant_evidence[e]['dispute']
                                    if ref != '' and ref is not None:
                                        res = f'{count}. 针对证据{evi}，{ref}\n'
                                    else:
                                        res = f'{count}. 针对证据{evi}，无反驳意见。'
                                    res = res.replace('。，', '，')
                                    system_prompt += f'{res}'
                                    count += 1
                            else:
                                system_prompt += '无\n'
                        elif '{other_statement}' in p:
                            if len(other_statement) > 0:
                                system_prompt += other_statement + '\n'
                            else:
                                system_prompt += '无\n'
                        elif '同时，你需要遵循如下的注意事' in p:
                            system_prompt += '\n' + p + '\n'
                        elif '{' not in p:
                            system_prompt += p + '\n'
                else:
                    for p in profile:
                        if '{plaintiff_name}' in p:
                            system_prompt += p.format(plaintiff_name = plaintiff['name']) + '\n'
                        elif '{plaintiff_sex}' in p:
                            system_prompt += p.format(plaintiff_sex = plaintiff['gender']) + '\n'
                        elif '{plaintiff_birth}' in p:
                            system_prompt += p.format(plaintiff_birth = plaintiff['birth_date']) + '\n'
                        elif '{plaintiff_nation}' in p:
                            system_prompt += p.format(plaintiff_nation = plaintiff['ethnicity']) + '\n'
                        elif '{plaintiff_address}' in p:
                            system_prompt += p.format(plaintiff_address = plaintiff['address']) + '\n'
                        elif '{defendant_company_name}' in p:
                            system_prompt += p.format(defendant_company_name = defendant['name']) + '\n'
                        elif '{defendant_company_legal_person}' in p:
                            system_prompt += p.format(defendant_company_legal_person = defendant['representative']) + '\n'
                        elif '{defendant_company_address}' in p:
                            system_prompt += p.format(defendant_company_address = defendant['address']) + '\n'
                        elif '{case_details}' in p:
                            system_prompt += p.format(case_details = plaintiff_case_details) + '\n'
                        elif '{claims}' in p:
                            count = 1
                            for claim in plaintiff_claim:
                                system_prompt += f'{count}. {claim}\n'
                                count += 1
                        elif '{evidences}' in p:
                            count = 1
                            if len(list(plaintiff_evidence.keys())) >= 1:
                                for e in plaintiff_evidence.keys():
                                    evi = plaintiff_evidence[e]['evidence']
                                    system_prompt += f'{count}. {evi}\n'
                                    count += 1
                            else:
                                system_prompt += '无\n'
                        elif '{refute}' in p:
                            count = 1
                            if len(list(defendant_evidence.keys())) >= 1:
                                for e in defendant_evidence.keys():
                                    evi = defendant_evidence[e]['evidence']
                                    ref = defendant_evidence[e]['dispute']
                                    if ref != '' and ref is not None:
                                        res = f'{count}. 针对证据{evi}，{ref}\n'
                                    else:
                                        res = f'{count}. 针对证据{evi}，无反驳意见。'
                                    res = res.replace('。，', '，')
                                    system_prompt += f'{res}'
                                    count += 1
                            else:
                                system_prompt += '无\n'
                        elif '{other_statement}' in p:
                            if len(other_statement) > 0:
                                system_prompt += other_statement + '\n'
                            else:
                                system_prompt += '无\n'
                        elif '同时，你需要遵循如下的注意事' in p:
                            system_prompt += '\n' + p + '\n'
                        elif '{' not in p:
                            system_prompt += p + '\n'
            else:
                if "sex" in defendant.keys():
                    for p in profile:
                        if '{plaintiff_company_name}' in p:
                            system_prompt += p.format(plaintiff_company_name = plaintiff['name']) + '\n'
                        elif '{plaintiff_company_legal_person}' in p:
                            system_prompt += p.format(plaintiff_company_legal_person = plaintiff['representative']) + '\n'
                        elif '{plaintiff_company_address}' in p:
                            system_prompt += p.format(plaintiff_company_address = plaintiff['address']) + '\n'
                        elif '{defendant_name}' in p:
                            system_prompt += p.format(defendant_name = defendant['name']) + '\n'
                        elif '{defendant_sex}' in p:
                            system_prompt += p.format(defendant_sex = defendant['gender']) + '\n'
                        elif '{defendant_birth}' in p:
                            system_prompt += p.format(defendant_birth = defendant['birth_date']) + '\n'
                        elif '{defendant_nation}' in p:
                            system_prompt += p.format(defendant_nation = defendant['ethnicity']) + '\n'
                        elif '{defendant_address}' in p:
                            system_prompt += p.format(defendant_address = defendant['address']) + '\n'
                        elif '{case_details}' in p:
                            system_prompt += p.format(case_details = plaintiff_case_details) + '\n'
                        elif '{claims}' in p:
                            count = 1
                            for claim in plaintiff_claim:
                                system_prompt += f'{count}. {claim}\n'
                                count += 1
                        elif '{evidences}' in p:
                            count = 1
                            if len(list(plaintiff_evidence.keys())) >= 1:
                                for e in plaintiff_evidence.keys():
                                    evi = plaintiff_evidence[e]['evidence']
                                    system_prompt += f'{count}. {evi}\n'
                                    count += 1
                            else:
                                system_prompt += '无\n'
                        elif '{refute}' in p:
                            count = 1
                            if len(list(defendant_evidence.keys())) >= 1:
                                for e in defendant_evidence.keys():
                                    evi = defendant_evidence[e]['evidence']
                                    ref = defendant_evidence[e]['dispute']
                                    if ref != '' and ref is not None:
                                        res = f'{count}. 针对证据{evi}，{ref}\n'
                                    else:
                                        res = f'{count}. 针对证据{evi}，无反驳意见。'
                                    res = res.replace('。，', '，')
                                    system_prompt += f'{res}'
                                    count += 1
                            else:
                                system_prompt += '无\n'
                        elif '{other_statement}' in p:
                            if len(other_statement) > 0:
                                system_prompt += other_statement + '\n'
                            else:
                                system_prompt += '无\n'
                        elif '同时，你需要遵循如下的注意事' in p:
                            system_prompt += '\n' + p + '\n'
                        elif '{' not in p:
                            system_prompt += p + '\n'
                else:
                    for p in profile:
                        if '{plaintiff_company_name}' in p:
                            system_prompt += p.format(plaintiff_company_name = plaintiff['name']) + '\n'
                        elif '{plaintiff_company_legal_person}' in p:
                            system_prompt += p.format(plaintiff_company_legal_person = plaintiff['representative']) + '\n'
                        elif '{plaintiff_company_address}' in p:
                            system_prompt += p.format(plaintiff_company_address = plaintiff['address']) + '\n'
                        elif '{defendant_company_name}' in p:
                            system_prompt += p.format(defendant_company_name = defendant['name']) + '\n'
                        elif '{defendant_company_legal_person}' in p:
                            system_prompt += p.format(defendant_company_legal_person = defendant['representative']) + '\n'
                        elif '{defendant_company_address}' in p:
                            system_prompt += p.format(defendant_company_address = defendant['address']) + '\n'
                        elif '{case_details}' in p:
                            system_prompt += p.format(case_details = plaintiff_case_details) + '\n'
                        elif '{claims}' in p:
                            count = 1
                            for claim in plaintiff_claim:
                                system_prompt += f'{count}. {claim}\n'
                                count += 1
                        elif '{evidences}' in p:
                            count = 1
                            if len(list(plaintiff_evidence.keys())) >= 1:
                                for e in plaintiff_evidence.keys():
                                    evi = plaintiff_evidence[e]['evidence']
                                    system_prompt += f'{count}. {evi}\n'
                                    count += 1
                            else:
                                system_prompt += '无\n'
                        elif '{refute}' in p:
                            count = 1
                            if len(list(defendant_evidence.keys())) >= 1:
                                for e in defendant_evidence.keys():
                                    evi = defendant_evidence[e]['evidence']
                                    ref = defendant_evidence[e]['dispute']
                                    if ref != '' and ref is not None:
                                        res = f'{count}. 针对证据{evi}，{ref}\n'
                                    else:
                                        res = f'{count}. 针对证据{evi}，无反驳意见。'
                                    res = res.replace('。，', '，')
                                    system_prompt += f'{res}'
                                    count += 1
                            else:
                                system_prompt += '无\n'
                        elif '{other_statement}' in p:
                            if len(other_statement) > 0:
                                system_prompt += other_statement + '\n'
                            else:
                                system_prompt += '无\n'
                        elif '同时，你需要遵循如下的注意事' in p:
                            system_prompt += '\n' + p + '\n'
                        elif '{' not in p:
                            system_prompt += p + '\n'
            if system_prompt.endswith('\n'):
                system_prompt = system_prompt[:-1]
            self.system_prompt = system_prompt
            
        super(GPTPlaintiff_civilPrediction, self).__init__(engine)
        self.id = id
    
    @staticmethod
    def add_parser_args(parser):
        parser.add_argument('--plaintiff_openai_api_key', type=str, help='API key for OpenAI')
        parser.add_argument('--plaintiff_openai_api_base', type=str, help='API base for OpenAI')
        parser.add_argument('--plaintiff_openai_model_name', type=str, help='API model name for OpenAI')
        parser.add_argument('--plaintiff_temperature', type=float, default=0, help='temperature')
        parser.add_argument('--plaintiff_max_tokens', type=int, default=4096, help='max tokens')
    
    def speak(self, content, save_to_memory = True):
        messages = [{"role": memory[0], "content": memory[1]} for memory in self.memories]
        messages.append({"role": "user", "content": f"{content}"})

        response = self.engine.get_response(messages, flag =0)
        
        if save_to_memory:
            self.memorize(("user", f"{content}"))
            self.memorize(("assistant", response))
        
        return response



@register_class(alias="Agent.Plaintiff.Qwen3_32B_CI")
class Qwen3_32BPlaintiff_civilPrediction(Agent):
    def __init__(self, args, plaintiff_info=None, name="B"):
        engine = registry.get_class("Engine.qwen3_32B")()
        
        #编写profile
        id = plaintiff_info['id']
        plaintiff = plaintiff_info['specific_characters']['plaintiff']
        defendant = plaintiff_info['specific_characters']['defendant']
        plaintiff_claim = plaintiff_info['plaintiff_claim']
        plaintiff_case_details = plaintiff_info['plaintiff_case_details']
        plaintiff_evidence = plaintiff_info['evidence']['plaintiff_evidence']
        defendant_evidence = plaintiff_info['evidence']['defendant_evidence']
        other_statement = plaintiff_info['other_statement']['plaintiff']['plaintiff_1']
        if other_statement == '':
            other_statement = '无'
        
        with open("/root/J1Bench/src/agents/profiles.json", "r", encoding="utf-8") as f:
            profiles = json.load(f)
            
        if args.scenario == "J1Bench.Scenario.CI":
            profile = profiles['plaintiff_CI']
            system_prompt = ''
            
            if "gender" in plaintiff.keys():
                if "gender" in defendant.keys():
                    for p in profile:
                        if '{plaintiff_name}' in p:
                            system_prompt += p.format(plaintiff_name = plaintiff['name']) + '\n'
                        elif '{plaintiff_sex}' in p:
                            system_prompt += p.format(plaintiff_sex = plaintiff['gender']) + '\n'
                        elif '{plaintiff_birth}' in p:
                            system_prompt += p.format(plaintiff_birth = plaintiff['birth_date']) + '\n'
                        elif '{plaintiff_nation}' in p:
                            system_prompt += p.format(plaintiff_nation = plaintiff['ethnicity']) + '\n'
                        elif '{plaintiff_address}' in p:
                            system_prompt += p.format(plaintiff_address = plaintiff['address']) + '\n'
                        elif '{defendant_name}' in p:
                            system_prompt += p.format(defendant_name = defendant['name']) + '\n'
                        elif '{defendant_sex}' in p:
                            system_prompt += p.format(defendant_sex = defendant['gender']) + '\n'
                        elif '{defendant_birth}' in p:
                            system_prompt += p.format(defendant_birth = defendant['birth_date']) + '\n'
                        elif '{defendant_nation}' in p:
                            system_prompt += p.format(defendant_nation = defendant['ethnicity']) + '\n'
                        elif '{defendant_address}' in p:
                            system_prompt += p.format(defendant_address = defendant['address']) + '\n'
                        elif '{case_details}' in p:
                            system_prompt += p.format(case_details = plaintiff_case_details) + '\n'
                        elif '{claims}' in p:
                            count = 1
                            for claim in plaintiff_claim:
                                system_prompt += f'{count}. {claim}\n'
                                count += 1
                        elif '{evidences}' in p:
                            count = 1
                            if len(list(plaintiff_evidence.keys())) >= 1:
                                for e in plaintiff_evidence.keys():
                                    evi = plaintiff_evidence[e]['evidence']
                                    system_prompt += f'{count}. {evi}\n'
                                    count += 1
                            else:
                                system_prompt += '无\n'
                        elif '{refute}' in p:
                            count = 1
                            if len(list(defendant_evidence.keys())) >= 1:
                                for e in defendant_evidence.keys():
                                    evi = defendant_evidence[e]['evidence']
                                    ref = defendant_evidence[e]['dispute']
                                    if ref != '' and ref is not None:
                                        res = f'{count}. 针对证据{evi}，{ref}\n'
                                    else:
                                        res = f'{count}. 针对证据{evi}，无反驳意见。'
                                    res = res.replace('。，', '，')
                                    system_prompt += f'{res}'
                                    count += 1
                            else:
                                system_prompt += '无\n'
                        elif '{other_statement}' in p:
                            if len(other_statement) > 0:
                                system_prompt += other_statement + '\n'
                            else:
                                system_prompt += '无\n'
                        elif '同时，你需要遵循如下的注意事' in p:
                            system_prompt += '\n' + p + '\n'
                        elif '{' not in p:
                            system_prompt += p + '\n'
                else:
                    for p in profile:
                        if '{plaintiff_name}' in p:
                            system_prompt += p.format(plaintiff_name = plaintiff['name']) + '\n'
                        elif '{plaintiff_sex}' in p:
                            system_prompt += p.format(plaintiff_sex = plaintiff['gender']) + '\n'
                        elif '{plaintiff_birth}' in p:
                            system_prompt += p.format(plaintiff_birth = plaintiff['birth_date']) + '\n'
                        elif '{plaintiff_nation}' in p:
                            system_prompt += p.format(plaintiff_nation = plaintiff['ethnicity']) + '\n'
                        elif '{plaintiff_address}' in p:
                            system_prompt += p.format(plaintiff_address = plaintiff['address']) + '\n'
                        elif '{defendant_company_name}' in p:
                            system_prompt += p.format(defendant_company_name = defendant['name']) + '\n'
                        elif '{defendant_company_legal_person}' in p:
                            system_prompt += p.format(defendant_company_legal_person = defendant['representative']) + '\n'
                        elif '{defendant_company_address}' in p:
                            system_prompt += p.format(defendant_company_address = defendant['address']) + '\n'
                        elif '{case_details}' in p:
                            system_prompt += p.format(case_details = plaintiff_case_details) + '\n'
                        elif '{claims}' in p:
                            count = 1
                            for claim in plaintiff_claim:
                                system_prompt += f'{count}. {claim}\n'
                                count += 1
                        elif '{evidences}' in p:
                            count = 1
                            if len(list(plaintiff_evidence.keys())) >= 1:
                                for e in plaintiff_evidence.keys():
                                    evi = plaintiff_evidence[e]['evidence']
                                    system_prompt += f'{count}. {evi}\n'
                                    count += 1
                            else:
                                system_prompt += '无\n'
                        elif '{refute}' in p:
                            count = 1
                            if len(list(defendant_evidence.keys())) >= 1:
                                for e in defendant_evidence.keys():
                                    evi = defendant_evidence[e]['evidence']
                                    ref = defendant_evidence[e]['dispute']
                                    if ref != '' and ref is not None:
                                        res = f'{count}. 针对证据{evi}，{ref}\n'
                                    else:
                                        res = f'{count}. 针对证据{evi}，无反驳意见。'
                                    res = res.replace('。，', '，')
                                    system_prompt += f'{res}'
                                    count += 1
                            else:
                                system_prompt += '无\n'
                        elif '{other_statement}' in p:
                            if len(other_statement) > 0:
                                system_prompt += other_statement + '\n'
                            else:
                                system_prompt += '无\n'
                        elif '同时，你需要遵循如下的注意事' in p:
                            system_prompt += '\n' + p + '\n'
                        elif '{' not in p:
                            system_prompt += p + '\n'
            else:
                if "sex" in defendant.keys():
                    for p in profile:
                        if '{plaintiff_company_name}' in p:
                            system_prompt += p.format(plaintiff_company_name = plaintiff['name']) + '\n'
                        elif '{plaintiff_company_legal_person}' in p:
                            system_prompt += p.format(plaintiff_company_legal_person = plaintiff['representative']) + '\n'
                        elif '{plaintiff_company_address}' in p:
                            system_prompt += p.format(plaintiff_company_address = plaintiff['address']) + '\n'
                        elif '{defendant_name}' in p:
                            system_prompt += p.format(defendant_name = defendant['name']) + '\n'
                        elif '{defendant_sex}' in p:
                            system_prompt += p.format(defendant_sex = defendant['gender']) + '\n'
                        elif '{defendant_birth}' in p:
                            system_prompt += p.format(defendant_birth = defendant['birth_date']) + '\n'
                        elif '{defendant_nation}' in p:
                            system_prompt += p.format(defendant_nation = defendant['ethnicity']) + '\n'
                        elif '{defendant_address}' in p:
                            system_prompt += p.format(defendant_address = defendant['address']) + '\n'
                        elif '{case_details}' in p:
                            system_prompt += p.format(case_details = plaintiff_case_details) + '\n'
                        elif '{claims}' in p:
                            count = 1
                            for claim in plaintiff_claim:
                                system_prompt += f'{count}. {claim}\n'
                                count += 1
                        elif '{evidences}' in p:
                            count = 1
                            if len(list(plaintiff_evidence.keys())) >= 1:
                                for e in plaintiff_evidence.keys():
                                    evi = plaintiff_evidence[e]['evidence']
                                    system_prompt += f'{count}. {evi}\n'
                                    count += 1
                            else:
                                system_prompt += '无\n'
                        elif '{refute}' in p:
                            count = 1
                            if len(list(defendant_evidence.keys())) >= 1:
                                for e in defendant_evidence.keys():
                                    evi = defendant_evidence[e]['evidence']
                                    ref = defendant_evidence[e]['dispute']
                                    if ref != '' and ref is not None:
                                        res = f'{count}. 针对证据{evi}，{ref}\n'
                                    else:
                                        res = f'{count}. 针对证据{evi}，无反驳意见。'
                                    res = res.replace('。，', '，')
                                    system_prompt += f'{res}'
                                    count += 1
                            else:
                                system_prompt += '无\n'
                        elif '{other_statement}' in p:
                            if len(other_statement) > 0:
                                system_prompt += other_statement + '\n'
                            else:
                                system_prompt += '无\n'
                        elif '同时，你需要遵循如下的注意事' in p:
                            system_prompt += '\n' + p + '\n'
                        elif '{' not in p:
                            system_prompt += p + '\n'
                else:
                    for p in profile:
                        if '{plaintiff_company_name}' in p:
                            system_prompt += p.format(plaintiff_company_name = plaintiff['name']) + '\n'
                        elif '{plaintiff_company_legal_person}' in p:
                            system_prompt += p.format(plaintiff_company_legal_person = plaintiff['representative']) + '\n'
                        elif '{plaintiff_company_address}' in p:
                            system_prompt += p.format(plaintiff_company_address = plaintiff['address']) + '\n'
                        elif '{defendant_company_name}' in p:
                            system_prompt += p.format(defendant_company_name = defendant['name']) + '\n'
                        elif '{defendant_company_legal_person}' in p:
                            system_prompt += p.format(defendant_company_legal_person = defendant['representative']) + '\n'
                        elif '{defendant_company_address}' in p:
                            system_prompt += p.format(defendant_company_address = defendant['address']) + '\n'
                        elif '{case_details}' in p:
                            system_prompt += p.format(case_details = plaintiff_case_details) + '\n'
                        elif '{claims}' in p:
                            count = 1
                            for claim in plaintiff_claim:
                                system_prompt += f'{count}. {claim}\n'
                                count += 1
                        elif '{evidences}' in p:
                            count = 1
                            if len(list(plaintiff_evidence.keys())) >= 1:
                                for e in plaintiff_evidence.keys():
                                    evi = plaintiff_evidence[e]['evidence']
                                    system_prompt += f'{count}. {evi}\n'
                                    count += 1
                            else:
                                system_prompt += '无\n'
                        elif '{refute}' in p:
                            count = 1
                            if len(list(defendant_evidence.keys())) >= 1:
                                for e in defendant_evidence.keys():
                                    evi = defendant_evidence[e]['evidence']
                                    ref = defendant_evidence[e]['dispute']
                                    if ref != '' and ref is not None:
                                        res = f'{count}. 针对证据{evi}，{ref}\n'
                                    else:
                                        res = f'{count}. 针对证据{evi}，无反驳意见。'
                                    res = res.replace('。，', '，')
                                    system_prompt += f'{res}'
                                    count += 1
                            else:
                                system_prompt += '无\n'
                        elif '{other_statement}' in p:
                            if len(other_statement) > 0:
                                system_prompt += other_statement + '\n'
                            else:
                                system_prompt += '无\n'
                        elif '同时，你需要遵循如下的注意事' in p:
                            system_prompt += '\n' + p + '\n'
                        elif '{' not in p:
                            system_prompt += p + '\n'
            if system_prompt.endswith('\n'):
                system_prompt = system_prompt[:-1]
            self.system_prompt = system_prompt
            
        super(Qwen3_32BPlaintiff_civilPrediction, self).__init__(engine)
        self.id = id
    
    @staticmethod
    def add_parser_args(parser):
        parser.add_argument('--plaintiff_temperature', type=float, default=0, help='temperature')
        parser.add_argument('--plaintiff_max_tokens', type=int, default=4096, help='max tokens')
        parser.add_argument('--plaintiff_top_p', type=float, default=1, help='top p')
        parser.add_argument('--plaintiff_frequency_penalty', type=float, default=0, help='frequency penalty')
        parser.add_argument('--plaintiff_presence_penalty', type=float, default=0, help='presence penalty')
    
    def speak(self, content, save_to_memory = True):
        messages = [{"role": memory[0], "content": memory[1]} for memory in self.memories]
        messages.append({"role": "user", "content": f"{content}"})

        response = self.engine.get_response(messages)
        
        if save_to_memory:
            self.memorize(("user", f"{content}"))
            self.memorize(("assistant", response))
        
        return response