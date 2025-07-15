#!/bin/bash
set -e

python /root/J1Bench/src/Eval/bench/KQ/KQ.py
python /root/J1Bench/src/Eval/bench/LC/LC.py
python /root/J1Bench/src/Eval/bench/CD/CD.py
python /root/J1Bench/src/Eval/bench/DD/DD.py
python /root/J1Bench/src/Eval/bench/CI/CI.py
python /root/J1Bench/src/Eval/bench/CR/CR.py