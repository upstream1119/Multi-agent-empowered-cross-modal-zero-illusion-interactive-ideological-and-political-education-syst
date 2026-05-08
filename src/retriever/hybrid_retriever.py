import os


PROJECT_NAME = "多智能体赋能的跨模态零幻觉交互式思政教育系统"
TEAM_MODE = "team"
MOCK_MODE = "mock"
VECTOR_TOP_K = 3
GRAPH_TOP_K = 3
VECTOR_WEIGHT = 0.6
GRAPH_WEIGHT = 0.4

# 当前阶段用固定词表演示 query -> entities 的流程，后续替换为真实实体识别。
MOCK_ENTITY_MAP = {
    "遵义会议": "遵义会议",
    "长征": "长征",
    "毛泽东": "毛泽东",
    "与妻书": "与妻书",
    "林觉民": "林觉民",
    "抗日战争": "抗日战争",
    "嘉兴南湖": "嘉兴南湖",
    "井冈山": "井冈山",
    "延安": "延安",
}

MOCK_KNOWLEDGE_BASE = [
    {
        "id": "event_1935_001",
        "source": "中国共产党一百年大事记",
        "title": "遵义会议召开",
        "text": "1935年1月，中共中央政治局在长征途中举行遵义会议，集中解决军事和组织问题。",
        "citation": {"doc": "中国共产党一百年大事记", "section": "1935年", "page": None},
        "entities": ["遵义会议", "长征", "毛泽东"],
        "related_entities": ["中央政治局", "长征", "毛泽东"],
        "topic": "长征",
        "tags": ["史实", "会议", "党史"],
    },
    {
        "id": "event_1935_002",
        "source": "中国共产党一百年大事记",
        "title": "遵义会议的历史转折",
        "text": "遵义会议事实上确立了毛泽东在党中央和红军的领导地位，成为党的历史上生死攸关的转折点。",
        "citation": {"doc": "中国共产党一百年大事记", "section": "1935年", "page": None},
        "entities": ["遵义会议", "毛泽东"],
        "related_entities": ["党中央", "红军", "毛泽东"],
        "topic": "长征",
        "tags": ["史实", "意义", "党史"],
    },
    {
        "id": "event_1935_003",
        "source": "中国近现代史纲要（2023年版）",
        "title": "长征中的关键会议",
        "text": "在第五次反围剿失利和长征初期严重受挫的背景下，遵义会议纠正了博古、李德的错误指挥。",
        "citation": {"doc": "中国近现代史纲要（2023年版）", "section": "长征与遵义会议", "page": 128},
        "entities": ["遵义会议", "长征"],
        "related_entities": ["第五次反围剿", "博古", "李德"],
        "topic": "长征",
        "tags": ["史实", "背景", "党史"],
    },
    {
        "id": "letter_1911_001",
        "source": "《红色家书》经典篇目梗概整理版",
        "title": "林觉民《与妻书》",
        "text": "《与妻书》写于广州起义前，展现了林觉民将个人深情与民族大义统一起来的革命精神。",
        "citation": {"doc": "《红色家书》经典篇目梗概整理版", "section": "林觉民《与妻书》", "page": None},
        "entities": ["与妻书", "林觉民"],
        "related_entities": ["广州起义", "陈意映", "革命精神"],
        "topic": "红色家书",
        "tags": ["叙事", "家书", "人物"],
    },
    {
        "id": "letter_1911_002",
        "source": "《红色家书》经典篇目梗概整理版",
        "title": "林觉民的牺牲抉择",
        "text": "林觉民在《与妻书》中以“为天下人谋永福”的理想说明舍小家为大家的选择。",
        "citation": {"doc": "《红色家书》经典篇目梗概整理版", "section": "林觉民《与妻书》", "page": None},
        "entities": ["与妻书", "林觉民"],
        "related_entities": ["天下人", "家国情怀", "革命理想"],
        "topic": "红色家书",
        "tags": ["叙事", "精神", "人物"],
    },
    {
        "id": "letter_1911_003",
        "source": "《红色家书》经典篇目梗概整理版",
        "title": "家书中的革命伦理",
        "text": "这封家书既有对妻子的深情，也表达了为了民族解放而甘于牺牲的伦理选择。",
        "citation": {"doc": "《红色家书》经典篇目梗概整理版", "section": "林觉民《与妻书》", "page": None},
        "entities": ["与妻书", "林觉民"],
        "related_entities": ["民族解放", "革命伦理", "牺牲精神"],
        "topic": "红色家书",
        "tags": ["叙事", "情感", "精神"],
    },
    {
        "id": "exam_2025_001",
        "source": "2025考研政治史纲真题整理版",
        "title": "抗日战争胜利的关键",
        "text": "中国共产党在抗战中发挥中流砥柱作用，是中国人民抗日战争胜利的关键。",
        "citation": {"doc": "2025考研政治史纲真题整理版", "section": "抗日战争胜利的关键", "page": None},
        "entities": ["抗日战争", "中国共产党"],
        "related_entities": ["中流砥柱", "全面抗战路线", "抗日根据地"],
        "topic": "史纲",
        "tags": ["考点", "抗战", "真题"],
    },
    {
        "id": "exam_2025_002",
        "source": "中国近现代史纲要（2023年版）",
        "title": "抗日战争的人民性",
        "text": "抗日战争的胜利离不开全民族抗战，但中国共产党对敌后战场和持久战的领导具有关键意义。",
        "citation": {"doc": "中国近现代史纲要（2023年版）", "section": "中华民族的抗日战争", "page": 201},
        "entities": ["抗日战争", "中国共产党"],
        "related_entities": ["敌后战场", "持久战", "全民族抗战"],
        "topic": "史纲",
        "tags": ["考点", "抗战", "教材"],
    },
    {
        "id": "exam_2025_003",
        "source": "中国共产党一百年大事记",
        "title": "抗战中的中流砥柱",
        "text": "中国共产党倡导建立抗日民族统一战线，成为全民族抗战的中坚力量。",
        "citation": {"doc": "中国共产党一百年大事记", "section": "1937年", "page": None},
        "entities": ["抗日战争", "中国共产党"],
        "related_entities": ["统一战线", "民族抗战", "中坚力量"],
        "topic": "抗战",
        "tags": ["考点", "党史", "抗战"],
    },
    {
        "id": "geo_1921_001",
        "source": "中国共产党一百年大事记",
        "title": "嘉兴南湖红船",
        "text": "中共一大最后一天的会议转移到浙江嘉兴南湖的游船上举行，红船因此成为党的精神象征。",
        "citation": {"doc": "中国共产党一百年大事记", "section": "1921年", "page": None},
        "entities": ["嘉兴南湖", "中国共产党第一次全国代表大会"],
        "related_entities": ["红船", "中共一大", "浙江嘉兴"],
        "topic": "建党",
        "tags": ["地理", "建党", "党史"],
    },
    {
        "id": "geo_1921_002",
        "source": "红色地标资料整理版",
        "title": "南湖革命纪念地",
        "text": "嘉兴南湖是中国共产党诞生的重要见证地，也是开展党史学习教育的重要红色地标。",
        "citation": {"doc": "红色地标资料整理版", "section": "嘉兴南湖", "page": None},
        "entities": ["嘉兴南湖"],
        "related_entities": ["红色地标", "党史教育", "红船精神"],
        "topic": "地标",
        "tags": ["地理", "地标", "党史"],
    },
    {
        "id": "geo_1921_003",
        "source": "中国近现代史纲要（2023年版）",
        "title": "红船精神的历史来源",
        "text": "嘉兴南湖承载着中国共产党创建初期的历史记忆，成为红船精神的重要历史坐标。",
        "citation": {"doc": "中国近现代史纲要（2023年版）", "section": "中国共产党的成立", "page": 42},
        "entities": ["嘉兴南湖", "红船精神"],
        "related_entities": ["中国共产党成立", "建党精神", "历史坐标"],
        "topic": "建党",
        "tags": ["地理", "精神", "党史"],
    },
]


def _resolve_mode() -> str:
    requested_mode = os.getenv("DACHUANG_RETRIEVE_MODE", TEAM_MODE).strip().lower()
    local_ack = os.getenv("DACHUANG_LOCAL_MOCK_ACK", "").strip()
    if requested_mode == MOCK_MODE and local_ack == "1":
        return MOCK_MODE
    return TEAM_MODE


def _extract_query_entities(query: str) -> list[str]:
    entities: list[str] = []
    for keyword, entity in MOCK_ENTITY_MAP.items():
        if keyword in query and entity not in entities:
            entities.append(entity)
    return entities


def _score_vector_hit(query: str, query_entities: list[str], item: dict) -> float:
    score = 0.0
    if any(entity in item["entities"] for entity in query_entities):
        score += 0.55
    if any(entity in item["text"] for entity in query_entities):
        score += 0.25
    if any(tag in query for tag in item["tags"]):
        score += 0.1
    if item["topic"] in query:
        score += 0.1
    return min(score, 0.99)


def _score_graph_hit(query_entities: list[str], item: dict) -> float:
    score = 0.0
    overlap = sum(1 for entity in query_entities if entity in item["entities"])
    score += overlap * 0.45
    related_overlap = sum(1 for entity in query_entities if entity in item["related_entities"])
    score += related_overlap * 0.15
    if overlap > 0 and item["related_entities"]:
        score += 0.2
    return min(score, 0.99)


def _retrieve_vector_topk(query: str, query_entities: list[str], top_k: int = VECTOR_TOP_K) -> list[dict]:
    scored_hits = []
    for item in MOCK_KNOWLEDGE_BASE:
        score = _score_vector_hit(query, query_entities, item)
        if score <= 0:
            continue
        scored_hits.append(
            {
                "id": item["id"],
                "source": item["source"],
                "text": item["text"],
                "citation": item["citation"],
                "vector_score": round(score, 3),
            }
        )
    scored_hits.sort(key=lambda hit: hit["vector_score"], reverse=True)
    return scored_hits[:top_k]


def _retrieve_graph_topk(query_entities: list[str], top_k: int = GRAPH_TOP_K) -> list[dict]:
    scored_hits = []
    for item in MOCK_KNOWLEDGE_BASE:
        score = _score_graph_hit(query_entities, item)
        if score <= 0:
            continue
        scored_hits.append(
            {
                "id": item["id"],
                "related_entities": item["related_entities"],
                "graph_score": round(score, 3),
            }
        )
    scored_hits.sort(key=lambda hit: hit["graph_score"], reverse=True)
    return scored_hits[:top_k]


def _fuse_hits(vector_hits: list[dict], graph_hits: list[dict]) -> list[dict]:
    vector_by_id = {hit["id"]: hit for hit in vector_hits}
    graph_by_id = {hit["id"]: hit for hit in graph_hits}
    fused_ids = sorted(set(vector_by_id) | set(graph_by_id))
    hybrid_hits = []

    for hit_id in fused_ids:
        vector_hit = vector_by_id.get(hit_id)
        graph_hit = graph_by_id.get(hit_id)
        item = next(entry for entry in MOCK_KNOWLEDGE_BASE if entry["id"] == hit_id)
        vector_score = vector_hit["vector_score"] if vector_hit else 0.0
        graph_score = graph_hit["graph_score"] if graph_hit else 0.0
        hybrid_score = round(
            vector_score * VECTOR_WEIGHT + graph_score * GRAPH_WEIGHT,
            3,
        )
        hybrid_hits.append(
            {
                "id": hit_id,
                "source": item["source"],
                "citation": item["citation"],
                "vector_score": vector_score,
                "graph_score": graph_score,
                "hybrid_score": hybrid_score,
            }
        )

    hybrid_hits.sort(key=lambda hit: hit["hybrid_score"], reverse=True)
    return hybrid_hits


def _build_response(
    query: str,
    query_entities: list[str],
    vector_hits: list[dict],
    graph_hits: list[dict],
    hybrid_hits: list[dict],
) -> dict:
    return {
        "status": "success",
        "project": PROJECT_NAME,
        "query": query,
        "query_entities": query_entities,
        "vector_hits": vector_hits,
        "graph_hits": graph_hits,
        "hybrid_hits": hybrid_hits,
    }


def retrieve(query: str) -> dict:
    query_text = (query or "").strip()
    mode = _resolve_mode()

    if mode == MOCK_MODE:
        query_entities = _extract_query_entities(query_text)
        vector_hits = _retrieve_vector_topk(query_text, query_entities)
        graph_hits = _retrieve_graph_topk(query_entities)
        hybrid_hits = _fuse_hits(vector_hits, graph_hits)
    else:
        query_entities = []
        vector_hits, graph_hits, hybrid_hits = [], [], []

    return _build_response(
        query=query_text,
        query_entities=query_entities,
        vector_hits=vector_hits,
        graph_hits=graph_hits,
        hybrid_hits=hybrid_hits,
    )
