# Monsterapi v2

A Python client for interacting with Monster API v2 in .

## Installation

```bash
pip install monsterapi
```

Note: For detailed documentation please visit [here](https://github.com/Qblocks/monsterapiclient/blob/main/README.md)

### Has support to following MonsterAPI services:

#### **Beta Next Gen LLM Services**
##### Supported Models:
    1. "TinyLlama/TinyLlama-1.1B-Chat-v1.0", 
    2. "microsoft/phi-2"
    3. "mistralai/Mistral-7B-Instruct-v0.2" 
    4. "HuggingFaceH4/zephyr-7b-beta" 

##### Highlights:

    1. 99% Cheaper 
    2. Synchronous results
    3. Token based Pricing. 


Service Introduction: [here](https://dash.readme.com/project/monster-api/v1.0/docs/introducing-monsterapis-new-nextgen-llm-inference-api)
API Reference: [here](https://developer.monsterapi.ai/reference)
Usage Guide: [here](https://developer.monsterapi.ai/docs/pypi-client-usage-guide)

#### GA LLM Models Old Generation

##### Supported Models:
    1. falcon-7b-instruct
    2. mpt-7b-instruct
    3. llama2-7b-chat
    4. falcon-40b-instruct
    5. mpt-30b-instruct
    6. codellama-13b-instruct
    7. zephyr-7b-beta
    8. Monster Deploy LLMs (deploy-llm)

Detailed payloads of models that are supported ? [here](https://github.com/Qblocks/monsterapiclient/blob/main/docs/InputModelPayload.md)


2. QuickServe API: New service from monsterapi deploy popular LLM models into monsterapi compute infrastructure with one request. 
    
    a. How to use client to launch and manage a quickserve deployment ? [here](https://github.com/Qblocks/monsterapiclient/blob/main/docs/QuickServe_readme.md)

Additional Information link: [here](https://developer.monsterapi.ai/reference/introduction-1)


## Code Documentation: 
Client module code documentation can be found [here](https://github.com/Qblocks/monsterapiclient/blob/main/docs/client.md)

## Basic Usage to access Hosted AI-Models

#### Import Module

```python
from monsterapi import client
```

#### set `MONSTER_API_KEY` env variable to your API key.

```bash
os.environ["MONSTER_API_KEY"] = <your_api_key>
client = client() # Initialize client
```

or

#### pass `api_key` parameter to client constructor.

```bash
client = client(<api_key>) # pass api_key as parameter
```

#### Use generate method
```python
result = client.generate(model='falcon-7b-instruct', data={
    "prompt": "Your prompt here",
    # ... other parameters
})
```

### Quick Serve LLM


#### Launch a llama2-7b model using QuickServe API 

Prepare and send payload to launch a LLM deployment. 
    a. Choose Per_GPU_VRAM and GPU_Count based on your model size and batch size. Please see here for detailed list of supported model and infrastructure matrix.

```python3
launch_payload = {
    "basemodel_path": "meta-llama/Llama-2-7b-chat",
    "loramodel_path": "",
    "prompt_template": "{prompt}{completion}",
    "api_auth_token": "b6a97d3b-35d0-4720-a44c-59ee33dbc25b",
    "per_gpu_vram": 24,
    "gpu_count": 1
}

# Launch a deployment
ret = client.deploy("llm", launch_payload) 
deployment_id = ret.get("deployment_id")
print(ret)

# Get deployment status
status_ret = client.get_deployment_status(deployment_id)
print(status_ret)

logs_ret = client.get_deployment_logs(deployment_id)
print(logs_ret)

# Terminate Deployment
terminate_return = client.terminate_deployment(deployment_id)
print(terminate_return)
```

## Run tests

### Install test dependencies

```bash
pip install monsterapi[tests]
```

### Run functional tests involving actual API key

```bash
export MONSTER_API_KEY=<your_api_key>
python3 -m pytest tests/ # Run all tests includes functional tests using actual API key
```

### Run unit tests

```bash
export MONSTER_API_KEY="dummy"
python3 -m pytest tests/ -m "not slow" # Run only unit tests
```

## PIP package push Instructions

```
pip install --upgrade setuptools wheel

python setup.py sdist bdist_wheel

pip install twine

twine upload dist/*
```

## LLama Index CLient Usage

```bash
pip install llama_index llama-index-core llama-parse llama-index-readers-file 
```

``` python3
from monsterapi.LLamaIndexClient import MonsterLLM

model = "meta-llama/Meta-Llama-3-8B-Instruct"
llm = MonsterLLM(
        model=model, temperature=0.1, max_tokens=256
    )
```

see examples/llama_index_and_chainlit/ for detailed chainlit example

# About us

Check us out at [monsterapi.ai](https://monsterapi.ai)

Checkout our new MonsterAPI Deploy service [here](https://developer.monsterapi.ai/docs/monster-deploy-beta)

Check out new no-code finetuning service [here](https://docs.monsterapi.ai/fine-tune-a-large-language-model-llm/launch-a-fine-tuning-job)

Checkout our Monster-SD Stable Diffusion v1.5 vs XL Comparison space [here](https://huggingface.co/spaces/qblocks/Monster-SD)

Checkout our Monster API LLM comparison space [here](https://huggingface.co/spaces/qblocks/Monster-LLMs)

