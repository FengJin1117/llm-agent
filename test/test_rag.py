"""
RAG 功能测试
"""

from rag.retriever import retrieve
from rag.vector_store import build_vector_store
from core.llm_manager import get_llm

# 测试向量数据库的构建，确保能够成功构建向量数据库
def test_vector_store():

    vs = build_vector_store()

    assert vs is not None

    print("Vector store built successfully")


# 测试 RAG 的检索功能，确保能够从向量数据库中检索到相关文档
def test_rag_retrieval():

    query = "什么是RAG"

    context = retrieve(query)

    print("Retrieved context:\n", context)

    assert context is not None
    assert len(context) > 0


#  测试完整的 RAG pipeline：从检索到生成
def test_rag_generation():

    llm = get_llm("deepseek-chat")

    query = "什么是RAG"

    context = retrieve(query)

    prompt = f"""
根据以下资料回答问题：

{context}

问题：
{query}
"""

    response = llm.invoke(prompt)

    print("RAG Response:", response)

    assert response is not None