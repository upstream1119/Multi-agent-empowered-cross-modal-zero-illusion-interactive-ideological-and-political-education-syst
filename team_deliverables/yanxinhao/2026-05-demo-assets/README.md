# 严欣浩 2026-05 Demo 展示素材交付说明

## 1. 本阶段任务

本阶段用于 5 月线上 Demo 汇报的展示增强，不涉及完整前端开发、Three.js 沙盘实现、FAISS、NetworkX、后端 API 或知识库清洗主链路。

## 2. 本目录包含

- docs/demo_assets_sizheng.md：展示素材说明文档与讲解词
- figures/system_pipeline.png：系统总体链路图
- figures/kg_rag_flow.png：KG-RAG 检索与融合打分流程图
- figures/future_sandbox_demo.png：未来 XR 时空沙盘设想图
- scripts/draw_demo_figures.py：生成三张展示图的辅助脚本

## 3. 与主项目的关系

本目录中的文件主要用于汇报展示、阶段说明和素材管理，不直接参与后端运行。

真正可能被系统读取的数据仍保留在：

data/processed/landmarks_demo.jsonl
data/processed/landmarks_demo.geojson
data/processed/timeline_demo_sizheng.json

## 4. 后续说明

如果后续进入正式前端联调或 XR 沙盘开发，应将真正被系统读取的配置、数据和代码迁移到对应正式目录，而不是继续放在 team_deliverables 中。
