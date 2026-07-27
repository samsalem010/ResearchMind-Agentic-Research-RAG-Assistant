import os
import google.generativeai as genai
import instructor
from agentic_research_rag.config import settings
from agentic_research_rag.logger import logger

from openai import OpenAI
import threading
from dataclasses import dataclass

@dataclass
class UsageStats:
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0

_local = threading.local()

def get_token_usage() -> UsageStats:
    if not hasattr(_local, "usage"):
        _local.usage = UsageStats()
    return _local.usage

def reset_token_usage():
    _local.usage = UsageStats()


# Configure native Gemini API Key if present (for embeddings elsewhere)
if settings.gemini_api_key:
    genai.configure(api_key=settings.gemini_api_key)

# Configure Groq API Key
groq_key = settings.groq_api_key or settings.groke_api_key
if not groq_key:
    raise ValueError("Groq API key is missing. Set GROQ_API_KEY or GROKE_API_KEY in environment.")

# Instantiate OpenAI client pointing to Groq
_groq_client = OpenAI(
    api_key=groq_key,
    base_url="https://api.groq.com/openai/v1"
)

# Model configuration
GROQ_MODEL_NAME = "llama-3.3-70b-versatile"

# Wrap it with Instructor for structured output using JSON mode for maximum compatibility
client = instructor.from_openai(_groq_client, mode=instructor.Mode.JSON)

from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception

def is_rate_limit_error(exception):
    exc_str = str(exception).lower()
    return "429" in exc_str or "quota" in exc_str or "rate limit" in exc_str

_raw_create = client.chat.completions.create

@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=2, min=4, max=60),
    retry=retry_if_exception(is_rate_limit_error),
    reraise=True
)
def _retry_create(*args, **kwargs):
    if "model" not in kwargs:
        kwargs["model"] = GROQ_MODEL_NAME
    
    try:
        result = _raw_create(*args, **kwargs)
    except Exception as e:
        if is_rate_limit_error(e) and kwargs["model"] == "llama-3.3-70b-versatile":
            logger.warning("Rate/Token limit reached for llama-3.3-70b-versatile. Falling back to llama-3.1-8b-instant...")
            kwargs["model"] = "llama-3.1-8b-instant"
            try:
                result = _raw_create(*args, **kwargs)
            except Exception as e2:
                if is_rate_limit_error(e2):
                    logger.warning("Rate/Token limit reached for llama-3.1-8b-instant. Falling back to llama3-8b-8192...")
                    kwargs["model"] = "llama3-8b-8192"
                    result = _raw_create(*args, **kwargs)
                else:
                    raise
        else:
            raise
    
    # Capture instructor tokens
    if hasattr(result, "_raw_response") and hasattr(result._raw_response, "usage") and result._raw_response.usage:
        usage = get_token_usage()
        usage.prompt_tokens += result._raw_response.usage.prompt_tokens
        usage.completion_tokens += result._raw_response.usage.completion_tokens
        usage.total_tokens += result._raw_response.usage.total_tokens
        
    return result

client.chat.completions.create = _retry_create

@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=2, min=4, max=60),
    retry=retry_if_exception(is_rate_limit_error),
    reraise=True
)
def generate_text(prompt: str) -> str:
    """Helper method for unstructured text generation using Groq client."""
    model = GROQ_MODEL_NAME
    try:
        response = _groq_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
    except Exception as e:
        if is_rate_limit_error(e) and model == "llama-3.3-70b-versatile":
            logger.warning("Rate/Token limit reached for llama-3.3-70b-versatile. Falling back to llama-3.1-8b-instant...")
            model = "llama-3.1-8b-instant"
            try:
                response = _groq_client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
            except Exception as e2:
                if is_rate_limit_error(e2):
                    logger.warning("Rate/Token limit reached for llama-3.1-8b-instant. Falling back to llama3-8b-8192...")
                    model = "llama3-8b-8192"
                    response = _groq_client.chat.completions.create(
                        model=model,
                        messages=[
                            {"role": "user", "content": prompt}
                        ]
                    )
                else:
                    raise
        else:
            raise
    
    # Capture raw text generation tokens
    if hasattr(response, "usage") and response.usage:
        usage = get_token_usage()
        usage.prompt_tokens += response.usage.prompt_tokens
        usage.completion_tokens += response.usage.completion_tokens
        usage.total_tokens += response.usage.total_tokens
        
    return response.choices[0].message.content
