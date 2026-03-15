这个错误其实是 **LangChain 1.x 版本结构变化导致的**，不是你代码写错。

核心问题是这一行：

```python
from langchain.vectorstores import FAISS
```

在 **LangChain 1.0 以后被移除了**，向量数据库被拆到了 **langchain-community** 包。

所以会出现：

```
ModuleNotFoundError: No module named 'langchain.vectorstores'
```

而你现在的版本是：

```
langchain 1.2.10
```

这是 **新架构版本**。

---

# 一、正确解决方法（推荐）

安装新模块：

```bash
pip install langchain-community
pip install langchain-huggingface
```

然后修改代码。

---

# 二、修改 vector_store.py

原代码（旧版本）：

```python
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
```

改成 **LangChain 1.x 写法**：

```python
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
```

完整示例：

```python
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
```

---

# 三、同时确认安装 FAISS

如果没装还会报错：

```
faiss not found
```

安装：

```bash
pip install faiss-cpu
```

---

# 四、LangChain 现在的包结构（很多人踩坑）

现在 LangChain 已经拆成：

| 包                     | 功能            |
| --------------------- | ------------- |
| langchain             | 主框架           |
| langchain-core        | 核心接口          |
| langchain-community   | 向量库 / loaders |
| langchain-openai      | OpenAI        |
| langchain-huggingface | embedding     |

所以常见导入现在是：

```python
from langchain_core.messages import HumanMessage
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
```

---

# 五、如果你想最省事（另一种办法）

直接降级 LangChain：

```bash
pip install langchain==0.1.20
```

旧版本就可以继续用：

```python
from langchain.vectorstores import FAISS
```

但是 **我不建议**，因为：

```
LangChain 0.x 已经基本废弃
```

---

# 六、你这个项目建议版本（最稳定）

建议 requirements.txt 写：

```text
langchain>=1.0
langchain-community
langchain-huggingface
faiss-cpu
sentence-transformers
```

---

# 七、修复后再运行

```bash
pytest test/test_rag.py -s
```

如果成功会看到类似：

```
Vector store built successfully
Retrieved context: ...
RAG Response: ...
```

---

# 八、一个隐藏优化（非常建议）

你现在的代码每次都会：

```
build_vector_store()
```

这会 **重复 embedding 文档**，非常慢。

建议改成：

```python
vector_store = build_vector_store()
```

只初始化一次。

---

如果你愿意，我可以 **直接给你一份完整可运行的 RAG 文件结构（大约200行代码）**，会比现在稳定很多，而且**非常适合做 Agent Demo**。
