<div align="center">

<h1>Ready Jurist One: Benchmarking Language Agents for Legal Intelligence in Dynamic Environments</h1>
  
[![Generic badge](https://img.shields.io/badge/🤗-Huggingface%20Repo-green.svg)](https://huggingface.co/Go4miii/DISC-FinLLM)
[![license](https://img.shields.io/github/license/modelscope/modelscope.svg)](./LICENSE)

[Project Home](https://j1bench.github.io/) | [Paper](https://arxiv.org/abs/2507.04037) | [Hugging Face](https://huggingface.co/papers/2507.04037) | [Open Compass](https://hub.opencompass.org.cn/dataset-detail/J1-Bench) 

*Zheng Jia\*, Shengbin Yue\*, Wei Chen, Siyuan Wang, Yidong Liu, Yun Song, Zhongyu Wei*


</div>

J1-Bench is an **interactive and comprehensive legal benchmark** where LLM agents engage in diverse legal scenarios, completing tasks through interactions with various participants under procedural rules.

![Demonstration of J1-Envs](https://github.com/FudanDISC/J1Bench/blob/main/assets/J1-ENVS.png)

In this repository, we will release:

- J1-Envs: Interactive Legal Environments
- The constructed [J1-Eval Dataset](https://huggingface.co/datasets/CharlesBeaumont/J1-Eval_Dataset).
- J1-Eval: Holistic Legal Agent Evaluation

## News
- **2025.10.01**  🎉🎉🎉 We’re thrilled to announce that we’ll be organizing the [**Agent Court Arena Track**](http://cail.cipsc.org.cn/task_summit?raceID=2&cail_tag=2025) for CAIL 2025 (China AI and Law Challenge)! 

## Content
- [J1-Envs: Interactiv Legal Environments](#j1-envs-interactive-legal-environments)
- [J1-Eval: Holistic Legal Agent Evaluation](#j1-eval-holistic-legal-agent-evaluation)
- [Citation](#citation)

## J1-Envs: Interactive Legal Environments

### Environment Setup
To set up your environment, run the following command:
```
pip install -r requirements.txt 
```


### Run J1-Envs

Navigate to the source directory
```
cd ./src
```
Before running the script, open 'utils/utils_func.py' and enter your API keys for the required services. For instance:
- For OpenAI Models (e.g., GPT-4o): `api_key =""`, `api_base = ""`
- For `vllm serve` (e.g., Qwen3-Instruct-32B) : set `vllm_api_url` with `api_key = ""` and `base_url = ""`

In addition, for `vllm serve`, deploy the api service with the following command:
```
CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 \
vllm serve Qwen/Qwen3-32B \
  --api-key EMPTY --port 8888 \
  --served-model-name Qwen3-32B 
  --tensor-parallel-size 8 \
  --chat-template ./templates/qwen3_nonthinking.jinja \
  --rope-scaling '{"rope_type":"yarn","factor":4.0,"original_max_position_embeddings":32768}' \
  --max-model-len 131072
```
Check [qwen3_nonthinking.jinja](src/templates) for the template.

Execute the script with:
```
bash run_J1-ENVS.sh
```
You can find dialog history documents at [data/dialog_history](src/data/dialog_history)

## J1-Eval: Holistic Legal Agent Evaluation
### Dataset
We construct a high-quality [J1-Eval Dataset](https://huggingface.co/datasets/CharlesBeaumont/J1-Eval_Dataset). Download the dataset and place it in [data/case](src/data/case) before running J1-Envs.

![Distribution of legal attributes for six environments in J1-Eval](https://github.com/FudanDISC/J1Bench/blob/main/assets/J1-Eval.png)

### Evaluation
After running J1-Envs, execute the J1-Eval script with:
```
bash run_J1-Eval.sh
```
You can find the score at [Eval/final_result](src/Eval/final_result). We also provide detailed evaluation results for later check at [Eval/eval_result](src/Eval/eval_result).


![Overall performance ranking across different LLM agent sizes](https://github.com/FudanDISC/J1Bench/blob/main/assets/total_performance.png)


## Citation
If you find our code and data helpful, we kindly request citation of our paper as follows:
```
@article{jia2025readyjuristonebenchmarking,
  author    = {Zheng Jia and Shengbin Yue and Wei Chen and Siyuan Wang and Yidong Liu and Yun Song and Zhongyu Wei},
  title     = {Ready Jurist One: Benchmarking Language Agents for Legal Intelligence in Dynamic Environments},
  year      = {2025},
 journal    = {arXiv preprint arXiv:2507.04037},
 url        = {https://arxiv.org/abs/2507.04037}
}
```
