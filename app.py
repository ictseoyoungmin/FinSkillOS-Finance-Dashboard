from __future__ import annotations

from pathlib import Path
import json

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from engine.chart_planner import plan_charts
from engine.data_profiler import profile_dataframe
from engine.insight_engine import generate_insights
from engine.metrics import compute_metrics, format_percent, format_ratio
from engine.report_builder import build_html_report
from engine.rule_engine import RuleAuditLog
from engine.schema_mapper import infer_schema
from ui.components import empty_state, metric_card, section_header
from ui.layout import date_range_label, render_sidebar_nav, render_topbar, render_topbar_controls
from ui.tabs import (
    render_applied_rules_tab,
    render_data_profile_tab,
    render_diversification_tab,
    render_insights_tab,
    render_overview_dashboard,
    render_reports_tab,
    render_return_analysis_tab,
    render_risk_analysis_tab,
)
from ui.theme import apply_dashboard_style, style_plotly_figure


APP_ROOT = Path(__file__).resolve().parent
SAMPLE_DATA_DIR = APP_ROOT / "sample_data"
SKILLS_DIR = APP_ROOT / "FinSkillOS_skills"


def list_sample_files() -> list[str]:
    if not SAMPLE_DATA_DIR.exists():
        return []
    return sorted(path.name for path in SAMPLE_DATA_DIR.glob("*.csv"))


def read_uploaded_or_sample(uploaded_file, sample_name: str | None) -> tuple[pd.DataFrame | None, str]:
    if uploaded_file is not None:
        return pd.read_csv(uploaded_file), uploaded_file.name

    if sample_name and sample_name != "샘플 없음":
        sample_path = SAMPLE_DATA_DIR / sample_name
        if sample_path.exists():
            return pd.read_csv(sample_path), sample_name

    return None, "데이터 미선택"


def build_initial_audit_log(mode: str, source_name: str) -> RuleAuditLog:
    audit = RuleAuditLog()
    audit.add(
        rule_id="AUTO-STRUCT-001",
        step="project_skeleton",
        condition="FinSkillOS MVP requires the documented app and engine layout.",
        action="Initialized Streamlit app, engine package, sample_data, and reports folders.",
        result="Slice 1 project skeleton is active.",
    )
    audit.add(
        rule_id="DASH-001",
        step="dashboard_layout",
        condition="Default dashboard section order is required.",
        action="Rendered the initial sections in the Skill-defined sequence.",
        result="Header, Data Profile, Schema Mapping, Summary, Analysis, Insights, Rules, and Export placeholders are visible.",
    )
    audit.add(
        rule_id="DASH-002",
        step="dashboard_header",
        condition="Header must include service name, description, mode, and dataset name.",
        action="Displayed FinSkillOS header metadata.",
        result=f"Mode={mode}; Dataset={source_name}.",
    )
    audit.add(
        rule_id="DASH-003",
        step="sidebar_controls",
        condition="Sidebar must provide upload, sample selection, analysis mode, risk-free rate, run, and export controls.",
        action="Rendered required sidebar controls.",
        result="All required sidebar controls are present.",
    )
    audit.add(
        rule_id="AUTO-APP-002",
        step="rule_trace_visibility",
        condition="Applied Skill Rules must be visible in the web UI.",
        action="Rendered an Applied Skill Rules table.",
        result="Rule audit records are displayed at the bottom of the dashboard.",
    )
    return audit


def render_sidebar() -> dict[str, object]:
    st.sidebar.header("FinSkillOS Controls")
    uploaded_file = st.sidebar.file_uploader("CSV Upload", type=["csv"])
    sample_files = ["샘플 없음"] + list_sample_files()
    sample_name = st.sidebar.selectbox("Sample Dataset", sample_files)
    mode = st.sidebar.selectbox(
        "Analysis Mode",
        ["Auto Detect", "Single Asset", "Multi Asset", "Allocation"],
    )
    risk_free_rate = st.sidebar.number_input(
        "Risk-Free Rate",
        min_value=-1.0,
        max_value=1.0,
        value=0.0,
        step=0.005,
        format="%.4f",
    )
    run_analysis = st.sidebar.button("Run Analysis", type="primary")
    export_requested = st.sidebar.button("Export Report")
    return {
        "uploaded_file": uploaded_file,
        "sample_name": sample_name,
        "mode": mode,
        "risk_free_rate": risk_free_rate,
        "run_analysis": run_analysis,
        "export_requested": export_requested,
    }


def render_profile(profile: dict[str, object]) -> None:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Rows", f"{profile['row_count']:,}")
    col2.metric("Columns", f"{profile['column_count']:,}")
    col3.metric("Frequency", str(profile["frequency"]).title())
    col4.metric("Periods / Year", str(profile["periods_per_year"]))

    candidates = profile.get("date_candidates", [])
    if candidates:
        st.write("Date Candidates")
        st.dataframe(candidates, use_container_width=True)
    else:
        st.warning("No date candidate detected. Static allocation analysis remains available.")

    column_cols = st.columns(2)
    column_cols[0].write("Numeric Columns")
    column_cols[0].dataframe(pd.DataFrame({"column": profile["numeric_columns"]}), use_container_width=True)
    column_cols[1].write("Categorical Columns")
    column_cols[1].dataframe(pd.DataFrame({"column": profile["categorical_columns"]}), use_container_width=True)

    missing_df = pd.DataFrame(
        [
            {"column": column, "missing_rate": rate}
            for column, rate in profile["missing_rates"].items()
        ]
    )
    st.write("Missing Rates")
    st.dataframe(missing_df, use_container_width=True)

    warnings = profile.get("quality_warnings", [])
    if warnings:
        st.write("Quality Warnings")
        st.dataframe(warnings, use_container_width=True)


def render_schema_mapping(schema: dict[str, object] | None) -> None:
    if schema is None:
        st.info("No dataset selected.")
        return

    st.metric("Detected Schema", str(schema["schema_type"]))
    mapping_table = schema.get("mapping_table", [])
    if mapping_table:
        st.dataframe(mapping_table, use_container_width=True)
    else:
        st.warning("No standard fields were mapped automatically.")

    standardized_df = schema.get("standardized_df")
    if isinstance(standardized_df, pd.DataFrame) and not standardized_df.empty:
        st.write("Standardized Data Preview")
        st.dataframe(standardized_df.head(20), use_container_width=True)


def render_executive_summary(metrics: dict[str, object] | None) -> None:
    if metrics is None:
        empty_state("No Metrics Available", "Select a sample dataset or upload a CSV to generate the KPI strip.")
        return

    summary = metrics.get("summary", {})
    cols = st.columns(6)
    with cols[0]:
        metric_card("Total Return", format_percent(summary.get("total_return")), "Total over selected period", "teal", "↗")
    with cols[1]:
        metric_card("Annualized Return", format_percent(summary.get("annualized_return")), "Compounded per year", "teal", "⟳")
    with cols[2]:
        metric_card("Volatility (Ann.)", format_percent(summary.get("annualized_volatility")), "Standard deviation", "blue", "~")
    with cols[3]:
        metric_card("Max Drawdown", format_percent(summary.get("max_drawdown")), "From peak to trough", "red", "↘")
    with cols[4]:
        metric_card("Sharpe Ratio", format_ratio(summary.get("sharpe_ratio")), "Risk-adjusted return", "purple", "Σ")
    with cols[5]:
        metric_card("Risk Level", str(summary.get("risk_level", "UNKNOWN")), "Balanced risk profile", "amber", "◇")

    details = {
        "Drawdown Risk": summary.get("drawdown_risk_level", "UNKNOWN"),
        "Volatility Risk": summary.get("volatility_risk_level", "UNKNOWN"),
        "Sharpe Quality": summary.get("sharpe_quality", "N/A"),
        "Data Sufficiency": summary.get("data_sufficiency", "N/A"),
    }
    st.dataframe(pd.DataFrame([details]), use_container_width=True)

    allocation = metrics.get("allocation", {})
    if allocation:
        st.write("Allocation Concentration")
        st.dataframe(pd.DataFrame([allocation]), use_container_width=True)

    missing_reasons = summary.get("missing_reasons", [])
    if missing_reasons:
        st.write("Metric Notes")
        st.dataframe(pd.DataFrame({"reason": missing_reasons}), use_container_width=True)


def render_insights(insights: dict[str, object] | None) -> None:
    if insights is None:
        st.info("No insights available.")
        return
    items = insights.get("insights", [])
    if not items:
        st.info("No evidence-linked insights were generated.")
        return

    for item in items:
        severity = item.get("severity", "INFO")
        title = f"{item.get('id', '')} · {item.get('category', '').title()} · {severity}"
        with st.container(border=True):
            st.markdown(f"**{title}**")
            st.write(f"Fact: {item.get('fact')}")
            st.write(f"Interpretation: {item.get('interpretation')}")
            st.write(f"Caution: {item.get('caution')}")
            st.caption(f"Evidence: {item.get('evidence')}")

    blocked_terms = insights.get("blocked_terms", [])
    if blocked_terms:
        st.warning(f"Safety rewrite applied for prohibited term(s): {', '.join(blocked_terms)}")


def render_applied_rules(audit: RuleAuditLog) -> None:
    records = audit.deduplicated_records()
    summary = audit.summary_by_prefix()
    coverage = audit.has_prefixes(["DATA", "METRIC", "VIS", "INSIGHT", "SAFE"])

    cols = st.columns(4)
    cols[0].metric("Applied Rules", len(records))
    cols[1].metric("Rule Categories", len(summary))
    cols[2].metric("Warnings", sum(1 for row in records if row.get("severity") == "WARNING"))
    cols[3].metric("Required Coverage", f"{sum(coverage.values())}/{len(coverage)}")

    st.write("Rule Category Summary")
    st.dataframe(summary, use_container_width=True)

    coverage_df = pd.DataFrame(
        [{"prefix": prefix, "present": present} for prefix, present in coverage.items()]
    )
    st.write("Required Rule Coverage")
    st.dataframe(coverage_df, use_container_width=True)

    st.write("Rule Audit Detail")
    st.dataframe(records, use_container_width=True)

    csv_data = pd.DataFrame(records).to_csv(index=False).encode("utf-8-sig")
    json_data = json.dumps(records, ensure_ascii=False, indent=2).encode("utf-8")
    download_cols = st.columns(2)
    download_cols[0].download_button(
        "Download Rules CSV",
        data=csv_data,
        file_name="finskillos_applied_rules.csv",
        mime="text/csv",
    )
    download_cols[1].download_button(
        "Download Rules JSON",
        data=json_data,
        file_name="finskillos_applied_rules.json",
        mime="application/json",
    )


def render_report_export(analysis_result: dict[str, object] | None) -> None:
    if analysis_result is None:
        st.info("No analysis result available for report export.")
        return
    html_report = build_html_report(analysis_result)
    st.download_button(
        "Download HTML Report",
        data=html_report.encode("utf-8"),
        file_name="finskillos_analysis_report.html",
        mime="text/html",
    )
    st.caption("The report includes dataset summary, schema mapping, metrics, risk insights, rule audit log, and disclaimer.")


def render_metric_tables(metrics: dict[str, object] | None) -> None:
    if metrics is None:
        return
    asset_metrics = metrics.get("asset_metrics", [])
    if asset_metrics:
        st.write("Asset Metric Table")
        st.dataframe(asset_metrics, use_container_width=True)

    corr = metrics.get("correlation_matrix")
    if isinstance(corr, pd.DataFrame) and not corr.empty:
        st.write("Correlation Matrix")
        st.dataframe(corr, use_container_width=True)


def add_chart_rules(audit: RuleAuditLog, chart_plan: list[dict[str, object]]) -> None:
    for chart in chart_plan:
        audit.add(
            rule_id=str(chart["rule_id"]),
            step="chart_planning",
            condition=str(chart["reason"]),
            action=f"Plan chart `{chart['chart_id']}`.",
            result="Selected for rendering." if chart.get("available") else "Not rendered; prerequisites are unavailable.",
        )


def _plotly_layout(fig: go.Figure) -> go.Figure:
    return style_plotly_figure(fig)


def render_chart_plan(chart_plan: list[dict[str, object]], schema: dict[str, object] | None, metrics: dict[str, object] | None, section: str) -> None:
    if schema is None or metrics is None:
        st.info("No chart plan available.")
        return

    section_charts = [chart for chart in chart_plan if chart.get("section") == section]
    if not section_charts:
        st.info("이 섹션에 선택된 차트가 없습니다.")
        return

    std_df = schema.get("standardized_df")
    for chart in section_charts:
        st.caption(f"{chart['title']} | Rule: {chart['rule_id']} | {chart['reason']}")
        if not chart.get("available"):
            st.warning(f"{chart['title']} was not generated because prerequisites are unavailable.")
            continue

        chart_id = chart["chart_id"]
        if chart_id == "price_trend" and isinstance(std_df, pd.DataFrame):
            fig = px.line(std_df, x="date", y="price", color="asset" if "asset" in std_df.columns else None)
            st.plotly_chart(_plotly_layout(fig), use_container_width=True)

        elif chart_id in {"cumulative_return", "indexed_cumulative_return"}:
            cumulative = metrics.get("cumulative_returns")
            if isinstance(cumulative, pd.DataFrame) and not cumulative.empty:
                plot_df = cumulative.copy()
                plot_df["indexed_value"] = 100.0 * (1.0 + plot_df["cumulative_return"])
                fig = px.line(plot_df, x="date", y="indexed_value", color="asset")
                st.plotly_chart(_plotly_layout(fig), use_container_width=True)

        elif chart_id in {"drawdown", "drawdown_comparison"}:
            drawdowns = metrics.get("drawdowns")
            if isinstance(drawdowns, pd.DataFrame) and not drawdowns.empty:
                fig = px.area(drawdowns, x="date", y="drawdown", color="asset")
                fig.update_yaxes(tickformat=".0%")
                st.plotly_chart(_plotly_layout(fig), use_container_width=True)

        elif chart_id == "metric_summary_table":
            render_metric_tables(metrics)

        elif chart_id == "risk_return_scatter":
            asset_metrics = pd.DataFrame(metrics.get("asset_metrics", []))
            required = {"annualized_volatility", "annualized_return", "asset"}
            if not asset_metrics.empty and required.issubset(asset_metrics.columns):
                asset_metrics = asset_metrics.dropna(subset=["annualized_volatility", "annualized_return"])
                fig = px.scatter(
                    asset_metrics,
                    x="annualized_volatility",
                    y="annualized_return",
                    text="asset",
                    size=asset_metrics["max_drawdown"].abs() if "max_drawdown" in asset_metrics.columns else None,
                )
                fig.update_traces(textposition="top center")
                fig.update_xaxes(tickformat=".0%")
                fig.update_yaxes(tickformat=".0%")
                st.plotly_chart(_plotly_layout(fig), use_container_width=True)

        elif chart_id == "correlation_heatmap":
            corr = metrics.get("correlation_matrix")
            if isinstance(corr, pd.DataFrame) and not corr.empty:
                fig = px.imshow(
                    corr,
                    text_auto=".2f",
                    zmin=-1,
                    zmax=1,
                    color_continuous_scale="RdBu_r",
                    aspect="auto",
                )
                st.plotly_chart(_plotly_layout(fig), use_container_width=True)

        elif chart_id == "allocation_chart" and isinstance(std_df, pd.DataFrame):
            fig = px.pie(std_df, names="asset", values="weight", hole=0.48)
            st.plotly_chart(_plotly_layout(fig), use_container_width=True)

        elif chart_id == "concentration_table":
            allocation = metrics.get("allocation", {})
            if allocation:
                st.dataframe(pd.DataFrame([allocation]), use_container_width=True)

        elif chart_id == "sector_exposure" and isinstance(std_df, pd.DataFrame):
            if {"sector", "weight"}.issubset(std_df.columns):
                sector_df = std_df.groupby("sector", as_index=False)["weight"].sum()
                fig = px.bar(sector_df, x="sector", y="weight")
                fig.update_yaxes(tickformat=".0%")
                st.plotly_chart(_plotly_layout(fig), use_container_width=True)


def render_dashboard_sections(
    df: pd.DataFrame | None,
    source_name: str,
    audit: RuleAuditLog,
    profile: dict[str, object] | None,
    schema: dict[str, object] | None,
    metrics: dict[str, object] | None,
    chart_plan: list[dict[str, object]],
    insights: dict[str, object] | None,
    analysis_result: dict[str, object] | None,
) -> None:
    section_header(2, "Data Profile", "DASH-001")
    if df is None:
        st.info("No dataset selected.")
    else:
        st.caption(f"Source: {source_name}")
        if profile is not None:
            render_profile(profile)
        with st.expander("Raw Data Preview", expanded=False):
            st.dataframe(df.head(20), use_container_width=True)

    section_header(3, "Schema Mapping Result", "DASH-001")
    render_schema_mapping(schema)

    section_header(4, "Executive Summary", "DASH-SUMMARY-001")
    render_executive_summary(metrics)

    section_header(5, "Return Analysis", "VIS-PRIORITY")
    render_chart_plan(chart_plan, schema, metrics, "return_analysis")

    section_header(6, "Risk Analysis", "VIS-003")
    render_chart_plan(chart_plan, schema, metrics, "risk_analysis")

    section_header(7, "Correlation & Diversification", "VIS-004")
    render_chart_plan(chart_plan, schema, metrics, "correlation_diversification")

    section_header(8, "Rule-Based Insights", "INSIGHT-001")
    render_insights(insights)

    section_header(9, "Applied Skill Rules", "AUTO-APP-002")
    render_applied_rules(audit)

    section_header(10, "Export Report", "REPORT-001")
    render_report_export(analysis_result)


def main() -> None:
    st.set_page_config(
        page_title="FinSkillOS",
        page_icon="FS",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    apply_dashboard_style()

    header_slot = st.container()
    controls_slot = st.container()
    with controls_slot:
        controls = render_topbar_controls(list_sample_files())
    df, source_name = read_uploaded_or_sample(
        controls["uploaded_file"],
        controls["sample_name"],
    )
    mode = str(controls["mode"])
    audit = build_initial_audit_log(mode=mode, source_name=source_name)
    profile = None
    schema = None
    metrics = None
    insights = None
    analysis_result = None
    chart_plan: list[dict[str, object]] = []
    if df is not None:
        profile = profile_dataframe(df)
        audit.extend(profile["applied_rules"])
        schema = infer_schema(df, profile, mode=mode)
        audit.extend(schema["applied_rules"])
        metrics = compute_metrics(
            schema["standardized_df"],
            schema,
            risk_free_rate=float(controls["risk_free_rate"]),
            profile=profile,
        )
        audit.extend(metrics["applied_rules"])
        chart_plan = plan_charts(schema, metrics)
        add_chart_rules(audit, chart_plan)
        insights = generate_insights(metrics, profile, schema)
        audit.extend(insights["applied_rules"])
        analysis_result = {
            "source_name": source_name,
            "mode": mode,
            "profile": profile,
            "schema": schema,
            "metrics": metrics,
            "chart_plan": chart_plan,
            "insights": insights,
            "applied_rules": audit.deduplicated_records(),
        }

    active_tab = render_sidebar_nav(
        active_tab="Overview",
        source_name=source_name,
        mode=mode,
    )
    with header_slot:
        render_topbar(
            title="Investment Analytics Dashboard" if active_tab == "Overview" else active_tab,
            subtitle="Skill-Governed Investment Analytics Dashboard",
            active_tab=active_tab,
            source_name=source_name,
            date_range=date_range_label(profile),
        )

    if controls["run_analysis"]:
        st.success("Analysis refreshed for the current dataset.")
    elif controls["export_requested"]:
        st.warning("Report export is not available yet.")

    if active_tab == "Overview":
        render_overview_dashboard(
            df=df,
            source_name=source_name,
            audit=audit,
            profile=profile,
            schema=schema,
            metrics=metrics,
            insights=insights,
            analysis_result=analysis_result,
        )
    elif active_tab == "Data Profile":
        render_data_profile_tab(
            df=df,
            audit=audit,
            profile=profile,
            schema=schema,
        )
    elif active_tab == "Return Analysis":
        render_return_analysis_tab(
            df=df,
            audit=audit,
            metrics=metrics,
            insights=insights,
            profile=profile,
        )
    elif active_tab == "Risk Analysis":
        render_risk_analysis_tab(
            df=df,
            audit=audit,
            metrics=metrics,
            insights=insights,
            profile=profile,
        )
    elif active_tab == "Diversification":
        render_diversification_tab(
            df=df,
            audit=audit,
            schema=schema,
            metrics=metrics,
            insights=insights,
        )
    elif active_tab == "Insights":
        render_insights_tab(
            df=df,
            source_name=source_name,
            audit=audit,
            schema=schema,
            metrics=metrics,
            insights=insights,
        )
    elif active_tab == "Applied Rules":
        render_applied_rules_tab(
            df=df,
            audit=audit,
        )
    elif active_tab == "Reports":
        render_reports_tab(
            df=df,
            source_name=source_name,
            audit=audit,
            profile=profile,
            schema=schema,
            metrics=metrics,
            analysis_result=analysis_result,
        )
    else:
        section_header(1, "Header & Upload Panel", "DASH-002")
        header_cols = st.columns(3)
        with header_cols[0]:
            metric_card("Analysis Mode", mode, "Selected execution profile", "blue", "▤")
        with header_cols[1]:
            metric_card("Dataset", source_name, "Uploaded file or sample", "teal", "▦")
        with header_cols[2]:
            metric_card("Risk-Free Rate", f"{controls['risk_free_rate']:.4f}", "Sharpe Ratio assumption", "amber", "%")

        render_dashboard_sections(
            df=df,
            source_name=source_name,
            audit=audit,
            profile=profile,
            schema=schema,
            metrics=metrics,
            chart_plan=chart_plan,
            insights=insights,
            analysis_result=analysis_result,
        )

    with st.expander("Skills.md 기반 구현 참조", expanded=False):
        st.write("이 앱은 `FinSkillOS_skills` 문서 세트의 Rule ID와 구현 계약을 기준으로 개발됩니다.")
        st.write(f"Skills directory: `{SKILLS_DIR}`")


if __name__ == "__main__":
    main()
