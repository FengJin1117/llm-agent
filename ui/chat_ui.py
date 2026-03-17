# ui/chat_ui.py

import gradio as gr

from core.agent import SimpleAgent
from config import MODEL_LIST

# 全局文档上下文（为了应对上传PDF的功能）
document_context = None

# 默认 agent
agent = SimpleAgent(model_name=MODEL_LIST[0])

# 响应函数: 这里message需要用role、content、chat_history的格式封装成一个dict
def respond(message, chat_history, model_name, use_rag=False):

    global document_context

    agent = SimpleAgent(model_name)

    if chat_history is None:
        chat_history = []

    chat_history.append({
        "role": "user",
        "content": message
    })

    # =========================
    # ✅ 关键改动：传 document_context
    # =========================
    result = agent.chat(
        message,
        chat_history,
        use_rag=use_rag,
        document_context=document_context
    )


    # =========================
    # ✅ 根据返回类型处理
    # =========================

    if result["type"] == "image":

        chat_history.append({
            "role": "assistant",
            "content": result["content"]
        })

        return "", chat_history, result["image_path"]

    else:

        chat_history.append({
            "role": "assistant",
            "content": result["content"]
        })

        return "", chat_history, None

def build_chat_ui():

    with gr.Blocks(title="LLM Agent Prototype System") as demo:

        # ======================
        # Header
        # ======================

        gr.Markdown("""
# 🤖 LLM Agent Prototype System

**Multimodal AI Agent Platform**
                    
💬 LLM Chat · 📚 RAG Retrieval · 🎨 Image Generation · 🛠 Tool Agent
                    """)

        # ======================
        # Main Layout
        # ======================

        with gr.Row():

            # ----------------------
            # 左：Chat Area
            # ----------------------

            with gr.Column(scale=4):

                gr.Markdown("### 💬 Chat")

                chatbot = gr.Chatbot(height=600, sanitize_html=False)

                # with gr.Tabs():

                #     # ======================
                #     # Chat Tab
                #     # ======================

                #     with gr.Tab("💬 Chat"):

                #         chatbot = gr.Chatbot(height=400, sanitize_html=False)


            # ======================
            # Image 展示（核心改动）
            # ======================
            with gr.Column(scale=2):

                gr.Markdown("### 🖼 Generated Image")

                image_output = gr.Image(
                    show_label=False,
                    height=500
                )

            # ----------------------
            # Agent Tools Panel
            # ----------------------

            with gr.Column(scale=1):

                gr.Markdown("## ⚙️ Agent Tools")

        
                model_select = gr.Dropdown(
                    choices=MODEL_LIST,
                    value=MODEL_LIST[0],
                    label="LLM Model"
                )

                gr.Markdown("---")

                tool_llm = gr.Checkbox(label="💬 LLM Chat", value=True)
                # tool_img = gr.Checkbox(label="🎨 Image Generation")
                # tool_video = gr.Checkbox(label="🎬 Video Generation")
                tool_web = gr.Checkbox(label="🌐 Web Search")

                tool_rag = gr.Checkbox(label="📚 RAG Document Search")
                # ======================
                # Document Upload
                # ======================

                gr.Markdown("### 📂 Knowledge Base")

                doc_upload = gr.File(
                    label="Upload Document",
                    file_types=[".txt", ".pdf", ".md"],
                    file_count="single"
                )

                upload_status = gr.Markdown(
                    "_No document uploaded._"
                )


        # ======================
        # Input Area
        # ======================

        with gr.Row():

            msg = gr.Textbox(
                placeholder="Ask the Agent...",
                label="Message",
                scale=4
            )

            send = gr.Button(
                "🚀 Send",
                variant="primary",
                scale=1
            )


        # ======================
        # Example Prompts
        # ======================

        # gr.Markdown("### 💡 Example Prompts")

        examples = gr.Examples(
            examples=[
                "介绍一下你自己",
                "总结一下LLM Agent是什么",
                "生成图片：未来城市、赛博朋克风格",
                "解释RAG检索增强生成",
                "列出最近的AI Agent研究方向"
            ],
            inputs=msg, # Examples 输入必须要绑定到一个输入组件上，这样点击示例时会自动填充输入框
        )

        # ======================
        # Events
        # ======================

        def upload_document(file):

            global document_context

            if file is None:
                return "No file uploaded."

            # =========================
            # ✅ 读取文件内容
            # =========================
            try:
                if file.name.endswith(".pdf"):
                    from PyPDF2 import PdfReader
                    reader = PdfReader(file.name)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text() or ""

                else:
                    with open(file.name, "r", encoding="utf-8") as f:
                        text = f.read()

                document_context = text

                return f"✅ Document loaded: {file.name} (已进入上下文模式)"

            except Exception as e:
                return f"❌ 解析失败: {str(e)}"

        doc_upload.upload(
            upload_document,
            inputs=doc_upload,
            outputs=upload_status
        )

        send.click(
            respond,
            # inputs=[msg, chatbot, model_select],
            inputs=[msg, chatbot, model_select, tool_rag], # 添加RAG选项
            outputs=[msg, chatbot, image_output]
        )

    return demo