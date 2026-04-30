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


APP_ROOT = Path(__file__).resolve().parent
SAMPLE_DATA_DIR = APP_ROOT / "sample_data"
SKILLS_DIR = APP_ROOT / "FinSkillOS_skills"


def apply_dashboard_style() -> None:
    st.markdown(
        """
        <style>
        :root {
            --fs-ink: #17202a;
            --fs-muted: #5f6f7d;
            --fs-line: #d8e0e7;
            --fs-blue: #245b8f;
            --fs-green: #1f7a5a;
            --fs-red: #a33a3a;
            --fs-amber: #9a6a16;
        }
        .main .block-container {
            padding-top: 1.5rem;
            padding-bottom: 3rem;
            max-width: 1420px;
        }
        h1, h2, h3 {
            color: var(--fs-ink);
            letter-spacing: 0;
        }
        div[data-testid="stMetric"] {
            border: 1px solid var(--fs-line);
            border-radius: 8px;
            padding: 0.75rem 0.85rem;
            background: #fbfcfd;
        }
        div[data-testid="stMetricLabel"] {
            color: var(--fs-muted);
            font-size: 0.78rem;
        }
        .fs-section {
            border-top: 1px solid var(--fs-line);
            padding-top: 1.1rem;
            margin-top: 1.6rem;
        }
        .fs-section-kicker {
            color: var(--fs-blue);
            font-size: 0.78rem;
            font-weight: 700;
            text-transform: uppercase;
        }
        .fs-section-title {
            color: var(--fs-ink);
            font-size: 1.25rem;
            font-weight: 720;
            margin: 0.1rem 0 0.65rem 0;
        }
        .fs-header-line {
            color: var(--fs-muted);
            font-size: 0.92rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def section_header(number: int, title: str, rule_id: str | None = None) -> None:
    label = f"Section {number:02d}"
    if rule_id:
        label = f"{label} · {rule_id}"
    st.markdown(
        f"""
        <div class="fs-section">
          <div class="fs-section-kicker">{label}</div>
          <div class="fs-section-title">{title}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


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
        st.info("No metrics available.")
        return

    summary = metrics.get("summary", {})
    cols = st.columns(6)
    cols[0].metric("Total Return", format_percent(summary.get("total_return")))
    cols[1].metric("Annualized Return", format_percent(summary.get("annualized_return")))
    cols[2].metric("Volatility", format_percent(summary.get("annualized_volatility")))
    cols[3].metric("Maximum Drawdown", format_percent(summary.get("max_drawdown")))
    cols[4].metric("Sharpe Ratio", format_ratio(summary.get("sharpe_ratio")))
    cols[5].metric("Risk Level", str(summary.get("risk_level", "UNKNOWN")))

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
    fig.update_layout(
        template="plotly_white",
        margin=dict(l=20, r=20, t=48, b=24),
        legend_title_text="",
        hovermode="x unified",
    )
    return fig


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

    controls = render_sidebar()
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

    section_header(1, "Header & Upload Panel", "DASH-002")
    st.title("FinSkillOS")
    st.markdown(
        '<div class="fs-header-line">Skill-Governed Investment Analytics Dashboard</div>',
        unsafe_allow_html=True,
    )

    header_cols = st.columns(3)
    header_cols[0].metric("Analysis Mode", mode)
    header_cols[1].metric("Dataset", source_name)
    header_cols[2].metric("Risk-Free Rate", f"{controls['risk_free_rate']:.4f}")

    if controls["run_analysis"]:
        st.success("Analysis refreshed for the current dataset.")
    elif controls["export_requested"]:
        st.warning("Report export is not available yet.")

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
