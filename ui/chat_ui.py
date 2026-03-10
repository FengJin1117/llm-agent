# ui/chat_ui.py

# ui/chat_ui.py

import gradio as gr

from core.agent import SimpleAgent
from config import MODEL_LIST


# 默认 agent
agent = SimpleAgent(model_name=MODEL_LIST[0])


def respond(message, chat_history, model_name):

    agent = SimpleAgent(model_name)

    if chat_history is None:
        chat_history = []

    # 用户消息
    chat_history.append({
        "role": "user",
        "content": message
    })

    # 调用Agent
    response = agent.chat(message, chat_history)

    # agent回复
    chat_history.append({
        "role": "assistant",
        "content": response
    })

    return "", chat_history, f"""
Step 1: Analyze user request  
Step 2: Select tool → **LLM Chat**  
Step 3: Call model `{model_name}`  
Step 4: Generate response
"""


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
        # System Status
        # ======================

        # with gr.Row():？

#             system_status = gr.Markdown(f"""
# ### 🧠 System Status

# - **LLM Model:** {MODEL_LIST[0]}
# - **Vector DB:** FAISS (Not Connected)
# - **Image Model:** Stable Diffusion
# - **Agent Mode:** Enabled
# """)

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

                        chatbot = gr.Chatbot(height=400)

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
                tool_rag = gr.Checkbox(label="📚 RAG Document Search")
                tool_img = gr.Checkbox(label="🎨 Image Generation")
                tool_video = gr.Checkbox(label="🎬 Video Generation")
                tool_web = gr.Checkbox(label="🌐 Web Search")

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
                "生成一个未来城市的图片描述",
                "解释RAG检索增强生成",
                "列出最近的AI Agent研究方向"
            ],
            inputs=msg, # Examples 输入必须要绑定到一个输入组件上，这样点击示例时会自动填充输入框
        )


        # ======================
        # Events
        # ======================

        send.click(
            respond,
            inputs=[msg, chatbot, model_select],
            outputs=[msg, chatbot]
        )

    return demo

# import gradio as gr

# from core.agent import SimpleAgent
# from config import MODEL_LIST


# agent = SimpleAgent(model_name=MODEL_LIST[0])


# def respond(message, chat_history, model_name):

#     agent = SimpleAgent(model_name)

#     if chat_history is None:
#         chat_history = []

#     chat_history.append({
#         "role": "user",
#         "content": message
#     })

#     response = agent.chat(message, chat_history)

#     chat_history.append({
#         "role": "assistant",
#         "content": response
#     })

#     return "", chat_history

# def build_chat_ui():

#     with gr.Blocks(title="LLM Agent Prototype") as demo:

#         gr.Markdown("# 🤖 LLM Agent Prototype")

#         with gr.Row():

#             model_select = gr.Dropdown(
#                 choices=MODEL_LIST,
#                 value=MODEL_LIST[0],
#                 label="LLM Model"
#             )

#         # chatbot = gr.Chatbot(height=500, type="messages")

#         chatbot = gr.Chatbot(height=500)

#         msg = gr.Textbox(
#             placeholder="输入问题...",
#             label="Message"
#         )

#         send = gr.Button("Send")

#         send.click(
#             respond,
#             inputs=[msg, chatbot, model_select],
#             outputs=[msg, chatbot]
#         )

#     return demo