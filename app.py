from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from engine.data_profiler import profile_dataframe
from engine.rule_engine import RuleAuditLog


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
    st.sidebar.header("Analysis Controls")
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
        st.warning("날짜 후보가 감지되지 않았습니다. Allocation/static 분석 모드가 필요할 수 있습니다.")

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


def render_placeholder_sections(
    df: pd.DataFrame | None,
    source_name: str,
    audit: RuleAuditLog,
    profile: dict[str, object] | None,
) -> None:
    st.subheader("Data Profile")
    if df is None:
        st.info("CSV를 업로드하거나 샘플 데이터를 선택하면 데이터 프로파일이 표시됩니다.")
    else:
        st.caption(f"Source: {source_name}")
        if profile is not None:
            render_profile(profile)
        st.dataframe(df.head(20), use_container_width=True)

    st.subheader("Schema Mapping Result")
    st.info("Slice 4에서 자동 표준 스키마 매핑 결과가 연결됩니다.")

    st.subheader("Executive Summary")
    st.info("Slice 5에서 수익률, 변동성, 최대낙폭, Sharpe Ratio, Risk Level 카드가 연결됩니다.")

    st.subheader("Return Analysis")
    st.info("Slice 6에서 가격 추세와 누적수익률 차트가 자동 선택됩니다.")

    st.subheader("Risk Analysis")
    st.info("Slice 5-6에서 변동성, 최대낙폭, drawdown 차트가 연결됩니다.")

    st.subheader("Correlation & Diversification")
    st.info("Slice 5-6에서 다중 자산 상관관계와 risk-return scatter가 연결됩니다.")

    st.subheader("Rule-Based Insights")
    st.info("Slice 8에서 Fact / Interpretation / Caution 구조의 리스크 우선 인사이트가 표시됩니다.")

    st.subheader("Applied Skill Rules")
    st.dataframe(audit.deduplicated_records(), use_container_width=True)

    st.subheader("Export Report")
    st.info("Slice 10에서 HTML 리포트 다운로드가 활성화됩니다.")


def main() -> None:
    st.set_page_config(
        page_title="FinSkillOS",
        page_icon="FS",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    controls = render_sidebar()
    df, source_name = read_uploaded_or_sample(
        controls["uploaded_file"],
        controls["sample_name"],
    )
    mode = str(controls["mode"])
    audit = build_initial_audit_log(mode=mode, source_name=source_name)
    profile = None
    if df is not None:
        profile = profile_dataframe(df)
        audit.extend(profile["applied_rules"])

    st.title("FinSkillOS")
    st.caption("Skill-Governed Investment Analytics Dashboard")

    header_cols = st.columns(3)
    header_cols[0].metric("Analysis Mode", mode)
    header_cols[1].metric("Dataset", source_name)
    header_cols[2].metric("Risk-Free Rate", f"{controls['risk_free_rate']:.4f}")

    if controls["run_analysis"]:
        st.success("Slice 1 골격 검증 완료. 이후 슬라이스에서 실제 분석 엔진이 순차적으로 연결됩니다.")
    elif controls["export_requested"]:
        st.warning("Report export는 Slice 10에서 활성화됩니다.")

    render_placeholder_sections(df=df, source_name=source_name, audit=audit, profile=profile)

    with st.expander("Skills.md 기반 구현 참조", expanded=False):
        st.write("이 앱은 `FinSkillOS_skills` 문서 세트의 Rule ID와 구현 계약을 기준으로 개발됩니다.")
        st.write(f"Skills directory: `{SKILLS_DIR}`")


if __name__ == "__main__":
    main()
