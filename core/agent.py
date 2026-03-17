# core/agent.py

from core.llm_manager import get_llm
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import os
from core.rag import simple_retrieval
from rag.retriever import retrieve



def generate_image_stub(prompt: str):
    """
    临时图像生成函数（MVP）
    实际上只是返回一张本地图片
    """

    img_path = "images/city_cyperpunk.png"

    if not os.path.exists(img_path):
        return None

    return img_path


class SimpleAgent:

    def __init__(self, model_name):
        # 设计模式：工厂模式。根据传入的 model_name 获取不同的 LLM 实例，方便后续扩展支持更多模型。
        self.llm = get_llm(model_name)

    def detect_tool(self, message: str):
        """
        最简单的工具判别
        """

        keywords = [
            "画",
            "生成图片",
            "画一张",
            "image",
            "picture"
        ]

        for k in keywords:
            if k in message:
                return "image_gen"

        return None

    def chat(self, message, history, use_rag=False, document_context=None):

        # 1 先判断是否调用工具
        tool = self.detect_tool(message)

        # =========================
        # ✅ 图片生成：返回结构化数据
        # =========================
        if tool == "image_gen":

            img_path = generate_image_stub(message)

            if img_path:
                return {
                    "type": "image",
                    "content": "我为你生成了一张图片",
                    "image_path": img_path
                }
            else:
                return {
                    "type": "text",
                    "content": "图片生成失败"
                }


        # 2 正常 LLM 对话
        messages = [
            SystemMessage(content="你是一个AI助手。")
        ]

        # 加入历史
        for msg in history:    # history 是一个列表，包含之前的对话记录，每条记录是一个字典，包含 "role" 和 "content" 两个字段

            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))

            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))

        # =========================
        # ✅ 优先：全文 context 模式
        # =========================
        if document_context:

            full_prompt = f"""
请基于以下完整文档回答问题：

{document_context}

问题：
{message}
"""

            messages.append(HumanMessage(content=full_prompt))

        elif use_rag:    # RAG

            context = retrieve(message)

            rag_prompt = f"""
根据以下资料回答问题：

{context}

问题：
{message}
"""

            messages.append(HumanMessage(content=rag_prompt))

        else:
            messages.append(HumanMessage(content=message))

        response = self.llm.invoke(messages)

        # return response.content

        return {
            "type": "text",
            "content": response.content
        }