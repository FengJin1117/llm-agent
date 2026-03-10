# llm-agent/app.py

import gradio as gr

from dotenv import load_dotenv
import os

load_dotenv()   # 自动读取 .env

from ui.chat_ui import build_chat_ui


def main():
    demo = build_chat_ui()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )


if __name__ == "__main__":
    main()