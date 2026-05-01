"""Tab-level renderers for the FinSkillOS dashboard."""

from __future__ import annotations

from typing import Any

import pandas as pd
import numpy as np
import streamlit as st

from engine.metrics import format_percent, format_ratio
from engine.report_builder import build_html_report
from engine.rule_engine import RuleAuditLog
from ui.charts import (
    render_allocation_chart,
    render_correlation_heatmap,
    render_cumulative_return_chart,
    render_drawdown_chart,
    render_frequency_coverage_chart,
    render_missing_values_chart,
    render_return_distribution,
    render_risk_contribution_chart,
    render_risk_return_scatter,
    render_rolling_return_chart,
    render_rolling_volatility_chart,
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


def _date_range(schema: dict[str, Any] | None) -> str:
    std_df = schema.get("standardized_df") if schema else None
    if not isinstance(std_df, pd.DataFrame) or "date" not in std_df.columns:
        return "N/A"
    dates = pd.to_datetime(std_df["date"], errors="coerce").dropna()
    if dates.empty:
        return "N/A"
    return f"{dates.min().date()} - {dates.max().date()}"


def _missing_summary(profile: dict[str, Any] | None) -> tuple[str, str]:
    if not profile:
        return "N/A", "Awaiting profile"
    rates = profile.get("missing_rates", {})
    row_count = int(profile.get("row_count", 0))
    missing_cells = int(sum(rate * row_count for rate in rates.values()))
    total_cells = max(row_count * len(rates), 1)
    return f"{missing_cells:,}", f"{missing_cells / total_cells:.2%} of cells"


def _average_correlation(metrics: dict[str, Any] | None) -> float | None:
    if not metrics:
        return None
    corr = metrics.get("correlation_matrix")
    if not isinstance(corr, pd.DataFrame) or corr.empty or corr.shape[0] < 2:
        return None
    values = corr.to_numpy(dtype=float)
    mask = ~np.eye(values.shape[0], dtype=bool)
    off_diag = values[mask]
    off_diag = off_diag[~np.isnan(off_diag)]
    if len(off_diag) == 0:
        return None
    return float(off_diag.mean())


def _allocation_rows(schema: dict[str, Any] | None) -> pd.DataFrame:
    std_df = schema.get("standardized_df") if schema else None
    if not isinstance(std_df, pd.DataFrame) or not {"asset", "weight"}.issubset(std_df.columns):
        return pd.DataFrame()
    return std_df.dropna(subset=["asset", "weight"]).copy()


def _largest_weight(schema: dict[str, Any] | None) -> tuple[str, str]:
    rows = _allocation_rows(schema)
    if rows.empty:
        return "N/A", "No allocation weights"
    idx = rows["weight"].astype(float).idxmax()
    row = rows.loc[idx]
    return format_percent(float(row["weight"])), str(row["asset"])


def _cash_exposure(schema: dict[str, Any] | None) -> str:
    rows = _allocation_rows(schema)
    if rows.empty:
        return "N/A"
    mask = rows["asset"].astype(str).str.contains("cash", case=False, na=False)
    if not mask.any():
        return "0.00%"
    return format_percent(float(rows.loc[mask, "weight"].sum()))


def _rule_cards_for_prefix(audit: RuleAuditLog, prefixes: set[str], limit: int = 4) -> None:
    records = [record for record in audit.deduplicated_records() if str(record.get("prefix")) in prefixes]
    if not records:
        empty_state("No Matching Rules", f"No rules with prefixes {', '.join(sorted(prefixes))} were recorded.")
        return
    columns = st.columns(min(limit, len(records)))
    for column, record in zip(columns, records[:limit], strict=False):
        with column:
            rule_card(
                rule_id=str(record.get("rule_id", "RULE")),
                title=str(record.get("step", "rule")),
                description=str(record.get("result", "")),
                status="Passed" if record.get("severity") != "WARNING" else "Review",
                severity=str(record.get("severity", "INFO")),
            )


def _require_analysis(df: pd.DataFrame | None, metrics: dict[str, Any] | None = None) -> bool:
    if df is None or metrics is None:
        empty_state(
            "Select a Dataset to Continue",
            "Choose a bundled sample or upload a CSV from the analysis controls. This tab will populate after the pipeline runs.",
        )
        return False
    return True


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


def render_data_profile_tab(
    df: pd.DataFrame | None,
    audit: RuleAuditLog,
    profile: dict[str, Any] | None,
    schema: dict[str, Any] | None,
) -> None:
    """Render the Data Profile detail tab."""

    if df is None or profile is None:
        empty_state("Select a Dataset for Data Profiling", "Data quality, schema mapping, and sample preview appear here after analysis.")
        return

    missing_value, missing_caption = _missing_summary(profile)
    kpi_cols = st.columns(6)
    with kpi_cols[0]:
        metric_card("Total Rows", f"{int(profile.get('row_count', 0)):,}", "Loaded rows", "teal", "#")
    with kpi_cols[1]:
        metric_card("Columns Detected", f"{int(profile.get('column_count', 0)):,}", "Auto-inferred", "blue", "[]")
    with kpi_cols[2]:
        metric_card("Date Range", _date_range(schema), "Standardized dates", "teal", "D")
    with kpi_cols[3]:
        metric_card("Missing Values", missing_value, missing_caption, "red" if missing_value != "0" else "teal", "!")
    with kpi_cols[4]:
        metric_card("Assets Detected", _asset_count(None, schema), "Unique assets", "purple", "A")
    with kpi_cols[5]:
        metric_card("Frequency", str(profile.get("frequency", "unknown")).title(), f"{profile.get('periods_per_year', 'N/A')} periods/year", "teal", "~")

    left, middle, right = st.columns([1.05, 1.24, 1.05])
    with left.container(border=True):
        st.markdown("#### Schema Mapping")
        st.caption("Raw columns mapped to FinSkillOS standard fields")
        mapping_table = pd.DataFrame(schema.get("mapping_table", [])) if schema else pd.DataFrame()
        if mapping_table.empty:
            empty_state("No Mapping Available", "No standard fields were mapped automatically.")
        else:
            st.dataframe(mapping_table, use_container_width=True, hide_index=True)

    with middle.container(border=True):
        st.markdown("#### Data Quality")
        st.caption("Completeness and missing value overview")
        render_missing_values_chart(profile, height=270)
        warnings = pd.DataFrame(profile.get("quality_warnings", []))
        if not warnings.empty:
            st.dataframe(warnings, use_container_width=True, hide_index=True)
        else:
            st.markdown(status_badge("No blocking quality warnings", "default"), unsafe_allow_html=True)

    with right.container(border=True):
        st.markdown("#### Rule Validation")
        st.caption("DATA and SCHEMA rules applied during profiling")
        _rule_cards_for_prefix(audit, {"DATA", "SCHEMA"}, limit=4)

    lower_left, lower_right = st.columns([1.0, 1.0])
    with lower_left.container(border=True):
        st.markdown("#### Sample Data Preview")
        st.caption("First 20 rows from the loaded dataset")
        st.dataframe(df.head(20), use_container_width=True, hide_index=True)
    with lower_right.container(border=True):
        st.markdown("#### Frequency & Coverage")
        st.caption("Rows observed through standardized time")
        render_frequency_coverage_chart(schema, height=300)

    numeric_columns = profile.get("numeric_columns", [])[:3]
    st.markdown("### Numeric Distributions")
    if not numeric_columns:
        empty_state("No Numeric Columns", "Distribution cards require numeric columns.")
    else:
        dist_cols = st.columns(len(numeric_columns))
        for column, col in zip(numeric_columns, dist_cols, strict=False):
            numeric = pd.to_numeric(df[column], errors="coerce").dropna()
            with col.container(border=True):
                st.markdown(f"#### {column}")
                if numeric.empty:
                    empty_state("Unavailable", "No numeric values after parsing.")
                else:
                    st.metric("Mean", f"{numeric.mean():,.4g}")
                    st.metric("Min / Max", f"{numeric.min():,.4g} / {numeric.max():,.4g}")
                    st.caption(f"Non-null observations: {len(numeric):,}")


def render_return_analysis_tab(
    df: pd.DataFrame | None,
    audit: RuleAuditLog,
    metrics: dict[str, Any] | None,
    insights: dict[str, Any] | None,
    profile: dict[str, Any] | None,
) -> None:
    """Render the Return Analysis detail tab."""

    if not _require_analysis(df, metrics):
        return
    summary = metrics.get("summary", {})
    returns = metrics.get("returns")
    clean_returns = returns["return"].dropna() if isinstance(returns, pd.DataFrame) and "return" in returns.columns else pd.Series(dtype=float)
    best_period = clean_returns.max() if not clean_returns.empty else None
    worst_period = clean_returns.min() if not clean_returns.empty else None
    rolling_caption = f"{min(int(profile.get('periods_per_year', 252)) if profile else 63, 252)} period window"

    kpi_cols = st.columns(6)
    with kpi_cols[0]:
        metric_card("Total Return", format_percent(summary.get("total_return")), "Total over selected period", "teal", "TR")
    with kpi_cols[1]:
        metric_card("Annualized Return", format_percent(summary.get("annualized_return")), "Compounded per year", "teal", "AR")
    with kpi_cols[2]:
        metric_card("Best Period", format_percent(best_period), "Max observed return", "teal", "UP")
    with kpi_cols[3]:
        metric_card("Worst Period", format_percent(worst_period), "Min observed return", "red", "DN")
    with kpi_cols[4]:
        metric_card("Sharpe Ratio", format_ratio(summary.get("sharpe_ratio")), "Risk-adjusted return", "purple", "SR")
    with kpi_cols[5]:
        metric_card("Data Sufficiency", str(summary.get("data_sufficiency", "N/A")), "Observation quality", "blue", "DQ")

    top_left, top_right = st.columns([1.38, 1.0])
    with top_left.container(border=True):
        st.markdown("#### Cumulative Return")
        st.caption("Portfolio or asset indexed cumulative return")
        render_cumulative_return_chart(metrics, height=340)
    with top_right.container(border=True):
        st.markdown("#### Return Insights")
        items = [item for item in (insights or {}).get("insights", []) if item.get("category") in {"return", "sharpe", "data_quality"}]
        if not items:
            empty_state("No Return Insights", "No return-specific insight was generated.")
        for item in items[:3]:
            insight_card(
                category=str(item.get("category", "return")),
                fact=str(item.get("fact", "")),
                interpretation=str(item.get("interpretation", "")),
                caution=str(item.get("caution", "")),
                severity=str(item.get("severity", "INFO")),
            )

    bottom_left, bottom_mid, bottom_right = st.columns([1.0, 1.0, 1.0])
    with bottom_left.container(border=True):
        st.markdown("#### Return Distribution")
        st.caption("Period return histogram")
        render_return_distribution(metrics, height=285)
    with bottom_mid.container(border=True):
        st.markdown("#### Rolling Return")
        st.caption(rolling_caption)
        render_rolling_return_chart(metrics, window=min(int(profile.get("periods_per_year", 63)) if profile else 63, 252), height=285)
    with bottom_right.container(border=True):
        st.markdown("#### Period Return Summary")
        asset_metrics = pd.DataFrame(metrics.get("asset_metrics", []))
        if asset_metrics.empty:
            empty_state("Metric Table Unavailable", "Asset-level metrics were not generated for this dataset.")
        else:
            display_cols = [col for col in ["asset", "total_return", "annualized_return", "annualized_volatility", "sharpe_ratio"] if col in asset_metrics.columns]
            st.dataframe(asset_metrics[display_cols], use_container_width=True, hide_index=True)

    st.markdown("### Applied Return Rules")
    _rule_cards_for_prefix(audit, {"METRIC", "VIS"}, limit=5)


def render_risk_analysis_tab(
    df: pd.DataFrame | None,
    audit: RuleAuditLog,
    metrics: dict[str, Any] | None,
    insights: dict[str, Any] | None,
    profile: dict[str, Any] | None,
) -> None:
    """Render the Risk Analysis detail tab."""

    if not _require_analysis(df, metrics):
        return
    summary = metrics.get("summary", {})
    periods = int(profile.get("periods_per_year", 252)) if profile else 252

    kpi_cols = st.columns(6)
    with kpi_cols[0]:
        metric_card("Volatility (Ann.)", format_percent(summary.get("annualized_volatility")), "Standard deviation", "blue", "VOL")
    with kpi_cols[1]:
        metric_card("Max Drawdown", format_percent(summary.get("max_drawdown")), "From peak to trough", "red", "MDD")
    with kpi_cols[2]:
        metric_card("VaR (95%)", format_percent(summary.get("historical_var_95")), "Historical approximation", "purple", "VAR")
    with kpi_cols[3]:
        metric_card("VaR (99%)", format_percent(summary.get("historical_var_99")), "Historical approximation", "purple", "V99")
    with kpi_cols[4]:
        metric_card("Downside Deviation", format_percent(summary.get("downside_deviation")), "Below zero return", "amber", "DD")
    with kpi_cols[5]:
        metric_card("Risk Level", str(summary.get("risk_level", "UNKNOWN")), "Rule-based classification", "amber", "RL")

    top_left, top_mid, top_right = st.columns([1.2, 1.05, 0.82])
    with top_left.container(border=True):
        st.markdown("#### Underwater Drawdown")
        st.caption("Cumulative drawdown through time")
        render_drawdown_chart(metrics, height=330)
    with top_mid.container(border=True):
        st.markdown("#### Rolling Volatility")
        st.caption("Annualized rolling volatility")
        render_rolling_volatility_chart(metrics, periods_per_year=periods, window=min(periods, 252), height=330)
    with top_right.container(border=True):
        st.markdown("#### Risk Commentary")
        items = [item for item in (insights or {}).get("insights", []) if item.get("category") in {"drawdown", "volatility", "data_quality"}]
        if not items:
            empty_state("No Risk Insights", "No risk-specific insight was generated.")
        for item in items[:3]:
            insight_card(
                category=str(item.get("category", "risk")),
                fact=str(item.get("fact", "")),
                interpretation=str(item.get("interpretation", "")),
                caution=str(item.get("caution", "")),
                severity=str(item.get("severity", "INFO")),
            )

    lower_left, lower_mid, lower_right = st.columns([1.0, 1.0, 1.0])
    with lower_left.container(border=True):
        st.markdown("#### VaR / Return Distribution")
        st.caption("Historical return distribution")
        render_return_distribution(metrics, height=285)
    with lower_mid.container(border=True):
        st.markdown("#### Stress Scenario Impact")
        stress = pd.DataFrame(
            [
                {"scenario": "Observed worst period", "impact": format_percent(summary.get("max_drawdown")), "severity": summary.get("drawdown_risk_level", "UNKNOWN")},
                {"scenario": "Volatility regime", "impact": format_percent(summary.get("annualized_volatility")), "severity": summary.get("volatility_risk_level", "UNKNOWN")},
                {"scenario": "Data sufficiency", "impact": str(summary.get("data_sufficiency", "N/A")), "severity": "INFO"},
            ]
        )
        st.dataframe(stress, use_container_width=True, hide_index=True)
    with lower_right.container(border=True):
        st.markdown("#### Data Profile & Assumptions")
        assumptions = pd.DataFrame(
            [
                {"item": "Return Frequency", "value": str(profile.get("frequency", "unknown")).title() if profile else "N/A"},
                {"item": "Periods / Year", "value": periods},
                {"item": "Observation Count", "value": summary.get("observation_count", "N/A")},
                {"item": "Risk-Free Rate", "value": "Applied from user input"},
            ]
        )
        st.dataframe(assumptions, use_container_width=True, hide_index=True)

    st.markdown("### Applied Risk Rules")
    _rule_cards_for_prefix(audit, {"RISK", "METRIC", "SAFE"}, limit=5)


def render_diversification_tab(
    df: pd.DataFrame | None,
    audit: RuleAuditLog,
    schema: dict[str, Any] | None,
    metrics: dict[str, Any] | None,
    insights: dict[str, Any] | None,
) -> None:
    """Render the Diversification detail tab."""

    if not _require_analysis(df, metrics):
        return
    avg_corr = _average_correlation(metrics)
    allocation = metrics.get("allocation", {})
    largest_weight, largest_asset = _largest_weight(schema)
    effective_diversification = "N/A" if avg_corr is None else f"{max(1.0, 1.0 / max(avg_corr, 0.01)):.1f}"

    kpi_cols = st.columns(6)
    with kpi_cols[0]:
        metric_card("Number of Assets", _asset_count(metrics, schema), "Detected assets", "blue", "AS")
    with kpi_cols[1]:
        metric_card("Avg Correlation", "N/A" if avg_corr is None else f"{avg_corr:.2f}", "Pairwise average", "purple", "COR")
    with kpi_cols[2]:
        metric_card("Concentration Risk", str(allocation.get("concentration_level", "N/A")), f"HHI {format_ratio(allocation.get('hhi'))}", "amber", "HHI")
    with kpi_cols[3]:
        metric_card("Effective Diversification", effective_diversification, "Correlation-derived proxy", "teal", "DIV")
    with kpi_cols[4]:
        metric_card("Largest Weight", largest_weight, largest_asset, "red" if largest_weight != "N/A" else "blue", "LW")
    with kpi_cols[5]:
        metric_card("Cash Exposure", _cash_exposure(schema), "Cash-like asset labels", "teal", "CA")

    top_left, top_mid, top_right = st.columns([1.1, 1.0, 0.95])
    with top_left.container(border=True):
        st.markdown("#### Correlation Heatmap")
        st.caption("Pearson correlation across asset returns")
        render_correlation_heatmap(metrics, height=350)
    with top_mid.container(border=True):
        st.markdown("#### Portfolio Allocation")
        st.caption("Weight-based exposure when available")
        render_allocation_chart(schema, height=350)
    with top_right.container(border=True):
        st.markdown("#### Diversification Insights")
        items = [item for item in (insights or {}).get("insights", []) if item.get("category") in {"correlation", "concentration", "data_quality"}]
        if not items:
            empty_state("No Diversification Insights", "Correlation or allocation-specific insight was not generated.")
        for item in items[:3]:
            insight_card(
                category=str(item.get("category", "diversification")),
                fact=str(item.get("fact", "")),
                interpretation=str(item.get("interpretation", "")),
                caution=str(item.get("caution", "")),
                severity=str(item.get("severity", "INFO")),
            )

    bottom_left, bottom_mid, bottom_right = st.columns([1.0, 1.0, 1.0])
    with bottom_left.container(border=True):
        st.markdown("#### Risk Contribution")
        st.caption("Volatility-weighted asset contribution proxy")
        render_risk_contribution_chart(metrics, height=290)
    with bottom_mid.container(border=True):
        st.markdown("#### Risk vs. Return")
        st.caption("Asset comparison")
        render_risk_return_scatter(metrics, height=290)
    with bottom_right.container(border=True):
        st.markdown("#### Concentration Analysis")
        if allocation:
            st.dataframe(pd.DataFrame([allocation]), use_container_width=True, hide_index=True)
        else:
            empty_state("Concentration Unavailable", "Concentration metrics require an allocation weight column.")

    st.markdown("### Rule Traceability & Data Quality")
    _rule_cards_for_prefix(audit, {"VIS", "RISK", "DATA", "INSIGHT"}, limit=5)
