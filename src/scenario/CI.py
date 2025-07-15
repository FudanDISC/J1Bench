import argparse
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import json
from typing import List
import jsonlines
from tqdm import tqdm
import time
import concurrent
import random
from utils.register import register_class, registry
import threading
from utils.utils_func import load_jsonl

@register_class(alias='J1Bench.Scenario.CI')
class CI:
    def __init__(self, args):
        case_database = load_jsonl(args.case_database)
        self.args = args
        self.case_triplet = []
        for case in case_database:
            plaintiff = registry.get_class(args.plaintiff)(
                args,
                plaintiff_info = case
                )
            defendant = registry.get_class(args.defendant)(
                args,
                defendant_info = case
                )
            judge = registry.get_class(args.judge)(
                args,
                judge_info = case
                )
            plaintiff.id = case['id']
            defendant.id = case['id']
            judge.id = case['id']
            self.case_triplet.append((plaintiff, defendant, judge))
        self.max_conversation_turn = args.max_conversation_turn
        self.save_path = args.save_path
        self.max_workers = args.max_workers
        self.lock = threading.Lock()
        
    @staticmethod
    def add_parser_args(parser):
        parser.add_argument("--case_database", default = "/root/J1Bench/src/data/case/J1-Eval_CI.jsonl", type=str)
        parser.add_argument("--plaintiff", default="Agent.Plaintiff.GPT_CI", help="registry name of plaintiff agent") 
        parser.add_argument("--defendant", default="Agent.Defendant.GPT_CI", help="registry name of defendant agent")
        parser.add_argument("--judge", default="Agent.Judge.GPT_CI", help="registry name of judge agent")
        parser.add_argument("--max_conversation_turn", default=50, type=int, help="max conversation turn")
        parser.add_argument("--save_path", default="/root/J1Bench/src/data/dialog_history/GPT/CI_dialog_history.jsonl", help="save path for dialog history")
        parser.add_argument("--max_workers", default=2, type=int, help="max workers for parallel CI")

    def remove_processed_cases(self):
        processed_case_ids = {}
        if os.path.exists(self.save_path):
            with jsonlines.open(self.save_path, "r") as f:
                for obj in f:
                    processed_case_ids[obj["case_id"]] = 1
            f.close()
        client_num = len(self.case_triplet)
        for i, client in enumerate(self.case_triplet[::-1]):
            print(client[0].id)
            if processed_case_ids.get(client[0].id) is not None:
                self.case_triplet.pop((client_num-(i+1)))
            
        random.shuffle(self.case_triplet)
        print("To-be-consulted case Number: ", len(self.case_triplet))
        
    def run(self):
        self.remove_processed_cases()
        for triplet in tqdm(self.case_triplet):
            plaintiff = triplet[0]
            defendant = triplet[1]
            judge = triplet[2]
            self._civil_prediction(plaintiff, defendant, judge)
    
    def parallel_run(self):
        self.remove_processed_cases()

        st = time.time() 
        print("Parallel Consult Start")
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [executor.submit(self._civil_prediction, plaintiff, defendant, judge) for plaintiff, defendant, judge in self.case_triplet]
            for _ in tqdm(concurrent.futures.as_completed(futures), total=len(self.case_triplet)):
                pass

        print("duration: ", time.time() - st)
        
        
    def save_dialog_info(self, dialog_info):
        with jsonlines.open(self.save_path, "a") as f:
            f.write(dialog_info)
    
    def _civil_prediction(self, plaintiff, defendant, judge):
        dialog_history = [{"turn": 0, "role": "Judge", "content": judge.judge_greetings}]
        print("############### Dialog ###############")
        print("--------------------------------------")
        print(dialog_history[-1]["turn"], dialog_history[-1]["role"])
        print(dialog_history[-1]["content"])
        
        for turn in range(self.max_conversation_turn):
            with self.lock:
                judge_response = judge.speak(dialog_history[-1]["content"])
            
            if judge_response is None:
                break
            else:
                judge_response = judge_response.replace('审判长：','')
            dialog_history.append({"turn": turn+1, "role": "Judge", "content": judge_response.replace('对原告说：', '').replace('对被告说：', '')})
            print("--------------------------------------")
            print(dialog_history[-1]["turn"], dialog_history[-1]["role"])
            print(dialog_history[-1]["content"])
            
            dialogue = ''
            for d in dialog_history:
                dialogue += d["role"] + ": " + d["content"] + "\n"
            
            if '对原告说' in judge_response:
                with self.lock:
                    plaintiff_response = plaintiff.speak(dialogue)
                dialog_history.append({"turn": turn+1, "role": "Plaintiff's Lawyer", "content": plaintiff_response})
            elif '对被告说' in judge_response:
                with self.lock:
                    defendant_response = defendant.speak(dialogue)
                dialog_history.append({"turn": turn+1, "role": "Defendant's Lawyer", "content": defendant_response})
            
            print("--------------------------------------")
            print(dialog_history[-1]["turn"], dialog_history[-1]["role"])
            print(dialog_history[-1]["content"])
            
            if '结束庭审' in judge_response:
                break
            
        dialog_info = {
            "case_id": plaintiff.id,
            'save_path': self.args.save_path,
            "judge": self.args.judge,
            "judge_engine_name": judge.engine.model_path,
            "plaintiff": self.args.plaintiff,
            "plaintiff_engine_name": plaintiff.engine.model_path,
            "defendant": self.args.defendant,
            "defendant_engine_name": defendant.engine.model_path,
            "dialog_history": dialog_history
        }
        print(dialog_info)
        self.save_dialog_info(dialog_info)
            