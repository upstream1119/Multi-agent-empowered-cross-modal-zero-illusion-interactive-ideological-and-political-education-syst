import os

from src.generator.template_generator import generate_answer_from_hits


TEMPLATE_MODE = "template"
LLM_MODE = "llm"


def _resolve_generator_mode() -> str:
    mode = os.getenv("DACHUANG_GENERATOR_MODE", TEMPLATE_MODE).strip().lower()
    if mode == LLM_MODE:
        return LLM_MODE
    return TEMPLATE_MODE


def _format_prompt_citation(citation: dict) -> str:
    doc = citation.get("doc") or "未知文献"
    section = citation.get("section") or "未知章节"
    page = citation.get("page")
    page_text = "PDF 页码待复核" if page is None else f"PDF 页码 {page}"
    return f"{doc} / {section} / {page_text}"


def build_evidence_prompt(query: str, hybrid_hits: list[dict], max_hits: int = 3) -> str:
    evidence_lines = []
    for index, hit in enumerate(hybrid_hits[:max_hits], start=1):
        citation = hit.get("citation", {})
        evidence_lines.append(
            f"[{index}] 标题：{hit.get('title', '')}\n"
            f"正文：{hit.get('text', '')}\n"
            f"来源：{_format_prompt_citation(citation)}"
        )

    evidence_text = "\n\n".join(evidence_lines) or "无可用证据"
    return (
        "你是思政教育系统中的生成智能体。\n"
        "你只能依据给定证据回答，不能补充证据外内容。\n"
        "如果证据不足，请明确说明证据不足，不能编造 citation。\n\n"
        f"问题：{query}\n\n"
        f"证据：\n{evidence_text}"
    )


def generate_answer(query: str, hybrid_hits: list[dict]) -> dict:
    mode = _resolve_generator_mode()
    if mode == LLM_MODE:
        # v0 先固定受控 prompt 和输出契约，真实国内模型 provider 下一轮接入。
        generated = generate_answer_from_hits(query, hybrid_hits)
        generated["generator_mode"] = LLM_MODE
        generated["prompt_preview"] = build_evidence_prompt(query, hybrid_hits)
        return generated

    generated = generate_answer_from_hits(query, hybrid_hits)
    generated["generator_mode"] = TEMPLATE_MODE
    return generated
