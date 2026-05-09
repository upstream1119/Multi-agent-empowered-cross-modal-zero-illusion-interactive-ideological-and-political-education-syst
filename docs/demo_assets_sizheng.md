# 严欣浩 5月Demo展示素材说明

## 1. 当前任务边界

严欣浩当前不负责完整前端、Three.js 沙盘、FAISS、NetworkX、后端 API 或知识库清洗主链路。

5月线上展示阶段的目标是做“展示增强”：

- 整理 5-8 个可视化红色地标节点。
- 输出 `landmarks_demo.jsonl` 和 `landmarks_demo.geojson`。
- 输出 5 条左右时间轴事件 `timeline_demo_sizheng.json`。
- 准备 3 张 PPT 可用图片。
- 说明未来 XR 时空沙盘如何承接当前 KG-RAG 检索结果。

## 2. 本次交付文件

### 图片文件

- `docs/figures/system_pipeline.png`
  - 主题：思政历史 KG-RAG Demo 系统总体链路图。
  - 作用：说明用户问题如何经过 `/retrieve`、实体识别、双路召回、融合排序、多智能体审查，最终得到可信回答。

- `docs/figures/kg_rag_flow.png`
  - 主题：KG-RAG 证据检索与融合打分流程图。
  - 作用：说明我们不是普通 RAG，而是 `vector_hits + graph_hits -> hybrid_hits + citation`。

- `docs/figures/future_sandbox_demo.png`
  - 主题：XR 时空沙盘与思政知识交互设想图。
  - 作用：说明未来如何把红色地标、时间轴、KG-RAG 证据卡片和数字人讲解连接起来。

### 数据文件

- `data/processed/landmarks_demo.jsonl`
  - 6 个红色地标节点。
  - 每行一个地标，便于后续脚本逐行读取。

- `data/processed/landmarks_demo.geojson`
  - 与 JSONL 对应的地图点。
  - 后续 Three.js、Mapbox、Leaflet 或其他地图工具都可以先读这个文件做落点测试。

- `data/processed/timeline_demo_sizheng.json`
  - 5 条时间轴事件。
  - 对应图 3 中的“1921 建党 -> 1935 遵义会议 -> 延安时期 -> 抗战时期 -> 新中国成立”。

### 脚本文件

- `scripts/draw_demo_figures.py`
  - 使用 Python + matplotlib 生成三张 PNG。
  - 如果要改图，不建议直接手动改 PNG，优先改这个脚本后重新运行。

运行命令：

```powershell
python -X utf8 scripts/draw_demo_figures.py
```

## 3. 为什么这样设计

这次不是要做完整前端，而是要让老师在 PPT 中一眼看懂三件事：

1. 当前 Demo 的主线是 KG-RAG 证据检索。
2. 检索结果必须带 citation，体现“零幻觉”和可溯源。
3. 严欣浩负责的时空展示素材，是未来 XR 沙盘承接 KG-RAG 的入口。

所以图片不追求复杂视觉效果，而是强调：

- 框少；
- 箭头清楚；
- 每个框不超过两行；
- 必须出现 `vector_hits`、`graph_hits`、`hybrid_hits`、`citation` 等关键词；
- 明确标注第三张图是“后续扩展示意”，避免被理解成已经完成前端。

## 4. 汇报话术草稿

我这部分暂时不做完整 Three.js 前端，而是为 5月 Demo 提供时空展示素材。当前已经整理了 6 个红色地标节点，包含嘉兴南湖、井冈山、瑞金、遵义、延安和西柏坡；同时整理了 5 条时间轴事件，用来说明未来 XR 时空沙盘的展示逻辑。

这些节点后续可以和 `/retrieve` 的返回结果连接：当用户点击地标或提出问题后，系统先通过 KG-RAG 返回带 citation 的证据，再根据实体匹配时间轴和地图节点，最终在 XR 沙盘中高亮相关地点，并展示可追溯的证据卡片。

因此，我这部分工作的作用不是替代检索系统，而是说明当前 KG-RAG 底座未来如何升级为可交互、可视化、可下钻的时空思政教育体验。
