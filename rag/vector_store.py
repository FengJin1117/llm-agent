# 构建向量数据库
# 在langchain v1.x中，FAISS和HuggingFaceEmbeddings被移到了langchain-community和langchain-huggingface中，所以需要从这两个库中导入。
# from langchain.vectorstores import FAISS
# from langchain.embeddings import HuggingFaceEmbeddings

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from rag.loader import load_documents


def build_vector_store():

    docs = load_documents()

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = FAISS.from_documents(
        docs,
        embeddings
    )

    return vector_store