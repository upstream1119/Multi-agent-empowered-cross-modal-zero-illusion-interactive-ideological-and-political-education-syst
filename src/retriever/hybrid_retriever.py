PROJECT_NAME = "多智能体赋能的跨模态零幻觉交互式思政教育系统"


def retrieve(query: str) -> dict:
    # 最小可运行版本：先固定返回结构，后续在此接入真实检索逻辑
    return {
        "status": "success",
        "project": PROJECT_NAME,
        "query": query,
        "query_entities": [],
        "vector_hits": [],
        "graph_hits": [],
        "hybrid_hits": [],
    }
