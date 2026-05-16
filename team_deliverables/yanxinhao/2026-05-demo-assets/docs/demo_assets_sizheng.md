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

- `../figures/system_pipeline.png`
  - 主题：思政历史 KG-RAG Demo 系统总体链路图。
  - 作用：说明用户问题如何经过 `/retrieve`、实体识别、双路召回、融合排序、多智能体审查，最终得到可信回答。

- `../figures/kg_rag_flow.png`
  - 主题：KG-RAG 证据检索与融合打分流程图。
  - 作用：说明我们不是普通 RAG，而是 `vector_hits + graph_hits -> hybrid_hits + citation`。

- `../figures/future_sandbox_demo.png`
  - 主题：XR 时空沙盘与思政知识交互设想图。
  - 作用：说明未来如何把红色地标、时间轴、KG-RAG 证据卡片和数字人讲解连接起来。

### 数据文件

- `data/processed/landmarks_demo.jsonl`
  - 6 个红色地标节点。
  - 每行一个地标，便于后续脚本逐行读取。

- `data/processed/landmarks_demo.geojson`
  - 与 JSONL 对应的地图点。
  - 后续 Three.js、Mapbox、Leaflet 或其他地图工具都可以先读这个文件做落点测试。
  - 当前坐标统一为 `WGS84`。
  - `precision` 为 `city_demo` 或 `landmark_demo` 的点位都属于 Demo 级近似点位，不是正式测绘坐标。

- `data/processed/timeline_demo_sizheng.json`
  - 5 条时间轴事件。
  - 对应图 3 中的“1921 建党 -> 1935 遵义会议 -> 1942 延安整风 -> 抗战时期 -> 新中国成立”。

### 脚本文件

- `../scripts/draw_demo_figures.py`
  - 使用 Python + matplotlib 生成三张 PNG。
  - 如果要改图，不建议直接手动改 PNG，优先改这个脚本后重新运行。

运行命令：

```powershell
python -X utf8 team_deliverables/yanxinhao/2026-05-demo-assets/scripts/draw_demo_figures.py
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

## 5. 来源与坐标口径说明

### citation 口径

`landmarks_demo.jsonl` 中每个地标都保留 `citation` 字段。

- `doc`：说明当前依据的来源类型，例如《中国共产党思想政治教育史》方向资料、红色地标公开资料或仓库 demo 样例。
- `section`：说明该节点对应的主题段落或展示场景。
- `source_basis`：用一句话解释为什么这个地标可以作为展示节点。
- `page`：当前统一保留为 `null`，等待正式 PDF 清洗材料或权威来源页码复核后再补。
- `verification_status`：当前使用 `source_explained_page_pending` 表示“已有来源依据说明，但页码仍待复核”；延安节点使用 `demo_verified`，因为它和当前仓库 `text_chunks_demo.jsonl` 中的临时验证样例直接对应。

### 坐标口径

当前所有地标坐标统一使用 `WGS84`。

这些坐标只用于 5月 Demo 的 PPT 示意、GeoJSON 地图落点测试和未来 XR 时空沙盘方向说明，不代表正式测绘级坐标。

- `landmark_demo`：地标级近似点位，例如嘉兴南湖、西柏坡。
- `city_demo`：城市或区域级近似点位，例如遵义、延安、瑞金、井冈山。

后续如果进入正式 Three.js / AntV L7 前端联调，应逐点复核具体纪念馆、旧址或景区的准确坐标。

## 6. 1分钟讲解词

我负责的是这次 Demo 中的展示素材和时空补强部分，不负责 FAISS、NetworkX 或后端检索主链路。

我这边主要做了四类内容：第一是时间轴数据，用 5 条事件串起“1921 建党、1935 遵义会议、1942 延安整风、抗战时期、新中国成立”这条展示主线；第二是红色地标数据，整理了嘉兴南湖、井冈山、瑞金、遵义、延安和西柏坡 6 个节点，并输出 JSONL 和 GeoJSON，方便后续地图落点；第三是三张 PPT 流程图，用来说明系统总体链路、KG-RAG 证据检索流程，以及未来 XR 时空沙盘设想；第四是说明未来承接方式，也就是 KG-RAG 先返回带 citation 的证据块，后续沙盘再根据实体和地标节点进行高亮展示，并让数字人基于证据进行可信讲解。

所以我这部分不是完整前端实现，而是为线上汇报提供“能看懂、能展示、能承接后续 XR 沙盘”的素材底座。
