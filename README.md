# 版本管理
## v0.1
- ✅界面搭建
- ✅LLM：联通。使用Deepseek API。
- ✅自动测试：test/test_llm_connection.py。使用**pytest**命令
- github备份

## v1.0
- 版本条件：拿够6分


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


# QuickStart
创建环境：
```
conda create -n agent python=3.10 -y
conda activate agent
pip install -r requirements.txt
```

设置API_KEY:
```
export DEEPSEEK_API_KEY=sk-xxxx
```