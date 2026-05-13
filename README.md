# 多智能体赋能的跨模态零幻觉交互式思政教育系统

本项目面向思政教育场景，探索用 KG-RAG、多智能体协同、Citation 溯源和后续时空沙盘交互，构建一个可解释、可审查、可扩展的思政教育 Demo 系统。

当前阶段重点不是完整最终系统，而是围绕《中国共产党思想政治教育史》资料，先跑通本地 KG-RAG 最小可用链路。

## 1. 当前阶段

当前处于 5 月 Demo 冲刺阶段：

- 已完成 FastAPI 最小接口。
- 已完成 `/health` 和 `/retrieve`。
- 已固定 `/retrieve` 返回结构。
- 已完成 `configs/schema.yaml` 初版数据 Schema。
- 已完成 `src/retriever/hybrid_retriever.py` 的混合检索骨架。
- 已支持读取 `data/processed/text_chunks_demo.jsonl`。
- 已建立思政史展示问题集初版和自动验收脚本。
- 已建立 `team_deliverables/` 管理非核心阶段交付物。

尚未完成：

- 正式 FAISS 向量库。
- 正式 NetworkX 知识图谱。
- 真实 GraphSim。
- 生成智能体、溯源审查智能体、政治红线审查智能体联调。
- XR 时空沙盘前端。

## 2. 目录分工

```text
src/                  核心后端代码
configs/              Schema 与接口契约配置
data/                 系统运行会读取的数据
tests/                自动化测试与正式验收集
team_deliverables/    非核心阶段交付物、汇报素材、草稿和说明文档
outputs/              本地运行产物
README_run.md         本地运行说明
README_architecture.md 检索中枢架构说明
```

重要原则：

- 正式代码不放 `team_deliverables/`。
- 系统运行会读取的数据不放 `team_deliverables/`。
- 成员的说明文档、汇报素材、草稿、交付记录和辅助绘图脚本可以放 `team_deliverables/`。
- 正式代码应在成员个人分支开发，经负责人审核和测试后合并到 `main` 的正式目录。

## 3. 快速启动

建议使用项目虚拟环境：

```powershell
conda activate dachuang_2026
uvicorn src.api.main:app --reload
```

启动后访问：

```text
http://127.0.0.1:8000/docs
```

健康检查：

```text
GET /health
```

检索接口：

```text
POST /retrieve
```

请求示例：

```json
{
  "query": "延安时期思想政治教育有什么特点？"
}
```

## 4. 检索接口返回结构

`/retrieve` 当前返回：

- `status`
- `project`
- `query`
- `query_entities`
- `vector_hits`
- `graph_hits`
- `hybrid_hits`

其中：

- `query_entities`：从用户问题中识别出的关键实体。
- `vector_hits`：文本语义或关键词召回候选。
- `graph_hits`：实体关系召回候选。
- `hybrid_hits`：融合排序后的证据候选。
- `citation`：证据来源，是后续零幻觉审查的基础。

当前融合公式：

```text
hybrid_score = 0.7 * vector_score + 0.3 * graph_score
```

## 5. 本地 mock 模式

默认不设置环境变量时是 `team` 模式，返回固定结构但不主动构造 mock 命中。

如需在本地演示当前 Demo 数据，当前终端设置：

```cmd
set DACHUANG_RETRIEVE_MODE=mock
set DACHUANG_LOCAL_MOCK_ACK=1
uvicorn src.api.main:app --reload
```

PowerShell 示例：

```powershell
$env:DACHUANG_RETRIEVE_MODE="mock"
$env:DACHUANG_LOCAL_MOCK_ACK="1"
uvicorn src.api.main:app --reload
```

不要使用 `setx` 持久化这些变量。

## 6. 测试

运行当前检索验收测试：

```powershell
conda run -n dachuang_2026 python -m pytest tests/test_retrieve.py -q
```

当前测试主要验证：

- mock 模式下展示问题能返回期望证据结构。
- team 默认模式保持固定空结构契约。

## 7. 成员分支与交付规则

当前远程分支：

- `main`
- `pengyihan`
- `lizhuoyang`
- `zhangbohan`
- `zhangruiyang`
- `yanxinhao`

协作规则：

1. 正式代码在个人分支开发。
2. 负责人审核代码和测试结果。
3. 通过后再合并到 `main`。
4. 阶段说明、汇报素材、草稿、辅助绘图脚本放入 `team_deliverables/成员拼音/YYYY-MM-任务名/`。
5. 系统正式读取的数据仍放 `data/`。
6. 正式测试和验收集仍放 `tests/`。

## 8. 相关文档

- `README_run.md`：本地运行说明。
- `README_architecture.md`：检索中枢架构说明。
- `team_deliverables/README.md`：成员阶段性交付物管理规范。
- `configs/schema.yaml`：数据 Schema 初版。
- `configs/retrieve_response.json`：检索返回样例契约。
