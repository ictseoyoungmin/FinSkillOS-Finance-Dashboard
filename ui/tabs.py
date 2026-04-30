"""Tab-level renderers for the FinSkillOS dashboard."""

from __future__ import annotations

from typing import Any

import pandas as pd
import streamlit as st

from engine.metrics import format_percent, format_ratio
from engine.report_builder import build_html_report
from engine.rule_engine import RuleAuditLog
from ui.charts import (
    render_correlation_heatmap,
    render_cumulative_return_chart,
    render_drawdown_chart,
    render_risk_return_scatter,
)
from ui.components import empty_state, insight_card, metric_card, rule_card, status_badge


def _schema_compact_table(schema: dict[str, Any] | None, profile: dict[str, Any] | None) -> pd.DataFrame:
    if not schema:
        return pd.DataFrame(
            [
                {"item": "Schema", "value": "Awaiting dataset"},
                {"item": "Frequency", "value": "N/A"},
                {"item": "Rows", "value": "N/A"},
            ]
        )

    mapping = schema.get("mapping", {})
    rows = [
        {"item": "Detected Schema", "value": schema.get("schema_type", "unknown")},
        {"item": "Date Column", "value": mapping.get("date", {}).get("source", "N/A")},
        {"item": "Asset Column", "value": mapping.get("asset", {}).get("source", "N/A")},
        {"item": "Price Column", "value": mapping.get("price", {}).get("source", "N/A")},
        {"item": "Return Column", "value": mapping.get("return", {}).get("source", "N/A")},
    ]
    if profile:
        rows.extend(
            [
                {"item": "Frequency", "value": str(profile.get("frequency", "unknown")).title()},
                {"item": "Rows", "value": f"{int(profile.get('row_count', 0)):,}"},
            ]
        )
    return pd.DataFrame(rows)


def _quality_summary(profile: dict[str, Any] | None) -> str:
    if not profile:
        return "Awaiting data"
    warnings = profile.get("quality_warnings", [])
    if warnings:
        return f"{len(warnings)} warning(s)"
    return "No blocking warnings"


def _asset_count(metrics: dict[str, Any] | None, schema: dict[str, Any] | None) -> str:
    if metrics:
        rows = metrics.get("asset_metrics", [])
        if rows:
            return f"{len(rows):,}"
    std_df = schema.get("standardized_df") if schema else None
    if isinstance(std_df, pd.DataFrame) and "asset" in std_df.columns:
        return f"{std_df['asset'].nunique(dropna=True):,}"
    return "N/A"


def render_overview_dashboard(
    df: pd.DataFrame | None,
    source_name: str,
    audit: RuleAuditLog,
    profile: dict[str, Any] | None,
    schema: dict[str, Any] | None,
    metrics: dict[str, Any] | None,
    insights: dict[str, Any] | None,
    analysis_result: dict[str, Any] | None,
) -> None:
    """Render the product-style overview dashboard."""

    if df is None or metrics is None:
        empty_state(
            "Select a Dataset to Generate the Overview",
            "Use the analysis controls above to upload a CSV or choose a bundled sample. The overview will populate with KPI cards, charts, insights, and applied rule traceability.",
        )
        return

    summary = metrics.get("summary", {})
    kpi_cols = st.columns(6)
    with kpi_cols[0]:
        metric_card("Total Return", format_percent(summary.get("total_return")), "Total over selected period", "teal", "↗")
    with kpi_cols[1]:
        metric_card("Annualized Return", format_percent(summary.get("annualized_return")), "Compounded per year", "teal", "⟳")
    with kpi_cols[2]:
        metric_card("Volatility (Ann.)", format_percent(summary.get("annualized_volatility")), "Standard deviation", "blue", "~")
    with kpi_cols[3]:
        metric_card("Max Drawdown", format_percent(summary.get("max_drawdown")), "From peak to trough", "red", "↘")
    with kpi_cols[4]:
        metric_card("Sharpe Ratio", format_ratio(summary.get("sharpe_ratio")), "Risk-adjusted return", "purple", "Σ")
    with kpi_cols[5]:
        risk_level = str(summary.get("risk_level", "UNKNOWN"))
        metric_card("Risk Level", risk_level, "Rule-based classification", "amber", "◇")

    top_left, top_mid, top_right = st.columns([1.45, 1.0, 0.88])
    with top_left.container(border=True):
        st.markdown("#### Executive Summary")
        st.caption("Cumulative return over time")
        render_cumulative_return_chart(metrics, height=310)
    with top_mid.container(border=True):
        st.markdown("#### Risk Analysis")
        st.caption("Drawdown behavior")
        render_drawdown_chart(metrics, height=310)
    with top_right.container(border=True):
        st.markdown("#### Data Profile")
        st.caption(f"Source: {source_name}")
        st.dataframe(_schema_compact_table(schema, profile), use_container_width=True, hide_index=True)
        compact_cols = st.columns(2)
        compact_cols[0].metric("Assets", _asset_count(metrics, schema))
        compact_cols[1].metric("Quality", _quality_summary(profile))

    lower_left, lower_mid, lower_right = st.columns([1.08, 1.08, 1.15])
    with lower_left.container(border=True):
        st.markdown("#### Correlation & Diversification")
        st.caption("Asset relationship overview")
        render_correlation_heatmap(metrics, height=285)
    with lower_mid.container(border=True):
        st.markdown("#### Risk vs. Return")
        st.caption("Annualized return versus volatility")
        render_risk_return_scatter(metrics, height=285)
    with lower_right.container(border=True):
        st.markdown("#### Rule-Based Insights")
        st.caption("Fact, interpretation, and caution generated from Skills.md rules")
        items = (insights or {}).get("insights", [])
        if not items:
            empty_state("No Insights Generated", "The insight engine did not produce evidence-linked cards for this dataset.")
        for item in items[:3]:
            insight_card(
                category=str(item.get("category", "Insight")),
                fact=str(item.get("fact", "")),
                interpretation=str(item.get("interpretation", "")),
                caution=str(item.get("caution", "")),
                severity=str(item.get("severity", "INFO")),
            )

    records = audit.deduplicated_records()
    st.markdown("### Applied Skill Rules")
    st.caption("Rule traceability and execution status for this analysis")
    rule_cols = st.columns(5)
    for column, record in zip(rule_cols, records[:5], strict=False):
        with column:
            rule_card(
                rule_id=str(record.get("rule_id", "RULE")),
                title=str(record.get("step", "rule")),
                description=str(record.get("result", "")),
                status="Passed" if record.get("severity") != "WARNING" else "Review",
                severity=str(record.get("severity", "INFO")),
            )

    footer_cols = st.columns([1.2, 1.0, 1.0, 1.15])
    coverage = audit.has_prefixes(["DATA", "SCHEMA", "METRIC", "VIS", "INSIGHT", "SAFE"])
    footer_cols[0].markdown(f"**Rules Executed**  \n{len(records):,}")
    footer_cols[1].markdown(f"**Coverage**  \n{sum(coverage.values())}/{len(coverage)} categories")
    footer_cols[2].markdown(f"**Schema**  \n{schema.get('schema_type', 'unknown') if schema else 'unknown'}")
    with footer_cols[3]:
        if analysis_result is not None:
            html_report = build_html_report(analysis_result)
            st.download_button(
                "Generate Report",
                data=html_report.encode("utf-8"),
                file_name="finskillos_analysis_report.html",
                mime="text/html",
                use_container_width=True,
            )
        else:
            st.markdown(status_badge("Report unavailable", "warning"), unsafe_allow_html=True)

