import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")

DEFAULT_MODEL = "deepseek-chat"

MODEL_LIST = [
    "deepseek-chat",
    "gpt-4o-mini",
    "qwen2.5"
]