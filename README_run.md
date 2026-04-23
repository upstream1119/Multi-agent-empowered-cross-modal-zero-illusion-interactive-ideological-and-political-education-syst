# 多智能体赋能的跨模态零幻觉交互式思政教育系统 - 开发指南

## ⚙️ 1. 环境准备（当前：Windows 本地试运行）
确保你已经安装 Conda，并在 PowerShell 执行：
```powershell
conda activate dachuang
pip install fastapi uvicorn faiss-cpu networkx pyyaml
```

## 🛠️ 2. 执行纪律：先 Sample，后全量
为了保证数据质量，严禁跳过质检步骤！提交任何数据样本（Sample）或全量数据前，必须在本地运行质检脚本：

```powershell
# 示例：校验你清洗出来的 events.jsonl
python src/utils/validate_jsonl.py data/processed/events.jsonl
```

注意：只有终端打印出 ✅ 质检通过！，才允许将数据提交给组长验收。如果报错，请对照 configs/schema.yaml 自行修改。

## 🌐 3. 本地接口预览（Mock 环境）
当你需要调试后端接口时，启动 FastAPI 服务：

```powershell
uvicorn src.api.main:app --reload
```

服务启动后，可以在浏览器访问 http://127.0.0.1:8000/docs 查看自动生成的 API 文档。
后续迁移到实验室 WSL2 时，命令基本不变，仅终端环境切换。

