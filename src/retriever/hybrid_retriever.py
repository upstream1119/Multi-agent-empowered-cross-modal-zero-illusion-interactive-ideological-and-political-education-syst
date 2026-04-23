import os


PROJECT_NAME = "多智能体赋能的跨模态零幻觉交互式思政教育系统"
TEAM_MODE = "team"
MOCK_MODE = "mock"

# 学习模式下的最小关键词映射，用于演示 query -> entities 的契约过程。
MOCK_ENTITY_MAP = {
    "遵义会议": "遵义会议",
    "长征": "长征",
    "毛泽东": "毛泽东",
}


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


def _build_mock_hits(query_entities: list[str]) -> tuple[list[dict], list[dict], list[dict]]:
    if not query_entities:
        return [], [], []

    citation = {"doc": "中国共产党一百年大事记", "section": "1935年", "page": None}
    vector_score = 0.85
    graph_score = 0.90
    hybrid_score = round((vector_score + graph_score) / 2, 3)

    vector_hits = [
        {
            "id": "event_1935_001",
            "source": "中国共产党一百年大事记",
            "text": "1935年1月，中共中央政治局在长征途中举行遵义会议。",
            "citation": citation,
            "vector_score": vector_score,
        }
    ]
    graph_hits = [
        {
            "id": "event_1935_001",
            "related_entities": ["中央政治局", "长征", "毛泽东"],
            "graph_score": graph_score,
        }
    ]
    hybrid_hits = [
        {
            "id": "event_1935_001",
            "source": "中国共产党一百年大事记",
            "citation": citation,
            "vector_score": vector_score,
            "graph_score": graph_score,
            "hybrid_score": hybrid_score,
        }
    ]
    return vector_hits, graph_hits, hybrid_hits


def retrieve(query: str) -> dict:
    query_text = (query or "").strip()
    mode = _resolve_mode()

    if mode == MOCK_MODE:
        query_entities = _extract_query_entities(query_text)
        vector_hits, graph_hits, hybrid_hits = _build_mock_hits(query_entities)
    else:
        query_entities = []
        vector_hits, graph_hits, hybrid_hits = [], [], []

    return {
        "status": "success",
        "project": PROJECT_NAME,
        "query": query_text,
        "query_entities": query_entities,
        "vector_hits": vector_hits,
        "graph_hits": graph_hits,
        "hybrid_hits": hybrid_hits,
    }
