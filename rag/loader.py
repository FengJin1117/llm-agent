# from langchain.document_loaders import TextLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter

# v1.x拆包了
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_documents(path="data/docs.txt"):
    # loader: 读取文本文件
    loader = TextLoader(path, encoding="utf-8")
    documents = loader.load()

    # text_splitter: 将文本分割成更小的块，便于后续处理
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300, # 每个块的最大字符数
        chunk_overlap=50 # 块之间的重叠字符数，确保上下文连续性
    )

    docs = text_splitter.split_documents(documents)

    return docs