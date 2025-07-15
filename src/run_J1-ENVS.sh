#!/bin/bash
set -e

python run.py --scenario J1Bench.Scenario.KQ --trainee Agent.Trainee.ConsultGPT --save_path "/root/J1Bench/src/data/dialog_history/GPT/KQ_dialog_history.jsonl"
python run.py --scenario J1Bench.Scenario.LC --trainee Agent.Trainee.LC_GPT --save_path "/root/J1Bench/src/data/dialog_history/GPT/LC_dialog_history.jsonl"
python run.py --scenario J1Bench.Scenario.CD --lawyer Agent.Lawyer.GPT_CD --save_path "/root/J1Bench/src/data/dialog_history/GPT/CD_dialog_history.jsonl"
python run.py --scenario J1Bench.Scenario.DD --lawyer Agent.Lawyer.GPT_DD --save_path "/root/J1Bench/src/data/dialog_history/GPT/DD_dialog_history.jsonl"
python run.py --scenario J1Bench.Scenario.CI --judge Agent.Judge.GPT_CI --save_path "/root/J1Bench/src/data/dialog_history/GPT/CI_dialog_history.jsonl"
python run.py --scenario J1Bench.Scenario.CR --judge Agent.Judge.GPT_CR --save_path "/root/J1Bench/src/data/dialog_history/GPT/CR_dialog_history.jsonl"