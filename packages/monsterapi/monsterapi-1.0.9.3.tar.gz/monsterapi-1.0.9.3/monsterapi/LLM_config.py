from pydantic import BaseModel, ConfigDict, validator, model_validator, ValidationError, Field, root_validator
from typing import Optional, Literal, Dict
import re

class PretrainedModelConfig(BaseModel):
    model_path: str = "mistralai/Mistral-7B-v0.1"
    resume_checkpoint_path: str = ''
    use_lora: bool = True
    lora_r: int = Field(8, gt=0, lt=2048)
    lora_alpha: int = Field(16, gt=0, lt=2048)
    lora_dropout: float = Field(0.0, ge=0.0, le=1.0)
    lora_bias: str = 'none' 
    use_quantization : bool = Field(False, description = "Enable to Use QLoRA")
    use_gradient_checkpointing : bool = Field(False, description = "Enable to use gradient checkpointing")
    parallelization : Literal["nmp"] =  Field("nmp", description = "Parallelization to use currently only support nmp.")
    
    model_config = ConfigDict(protected_namespaces=())

class DataConfig(BaseModel):
    data_path: str = Field("tatsu-lab/alpaca", description="Hugging Face Dataset Path", 
                           examples=["Zangs3011/large_context_length_dummy_data", 
                                     "s3://example/presignedurl/data.parquet?sdsdsddfsd"])
    data_subset: Optional[str] = Field(default=None, description="Optional subset of the dataset to use.")
    data_source_type: Literal['hub_link', 's3_presigned_link'] = Field(default='hub_link')
    prompt_template: str = Field("Here is an example on how to use tatsu-lab/alpaca dataset ### Input: {instruction} ### Output: {output}", description = "Prompt template to be used to traning keys between curly braces is interpreted as column name and they should be present in the dataset." ,
                                    examples=["Here is an example on how to use tatsu-lab/alpaca dataset ### Input: {instruction} ### Output: {output}"])  
    cutoff_len: int = Field(default=512)
    data_split_config: Dict[str, float] = Field(default={'train': 0.9, 'validation': 0.1}, description="Ratio to split the data provided as train and validation set.")
    prevalidated: bool = Field(default=False, description = "For non pro user using private hf dataset datavalidations cannot be dynamic please set this to True to you are sure dataset has all column names expected in prompt_config and structure is proper and data_subset is appropriate!")

class TrainingConfig(BaseModel):
    early_stopping_patience: int = Field(5, gt = 0, description = "Early stopping patience steps")
    num_train_epochs: float = Field(1, gt=0, description="Number of training epochs. Must be greater than 0.")
    gradient_accumulation_steps: int = Field(1, gt = 0, lt = 1000, description = "Number of steps to forward pass and accumulate steps.")
    warmup_steps: int = Field(50, ge=1, description="Number of warm-up steps. Must be a positive integer.")
    learning_rate: float = Field(0.001, gt=0, lt=1, description="Learning rate for training. Must be between 0 and 1.")
    lr_scheduler_type: Literal["linear", "cosine", "cosine_with_restarts", "polynomial", "constant", "constant_with_warmup", "inverse_sqrt", "reduce_lr_on_plateau"] = Field("reduce_lr_on_plateau", description="Type of learning rate scheduler.")
    group_by_length: bool = Field(False, description="Group sequence by length to optimize training.")
    preference_optimization: Literal["ORPO","DONT"] = Field("DONT", description="Preference Optimization method to use for training.")

class LoggingConfig(BaseModel):
    use_wandb: bool = False
    wandb_username: str = ''
    wandb_login_key: str = ''
    wandb_project: str = ''
    wandb_run_name: str = ''

class HuggingfaceConfig(BaseModel):
    hf_token: Optional[str] = Field(None, description = "hf_token to use to download if private dataset is provided and also push the model into hub.")
    hf_model_path: Optional[str] = Field(None, description = "Name of model to push into hugging face, above token will be used.")

class LLMServiceParams(BaseModel):
    pretrainedmodel_config: PretrainedModelConfig
    data_config: DataConfig
    training_config: TrainingConfig
    logging_config: LoggingConfig
    hf_config: HuggingfaceConfig = HuggingfaceConfig()
    user_session_token: Optional[str] = None
    
    
