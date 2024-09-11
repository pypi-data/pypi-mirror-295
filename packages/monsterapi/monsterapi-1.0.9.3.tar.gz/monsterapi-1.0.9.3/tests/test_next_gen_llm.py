# test_generation.py
import pytest
from monsterapi.nextGenLLMClient import LLMClient, GenerateRequest


client = LLMClient()

@pytest.mark.parametrize("model,expected_behavior", [
    ("google/gemma-2-9b-it", {
        "formatted_prompt": None,
        "max_tokens": 128,
        "use_messages": True
    }),
    ("mistralai/Mistral-7B-Instruct-v0.2", {
        "formatted_prompt": None,
        "max_tokens": 128,
        "use_messages": True
    }),
    ("meta-llama/Meta-Llama-3-8B-Instruct", {
        "formatted_prompt": None,
        "max_tokens": 128,
        "use_messages": True
    }),
    ("microsoft/Phi-3-mini-4k-instruct", {
        "formatted_prompt": None,
        "max_tokens": 128,
        "use_messages": True
    })
    # Add more models and their expected behaviors as needed
])
def test_create_and_send_request(model, expected_behavior):
    request = create_request(model)
    response = client.generate(request)  # Send the request using the LLMClient

    assert response is not None, "Expected a response from the API, got None"

    # Additional assertions can be made here based on the expected structure of the response
    # For example, you might want to check the type of response, the presence of certain fields, etc.

def create_request(model: str) -> GenerateRequest:
    return GenerateRequest(
            model=model,
            messages=[
                {"role": "user", "content": "What is your favourite condiment?"},
                {"role": "assistant", "content": "Well, I'm quite partial to a good squeeze of fresh lemon juice. It adds just the right amount of zesty flavour to whatever I'm cooking up in the kitchen!"},
                {"role": "user", "content": "Do you have mayonnaise recipes?"}
            ],
            max_tokens=128,
            n=1,
            temperature=1,
        )
