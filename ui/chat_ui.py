# ui/chat_ui.py

import gradio as gr

from core.agent import SimpleAgent
from config import MODEL_LIST


# 默认 agent
agent = SimpleAgent(model_name=MODEL_LIST[0])

# 响应函数: 这里message需要用role、content、chat_history的格式封装成一个dict
def respond(message, chat_history, model_name, use_rag=False):

    agent = SimpleAgent(model_name)

    if chat_history is None:
        chat_history = []

    # 添加用户消息（dict格式）
    chat_history.append({
        "role": "user",
        "content": message
    })

    # 调用Agent
    response = agent.chat(message, chat_history, use_rag)

    # 添加assistant回复
    chat_history.append({
        "role": "assistant",
        "content": response
    })

    if use_rag:
        tool = "RAG Retrieval"
    else:
        tool = "LLM Chat"

    reasoning = f"""
Step 1: Analyze user request  
Step 2: Select tool → **{tool}**  
Step 3: Call model `{model_name}`  
Step 4: Generate response
"""

    return "", chat_history, reasoning

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
            # Chat Area
            # ----------------------

            with gr.Column(scale=4):

                with gr.Tabs():

                    # ======================
                    # Chat Tab
                    # ======================

                    with gr.Tab("💬 Chat"):

                        chatbot = gr.Chatbot(height=400, sanitize_html=False)

                        # with gr.Accordion("Agent Reasoning", open=False):

                        #     reasoning = gr.Markdown(
                        #         "Agent reasoning steps will appear here."
                        #     )

                    # ======================
                    # Image Generation
                    # ======================

                    with gr.Tab("🎨 Image Generation"):

                        gr.Markdown(
                            "Generate images using Stable Diffusion"
                        )

                        image_prompt = gr.Textbox(
                            label="Prompt",
                            placeholder="A futuristic city skyline at sunset"
                        )

                        generate_btn = gr.Button("Generate Image")

                        image_output = gr.Image(
                            label="Generated Image"
                        )

                        gr.Markdown(
                            "_Image generation backend will be integrated later._"
                        )

            # ----------------------
            # Agent Tools Panel
            # ----------------------

            with gr.Column(scale=0.6):

                gr.Markdown("## ⚙️ Agent Tools")

                tool_llm = gr.Checkbox(label="💬 LLM Chat", value=True)
                tool_img = gr.Checkbox(label="🎨 Image Generation")
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


                gr.Markdown("---")

                model_select = gr.Dropdown(
                    choices=MODEL_LIST,
                    value=MODEL_LIST[0],
                    label="LLM Model"
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

            if file is None:
                return "No file uploaded."

            return f"✅ Document loaded: {file.name}"

        doc_upload.upload(
            upload_document,
            inputs=doc_upload,
            outputs=upload_status
        )

        send.click(
            respond,
            # inputs=[msg, chatbot, model_select],
            inputs=[msg, chatbot, model_select, tool_rag], # 添加RAG选项
            outputs=[msg, chatbot]
        )

    return demo