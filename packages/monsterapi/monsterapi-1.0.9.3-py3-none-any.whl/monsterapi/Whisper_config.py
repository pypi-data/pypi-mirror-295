from pydantic import BaseModel, Field, validator
from typing import Literal, Optional
import re
import requests

supported_models = [
    "OpenAI/whisper-large-v3",
    "OpenAI/whisper-large",
    "OpenAI/whisper-medium",
    "OpenAI/whisper-small",
    "OpenAI/whisper-base",
    "OpenAI/whisper-tiny",
    "OpenAI/whisper-large-v2",
    "distil-whisper/distil-small.en",
    "distil-whisper/distil-medium.en",
    "distil-whisper/distil-large-v2",
    "OpenAI/whisper-small.en",
    "OpenAI/whisper-medium.en",
    "OpenAI/whisper-base.en",
    "OpenAI/whisper-tiny.en"
]

class HuggingFaceConfig(BaseModel):
    hf_login_key: str = Field(None, description="Login key for HuggingFace. If using a private dataset from HuggingFace, this key is required.")
    hf_modelsavepath: Optional[str] = Field(None, description="Path to save the finetuned model on HuggingFace.", examples=["qblocks/test_model"])

default_hf_config = HuggingFaceConfig()

class PretrainedModelConfig(BaseModel):
    model_path: str = Field(..., description="Path to the pretrained model. Must be a valid HuggingFace model path.")
    task: Literal["transcribe", "translate"] = Field(..., description="The task for which the model is trained, either 'transcribe' or 'translate'.")
    language: str = Field(..., description="The language of the model.")

    @validator('model_path')
    def _validate_model_path(cls, value):
        if value not in supported_models:
            raise ValueError(f"Model not supported: {value}")
        return value

class DataConfig(BaseModel):
    hf_login_key: Optional[str] = Field(default=None, description="Login key for HuggingFace, if applicable.")
    data_path: str = Field(..., description="Path to the training data. Can be a HuggingFace dataset path or an S3 path.")
    data_subset: Optional[str] = Field(None, description="Specific subset of the training data, if applicable.")
    data_source_type: Literal["hub_link"] = Field("hub_link", description="Type of the data source, default is 'hub_link'.")

class TrainingConfig(BaseModel):
    gradient_accumulation_steps: int = Field(4, ge=1, description="Number of steps for gradient accumulation. Must be a positive integer.")
    learning_rate: float = Field(0.001, gt=0, lt=1, description="Learning rate for training. Must be between 0 and 1.")
    warmup_steps: int = Field(50, ge=1, description="Number of warm-up steps. Must be a positive integer.")
    num_train_epochs: float = Field(1, gt=0, description="Number of training epochs. Must be greater than 0.")
    generation_max_length: int = Field(128, ge=1, le=256, description="Maximum length of the generated text. Must be a positive integer.")
    lr_scheduler_type: Literal["linear", "cosine", "cosine_with_restarts", "polynomial", "constant", "constant_with_warmup", "inverse_sqrt", "reduce_lr_on_plateau"] = Field("reduce_lr_on_plateau", description="Type of learning rate scheduler.")

class LoggingConfig(BaseModel):
    use_wandb: bool = Field(False, description="Flag to indicate if wandb (Weights & Biases) is used for logging.")
    wandb_login_key: str = Field("", description="Login key for wandb, if used.")
    wandb_run_name: str = Field("", description="Run name for wandb logging.")

class WhisperServiceParams(BaseModel):
    huggingface_config: HuggingFaceConfig = Field(default=default_hf_config, description="Configuration for HuggingFace integration.")
    pretrainedmodel_config: PretrainedModelConfig = Field(default=PretrainedModelConfig(model_path="OpenAI/whisper-large-v3", task="transcribe", language="Hindi"), description="Configuration for the pretrained model.")
    data_config: DataConfig = Field(default=DataConfig(data_path="mozilla-foundation/common_voice_13_0", data_subset="hi", data_source_type="hub_link"), description="Configuration for the training data.")
    training_config: TrainingConfig = Field(default=TrainingConfig(gradient_accumulation_steps=4, learning_rate=0.001, warmup_steps=50, num_train_epochs=0.01), description="Configuration for training.")
    logging_config: LoggingConfig = Field(default=LoggingConfig(use_wandb=False, wandb_login_key="API_KEY", wandb_run_name=""), description="Configuration for logging.")
