from pydantic import BaseModel, Field, validator
from typing import Optional, Literal, List
import uuid


FINETUNE_SERVICES = ["llm", "speech2text/whisper", "text2image/sdxl-dreambooth"]
DEPLOY_SERVICES = ["llm", "custom_image", "sdxl-dreambooth"]
loramodel_path_examples = ["qblocks/OpenPlatypus_LLAMA2_7b", "", "https://finetuning-service.s3.us-east-2.amazonaws.com/finetune_outputs/634d0d26-b518-47b8-a0c9-84df7c672b12/634d0d26-b518-47b8-a0c9-84df7c672b12.zip"]
basemodel_path_examples = ["meta-llama/Llama-2-7b-hf"]

### LLM Deploy ###
class LLMServingParams(BaseModel):
    deployment_name: str = Field(None, description="Unique deployment for the instance, auto-generated if not provided.")
    basemodel_path: str = Field(..., description = "Path to a huggingface base model or a url to a zip file containing model. Either way model provided should be compatible with transformers.AutoModelForCausalLM and vllm.", examples= basemodel_path_examples)
    loramodel_path: str = Field(None, description = "Path to the LoRA model can be a huggingface model or a custom model link to zip file or leave empty string to not use lora model.", examples=loramodel_path_examples)
    prompt_template: str = Field("{prompt}{completion}", description = f"Template for the prompt", examples=["{prompt}{completion}"])
    per_gpu_vram: Literal[8, 16, 24, 40, 48, 80] = Field(..., description = "Per GPU VRAM to be used", examples=[24])
    gpu_count: Literal[1, 2, 4, 8] = Field(..., description = "Number of GPUs to be used, if multiple gpus are selected ", examples=[1])
    api_auth_token: str = Field(str(uuid.uuid4()), description = "API authentication token to be able to access the monsterapi deploy service llm endpoint, auto-generated if not provided.")
    use_nightly: bool = Field(False, description = "Use nightly docker image for the deployment, experimental!")
    multi_lora: bool = Field(False, description = "Use Multi LoRA docker image! If enabled engine switches to support multi lora. For non multi lora use cases performance will be dropped.")
    max_model_len: Optional[int] = Field(None, description="Set to None to use baseModel default context length or to set value!")

### Custom Image Deploy
class custom_image_serving_params(BaseModel):
    deployment_name: Optional[str] = Field(None, description="Unique deployment for the instance, auto-generated if not provided.")
    per_gpu_vram: Literal[8, 16, 24, 40, 48, 80] = Field(..., description = "Per GPU VRAM to be used", examples=[24])
    gpu_count: Literal[1, 2, 4, 8] = Field(..., description = "Number of GPUs to be used, if multiple gpus are selected ", examples=[1])

class InstanceParams(BaseModel):
    harddisk: str = Field("100", description="Hard disk size in GB. Provide value considering your model size.")
    blockName: str = Field("qb24-v2-n1", description="Name of the block to be used for the instance. Use pypi client for automation.")

class DockerImgParams(BaseModel):
    registryName: str = Field("hello-world", description="Name of the docker registry or docker image url", examples=[ "qblocks/dummy-imagepath:latest"])
    username: str = Field("", description="Username for the docker hub registry", examples=["qblocks"])
    password: str = Field("", description="Password for the docker hub registry", examples=["qblocksdummy password"])

class CustomImageParams(BaseModel):
    serving_params: custom_image_serving_params = Field(..., description="Instance parameters for the deployment")
    image_registry: DockerImgParams = Field(..., description="Docker image parameters for the deployment")
    env_params: dict = Field(..., description="Environment variables for the deployment")
    port_numbers: List[int] = Field(..., description="Port numbers for the deployment")
