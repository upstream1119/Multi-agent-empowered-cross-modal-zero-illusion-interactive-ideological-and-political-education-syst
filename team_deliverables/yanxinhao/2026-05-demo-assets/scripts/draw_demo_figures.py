from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Rectangle


TASK_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = TASK_ROOT / "figures"


def get_cjk_font():
    """Pick a local Chinese font so exported PNG text is readable in PPT."""
    preferred = [
        "Microsoft YaHei",
        "SimHei",
        "Noto Sans CJK SC",
        "Source Han Sans SC",
        "Arial Unicode MS",
    ]
    system_fonts = font_manager.findSystemFonts()
    for font_path in system_fonts:
        try:
            prop = font_manager.FontProperties(fname=font_path)
            if prop.get_name() in preferred:
                return prop
        except Exception:
            continue
    return font_manager.FontProperties()


FONT = get_cjk_font()
COLORS = {
    "bg": "#f8fafc",
    "ink": "#111827",
    "muted": "#374151",
    "blue": "#dbeafe",
    "blue_edge": "#2563eb",
    "green": "#dcfce7",
    "green_edge": "#16a34a",
    "yellow": "#fef3c7",
    "yellow_edge": "#d97706",
    "red": "#fee2e2",
    "red_edge": "#dc2626",
    "purple": "#ede9fe",
    "purple_edge": "#7c3aed",
    "gray": "#e5e7eb",
    "gray_edge": "#4b5563",
    "white": "#ffffff",
}


def setup_ax(width: float = 16, height: float = 9):
    fig, ax = plt.subplots(figsize=(width, height), dpi=300)
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.axis("off")
    fig.patch.set_facecolor(COLORS["bg"])
    ax.set_facecolor(COLORS["bg"])
    return fig, ax


def add_title(ax, title: str, subtitle: str | None = None):
    ax.text(
        8,
        8.55,
        title,
        ha="center",
        va="center",
        fontsize=22,
        fontproperties=FONT,
        color=COLORS["ink"],
        weight="bold",
    )
    if subtitle:
        ax.text(
            8,
            8.12,
            subtitle,
            ha="center",
            va="center",
            fontsize=11,
            fontproperties=FONT,
            color=COLORS["muted"],
        )


def box(
    ax,
    x: float,
    y: float,
    w: float,
    h: float,
    text: str,
    fc: str,
    ec: str,
    fontsize: int = 11,
    radius: float = 0.08,
    weight: str = "bold",
):
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle=f"round,pad=0.03,rounding_size={radius}",
        linewidth=2.2,
        facecolor=fc,
        edgecolor=ec,
    )
    ax.add_patch(patch)
    ax.text(
        x + w / 2,
        y + h / 2,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        fontproperties=FONT,
        color=COLORS["ink"],
        weight=weight,
        linespacing=1.25,
    )
    return patch


def label(ax, x: float, y: float, text: str, fontsize: int = 10, color: str | None = None):
    ax.text(
        x,
        y,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        fontproperties=FONT,
        color=color or COLORS["muted"],
        linespacing=1.25,
    )


def arrow(ax, start: tuple[float, float], end: tuple[float, float], color: str = "#374151", lw: float = 2.0):
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=14,
            linewidth=lw,
            color=color,
            shrinkA=3,
            shrinkB=3,
        )
    )


def elbow_arrow(ax, points: list[tuple[float, float]], color: str = "#374151", lw: float = 2.0):
    """Draw a right-angle arrow so connectors can avoid existing boxes."""
    if len(points) < 2:
        return
    for start, end in zip(points[:-2], points[1:-1]):
        ax.plot(
            [start[0], end[0]],
            [start[1], end[1]],
            color=color,
            linewidth=lw,
            solid_capstyle="round",
        )
    ax.add_patch(
        FancyArrowPatch(
            points[-2],
            points[-1],
            arrowstyle="-|>",
            mutation_scale=14,
            linewidth=lw,
            color=color,
            shrinkA=0,
            shrinkB=0,
        )
    )


def save(fig, filename: str):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / filename
    fig.savefig(path, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"saved: {path}")


def draw_system_pipeline():
    fig, ax = setup_ax()
    add_title(ax, "思政历史 KG-RAG Demo 系统总体链路图", "用户提问后：检索证据 -> 融合排序 -> 多智能体审查 -> 可信展示")

    y = 5.35
    h = 0.78
    nodes = [
        (0.9, y, 1.25, h, "用户问题", COLORS["white"], COLORS["gray_edge"]),
        (2.6, y, 1.55, h, "FastAPI\n/retrieve", COLORS["blue"], COLORS["blue_edge"]),
        (4.6, y, 1.45, h, "Query\n实体识别", COLORS["blue"], COLORS["blue_edge"]),
    ]
    for item in nodes:
        box(ax, *item, fontsize=11)
    arrow(ax, (2.15, y + h / 2), (2.6, y + h / 2))
    arrow(ax, (4.15, y + h / 2), (4.6, y + h / 2))

    # KG-RAG branch block
    box(ax, 6.65, 6.68, 3.2, 0.55, "KG-RAG 检索底座", COLORS["purple"], COLORS["purple_edge"], fontsize=12, weight="bold")
    box(ax, 6.65, 5.6, 3.35, 0.55, "向量召回：FAISS / Milvus\n-> vector_hits", COLORS["green"], COLORS["green_edge"], fontsize=10)
    box(ax, 6.65, 4.58, 3.35, 0.55, "图谱召回：NetworkX / Neo4j\n-> graph_hits", COLORS["yellow"], COLORS["yellow_edge"], fontsize=10)
    elbow_arrow(ax, [(6.05, y + h / 2), (6.32, y + h / 2), (6.32, 5.88), (6.65, 5.88)])
    elbow_arrow(ax, [(6.05, y + h / 2), (6.26, y + h / 2), (6.26, 4.86), (6.65, 4.86)])

    box(ax, 10.55, y, 2.15, h, "融合排序\n0.7×VectorSim\n+ 0.3×GraphSim", COLORS["purple"], COLORS["purple_edge"], fontsize=8.5)
    elbow_arrow(ax, [(10.0, 5.88), (10.28, 5.88), (10.28, y + h / 2), (10.55, y + h / 2)])
    elbow_arrow(ax, [(10.0, 4.86), (10.38, 4.86), (10.38, y + h / 2), (10.55, y + h / 2)])

    box(ax, 13.1, y, 2.05, h, "hybrid_hits\ntitle + text\ncitation + score", COLORS["green"], COLORS["green_edge"], fontsize=8.2)
    arrow(ax, (12.7, y + h / 2), (13.1, y + h / 2))

    agent_y = 2.55
    agent_nodes = [
        (4.7, agent_y, 1.65, h, "生成智能体", COLORS["white"], COLORS["gray_edge"]),
        (6.9, agent_y, 1.75, h, "溯源审查\n智能体", COLORS["white"], COLORS["gray_edge"]),
        (9.25, agent_y, 1.75, h, "政治审查\n智能体", COLORS["red"], COLORS["red_edge"]),
        (11.7, agent_y, 2.25, h, "可信回答\nSwagger / 展示端", COLORS["green"], COLORS["green_edge"]),
    ]
    for item in agent_nodes:
        box(ax, *item, fontsize=10)
    elbow_arrow(ax, [(14.13, y), (14.13, 4.15), (5.53, 4.15), (5.53, agent_y + h)])
    arrow(ax, (6.35, agent_y + h / 2), (6.9, agent_y + h / 2))
    arrow(ax, (8.65, agent_y + h / 2), (9.25, agent_y + h / 2))
    arrow(ax, (11.0, agent_y + h / 2), (11.7, agent_y + h / 2))

    label(ax, 8, 1.55, "当前 Demo 重点：先让 /retrieve 返回可溯源证据；多智能体与前端展示作为后续扩展。", fontsize=11)
    save(fig, "system_pipeline.png")


def draw_kg_rag_flow():
    fig, ax = setup_ax()
    add_title(ax, "KG-RAG 证据检索与融合打分流程图", "文本语义召回 + 图谱关系召回 + 融合打分 + citation 返回")

    # Column backgrounds
    for x, title, color, edge in [
        (0.55, "数据层", COLORS["blue"], COLORS["blue_edge"]),
        (5.55, "检索层", COLORS["purple"], COLORS["purple_edge"]),
        (10.55, "融合返回层", COLORS["green"], COLORS["green_edge"]),
    ]:
        ax.add_patch(Rectangle((x, 1.05), 4.25, 6.75, facecolor="#ffffff", edgecolor=edge, linewidth=1.4, alpha=0.82))
        box(ax, x + 1.25, 7.35, 1.75, 0.42, title, color, edge, fontsize=12, weight="bold")

    data_x = 1.15
    data_items = [
        ("《中国共产党\n思想政治教育史》PDF", 6.35),
        ("OCR / 文本清洗", 5.25),
        ("标准化切片\nChunking", 4.15),
        ("text_chunks_demo.jsonl", 3.05),
        ("entities / tags\n/ citation", 1.95),
    ]
    last_y = None
    for text, y in data_items:
        box(ax, data_x, y, 3.05, 0.62, text, COLORS["blue"], COLORS["blue_edge"], fontsize=10)
        if last_y is not None:
            arrow(ax, (data_x + 1.52, last_y), (data_x + 1.52, y + 0.62))
        last_y = y

    mid_x = 6.05
    box(ax, mid_x, 6.35, 3.25, 0.62, "用户 Query", COLORS["white"], COLORS["gray_edge"], fontsize=11)
    box(ax, mid_x, 5.25, 3.25, 0.62, "实体抽取", COLORS["purple"], COLORS["purple_edge"], fontsize=11)
    box(ax, mid_x, 4.28, 3.25, 0.62, "双路召回", COLORS["purple"], COLORS["purple_edge"], fontsize=11, weight="bold")
    arrow(ax, (7.68, 6.35), (7.68, 5.87))
    arrow(ax, (7.68, 5.25), (7.68, 4.9))
    box(ax, 5.75, 2.95, 1.65, 0.78, "Vector\nRetrieval\n-> vector_hits", COLORS["green"], COLORS["green_edge"], fontsize=9)
    box(ax, 8.05, 2.95, 1.65, 0.78, "Graph\nRetrieval\n-> graph_hits", COLORS["yellow"], COLORS["yellow_edge"], fontsize=9)
    label(ax, 6.58, 2.47, "语义相似文本", fontsize=9)
    label(ax, 8.88, 2.47, "实体关系证据", fontsize=9)
    elbow_arrow(ax, [(7.68, 4.28), (7.68, 3.98), (6.58, 3.98), (6.58, 3.73)])
    elbow_arrow(ax, [(7.68, 4.28), (7.68, 3.98), (8.88, 3.98), (8.88, 3.73)])

    out_x = 11.0
    box(ax, out_x, 5.95, 3.35, 0.78, "融合打分\n0.7 × VectorSim + 0.3 × GraphSim", COLORS["purple"], COLORS["purple_edge"], fontsize=9)
    box(ax, out_x, 4.55, 3.35, 0.68, "hybrid_hits", COLORS["green"], COLORS["green_edge"], fontsize=12, weight="bold")
    box(ax, out_x, 3.1, 3.35, 0.92, "title / text\ncitation / score", COLORS["green"], COLORS["green_edge"], fontsize=11)
    box(ax, out_x, 1.65, 3.35, 0.8, "返回证据块\n不是直接编答案", COLORS["red"], COLORS["red_edge"], fontsize=11, weight="bold")
    arrow(ax, (12.68, 5.95), (12.68, 5.23))
    arrow(ax, (12.68, 4.55), (12.68, 4.02))
    arrow(ax, (12.68, 3.1), (12.68, 2.45))
    elbow_arrow(ax, [(7.4, 3.08), (7.6, 3.08), (7.6, 2.78), (10.55, 2.78), (10.55, 6.34), (11.0, 6.34)], color=COLORS["green_edge"])
    elbow_arrow(ax, [(9.7, 3.34), (10.25, 3.34), (10.25, 6.12), (11.0, 6.12)], color=COLORS["yellow_edge"])

    save(fig, "kg_rag_flow.png")


def draw_future_sandbox_demo():
    fig, ax = setup_ax()
    add_title(ax, "XR 时空沙盘与思政知识交互设想图", "后续扩展：地标 + 时间轴 + KG-RAG 证据 + 数字人可信讲解")

    # Timeline
    timeline_y = 5.7
    ax.plot([0.9, 9.6], [timeline_y, timeline_y], color=COLORS["gray_edge"], linewidth=3)
    points = [
        (1.1, "1921\n建党", "嘉兴南湖"),
        (3.0, "1935\n遵义会议", "遵义"),
        (4.9, "1942\n延安整风", "延安"),
        (6.7, "抗战时期", "抗日根据地"),
        (8.7, "1949\n新中国成立", "西柏坡"),
    ]
    for x, time_text, place in points:
        ax.add_patch(Circle((x, timeline_y), 0.16, facecolor=COLORS["red_edge"], edgecolor="white", linewidth=1.5))
        label(ax, x, timeline_y + 0.62, time_text, fontsize=10, color=COLORS["ink"])
        box(ax, x - 0.55, timeline_y - 1.15, 1.1, 0.5, place, COLORS["yellow"], COLORS["yellow_edge"], fontsize=9)
        arrow(ax, (x, timeline_y - 0.18), (x, timeline_y - 0.62), color=COLORS["yellow_edge"], lw=1.4)

    box(ax, 1.0, 2.75, 1.35, 0.72, "用户点击\n红色地标", COLORS["white"], COLORS["gray_edge"], fontsize=10)
    box(ax, 3.0, 2.75, 1.55, 0.72, "触发\nKG-RAG 检索", COLORS["purple"], COLORS["purple_edge"], fontsize=10)
    box(ax, 5.25, 2.75, 1.65, 0.72, "返回\n证据卡片", COLORS["green"], COLORS["green_edge"], fontsize=10)
    arrow(ax, (2.35, 3.11), (3.0, 3.11))
    arrow(ax, (4.55, 3.11), (5.25, 3.11))
    elbow_arrow(ax, [(3.0, timeline_y - 1.15), (3.0, 3.85), (1.68, 3.85), (1.68, 3.47)], color=COLORS["gray_edge"], lw=1.4)

    # Knowledge card
    card_x, card_y, card_w, card_h = 10.15, 3.05, 4.95, 3.85
    box(ax, card_x, card_y, card_w, card_h, "", COLORS["white"], COLORS["green_edge"])
    ax.text(card_x + 0.28, card_y + card_h - 0.42, "证据卡片（示意）", ha="left", va="center", fontsize=14, fontproperties=FONT, color=COLORS["ink"], weight="bold")
    card_lines = [
        "事件：遵义会议",
        "证据：长征途中召开的关键会议",
        "来源：《中国共产党思想政治教育史》",
        "citation：章节 / 页码",
        "相关实体：长征、毛泽东、中央政治局",
    ]
    for i, line in enumerate(card_lines):
        ax.text(card_x + 0.35, card_y + card_h - 0.95 - i * 0.52, line, ha="left", va="center", fontsize=10.5, fontproperties=FONT, color=COLORS["ink"])
    elbow_arrow(ax, [(6.9, 3.11), (9.65, 3.11), (9.65, 4.8), (10.15, 4.8)], color=COLORS["green_edge"])

    # Digital human icon
    ax.add_patch(Circle((12.6, 1.35), 0.34, facecolor=COLORS["red"], edgecolor=COLORS["red_edge"], linewidth=1.6))
    ax.add_patch(Rectangle((12.25, 0.62), 0.7, 0.55, facecolor=COLORS["red"], edgecolor=COLORS["red_edge"], linewidth=1.6))
    label(ax, 12.6, 0.22, "小红军数字人 / 讲解员", fontsize=10, color=COLORS["ink"])
    box(ax, 10.2, 1.05, 1.65, 0.72, "基于证据\n生成讲解", COLORS["blue"], COLORS["blue_edge"], fontsize=10)
    box(ax, 13.35, 1.05, 1.95, 0.72, "经过溯源审查\n与政治审查", COLORS["red"], COLORS["red_edge"], fontsize=9.5)
    arrow(ax, (11.85, 1.41), (12.25, 1.41), color=COLORS["blue_edge"])
    arrow(ax, (12.95, 1.41), (13.35, 1.41), color=COLORS["red_edge"])
    arrow(ax, (12.6, 3.05), (12.6, 1.8), color=COLORS["green_edge"])

    box(ax, 0.75, 7.1, 2.35, 0.55, "后续扩展示意\n不是当前已完成前端", COLORS["red"], COLORS["red_edge"], fontsize=10, weight="bold")
    box(ax, 3.65, 7.1, 4.5, 0.55, "可点击地标：嘉兴南湖 / 井冈山 / 遵义 / 延安 / 西柏坡", COLORS["yellow"], COLORS["yellow_edge"], fontsize=9.5)

    save(fig, "future_sandbox_demo.png")


def main():
    draw_system_pipeline()
    draw_kg_rag_flow()
    draw_future_sandbox_demo()


if __name__ == "__main__":
    main()
