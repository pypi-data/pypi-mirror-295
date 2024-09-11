from pydantic import BaseModel, Field
from typing import Optional, Literal, Union, List, Dict, NewType

FileField = NewType('FileField', str)

class LLMInputModel1(BaseModel):
    """
    prompt:  
        type: string
        description: Prompt is a textual instruction for the model to produce an output.	Required

    top_k:
        type: integer	
        description: Top-k sampling helps improve quality by removing the tail and making it less likely to go off topic.	Optional
        default: 40
        
    top_p:
        type: float
        description: Top-p sampling helps generate more diverse and creative text by considering a broader range of tokens. Optional
        default: 1.0

    temp:
        type: float
        description: The temperature influences the randomness of the next token predictions. Optional
        default: 0.98

    max_length:
        type: integer
        description: The maximum length of the generated text. Optional
        default: 256

    repetition_penalty:
        type: float
        description: The model uses this penalty to discourage the repetition of tokens in the output. Optional
        default: 1.2

    beam_size:
        type: integer
        description: The beam size for beam search. A larger beam size results in better quality output, but slower generation times. Optional
        default: 1

    """
    prompt: str
    top_k: int = 40
    top_p: float = Field(0.9, ge=0., le=1.)
    temp: float = Field(0.98, ge=0., le=1.)
    max_length: int = 256
    repetition_penalty: float = 1.2
    beam_size: int = 1


class LLMInputModel2(BaseModel):
    """
    prompt:
        type: string
        description: Instruction is a textual command for the model to produce an output. Required

    top_k:
        type: integer
        description: Top-k sampling helps improve quality by removing the tail and making it less likely to go off topic. Optional
        default: 40

    top_p:
        type: float
        description: Top-p sampling helps generate more diverse and creative text by considering a broader range of tokens. Optional. Allowed Range: 0 - 1
        default: 1.0

    temp:
        type: float
        description: Temperature is a parameter that controls the randomness of the model's output. The higher the temperature, the more random the output. Optional
        default: 0.98

    max_length:
        type: integer
        description: Maximum length of the generated output. Optional
        default: 256

    """
    prompt: str
    top_k: int = 40
    top_p: float = Field(0.9, ge=0., le=1.)
    temp: float = Field(0.98, ge=0., le=1.)
    max_length: int = 256


class SDInputModel(BaseModel):
    """
    prompt:
        type: string
        description: Your input text prompt. Required

    negprompt:
        type: string
        description: Negative text prompt. Optional
        default: ""

    samples:
        type: integer
        description: No. of images to be generated. Allowed range: 1-4. Optional
        default: 1

    steps:
        type: integer
        description: Sampling steps per image. Allowed range 30-500. Optional
        default: 30

    aspect_ratio:
        type: string
        description: Allowed values: square, landscape, portrait. Optional
        default: square

    guidance_scale:
        type: float
        description: Prompt guidance scale. Optional
        default: 7.5

    seed:
        type: integer
        description: Random number used to initialize the image generation. Optional
        default: random

    """
    prompt: str
    negprompt: Optional[str] = ""
    samples: Optional[int] = Field(1, ge=1, le=4)
    steps: Optional[int] = Field(30, ge=30, le=500)
    aspect_ratio: Optional[Literal['square', 'landscape', 'portrait']] = 'square'
    guidance_scale: Optional[float] = 7.5
    seed: Optional[int] = None

class Img2Img(BaseModel):
    """
    prompt:
        type: string
        description: Your input text prompt. Required

    negprompt:
        type: string
        description: Negative text prompt. Optional
        default: ""

    steps:
        type: integer
        description: Sampling steps per image. Allowed range 30-500. Optional
        default: 30

    init_image_url:
        type: string
        description: Original Image URL or local file. Required

    strength:
        type: float
        description: Controls how much the original image will be modified. Optional
        default: 0.75

    guidance_scale:
        type: float
        description: Prompt guidance scale. Optional
        default: 12.5

    seed:
        type: integer
        description: Random number used to initialize the image generation. Optional
        default: random

    """
    prompt: str
    negprompt: Optional[str] = ""
    steps: Optional[int] = Field(30, ge=30, le=500)
    init_image_url: FileField
    strength: Optional[float] = Field(0.75, ge=0.0, le=1.0)
    guidance_scale: Optional[float] = 7.5
    seed: Optional[int] = None

class Pix2Pix(BaseModel):
    """
   prompt:
        type: string
        description: Your input text prompt. Required

    negprompt:
        type: string
        description: Negative text prompt. Optional
        default: ""

    steps:
        type: integer
        description: Sampling steps per image. Allowed range 30-500. Optional
        default: 30

    init_image_url:
        type: string
        description: Original Image URL or local file. Required

    guidance_scale:
        type: float
        description: Prompt guidance scale. Optional
        default: 12.5

    image_guidance_scale:
        type: float
        description: Image guidance scale. Optional
        default: 1.5

    seed:
        type: integer
        description: Random number used to initialize the image generation. Optional
        default: random

    """
    prompt: str
    negprompt: Optional[str] = ""
    steps: Optional[int] = Field(30, ge=30, le=500)
    init_image_url: FileField
    guidance_scale: Optional[float] = Field(7.5, ge=5, le=50)
    image_guidance_scale: Optional[float] = Field(1.5, ge=0, le=5)
    seed: Optional[int] = None

class Txt2Speech(BaseModel):
    """
    prompt:
        type: string
        description: Prompt is a text string that is going to be converted to an audio file. Required

    speaker:
        type: string
        description: Defines the language and speaker for speech. Optional
        default: None

    sample_rate:
        type: integer
        description: Sampling rate for output audio. Optional
        default: 25000

    text_temp:
        type: float
        description: Temperature setting for text prompt. Supported range: 0.1 to 1.0. Optional
        default: 0.5

    waveform_temp:
        type: float
        description: Temperature setting for audio waveform. Supported range: 0.1 to 1.0. Optional
        default: 0.5

    """
    prompt: str
    speaker: Optional[str]
    sample_rate: Optional[int] = 25000
    text_temp: Optional[float] = Field(0.5, ge=0.1, le=1.0)
    waveform_temp: Optional[float] = Field(0.5, ge=0.1, le=1.0)

class Speech2Txt(BaseModel):
    """
    file:
        type: string
        description: URL of a file or local file that needs to be transcribed. Required

    diarize:
        type: bool
        description: When diarize is set to true, an embedding model will be employed to identify speakers, along with their respective transcripts and durations. Optional
        default: False

    transcription_format:
        type: string
        description: Defines the output format. 
        default: 'text'

    prompt:
        type: string
        description: Initial prompt to the whisper model for recognizing words correctly. You can pass a comma separated list of words.
        default: ''

    remove_silence:
        type: bool
        description: If set as true, it will use VAD (Voice Activity Detection) filter to remove silent parts of the audio and then perform transcript with only audible parts.

    language:
        type: string
        description: Defines the language for transcription output. Translates the transcript to your preferred language.

    num_speakers:
        type: int
        description: It specifies the expected number of speakers present in the audio file and is used in conjunction with the "diarize" parameter, which enables speaker diarization.
        default: None

    """
    file: FileField
    diarize: Optional[bool] = False
    transcription_format: Optional[str] = 'text'
    prompt: Optional[str] = ''
    remove_silence: Optional[bool] = False
    language: Optional[str] = 'en'
    num_speakers: Optional[int] = Field(2, ge=1, le=11)

class DeployLLM(BaseModel):
    """
    Deploy LLM service input validator

    input_variables: dict Input to Deploy LLM endpoint in the form of a dictionary. 
            Either input_variables dict or prompt needs to be provided, but not both
    prompt: str Input to Deploy LLM endpoint in the form of a string. No prompt template formatting is
            applied as in case of input_variables. Either input_variables dict or prompt needs to be provided, but not both
    stream: bool If set to True, the output will be streamed back to the client. Optional
    n: int Number of outputs to generate. Optional
    temperature: float Temperature parameter for sampling. Optional
    max_tokens: int Maximum number of tokens to generate. Optional
    """
    input_variables: Optional[dict] = None
    prompt: Optional[str] = None
    stream: Optional[bool] = False
    n: Optional[int] = 1
    temperature: Optional[float] = 0.6
    max_tokens: Optional[int] = 256

class Speech2Txt_v2(BaseModel):
    """
    file:
        type: string
        description: URL of a file or local file that needs to be transcribed. Required

    diarize:
        type: bool
        description: When diarize is set to true, an embedding model will be employed to identify speakers, along with their respective transcripts and durations. Optional
        default: False

    do_sample:
        type: bool
        description: Whether or not to use sampling ; use greedy decoding otherwise. When set to True, this parameter enables decoding strategies such as beam-search multinomial sampling, Top-K sampling and Top-p sampling etc. All these strategies select the next token from the probability distribution over the entire vocabulary with various strategy-specific adjustments. Optional
        default: True
        
    transcription_format:
        type: string
        description: Defines the output format. 
        default: 'text'

    language:
        type: string
        description: Defines the language for transcription output. Translates the transcript to your preferred language.

    num_speakers:
        type: int
        description: It specifies the expected number of speakers present in the audio file and is used in conjunction with the "diarize" parameter, which enables speaker diarization.
        default: None

    top_k:
        type: integer
        description: The number of highest probability vocabulary tokens to keep for top-k-filtering. Optional
        default: 50

    top_p:
        type: float
        description: Top-p sampling helps generate more diverse and creative text by considering a broader range of tokens. Optional
        default: 0.9

    temperature:
        type: float
        description: The value used to modulate the next token probabilities. Optional
        default: 0.9

    repetition_penalty:
        type: float
        description: The model uses this penalty to discourage the repetition of tokens in the output. Optional
        default: 0.9
        
    """
    file: FileField
    diarize: Optional[bool] = False
    do_sample: Optional[bool] = True
    transcription_format: Optional[str] = 'text'
    language: Optional[str] = 'en'
    num_speakers: Optional[int] = Field(2, ge=1, le=11)
    top_k: int = 50
    top_p: float = Field(0.9, ge=0., le=1.)
    temperature: float = Field(0.9, ge=0., le=1.5)
    repetition_penalty: float = Field(0.9, ge=0., le=1.5)

class Photomaker(BaseModel):
    """
    prompt:
        type: string
        description: Your input text prompt. Required

    negprompt:
        type: string
        description: Negative text prompt. Optional
        default: ""

    steps:
        type: integer
        description: Sampling steps per image. Allowed range 10-60. Optional
        default: 30

    init_image_url:
        type: string
        description: Original Image URL or local file. Required

    strength:
        type: float
        description: Controls how much the original image will be modified. Optional
        default: 30

    samples:
        type: integer
        description: No. of images to be generated. Allowed range: 1-3. Optional
        default: 1
        
    seed:
        type: integer
        description: Random number used to initialize the image generation. Optional
        default: random

    safe_filter:
        type: boolean
        description: When the "safe_filter" is set to true, the model will actively filter out any potential NSFW (Not Safe for Work) content
        default: True
    """
    prompt: str
    negprompt: Optional[str] = ""
    steps: Optional[int] = Field(30, ge=10, le=60)
    init_image_url: FileField
    strength: Optional[float] = Field(30, ge=30, le=60)
    samples: Optional[int] = Field(1, ge=1, le=3)
    seed: Optional[int] = None
    safe_filter: Optional[bool] = True
    
MODELS_TO_DATAMODEL = {
            'falcon-7b-instruct': LLMInputModel1,
            'falcon-40b-instruct': LLMInputModel1,
            'mpt-7b-instruct': LLMInputModel2,
            'mpt-30B-instruct': LLMInputModel2,
            'llama2-7b-chat': LLMInputModel1,
            "sdxl-base": SDInputModel,
            "txt2img": SDInputModel,
            "img2img" : Img2Img,
            "pix2pix" : Pix2Pix,
            "sunoai-bark" : Txt2Speech,
            "whisper" : Speech2Txt,
            "codellama-13b-instruct": LLMInputModel1,
            "codellama-34b-instruct": LLMInputModel1,
            "zephyr-7b-beta": LLMInputModel1,
            "deploy-llm": DeployLLM,
            "speech2text-v2":Speech2Txt_v2,
            "photo-maker":Photomaker
            }

MODEL_TYPES = { 
                    "falcon-7b-instruct": "LLM",
                    "falcon-40b-instruct": "LLM",
                    "mpt-30B-instruct": "LLM",
                    "mpt-7b-instruct": "LLM",
                    "llama2-7b-chat": "LLM",
                    "zephyr-7b-beta": "LLM",
                    "deploy-llm": "LLM",
                    "sdxl-base": "TEXT-TO-IMG",
                    "txt2img": "TEXT-TO-IMG",
                    "codellama-13b-instruct": "LLM",
                    "codellama-34b-instruct": "LLM"
                    }