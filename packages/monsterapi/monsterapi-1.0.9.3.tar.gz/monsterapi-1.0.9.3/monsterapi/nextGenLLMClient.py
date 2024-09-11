"""
Introducing Next Generation Monster API LLM Client with 

1. Synchronous Results
2. Updated Input and Output token based pricing
3. 99% Cheaper 

Supported Models:
----------------

1. TinyLlama/TinyLlama-1.1B-Chat-v1.0" 
2. "HuggingFaceH4/zephyr-7b-beta" (To be Deprecated shortly)
3. "mistralai/Mistral-7B-Instruct-v0.2" 
4. "microsoft/phi-2" (To be Deprecated shortly)
5. "meta-llama/Meta-Llama-3-8B-Instruct"
6. "microsoft/Phi-3-mini-4k-instruct"
"""

import functools
import requests
import time
import os

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from requests.exceptions import HTTPError
from typing_extensions import TypedDict
from typing import Optional, Literal, List
from pydantic import Field, root_validator, BaseModel, validator

from monsterapi.utils import logging
logger = logging.getLogger(__name__)

class Message(TypedDict):
    role: str  # The role of the message, e.g., "user", "system", or "assistant"
    content: str  # The content of the message

openAI_Message = List[Message]
openai_message_description = """OpenAI Formatted Message:
    messages = [
    {"role": "user", "content": "What is your favourite condiment?"},
    {"role": "assistant", "content": "Well, I'm quite partial to a good squeeze of fresh lemon juice. It adds just the right amount of zesty flavour to whatever I'm cooking up in the kitchen!"},
    {"role": "user", "content": "Do you have mayonnaise recipes?"}]
    
    When this input format is used model prompt template is auto applied.
    **Note this is not supported for microsoft/phi-2.**
    """

class GenerateRequest(BaseModel):
    model: Literal["google/gemma-2-9b-it", "mistralai/Mistral-7B-Instruct-v0.2", "microsoft/Phi-3-mini-4k-instruct", "meta-llama/Meta-Llama-3-8B-Instruct"] = Field("TinyLlama/TinyLlama-1.1B-Chat-v1.0", description="The model to use for generation.")
    formatted_prompt: Optional[str] = Field(None, description="Input to the above model, Model feeds the input here directly to the model. Formatted prompts are to be fed here.")
    messages: Optional[openAI_Message] = Field(None, description=openai_message_description)
    max_tokens: int = Field(256, gt=0, le=4096, description="The maximum number of tokens to generate. Must be between 1 and 2048.")
    n: int = Field(1, gt=0, le=10, description="The number of completions to generate. Must be between 1 and 10.")
    best_of: int = Field(1, gt=0, le=10, description="Generates `n` completions server-side and returns the best. Must be between 1 and 10.")
    presence_penalty: float = Field(0.0, ge=0.0, le=2.0, description="The presence penalty to apply. Must be between 0.0 and 2.0.")
    frequency_penalty: float = Field(0.0, ge=0.0, le=2.0, description="The frequency penalty to apply. Must be between 0.0 and 2.0.")
    repetition_penalty: float = Field(1.0, ge=0.1, le=10.0, description="The repetition penalty to apply. Must be between 0.1 and 10.0.")
    temperature: float = Field(1.0, ge=0.0, le=2.0, description="Sampling temperature to use. Must be between 0.0 and 2.0.")
    top_p: float = Field(1.0, ge=0.0, le=1.0, description="The cumulative probability cutoff to use for nucleus sampling. Must be between 0.0 and 1.0.")
    top_k: int = Field(-1, ge=-1, description="The number of highest probability vocabulary tokens to keep for top-k sampling. Set to -1 to disable.")
    min_p: float = Field(0.0, ge=0.0, le=1.0, description="Minimum probability cutoff to use for nucleus sampling. Must be between 0.0 and 1.0.")
    use_beam_search: bool = Field(False, description="Flag to use beam search. Not all models support beam search.")
    length_penalty: float = Field(1.0, ge=0.0, description="Penalty for sequence length. Only used with beam search.")
    early_stopping: bool = Field(False, description="Flag to stop generation early when all beams reach the end token. Only used with beam search.")
    mock_response: bool = Field(False, description = "Enable to generate mock output useful for integration, doesn't eat any credits.")

    @validator('n', 'best_of')
    def check_n_best_of(cls, v, values, **kwargs):
        if 'n' in values and 'best_of' in values and v < values['n']:
            raise ValueError("`best_of` must be greater than or equal to `n`.")
        return v
    
    @root_validator(pre=True)
    def check_beam_search_settings(cls, values):
        use_beam_search = values.get('use_beam_search', False)
        best_of = values.get('best_of', 1)
        early_stopping = values.get('early_stopping', False)
        temperature = values.get('temperature', 1.0)
        top_p = values.get('top_p', 1)

        if use_beam_search:
            if best_of <= 1:
                raise ValueError('best_of must be greater than 1 when using beam search.')
            if temperature != 0:
                raise ValueError('temperature must be 0 when using beam search.')
            if top_p < 1:
                raise ValueError('top_p must be 1 when using beam search.')

        if not use_beam_search and early_stopping:
            raise ValueError('early_stopping is not effective and must be False when not using beam search.')

        return values

    @validator('top_p')
    def check_top_p(cls, v):
        if not 0 < v <= 1:
            raise ValueError('top_p must be in the range (0, 1], got {}'.format(v))
        return v
    
    @validator('model')
    def check_deprecated_model(cls, value):
        if value in ["HuggingFaceH4/zephyr-7b-beta", "microsoft/phi-2"]:
            logger.warning(f"The model '{value}' is deprecated and will be removed in future releases.")
        return value


class GatewayTimeoutError(Exception):
    """Exception raised for 504 Gateway Timeout errors."""
    def __init__(self, message="504 Gateway Timeout"):
        self.message = message
        super().__init__(self.message)


def retry_on_504(max_retries=3):
    def decorator_retry(func):
        @functools.wraps(func)
        def wrapper_retry(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)  # Attempt to call the function
                except GatewayTimeoutError:
                    retries += 1
                    logger.warning(f"504 Gateway Timeout received, retrying... Attempt {retries}/{max_retries}")
                    if retries >= max_retries:
                        logger.error("Max retries reached. Raising GatewayTimeoutException.")
                        raise  # Reraise the GatewayTimeoutException after max retries
                except Exception as e:
                    logger.error(f"An unexpected error occurred: {e}")
                    raise  # Reraise for any other exceptions
        return wrapper_retry
    return decorator_retry


class LLMClient:
    """
    ## Monster API Next Generation LLM inference API Client

    Monster API Python client for connecting to Generative AI Models on Monster API.

    This class provides methods for interacting with the Monster API to generate content using various Gen AI models.

    Args:
    - `api_key` (Optional[str]): The API key for authentication. If set to None, it will be fetched from the 'MONSTER_API_KEY' environment variable.
    - `base_url` (str): The base URL for the Monster API.

    Raises:
    - `ValueError`: If the 'api_key' is not provided and the 'MONSTER_API_KEY' environment variable is not set.
    """
    def __init__(self, api_key: Optional[str] = None, base_url: str = 'https://llm.monsterapi.ai/v1'):
        if api_key is not None:
            self.auth_token = api_key
        else:
            self.auth_token = os.environ.get('MONSTER_API_KEY')
            if not self.auth_token:
                raise ValueError("MONSTER_API_KEY environment variable not set!")
        
        self.headers = {
            "accept": "application/json",
            'Authorization': 'Bearer ' + self.auth_token}
        self.base_url = base_url

        if self.base_url == None:
            raise ValueError(f"invalid base URL: {self.base_url}!")

    @retry_on_504(max_retries=4)
    def generate(self, request: GenerateRequest):
        payload = request.dict()
        generate_url = f"{self.base_url}/generate"
        response = requests.post(generate_url, json=payload, headers=self.headers, verify=False)

        if response.status_code == 200:
            return response.json()  # Return the API response as a JSON object
        elif response.status_code == 504:
            raise GatewayTimeoutError()
        else:
            response.raise_for_status()
    
