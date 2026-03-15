# 项目结构
llm-agent-ui/
│
├── app.py                # ⭐入口文件（必须在第一层）
├── config.py             # 配置
├── requirements.txt
│
├── core/
│   ├── llm_manager.py    # LLM切换
│   ├── agent.py          # Agent逻辑
│
├── ui/
│   ├── chat_ui.py        # 聊天界面
│
├── tools/
│   ├── image_gen.py      # 图像生成（Stable Diffusion接口）
│   ├── search.py         # 搜索工具
│
└── rag/
    ├── vector_store.py
