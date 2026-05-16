# Demo Acceptance Checklist

## 1. 当前 10 条 query 适应性评估

- `demo_sizheng_001` ~ `demo_sizheng_005`, `demo_sizheng_009`：非常适合作为核心展示问题，覆盖思政史体系性的历史节点与典型事件。
- `demo_sizheng_006`、`demo_sizheng_007`、`demo_sizheng_008`、`demo_sizheng_010`：适合做专项补充问题，能展示系统在细节性检索和引用准确性方面的能力。
- 总体结论：10 条问题均可用于汇报展示，既包含宏观历史脉络，也兼顾专题性、可操作性和 citation 展示效果。

## 2. expected_chunk_ids 与真实文本一致性

已核对当前 `data/processed/text_chunks_demo.jsonl` 中的 chunk ID：

- `demo_sizheng_001`：`chunk_szzjys_demo_001`, `chunk_szzjys_demo_002`
- `demo_sizheng_002`：`chunk_szzjys_demo_003`, `chunk_szzjys_demo_004`
- `demo_sizheng_003`：`chunk_szzjys_demo_006`
- `demo_sizheng_004`：`chunk_szzjys_demo_012`
- `demo_sizheng_005`：`chunk_szzjys_demo_017`
- `demo_sizheng_006`：`chunk_szzjys_demo_013`
- `demo_sizheng_007`：`chunk_szzjys_demo_022`
- `demo_sizheng_008`：`chunk_szzjys_demo_025`
- `demo_sizheng_009`：`chunk_szzjys_demo_033`
- `demo_sizheng_010`：`chunk_szzjys_demo_034`

这些 ID 均存在于当前真实 `text_chunks_demo.jsonl`，且与 query 主题一致。

## 3. expected_citation_sections 与真实文义一致性

已核对每条问题对应 chunk 的 `citation.section`：

- `demo_sizheng_001`：`绪论` / `绪论 / 三、学习研究中国共产党思想政治教育史的目的、意义和方法`
- `demo_sizheng_002`：`第一章... / 第一节... / 一、马克思学说在中国的最初传入` / `... / 三、马克思主义在论战中成为新文化运动的主流`
- `demo_sizheng_003`：`第一章... / 第二节... / 二、党的一大与思想政治教育基本原则的确立`
- `demo_sizheng_004`：`第二章... / 第一节... / 一、人民军队初创时期的思想政治教育 / （二）秋收起义和三湾改编`
- `demo_sizheng_005`：`第二章... / 第三节... / 三、红军长征中的思想政治教育 / （二）鼓舞士气提高部队战斗力`
- `demo_sizheng_006`：`第二章... / 第二节... / 一、中央《宣传工作决议案》的主要内容 / （三）宣传工作的组织领导`
- `demo_sizheng_007`：`第三章... / 第二节加强党员干部的思想政治教育 / 二、抗日战争时期党的干部教育`
- `demo_sizheng_008`：`第三章... / 第三节思想政治教育理论形成体系 / 二、思想政治教育若干重要论著的发表`
- `demo_sizheng_009`：`第四章... / 第二节人民解放军的思想政治教育 / 一、“打开连队工作之门的三把重要钥匙” / （三）新式整军运动`
- `demo_sizheng_010`：`第四章... / 第二节人民解放军的思想政治教育 / 二、瓦解敌军工作和教育改造国民党起义投诚部队 / （三）教育改造国民党被俘、起义部队`

这些 `expected_citation_sections` 与当前 chunk 的 citation 元数据高度匹配，语义准确。

## 4. API / 返回字段 检查清单

### 4.1 API 接口

- `GET /health`
  - 期望返回：`{"status": "ok"}`
- `POST /retrieve`
  - 请求体格式：`{"query": "..."}`
  - 当前实现：`src/api/main.py` 使用 `RetrieveRequest` 校验请求体，并调用 `src/retriever/hybrid_retriever.py` 的 `retrieve`。

### 4.2 返回字段结构

当前 `retrieve` 返回值包含：

- `status`：`success`
- `project`：项目名称
- `query`：原始请求文本
- `query_entities`：查询抽取的实体列表
- `vector_hits`：向量召回结果列表
- `graph_hits`：图谱召回结果列表
- `hybrid_hits`：融合后结果列表

### 4.3 各条目字段

- `vector_hits` 中每条包含：
  - `id`
  - `source`
  - `title`
  - `text`
  - `citation`
  - `vector_score`
- `graph_hits` 中每条包含：
  - `id`
  - `related_entities`
  - `graph_score`
- `hybrid_hits` 中每条包含：
  - `id`
  - `source`
  - `title`
  - `text`
  - `citation`
  - `vector_score`
  - `graph_score`
  - `hybrid_score`

### 4.4 关键行为检查

- 查询结果必须包含 `citation`，可用于展示“引用来源与章节”。
- `hybrid_hits` 应按 `hybrid_score` 降序排序。
- `vector_hits` 与 `graph_hits` 结果允许不完全重合，但 `hybrid_hits` 需展示两路融合得分。
- 当前 mock 实现只有 `DACHUANG_RETRIEVE_MODE=mock` 且 `DACHUANG_LOCAL_MOCK_ACK=1` 时才会执行检索，否则返回空结果数组。

## 5. 核心必演问题截图建议

建议重点截图以下核心问题的 API 展示结果：

- `demo_sizheng_001`
- `demo_sizheng_002`
- `demo_sizheng_003`
- `demo_sizheng_004`
- `demo_sizheng_005`
- `demo_sizheng_009`

这些问题既是核心 demo 问题，又能覆盖：
- 文本 retrieval
- citation section 展示
- 核心事件与历史阶段
- 混合召回结果的排序效果

## 6. 发现与建议

- `expected_chunk_ids` 均为真实 `chunk_szzjys_demo_*` 格式，满足用户要求；不存在 `chunk_006` 这种旧 ID。
- `expected_citation_sections` 与当前 chunk metadata 一致，语义准确。
- 建议在后续版本中为 `expected_citation_keywords` 增加更细粒度关键词，例如：
  - `demo_sizheng_007` 可加入 `干部教育`
  - `demo_sizheng_010` 可加入 `国民党被俘` / `起义部队`
- 目前查询检查点均适合基于最新 `main` 进行整理。如果后续在 `zhangruiyang` 分支上操作，建议先基于最新 `main` 进行 rebase 或 cherry-pick，再提交，避免直接合并旧分支。
