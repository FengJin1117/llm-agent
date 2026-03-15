# rag/retriever.py

from rag.vector_store import build_vector_store

# 这里每每次 import 都会重新 embedding 文档。这会 非常慢，非常占GPU/CPU
# vector_store = build_vector_store()

# 使用单例模式，确保向量数据库只被构建一次
vector_store = None

def get_vector_store():

    global vector_store

    if vector_store is None:
        vector_store = build_vector_store()

    return vector_store

# 基于查询从向量数据库中检索相关文档
def retrieve(query, k=2):
    '''
    从向量数据库中检索与查询相关的文档
    :param query: 用户查询
    :param k: 返回的相关文档数量
    :return: 与查询相关的文档内容
    '''
    vs = get_vector_store()

    # 进行相似度搜索，返回最相关的 k 个文档
    docs = vs.similarity_search(query, k=k)

    # 将检索到的文档内容拼接成一个字符串，作为上下文返回
    context = "\n".join([d.page_content for d in docs])

    return context