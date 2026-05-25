PASS_STATUS = "pass"
WARNING_STATUS = "warning"
NEED_REVIEW_STATUS = "need_review"

FEEDBACK_LABEL_OPTIONS = [
    "通过",
    "证据不足",
    "表述不够稳妥",
    "历史语境不清",
    "结论超出材料",
    "需要专家复核",
]


def _build_feedback_collection(
    stage: str,
    recommended_reviewer: str,
    expert_review_priority: str,
) -> dict:
    return {
        "stage": stage,
        "recommended_reviewer": recommended_reviewer,
        "expert_review_priority": expert_review_priority,
        "label_options": FEEDBACK_LABEL_OPTIONS,
    }


def check_policy_risk(answer: str, citations_used: list[dict], source_check: dict) -> dict:
    """
    政治红线审查智能体最小原型。
    当前定位为专家反馈数据引擎的规则型初筛，不替代赵老师专家审查。
    """
    issues = []
    risk_types = []

    if not answer.strip() or not citations_used:
        return {
            "status": NEED_REVIEW_STATUS,
            "risk_types": ["evidence_missing"],
            "issues": ["当前回答缺少可用证据支撑，不建议直接输出。"],
            "suggestion": "请补充检索证据，或交由人工复核。",
            "feedback_collection": _build_feedback_collection(
                stage="student_initial_label",
                recommended_reviewer="研究生或项目组员先初标，赵老师抽样校准。",
                expert_review_priority="high",
            ),
        }

    source_status = source_check.get("status")
    if source_status in {"fail", "no_evidence"}:
        return {
            "status": NEED_REVIEW_STATUS,
            "risk_types": ["source_check_failed"],
            "issues": ["溯源审查未通过，回答来源链条不完整。"],
            "suggestion": "请先修复 citation，再进行政治红线审查。",
            "feedback_collection": _build_feedback_collection(
                stage="student_initial_label",
                recommended_reviewer="研究生或项目组员先初标，赵老师抽样校准。",
                expert_review_priority="high",
            ),
        }

    if source_status == "warning":
        risk_types.append("source_check_warning")
        issues.append("溯源审查存在 warning，需要人工复核来源完整性。")

    if "仅依据当前检索到的证据" not in answer:
        risk_types.append("missing_scope_statement")
        issues.append("回答缺少证据边界说明，可能让使用者误以为结论已经完全定稿。")

    status = WARNING_STATUS if issues else PASS_STATUS
    return {
        "status": status,
        "risk_types": risk_types,
        "issues": issues,
        "suggestion": "建议保留研究生初标与赵老师抽样校准机制。",
        "feedback_collection": _build_feedback_collection(
            stage="rule_seed",
            recommended_reviewer="低风险样例由研究生或组员初标，高风险和争议样例交赵老师校准。",
            expert_review_priority="normal" if status == PASS_STATUS else "medium",
        ),
    }
