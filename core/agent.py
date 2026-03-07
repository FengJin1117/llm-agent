from core.llm_manager import get_llm
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage


class SimpleAgent:

    def __init__(self, model_name):
        self.llm = get_llm(model_name)

    def chat(self, message, history):

        messages = [
            SystemMessage(content="你是一个AI助手。")
        ]

        for msg in history:

            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))

            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))

        response = self.llm.invoke(messages)

        return response.content