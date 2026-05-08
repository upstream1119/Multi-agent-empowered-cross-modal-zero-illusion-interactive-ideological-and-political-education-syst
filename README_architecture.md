# 检索中枢架构说明

## 1. 当前目标

当前阶段的目标不是直接接入真实 Milvus / Neo4j，而是先锁死检索中枢的固定流程、输入输出契约和验收口径，确保团队成员围绕同一条链路协作。

固定流程如下：

`Query -> 实体提取 -> 向量 Top-K -> 图谱 Top-K -> 融合打分 -> 返回带 citation 的候选证据`

## 2. 模块分工

- `src/api/main.py`
  - 负责 HTTP 接口编排
  - 接收 `POST /retrieve`
  - 调用 `src/retriever/hybrid_retriever.py`

- `src/retriever/hybrid_retriever.py`
  - 负责检索中枢逻辑
  - 当前阶段包含：
    - `extract_query_entities`：查询实体提取
    - `retrieve_vector`：向量 Top-K 检索骨架
    - `retrieve_graph`：图谱 Top-K 检索骨架
    - `fuse_results`：融合打分骨架
    - 标准返回体组装

- `configs/schema.yaml`
  - 负责统一数据字段规范
  - 为 ETL、向量索引、图谱构建和接口返回提供共同字段基础

- `tests/demo_queries.json`
  - 负责本地验收问题集合
  - 覆盖史实、叙事、考点、地理四类问题

## 3. 当前本地实现说明

为了保证链路先跑通，本地采用 `team/mock` 双模式：

- `team`
  - 团队默认模式
  - 返回固定结构，但不主动构造模拟命中

- `mock`
  - 学习与本地联调模式
  - 使用固定知识池模拟：
    - query 实体提取
    - 向量 Top-K 候选
    - 图谱 Top-K 候选
    - 融合排序结果

当前 `mock` 版的意义是锁死流程骨架，而不是替代真实检索系统。

融合分暂按作战文档口径执行：

`hybrid_score = 0.7 * vector_score + 0.3 * graph_score`

## 4. 返回契约

`/retrieve` 顶层返回固定字段：

- `status`
- `project`
- `query`
- `query_entities`
- `vector_hits`
- `graph_hits`
- `hybrid_hits`

其中：

- `vector_hits` 表示语义检索候选
- `graph_hits` 表示结构关系候选
- `hybrid_hits` 表示融合后的最终候选

`hybrid_hits` 当前必须保留：

- `id`
- `source`
- `citation`
- `vector_score`
- `graph_score`
- `hybrid_score`

这是后续可解释性、答辩展示和调参分析的基础。

## 5. 后续迁移路径

后续回到实验室环境时，优先替换 `src/retriever/hybrid_retriever.py` 内部实现，不改 API 契约：

1. 用真实实体识别替换固定词表
2. 用真实向量库替换 mock 向量候选
3. 用真实图谱检索替换 mock 图候选
4. 保留统一融合输出结构

这样可以保证前端、测试脚本和团队协作接口不因为底层实现变化而频繁返工。
