import os
import json
import torch

from dotenv import load_dotenv
from fastapi import HTTPException
from pydantic import ValidationError
from transformers import AutoTokenizer, AutoModelForCausalLM

from app.schemas.device import Device
from app.prompts.templet import SYSTEM_PROMPT, build_user_prompt


load_dotenv()

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "Qwen/Qwen2.5-0.5B-Instruct"
)


print(f"Loading local model: {MODEL_NAME}")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float32,
    device_map="auto"
)

model.eval()

print("Local model loaded successfully.")


SUSPICIOUS_PHRASES = [
    "ignore previous",
    "ignore all previous",
    "system prompt",
    "you are now",
]


def check_prompt_injection(text: str) -> None:
    """
    Reject obvious prompt-injection attempts.
    """

    text_lower = text.lower()

    for phrase in SUSPICIOUS_PHRASES:
        if phrase in text_lower:
            raise HTTPException(
                status_code=400,
                detail="Potential prompt injection detected."
            )


def generate_response(user_prompt: str) -> str:
    """
    Generate a response using the local Hugging Face model.
    """

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ]

    inputs = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
        return_dict=True,
        return_tensors="pt"
    )

    inputs = {
        key: value.to(model.device)
        for key, value in inputs.items()
    }

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=300,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id
        )

    generated_tokens = outputs[0][
        inputs["input_ids"].shape[-1]:
    ]

    result = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True
    )

    return result.strip()


def clean_json_response(result: str) -> str:
    """
    Extract JSON from the model response.
    """

    result = result.strip()

    if result.startswith("```json"):
        result = result[7:]

    elif result.startswith("```"):
        result = result[3:]

    if result.endswith("```"):
        result = result[:-3]

    result = result.strip()

    start = result.find("{")
    end = result.rfind("}")

    if start == -1 or end == -1 or end <= start:
        raise ValueError(
            "No valid JSON object found in model response."
        )

    return result[start:end + 1]


def extract_device(text: str) -> Device:
    """
    Extract mobile device information from unstructured text
    using a local Hugging Face LLM.
    """

    check_prompt_injection(text)

    max_retries = 2

    user_prompt = build_user_prompt(text)

    for attempt in range(max_retries + 1):

        try:
            result = generate_response(user_prompt)

            cleaned_result = clean_json_response(result)

            json.loads(cleaned_result)

            device = Device.model_validate_json(
                cleaned_result
            )

            return device

        except (
            ValidationError,
            ValueError,
            json.JSONDecodeError
        ) as e:

            if attempt == max_retries:
                raise HTTPException(
                    status_code=422,
                    detail=(
                        "Local LLM output could not be validated "
                        f"after {max_retries + 1} attempts."
                    )
                )

            user_prompt = f"""
The previous response did not match the required Device schema.

Validation error:
{str(e)}

Return ONLY a valid JSON object.

Do not add:
- explanations
- Markdown
- ```json
- comments
- extra text

The JSON must follow the required Device schema exactly.

Original external data:
<external_data>
{text}
</external_data>
"""