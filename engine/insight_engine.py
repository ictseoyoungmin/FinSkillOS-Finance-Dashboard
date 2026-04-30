"""Risk-first insight generation and financial safety checks."""

from __future__ import annotations

from typing import Any
import re

import numpy as np
import pandas as pd

from engine.metrics import format_percent, format_ratio
from engine.rule_engine import AppliedRule, RuleAuditLog


FORBIDDEN_TERMS = (
    "매수",
    "매도",
    "보유",
    "추천",
    "투자하세요",
    "투자하기",
    "진입",
    "손절",
    "익절",
    "확실",
    "보장",
    "매수하세요",
    "매도하세요",
    "보유하세요",
    "추천합니다",
    "투자하세요",
    "진입하세요",
    "손절하세요",
    "익절하세요",
    "확실합니다",
    "보장됩니다",
    "buy",
    "sell",
    "hold",
    "strong buy",
    "strong sell",
    "guaranteed",
    "risk-free profit",
    "must invest",
)

PRIORITY = {
    "data_quality": 1,
    "high_risk": 2,
    "drawdown": 3,
    "volatility": 4,
    "concentration": 5,
    "return": 6,
    "sharpe": 7,
    "correlation": 8,
}


def _severity_from_level(level: str | None) -> str:
    if level in {"VERY HIGH", "HIGH"}:
        return "HIGH"
    if level == "MODERATE":
        return "MEDIUM"
    return "INFO"


def _contains_forbidden(text: str) -> list[str]:
    lowered = text.lower()
    blocked = []
    for term in FORBIDDEN_TERMS:
        pattern = re.escape(term.lower())
        if re.search(pattern, lowered):
            blocked.append(term)
    return blocked


def _rewrite_if_needed(text: str) -> tuple[str, list[str]]:
    blocked = _contains_forbidden(text)
    if not blocked:
        return text, []
    return (
        "관측된 데이터는 추가적인 리스크 검토가 필요한 분석 신호를 보여주지만, 특정 투자 행동을 권유하지 않습니다.",
        blocked,
    )


def _safe_insight(insight: dict[str, Any]) -> tuple[dict[str, Any] | None, list[str]]:
    blocked_terms: list[str] = []
    if not insight.get("evidence"):
        return None, blocked_terms
    for key in ("fact", "interpretation", "caution"):
        rewritten, blocked = _rewrite_if_needed(str(insight.get(key, "")))
        insight[key] = rewritten
        blocked_terms.extend(blocked)
    if not insight.get("caution"):
        insight["caution"] = "데이터 한계와 시장 환경 변화 가능성을 함께 고려해야 합니다."
    return insight, blocked_terms


def _insight(
    category: str,
    severity: str,
    fact: str,
    interpretation: str,
    caution: str,
    evidence: dict[str, Any],
    rule_ids: list[str],
) -> dict[str, Any]:
    return {
        "category": category,
        "severity": severity,
        "fact": fact,
        "interpretation": interpretation,
        "caution": caution,
        "evidence": evidence,
        "rule_ids": rule_ids,
    }


def _quality_insight(quality: dict[str, Any]) -> dict[str, Any] | None:
    warnings = quality.get("quality_warnings", []) if quality else []
    if not warnings:
        return None
    return _insight(
        category="data_quality",
        severity="WARNING",
        fact=f"데이터 품질 경고가 {len(warnings)}개 감지되었습니다.",
        interpretation="일부 분석 결과는 결측치, 날짜 구조, 짧은 관측 기간 또는 이상치 후보의 영향을 받을 수 있습니다.",
        caution="의사결정 전 원본 데이터와 경고 항목을 검증해야 합니다.",
        evidence={"warning_count": len(warnings), "rule_id": "INSIGHT-CAT-007"},
        rule_ids=["INSIGHT-CAT-007", "INSIGHT-004"],
    )


def _drawdown_insight(summary: dict[str, Any]) -> dict[str, Any] | None:
    max_drawdown = summary.get("max_drawdown")
    if max_drawdown is None:
        return None
    level = summary.get("drawdown_risk_level", "UNKNOWN")
    return _insight(
        category="drawdown",
        severity=_severity_from_level(level),
        fact=f"최대낙폭(Maximum Drawdown)은 {format_percent(max_drawdown)}입니다.",
        interpretation=f"RISK-001 기준으로 손실 구간 리스크는 {level}입니다.",
        caution="최대낙폭은 과거 관측치이며 미래 최대 손실 한도가 아닙니다.",
        evidence={"metric": "max_drawdown", "value": max_drawdown, "rule_id": "RISK-001", "chart": "drawdown"},
        rule_ids=["INSIGHT-CAT-003", "RISK-001"],
    )


def _volatility_insight(summary: dict[str, Any]) -> dict[str, Any] | None:
    volatility = summary.get("annualized_volatility")
    if volatility is None:
        return None
    level = summary.get("volatility_risk_level", "UNKNOWN")
    return _insight(
        category="volatility",
        severity=_severity_from_level(level),
        fact=f"연율화 변동성(Annualized Volatility)은 {format_percent(volatility)}입니다.",
        interpretation=f"RISK-002 기준으로 변동성 리스크는 {level}입니다.",
        caution="변동성은 가격 변화의 크기를 나타내며 손실 방향만을 의미하지는 않습니다.",
        evidence={"metric": "annualized_volatility", "value": volatility, "rule_id": "RISK-002"},
        rule_ids=["INSIGHT-CAT-002", "RISK-002"],
    )


def _concentration_insight(metrics: dict[str, Any]) -> dict[str, Any] | None:
    allocation = metrics.get("allocation", {})
    if not allocation:
        return None
    max_weight = allocation.get("max_weight")
    hhi = allocation.get("hhi")
    level = allocation.get("concentration_level", "UNKNOWN")
    return _insight(
        category="concentration",
        severity="HIGH" if level == "HIGH" else "MEDIUM" if level == "MODERATE" else "INFO",
        fact=f"가장 큰 자산 비중은 {format_percent(max_weight)}이고 HHI는 {format_ratio(hhi)}입니다.",
        interpretation=f"METRIC-015 기준으로 집중도는 {level}로 분류됩니다.",
        caution="집중도는 성과 기여도를 높일 수 있지만 손실 집중 리스크도 확대할 수 있습니다.",
        evidence={"metric": "max_weight/hhi", "value": {"max_weight": max_weight, "hhi": hhi}, "rule_id": "METRIC-015"},
        rule_ids=["INSIGHT-CAT-006", "METRIC-015"],
    )


def _return_insight(summary: dict[str, Any]) -> dict[str, Any] | None:
    total_return = summary.get("total_return")
    if total_return is None:
        return None
    direction = "양(+)의 방향" if total_return >= 0 else "음(-)의 방향"
    return _insight(
        category="return",
        severity="INFO",
        fact=f"관측 기간의 누적수익률은 {format_percent(total_return)}입니다.",
        interpretation=f"동일 기간 기준 성과 방향은 {direction}입니다.",
        caution="수익률은 관측 기간에 민감하며, 기간을 바꾸면 결과가 달라질 수 있습니다.",
        evidence={"metric": "total_return", "value": total_return, "rule_id": "METRIC-003"},
        rule_ids=["INSIGHT-CAT-001", "METRIC-003"],
    )


def _sharpe_insight(summary: dict[str, Any]) -> dict[str, Any] | None:
    sharpe = summary.get("sharpe_ratio")
    if sharpe is None:
        return None
    quality = summary.get("sharpe_quality", "N/A")
    return _insight(
        category="sharpe",
        severity="INFO" if sharpe >= 0 else "WARNING",
        fact=f"샤프비율(Sharpe Ratio)은 {format_ratio(sharpe)}입니다.",
        interpretation=f"RISK-003 기준으로 위험 조정 성과는 {quality}로 분류됩니다.",
        caution="Sharpe Ratio는 수익률 분포가 안정적이라는 가정에 영향을 받습니다.",
        evidence={"metric": "sharpe_ratio", "value": sharpe, "rule_id": "RISK-003"},
        rule_ids=["INSIGHT-CAT-004", "RISK-003"],
    )


def _correlation_insight(metrics: dict[str, Any]) -> dict[str, Any] | None:
    corr = metrics.get("correlation_matrix")
    if not isinstance(corr, pd.DataFrame) or corr.empty or corr.shape[0] < 2:
        return None
    values = corr.to_numpy(dtype=float)
    mask = ~np.eye(values.shape[0], dtype=bool)
    avg_corr = float(np.nanmean(values[mask]))
    return _insight(
        category="correlation",
        severity="MEDIUM" if avg_corr > 0.7 else "INFO",
        fact=f"자산 간 평균 상관계수는 {avg_corr:.2f}입니다.",
        interpretation="상관계수가 높을수록 분산효과가 제한될 수 있습니다.",
        caution="상관관계는 시장 국면에 따라 변할 수 있습니다.",
        evidence={"metric": "average_correlation", "value": avg_corr, "rule_id": "METRIC-013", "chart": "correlation_heatmap"},
        rule_ids=["INSIGHT-CAT-005", "METRIC-013"],
    )


def _rank(insight: dict[str, Any]) -> tuple[int, int]:
    severity_rank = {"HIGH": 0, "WARNING": 1, "MEDIUM": 2, "INFO": 3}
    category = insight.get("category", "")
    if insight.get("severity") == "HIGH" and category in {"drawdown", "volatility"}:
        category = "high_risk"
    return (PRIORITY.get(category, 99), severity_rank.get(insight.get("severity"), 9))


def generate_insights(metrics: dict[str, Any], quality: dict[str, Any], schema: dict[str, Any]) -> dict[str, Any]:
    """Generate risk-first, evidence-linked insights."""

    audit = RuleAuditLog()
    raw: list[dict[str, Any] | None] = []
    summary = metrics.get("summary", {}) if metrics else {}
    raw.extend(
        [
            _quality_insight(quality),
            _drawdown_insight(summary),
            _volatility_insight(summary),
            _concentration_insight(metrics),
            _return_insight(summary),
            _sharpe_insight(summary),
            _correlation_insight(metrics),
        ]
    )

    blocked_terms: list[str] = []
    checked: list[dict[str, Any]] = []
    for item in raw:
        if item is None:
            continue
        safe, blocked = _safe_insight(item)
        blocked_terms.extend(blocked)
        if safe is not None:
            checked.append(safe)

    checked = sorted(checked, key=_rank)[:5]
    for idx, insight in enumerate(checked, start=1):
        insight["id"] = f"insight_{idx:03d}"

    audit.add(
        rule_id="INSIGHT-001",
        step="insight_generation",
        condition="Major insights must use Fact / Interpretation / Caution.",
        action="Generate structured insight cards.",
        result=f"{len(checked)} insight(s) generated.",
    )
    audit.add(
        rule_id="INSIGHT-002",
        step="insight_generation",
        condition="Each insight must include evidence.",
        action="Drop insights without evidence.",
        result="Evidence check applied.",
    )
    audit.add(
        rule_id="INSIGHT-003",
        step="insight_generation",
        condition="Risk and limitation insights should be ordered before return interpretation.",
        action="Rank insights by data quality, high risk, drawdown, volatility, concentration, return, Sharpe, correlation.",
        result="Risk-first ordering applied.",
    )
    audit.add(
        rule_id="SAFE-POST-001",
        step="safety_check",
        condition="Generated insights must not include prohibited financial advice terms.",
        action="Scan and rewrite prohibited wording.",
        result=f"{len(blocked_terms)} prohibited term occurrence(s) handled.",
        severity="WARNING" if blocked_terms else "INFO",
    )
    audit.add(
        rule_id="SAFE-POST-002",
        step="safety_check",
        condition="Insights without evidence must not be shown.",
        action="Filter insights with missing evidence.",
        result="All displayed insights include evidence.",
    )
    audit.add(
        rule_id="SAFE-POST-003",
        step="safety_check",
        condition="Insights should include caution text when uncertainty exists.",
        action="Ensure caution text exists.",
        result="Caution text verified.",
    )

    return {
        "insights": checked,
        "blocked_terms": sorted(set(blocked_terms)),
        "applied_rules": audit.to_records(),
        "schema_type": schema.get("schema_type") if schema else "unknown",
    }
