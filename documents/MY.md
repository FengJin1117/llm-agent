# 一些“坑”
1. 在 Gradio 6.9.0 中：
Chatbot 只接受 message dict 格式
```
[
 {"role": "user", "content": "..."},
 {"role": "assistant", "content": "..."}
]
```

而不是：

[
 ("user msg", "assistant msg")
]

tuple 是 旧版 Gradio (<4.x) 的格式。

# LangChain 现在的包结构（很多人踩坑）

现在 LangChain 已经拆成：

| 包                     | 功能            |
| --------------------- | ------------- |
| langchain             | 主框架           |
| langchain-core        | 核心接口          |
| langchain-community   | 向量库 / loaders |
| langchain-openai      | OpenAI        |
| langchain-huggingface | embedding     |