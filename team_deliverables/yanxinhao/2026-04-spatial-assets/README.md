# 严欣浩 2026-04 空间数据与前端前置交付

本目录用于补齐 4 月原始任务：处理地理坐标偏移，输出后端可读、前端可用的地理结构数据。

## 文件

- `landmarks.jsonl`：10 个红色地标结构化记录。
- `landmarks.geojson`：与 `landmarks.jsonl` 一一对应的 GeoJSON 点数据。
- `timeline_demo.json`：25 条带地点事件，用于沙盘前端时间轴测试。
- `geo_schema_example.json`：前端地理接口规范示例。
- `scripts/build_spatial_assets.py`：生成本目录交付物的辅助脚本。

## 坐标口径

源文件 `red_landmarks_dict.json.txt` 中的坐标按 BD-09 输入处理，本次统一转换为 WGS84 输出。

GeoJSON 坐标顺序为 `[lng, lat]`。

## 任务边界

本目录只补 4 月严欣浩个人任务，不修改 `src/`、`tests/` 或正式 `data/processed` 文件，不实现完整 Three.js 前端、FAISS、NetworkX 或后端 API。
