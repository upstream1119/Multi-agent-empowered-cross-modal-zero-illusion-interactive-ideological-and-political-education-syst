"""Build Yan Xinhao's 2026-04 spatial demo deliverables.

This script is intentionally scoped to team_deliverables. It reads local
reference materials, converts landmark coordinates from BD-09 to WGS84, and
emits static JSON/GeoJSON assets for the April spatial-data task.
"""

from __future__ import annotations

import json
import math
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


REPO_ROOT = Path(__file__).resolve().parents[4]
OUT_DIR = Path(__file__).resolve().parents[1]
LANDMARK_SOURCE = Path(r"D:\学习文件\杂\大创pyh\大创\彭意涵_2026年大创\知识库\red_landmarks_dict.json.txt")
EVENT_SOURCE = Path(r"D:\学习文件\杂\大创pyh\大创\彭意涵_2026年大创\知识库\中国共产党一百年大事记.docx")

X_PI = math.pi * 3000.0 / 180.0
PI = math.pi
A = 6378245.0
EE = 0.00669342162296594323


LANDMARK_SPECS = [
    ("landmark_1919_beida_red_building_001", "北京大学红楼", "马克思主义传播与五四运动相关节点", "1919-1920"),
    ("landmark_1921_shanghai_cpc_1st_002", "上海中共一大会址", "中共一大开幕地", "1921"),
    ("landmark_1921_jiaxing_nanhu_003", "嘉兴南湖红船", "中共一大闭幕地", "1921"),
    ("landmark_1922_shanghai_cpc_2nd_004", "上海中共二大会址", "中共二大会址", "1922"),
    ("landmark_1923_guangzhou_cpc_3rd_005", "广州中共三大会址", "中共三大会址", "1923"),
    ("landmark_1927_wuhan_cpc_5th_006", "武汉中共五大会址", "中共五大会址", "1927"),
    ("landmark_1927_wuhan_august7_007", "武汉八七会议会址", "八七会议会址", "1927"),
    ("landmark_1927_nanchang_uprising_008", "南昌八一起义总指挥部旧址", "南昌起义相关旧址", "1927"),
    ("landmark_1927_jinggangshan_maoping_009", "井冈山茅坪", "井冈山革命根据地相关节点", "1927-1930"),
    ("landmark_1935_zunyi_meeting_010", "遵义会议会址", "遵义会议会址", "1935"),
]


TIMELINE_SPECS = [
    {
        "id": "timeline_1919_may_fourth_001",
        "date": "1919-05-04",
        "title": "五四运动在北京爆发",
        "keyword": "五四运动",
        "location_key": "北京天安门广场",
        "entities": ["五四运动", "北京学生", "反帝反封建"],
        "tags": ["五四运动", "思想启蒙", "群众动员"],
    },
    {
        "id": "timeline_1920_marxism_study_002",
        "date": "1920-03",
        "title": "北京大学马克思学说研究会成立",
        "keyword": "早期组织",
        "location_key": "北京大学红楼",
        "entities": ["李大钊", "北京大学", "马克思学说研究会"],
        "tags": ["马克思主义传播", "早期组织", "理论教育"],
    },
    {
        "id": "timeline_1921_cpc_1st_shanghai_003",
        "date": "1921-07-23",
        "title": "中国共产党第一次全国代表大会在上海开幕",
        "keyword": "第一次全国代表大会",
        "location_key": "上海中共一大会址",
        "entities": ["中国共产党第一次全国代表大会", "上海", "中国共产党"],
        "tags": ["建党", "会议", "组织建设"],
    },
    {
        "id": "timeline_1921_cpc_1st_nanhu_004",
        "date": "1921-07",
        "title": "中共一大最后一天会议转移到嘉兴南湖游船举行",
        "keyword": "浙江嘉兴南湖",
        "location_key": "嘉兴南湖红船",
        "entities": ["嘉兴南湖", "红船", "中国共产党第一次全国代表大会"],
        "tags": ["建党", "红船精神", "空间展示"],
    },
    {
        "id": "timeline_1922_cpc_2nd_005",
        "date": "1922-07-16",
        "title": "中国共产党第二次全国代表大会在上海举行",
        "keyword": "第二次全国代表大会",
        "location_key": "上海中共二大会址",
        "entities": ["中国共产党第二次全国代表大会", "民主革命纲领", "上海"],
        "tags": ["党代会", "纲领", "组织建设"],
    },
    {
        "id": "timeline_1923_cpc_3rd_006",
        "date": "1923-06-12",
        "title": "中国共产党第三次全国代表大会在广州举行",
        "keyword": "第三次全国代表大会",
        "location_key": "广州中共三大会址",
        "entities": ["中国共产党第三次全国代表大会", "国共合作", "广州"],
        "tags": ["党代会", "统一战线", "广州"],
    },
    {
        "id": "timeline_1925_may_thirtieth_007",
        "date": "1925-05-30",
        "title": "五卅运动在上海爆发",
        "keyword": "五卅运动",
        "location_key": "上海中共二大会址",
        "entities": ["五卅运动", "上海", "工人运动"],
        "tags": ["群众运动", "反帝斗争", "上海"],
    },
    {
        "id": "timeline_1927_cpc_5th_008",
        "date": "1927-04-27",
        "title": "中国共产党第五次全国代表大会在武汉举行",
        "keyword": "第五次全国代表大会",
        "location_key": "武汉中共五大会址",
        "entities": ["中国共产党第五次全国代表大会", "武汉", "中央监察委员会"],
        "tags": ["党代会", "组织建设", "武汉"],
    },
    {
        "id": "timeline_1927_nanchang_uprising_009",
        "date": "1927-08-01",
        "title": "南昌起义打响武装反抗国民党反动派的第一枪",
        "keyword": "南昌起义",
        "location_key": "南昌八一起义总指挥部旧址",
        "entities": ["南昌起义", "人民军队", "周恩来"],
        "tags": ["武装斗争", "人民军队", "南昌"],
    },
    {
        "id": "timeline_1927_august7_meeting_010",
        "date": "1927-08-07",
        "title": "八七会议在湖北汉口召开",
        "keyword": "八七会议",
        "location_key": "武汉八七会议会址",
        "entities": ["八七会议", "土地革命", "武装反抗"],
        "tags": ["会议", "历史转折", "武汉"],
    },
    {
        "id": "timeline_1927_sanwan_reorganization_011",
        "date": "1927-09-29",
        "title": "秋收起义部队到达三湾并进行改编",
        "keyword": "三湾村",
        "location_key": "三湾改编旧址",
        "entities": ["秋收起义", "三湾改编", "支部建在连上"],
        "tags": ["军队建设", "政治工作", "土地革命"],
    },
    {
        "id": "timeline_1927_jinggangshan_012",
        "date": "1927-10",
        "title": "秋收起义部队到达井冈山并开始创建农村革命根据地",
        "keyword": "井冈山",
        "location_key": "井冈山茅坪",
        "entities": ["井冈山", "农村革命根据地", "秋收起义"],
        "tags": ["根据地", "群众动员", "井冈山"],
    },
    {
        "id": "timeline_1929_gutian_meeting_013",
        "date": "1929-12-28",
        "title": "古田会议确立思想建党、政治建军原则",
        "keyword": "古田会议",
        "location_key": "古田会议旧址",
        "entities": ["古田会议", "思想建党", "政治建军"],
        "tags": ["会议", "军队政治工作", "思想政治教育"],
    },
    {
        "id": "timeline_1931_ruijin_soviet_014",
        "date": "1931-11-07",
        "title": "中华苏维埃第一次全国代表大会在瑞金召开",
        "keyword": "中华苏维埃第一次全国代表大会",
        "location_key": "瑞金中华苏维埃共和国临时中央政府旧址",
        "entities": ["瑞金", "中华苏维埃共和国", "毛泽东"],
        "tags": ["苏区", "政权建设", "瑞金"],
    },
    {
        "id": "timeline_1934_long_march_start_015",
        "date": "1934-10",
        "title": "中共中央和中央红军主力开始长征",
        "keyword": "开始长征",
        "location_key": "瑞金红军长征出发地",
        "entities": ["长征", "中央红军", "战略转移"],
        "tags": ["长征", "战略转移", "瑞金"],
    },
    {
        "id": "timeline_1935_zunyi_meeting_016",
        "date": "1935-01-15",
        "title": "遵义会议在贵州遵义召开",
        "keyword": "遵义会议",
        "location_key": "遵义会议会址",
        "entities": ["遵义会议", "长征", "毛泽东"],
        "tags": ["会议", "历史转折", "遵义"],
    },
    {
        "id": "timeline_1936_huining_join_017",
        "date": "1936-10-09",
        "title": "红军三大主力胜利会师",
        "keyword": "会宁会师",
        "location_key": "会宁红军会师旧址",
        "entities": ["会宁会师", "红军三大主力", "长征精神"],
        "tags": ["长征", "会师", "理想信念教育"],
    },
    {
        "id": "timeline_1936_xian_incident_018",
        "date": "1936-12-12",
        "title": "西安事变推动时局转换",
        "keyword": "西安事变",
        "location_key": "西安事变旧址",
        "entities": ["西安事变", "周恩来", "第二次国共合作"],
        "tags": ["统一战线", "抗日民族统一战线", "西安"],
    },
    {
        "id": "timeline_1937_luochuan_meeting_019",
        "date": "1937-08-22",
        "title": "洛川会议标志党的全面抗战路线正式形成",
        "keyword": "洛川会议",
        "location_key": "洛川会议旧址",
        "entities": ["洛川会议", "全面抗战路线", "抗日救国十大纲领"],
        "tags": ["抗战", "会议", "群众动员"],
    },
    {
        "id": "timeline_1937_pingxingguan_020",
        "date": "1937-09-25",
        "title": "八路军取得平型关大捷",
        "keyword": "平型关大捷",
        "location_key": "平型关大捷遗址",
        "entities": ["平型关大捷", "八路军", "抗日战争"],
        "tags": ["抗战", "军事斗争", "民族精神"],
    },
    {
        "id": "timeline_1938_base_areas_021",
        "date": "1937-11",
        "title": "八路军逐渐向敌后实行战略展开并创建抗日根据地",
        "keyword": "抗日根据地",
        "location_key": "晋察冀军区司令部旧址",
        "entities": ["抗日根据地", "晋察冀", "八路军"],
        "tags": ["抗战", "根据地", "群众组织"],
    },
    {
        "id": "timeline_1942_rectification_022",
        "date": "1942-02",
        "title": "延安整风运动在全党普遍展开",
        "keyword": "整风运动",
        "location_key": "延安革命旧址",
        "entities": ["延安整风", "毛泽东", "整顿党的作风"],
        "tags": ["延安", "理论教育", "党的建设"],
    },
    {
        "id": "timeline_1945_cpc_7th_023",
        "date": "1945-04-23",
        "title": "中国共产党第七次全国代表大会在延安举行",
        "keyword": "第七次全国代表大会",
        "location_key": "延安革命旧址",
        "entities": ["中国共产党第七次全国代表大会", "延安", "毛泽东思想"],
        "tags": ["党代会", "延安", "指导思想"],
    },
    {
        "id": "timeline_1945_chongqing_talks_024",
        "date": "1945-08-28",
        "title": "毛泽东赴重庆进行和平谈判",
        "keyword": "重庆谈判",
        "location_key": "重庆谈判旧址",
        "entities": ["重庆谈判", "双十协定", "毛泽东"],
        "tags": ["和平谈判", "统一战线", "重庆"],
    },
    {
        "id": "timeline_1949_xibaipo_025",
        "date": "1949-03-05",
        "title": "中共七届二中全会在西柏坡召开",
        "keyword": "七届二中全会",
        "location_key": "西柏坡中共中央旧址",
        "entities": ["七届二中全会", "西柏坡", "两个务必"],
        "tags": ["解放战争", "执政准备", "西柏坡"],
    },
]


def bd09_to_gcj02(lng: float, lat: float) -> tuple[float, float]:
    x = lng - 0.0065
    y = lat - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * X_PI)
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * X_PI)
    return z * math.cos(theta), z * math.sin(theta)


def _transform_lat(lng: float, lat: float) -> float:
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + 0.1 * lng * lat + 0.2 * math.sqrt(abs(lng))
    ret += (20.0 * math.sin(6.0 * lng * PI) + 20.0 * math.sin(2.0 * lng * PI)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * PI) + 40.0 * math.sin(lat / 3.0 * PI)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * PI) + 320 * math.sin(lat * PI / 30.0)) * 2.0 / 3.0
    return ret


def _transform_lng(lng: float, lat: float) -> float:
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + 0.1 * lng * lat + 0.1 * math.sqrt(abs(lng))
    ret += (20.0 * math.sin(6.0 * lng * PI) + 20.0 * math.sin(2.0 * lng * PI)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * PI) + 40.0 * math.sin(lng / 3.0 * PI)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * PI) + 300.0 * math.sin(lng / 30.0 * PI)) * 2.0 / 3.0
    return ret


def out_of_china(lng: float, lat: float) -> bool:
    return not (73.66 <= lng <= 135.05 and 3.86 <= lat <= 53.55)


def gcj02_to_wgs84(lng: float, lat: float) -> tuple[float, float]:
    if out_of_china(lng, lat):
        return lng, lat
    dlat = _transform_lat(lng - 105.0, lat - 35.0)
    dlng = _transform_lng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * PI
    magic = math.sin(radlat)
    magic = 1 - EE * magic * magic
    sqrt_magic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((A * (1 - EE)) / (magic * sqrt_magic) * PI)
    dlng = (dlng * 180.0) / (A / sqrt_magic * math.cos(radlat) * PI)
    return lng * 2 - (lng + dlng), lat * 2 - (lat + dlat)


def bd09_to_wgs84(lng: float, lat: float) -> tuple[float, float]:
    gcj_lng, gcj_lat = bd09_to_gcj02(lng, lat)
    return gcj02_to_wgs84(gcj_lng, gcj_lat)


def read_docx_paragraphs(path: Path) -> list[str]:
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    with zipfile.ZipFile(path) as zf:
        root = ET.fromstring(zf.read("word/document.xml"))
    paragraphs: list[str] = []
    for para in root.findall(".//w:p", ns):
        text = "".join(t.text or "" for t in para.findall(".//w:t", ns)).strip()
        if text:
            paragraphs.append(text)
    return paragraphs


def compact_text(text: str, limit: int = 180) -> str:
    text = re.sub(r"\s+", "", text)
    return text[:limit]


def load_landmark_source() -> dict[str, dict[str, float]]:
    if not LANDMARK_SOURCE.exists():
        raise FileNotFoundError(f"Missing landmark source: {LANDMARK_SOURCE}")
    return json.loads(LANDMARK_SOURCE.read_text(encoding="utf-8"))


def converted_point(source: dict[str, dict[str, float]], key: str) -> dict[str, object]:
    if key not in source:
        raise KeyError(f"Landmark not found in source dictionary: {key}")
    raw = source[key]
    lng, lat = bd09_to_wgs84(float(raw["lng"]), float(raw["lat"]))
    return {
        "name": key,
        "lng": round(lng, 6),
        "lat": round(lat, 6),
        "coord_sys": "WGS84",
        "source_coord_sys": "BD-09",
        "source_lng": raw["lng"],
        "source_lat": raw["lat"],
        "conversion": "BD-09 -> GCJ-02 -> WGS84",
    }


def build_landmarks(source: dict[str, dict[str, float]]) -> list[dict[str, object]]:
    records = []
    for record_id, name, summary, display_time in LANDMARK_SPECS:
        location = converted_point(source, name)
        records.append(
            {
                "id": record_id,
                "name": name,
                "category": "红色地标",
                "location": location,
                "time": {"start": display_time.split("-")[0], "end": None, "display": display_time},
                "summary": summary,
                "entities": [name],
                "tags": ["4月空间数据", "红色地标", "WGS84"],
                "citation": {
                    "doc": "red_landmarks_dict.json.txt",
                    "section": name,
                    "page": None,
                    "source_basis": "4月空间数据任务使用的红色地标坐标字典；本次按BD-09输入转换为WGS84。",
                },
            }
        )
    return records


def build_geojson(records: list[dict[str, object]]) -> dict[str, object]:
    features = []
    for item in records:
        loc = item["location"]
        features.append(
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [loc["lng"], loc["lat"]],
                },
                "properties": {
                    "id": item["id"],
                    "name": item["name"],
                    "category": item["category"],
                    "time": item["time"],
                    "summary": item["summary"],
                    "entities": item["entities"],
                    "tags": item["tags"],
                    "citation": item["citation"],
                    "coord_sys": "WGS84",
                    "source_coord_sys": "BD-09",
                },
            }
        )
    return {
        "type": "FeatureCollection",
        "name": "yanxinhao_2026_04_landmarks",
        "crs_note": "GeoJSON coordinates are [lng, lat] in WGS84. Source coordinates are treated as BD-09 and converted for the April task.",
        "features": features,
    }


def find_source_paragraph(paragraphs: list[str], keyword: str) -> str:
    for para in paragraphs:
        if keyword in para:
            return para
    raise ValueError(f"Timeline keyword not found in event source: {keyword}")


def build_timeline(source: dict[str, dict[str, float]], paragraphs: list[str]) -> dict[str, object]:
    events = []
    for spec in TIMELINE_SPECS:
        loc = converted_point(source, spec["location_key"])
        paragraph = find_source_paragraph(paragraphs, spec["keyword"])
        events.append(
            {
                "id": spec["id"],
                "date": spec["date"],
                "title": spec["title"],
                "text": compact_text(paragraph, 220),
                "location": loc,
                "related_landmarks": [spec["location_key"]],
                "entities": spec["entities"],
                "tags": spec["tags"],
                "citation": {
                    "doc": "中国共产党一百年大事记",
                    "section": spec["keyword"],
                    "page": None,
                    "source_excerpt": compact_text(paragraph, 140),
                },
            }
        )
    return {
        "metadata": {
            "name": "timeline_demo",
            "owner": "yanxinhao",
            "task": "2026-04 spatial frontend prework",
            "event_count": len(events),
            "coordinate_policy": "Source landmark coordinates are treated as BD-09 and converted to WGS84.",
            "source_doc": str(EVENT_SOURCE),
        },
        "events": events,
    }


def build_schema_example() -> dict[str, object]:
    return {
        "metadata": {
            "name": "geo_schema_example",
            "owner": "yanxinhao",
            "purpose": "April spatial-data contract for future map, timeline, and sandbox frontend tests.",
        },
        "coordinate_policy": {
            "input_coord_sys": "BD-09",
            "output_coord_sys": "WGS84",
            "geojson_coordinate_order": "[lng, lat]",
            "conversion": "BD-09 -> GCJ-02 -> WGS84",
        },
        "landmark_record": {
            "id": "string",
            "name": "string",
            "category": "红色地标",
            "location": {
                "name": "string",
                "lng": "float, WGS84",
                "lat": "float, WGS84",
                "coord_sys": "WGS84",
                "source_coord_sys": "BD-09",
                "source_lng": "float",
                "source_lat": "float",
            },
            "time": {"start": "string|null", "end": "string|null", "display": "string"},
            "summary": "string",
            "entities": ["string"],
            "tags": ["string"],
            "citation": {"doc": "string", "section": "string", "page": "integer|null"},
        },
        "timeline_event": {
            "id": "string",
            "date": "YYYY-MM-DD or YYYY-MM",
            "title": "string",
            "text": "string",
            "location": "same structure as landmark.location",
            "related_landmarks": ["string"],
            "entities": ["string"],
            "tags": ["string"],
            "citation": {"doc": "string", "section": "string", "page": "integer|null", "source_excerpt": "string"},
        },
        "geojson_feature": {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": ["lng", "lat"]},
            "properties": {
                "id": "string",
                "name": "string",
                "category": "string",
                "time": "object",
                "summary": "string",
                "entities": ["string"],
                "tags": ["string"],
                "citation": "object",
                "coord_sys": "WGS84",
                "source_coord_sys": "BD-09",
            },
        },
    }


def write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path: Path, records: list[dict[str, object]]) -> None:
    path.write_text("\n".join(json.dumps(item, ensure_ascii=False, separators=(",", ":")) for item in records) + "\n", encoding="utf-8")


def write_readme() -> None:
    readme = """# 严欣浩 2026-04 空间数据与前端前置交付

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
"""
    (OUT_DIR / "README.md").write_text(readme, encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    source = load_landmark_source()
    paragraphs = read_docx_paragraphs(EVENT_SOURCE)

    landmarks = build_landmarks(source)
    timeline = build_timeline(source, paragraphs)

    write_jsonl(OUT_DIR / "landmarks.jsonl", landmarks)
    write_json(OUT_DIR / "landmarks.geojson", build_geojson(landmarks))
    write_json(OUT_DIR / "timeline_demo.json", timeline)
    write_json(OUT_DIR / "geo_schema_example.json", build_schema_example())
    write_readme()

    print(f"Wrote {len(landmarks)} landmarks and {len(timeline['events'])} timeline events to {OUT_DIR}")


if __name__ == "__main__":
    main()
