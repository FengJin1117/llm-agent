"""
测试 DeepSeek API 是否可用
"""

from core.llm_manager import get_llm


def test_deepseek_connection():

    llm = get_llm("deepseek-chat")

    response = llm.invoke("Hello")

    print("Response:", response)

    assert response is not None