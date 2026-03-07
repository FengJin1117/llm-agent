# ui/chat_ui.py

import gradio as gr

from core.agent import SimpleAgent
from config import MODEL_LIST


agent = SimpleAgent(model_name=MODEL_LIST[0])


def respond(message, chat_history, model_name):

    agent = SimpleAgent(model_name)

    if chat_history is None:
        chat_history = []

    chat_history.append({
        "role": "user",
        "content": message
    })

    response = agent.chat(message, chat_history)

    chat_history.append({
        "role": "assistant",
        "content": response
    })

    return "", chat_history

def build_chat_ui():

    with gr.Blocks(title="LLM Agent Prototype") as demo:

        gr.Markdown("# 🤖 LLM Agent Prototype")

        with gr.Row():

            model_select = gr.Dropdown(
                choices=MODEL_LIST,
                value=MODEL_LIST[0],
                label="LLM Model"
            )

        # chatbot = gr.Chatbot(height=500, type="messages")

        chatbot = gr.Chatbot(height=500)

        msg = gr.Textbox(
            placeholder="输入问题...",
            label="Message"
        )

        send = gr.Button("Send")

        send.click(
            respond,
            inputs=[msg, chatbot, model_select],
            outputs=[msg, chatbot]
        )

    return demo