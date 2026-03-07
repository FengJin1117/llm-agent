from langchain_openai import ChatOpenAI
from config import DEFAULT_MODEL
import os

def get_llm(model_name=DEFAULT_MODEL):

    if model_name == "deepseek-chat":
        api_key = os.getenv("DEEPSEEK_API_KEY")

        if not api_key:
            raise ValueError(
                "DEEPSEEK_API_KEY not found. Please set environment variable."
            )
        
        return ChatOpenAI(
            model="deepseek-chat",
            base_url="https://api.deepseek.com",
            api_key=api_key,
            temperature=0.7
        )

    if model_name == "gpt-4o-mini":
        return ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7
        )

    return ChatOpenAI(model="gpt-4o-mini")