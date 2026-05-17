# 张睿扬 2026-05 Demo 问题集阶段交付说明

## 1. 本阶段任务

本阶段用于整理 5 月思政史 Demo 的候选展示问题、标准答案草稿和预期命中 chunk ID，为后续演示验收提供问题基础。

## 2. 本目录包含

- golden_queries.json：10 条候选问题、标准答案草稿和 expected_chunk_ids

## 3. 当前状态

当前文件属于阶段性交付物和题库草稿，还不能直接作为正式自动化验收标准。

主要原因：

- `expected_chunk_ids` 仍使用 `text_chunk_001` 等占位式 ID。
- 李卓洋最终版 `text_chunks_demo.jsonl` 尚未交付，真实 chunk ID 还未锁定。
- 当前字段结构为 `question/standard_answer/expected_chunk_ids`，与 `tests/demo_queries_sizheng_history.json` 的自动验收字段还不完全一致。

## 4. 后续处理

等李卓洋交付最终 `data/processed/text_chunks_demo.jsonl` 后，需要继续完成：

1. 将 `expected_chunk_ids` 改成真实 chunk ID。
2. 补充或转换为自动验收需要的字段，例如 `query`、`expected_entities`、`expected_citation_keywords`、`min_hybrid_hits`。
3. 经负责人确认后，再决定是否迁移到 `tests/` 目录作为正式验收集。

## 5. 与主项目的关系

本目录中的文件是张睿扬的阶段性交付物，不直接参与当前后端运行。当前 `/retrieve` 自动测试仍以 `tests/demo_queries_sizheng_history.json` 为准。
