from pydantic import BaseModel, Field, ConfigDict, validator
from typing import Literal, Optional

from monsterapi.utils import generate_random_name    

supported_models = [
    "stabilityai/stable-diffusion-xl-base-1.0",
    "stabilityai/stable-diffusion-2",
    "stabilityai/stable-diffusion-2-1"
]

class DreamboothConfig(BaseModel):
    model_name: str = Field(default="stabilityai/stable-diffusion-xl-base-1.0", description="The name of the model to use for training.")
    prompt: str = Field(default="Wolf in Full Moon Light", description="Default training prompt.")
    learning_rate: float = Field(default=1e-4, description="Learning rate for training.")
    num_steps: int = Field(default=500, description="Number of training steps.")
    gradient_accumulation: int = Field(default=4, description="Number of steps for gradient accumulation.")
    resolution: int = Field(default=1024)
    gradient_checkpointing: bool = Field(default=False, description="Whether to use gradient checkpointing.")
    scheduler: str = Field(default="constant", description="Scheduler to use for learning rate.")

    model_config = ConfigDict(protected_namespaces=())
    
    @validator('model_name')
    def _validate_model_path(cls, variable):
        if variable not in supported_models:
            raise ValueError(f"{variable} is an invalid base model. Please choose from the predefined list.")

class HuggingFaceConfig(BaseModel):
    push_to_hub: bool = Field(default=False, description="Whether to push the model to Hugging Face's model hub.")
    repo_id: str = Field(default="", description="Repository ID for the model in the Hugging Face hub.")

class UserCreds(BaseModel):
    hf_token: str = Field(default="", description="Hugging Face Write token for authentication.")
    aws_access_key_id: str = Field(default="", description="AWS access key ID.")
    aws_secret_access_key: str = Field(default="", description="AWS secret access key.")

class DatasetConfig(BaseModel):
    data_source_type: Literal['s3_presigned_link', 's3_creds', 'local'] = Field(default="local", description="Type of the data source.")
    s3_presigned_url: str = Field(default="", description="Presigned URL for S3 if using s3_presigned_link.")
    s3_bucket_name: str = Field(default="", description="Bucket name for S3 if using s3_creds.")
    s3_object_key: str = Field(default="", description="The object key of the dataset in the S3 bucket.")
   
default_dataset_config = DatasetConfig(data_source_type="s3_presigned_link", s3_presigned_url = "https://finetuning-service.s3.us-east-2.amazonaws.com/test_bucket/sdxl_dreambooth_test_images.zip")
                                                  
class DreamboothServiceParams(BaseModel):
    dreambooth_config: DreamboothConfig = Field(default_factory=DreamboothConfig, description="Dreambooth training configuration.")
    huggingface_config: HuggingFaceConfig = Field(default_factory=HuggingFaceConfig, description="Huggingface config to push model to hub and to which repo id. If not set model will downloadable through link.")
    dataset_config: DatasetConfig = Field(default = default_dataset_config, description= "Dreambooth dataset config lets user provide dataset as zip of image from s3 pregigned link of path to s3 file. When path to s3 file is provided s3 creds are expected in user_creds.")
    user_creds: UserCreds = Field(default_factory=UserCreds, description="Provide HuggingFace Write Key if model is to be pushed into HuggingFace. Provide s3 creds if above dataset config s3 bucket and key is being used.")

default_hf_token = "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"

class DreamboothDeploymentConfig(BaseModel):
    deployment_name: str = Field(generate_random_name(with_uuid=False), description="Unique deployment for the instance, auto-generated if not provided.")
    basemodel_path: Literal[
        "stabilityai/stable-diffusion-xl-base-1.0",
        "stabilityai/stable-diffusion-2",
        "stabilityai/stable-diffusion-2-1"
    ] = Field(None, description="SDXL basemodel used for finetuning.", examples=["stabilityai/stable-diffusion-xl-base-1.0"])
    hf_token: str = Field(default_hf_token, description="Token for accessing private models in the Hugging Face repository.")
    loramodel_path: str = Field(None, description="Path to the LoRA model can be a huggingface model or a custom model link to zip file or leave empty string to not use lora model.", examples=["monsterapi/sdxl_finetuning_anime"])
    


