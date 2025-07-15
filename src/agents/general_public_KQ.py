from .base_agent import Agent
from utils.register import registry, register_class
import json

@register_class(alias="Agent.General_public.ConsultBase")
class General_public_consult(Agent):
    def __init__(self, engine=None, general_public_info=None, name="B"):
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
        messages.append({"role": "user", "content": f"<General_public> {content}"})

        response = self.engine.get_response(messages)
        
        if save_to_memory:
            self.memorize(("user", f"<General_public> {content}"))
            self.memorize(("assistant", response))
        
        return response

@register_class(alias="Agent.General_public.ConsultGPT")
class GPTGeneral_public_consult(Agent):
    def __init__(self, args, general_public_info=None, name="B"):
        engine = registry.get_class("Engine.GPT4o_1120")(
            openai_api_key=args.general_public_openai_api_key,
            openai_api_base=args.general_public_openai_api_base,
            openai_model_name=args.general_public_openai_model_name,
            temperature=args.general_public_temperature,
            max_tokens=args.general_public_max_tokens
        )

        id = 1
        roles = general_public_info['roles']
        topic_list = general_public_info['topic_list']
        
        if args.scenario == "J1Bench.Scenario.KQ":
            system_prompt = '''你是{occupation}，正在与{legal_agent}交流{theme}主题。请根据你的人物设定，按照下方“咨询列表”中的话题内容，逐项向{legal_agent}提问。
            以下是你的人物设定：
            职业：{occupation}
            感兴趣的主题：{theme}
            说话风格：{style}  
            
            咨询列表（请从中逐一提问）：
            {topic_list}

            在咨询过程中，你必须遵循以下要求：  
            1、逐项提问：你必须首先请求{legal_agent}讲解“感兴趣的主题”，再严格按照咨询列表的顺序进行提问，每轮对话只聚焦一个话题。在当前话题完全讨论清楚之前，不得跳过或提前切换到其他话题。
            2、自然表达：你的所有发言需以第一人称视角展开，语言风格应贴合你的设定，像现实中向{legal_agent}咨询一样，语言要口语化、有情绪、可以有犹豫、重复和停顿。请不要机械照搬咨询列表中的内容，应结合实际语境自然转述。
            3、深入追问：如果{legal_agent}的回答不清楚或无法解决你的疑问，你可以围绕当前话题继续追问，直到获得明确解答。但禁止跨话题或提前提问下一个话题。
            4、完成所有咨询后再结束：你只有在确认所有话题均已完成后才能结束对话。此时，请直接输出“结束对话”，并终止交流。

            以下是还没有完成咨询的话题列表：
            {unfinished_topics}'''

            
            count = 1
            content = ''
            for l in topic_list:
                topic = l['topic']
                content += f'话题{count}.' + topic + '\n'
                count += 1

            system_prompt = system_prompt.format(
                occupation = roles['general_public']['occupation'],
                legal_agent = roles['legal_agent'],
                topic_list = content,
                unfinished_topics = content,
                style = roles['general_public']['behavioral_style'],
                theme = general_public_info['theme'],
                ) 

            
            
            system_prompt = system_prompt.replace(' ','').replace('。。','。').replace('\n\n\n','\n')
            if system_prompt.endswith('\n'):
                system_prompt = system_prompt[:-1]
            
            self.system_prompt = system_prompt
            self.topic_list = topic_list
            self.legal_agent = roles['legal_agent']
            self.general_public_role = roles['general_public']['occupation']

        super(GPTGeneral_public_consult, self).__init__(engine)
        self.id = id
    
    @staticmethod
    def add_parser_args(parser):
        parser.add_argument('--general_public_openai_api_key', type=str, help='API key for OpenAI')
        parser.add_argument('--general_public_openai_api_base', type=str, help='API base for OpenAI')
        parser.add_argument('--general_public_openai_model_name', type=str, help='API model name for OpenAI')
        parser.add_argument('--general_public_temperature', type=float, default=0, help='temperature')
        parser.add_argument('--general_public_max_tokens', type=int, default=4096, help='max tokens')

    def speak(self, content, save_to_memory = True):
        messages = [{"role": memory[0], "content": memory[1]} for memory in self.memories]
        messages.append({"role": "user", "content": f"{content}"})

        response = self.engine.get_response(messages)
        
        if save_to_memory:
            self.memorize(("user", f"{content}"))
            self.memorize(("assistant", response))
        
        return response
    



@register_class(alias="Agent.General_public.ConsultQwen3_32B")
class Qwen3_32BGeneral_public_consult(Agent):
    def __init__(self, args, general_public_info=None, name="B"):
        engine = registry.get_class("Engine.qwen3_32B")()

        id = 1
        roles = general_public_info['roles']
        topic_list = general_public_info['topic_list']
        
        if args.scenario == "J1Bench.Scenario.KQ":
            system_prompt = '''你是{occupation}，正在与{legal_agent}交流{theme}主题。请根据你的人物设定，按照下方“咨询列表”中的话题内容，逐项向{legal_agent}提问。
            以下是你的人物设定：
            职业：{occupation}
            感兴趣的主题：{theme}
            说话风格：{style}  
            
            咨询列表（请从中逐一提问）：
            {topic_list}

            在咨询过程中，你必须遵循以下要求：  
            1、逐项提问：你必须首先请求{legal_agent}讲解“感兴趣的主题”，再严格按照咨询列表的顺序进行提问，每轮对话只聚焦一个话题。在当前话题完全讨论清楚之前，不得跳过或提前切换到其他话题。
            2、自然表达：你的所有发言需以第一人称视角展开，语言风格应贴合你的设定，像现实中向{legal_agent}咨询一样，语言要口语化、有情绪、可以有犹豫、重复和停顿。请不要机械照搬咨询列表中的内容，应结合实际语境自然转述。
            3、深入追问：如果{legal_agent}的回答不清楚或无法解决你的疑问，你可以围绕当前话题继续追问，直到获得明确解答。但禁止跨话题或提前提问下一个话题。
            4、完成所有咨询后再结束：你只有在确认所有话题均已完成后才能结束对话。此时，请直接输出“结束对话”，并终止交流。

            以下是还没有完成咨询的话题列表：
            {unfinished_topics}'''

            
            count = 1
            content = ''
            for l in topic_list:
                topic = l['topic']
                content += f'话题{count}.' + topic + '\n'
                count += 1

            system_prompt = system_prompt.format(
                occupation = roles['general_public']['occupation'],
                legal_agent = roles['legal_agent'],
                topic_list = content,
                unfinished_topics = content,
                style = roles['general_public']['behavioral_style'],
                theme = general_public_info['theme'],
                ) 

            
            
            system_prompt = system_prompt.replace(' ','').replace('。。','。').replace('\n\n\n','\n')
            if system_prompt.endswith('\n'):
                system_prompt = system_prompt[:-1]
            
            self.system_prompt = system_prompt
            self.topic_list = topic_list
            self.legal_agent = roles['legal_agent']
            self.general_public_role = roles['general_public']['occupation']
        
        super(Qwen3_32BGeneral_public_consult, self).__init__(engine)
        self.id = id
    
    @staticmethod
    def add_parser_args(parser):
        parser.add_argument('--general_public_openai_api_key', type=str, help='API key for OpenAI')
        parser.add_argument('--general_public_openai_api_base', type=str, help='API base for OpenAI')
        parser.add_argument('--general_public_openai_model_name', type=str, help='API model name for OpenAI')
        parser.add_argument('--general_public_temperature', type=float, default=0, help='temperature')
        parser.add_argument('--general_public_max_tokens', type=int, default=4096, help='max tokens')
        parser.add_argument('--general_public_top_p', type=float, default=1, help='top p')
        parser.add_argument('--general_public_frequency_penalty', type=float, default=0, help='frequency penalty')
        parser.add_argument('--general_public_presence_penalty', type=float, default=0, help='presence penalty')

    def speak(self, content, save_to_memory = True):
        messages = [{"role": memory[0], "content": memory[1]} for memory in self.memories]
        messages.append({"role": "user", "content": f"{content}"})

        response = self.engine.get_response(messages)
        
        if save_to_memory:
            self.memorize(("user", f"{content}"))
            self.memorize(("assistant", response))
        
        return response