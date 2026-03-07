# llm-agent/app.py

import gradio as gr

from ui.chat_ui import build_chat_ui

from dotenv import load_dotenv
load_dotenv()

def main():
    demo = build_chat_ui()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )


if __name__ == "__main__":
    main()