"""Application shell and controls for FinSkillOS."""

from __future__ import annotations

from html import escape
from typing import Sequence

import streamlit as st


NAV_ITEMS = [
    ("Overview", "[Overview]"),
    ("Data Profile", "[Data]"),
    ("Return Analysis", "[Return]"),
    ("Risk Analysis", "[Risk]"),
    ("Diversification", "[Diversify]"),
    ("Insights", "[Insights]"),
    ("Applied Rules", "[Rules]"),
    ("Reports", "[Reports]"),
]


def _html(value: object) -> str:
    return escape("" if value is None else str(value))


def render_sidebar_nav(active_tab: str, source_name: str, mode: str) -> str:
    """Render the product navigation shell and return the selected tab."""

    st.sidebar.markdown(
        """
        <div class="fs-brand">
          <div class="fs-logo-mark">FS</div>
          <div>
            <div class="fs-brand-title">FinSkill<span>OS</span></div>
            <div class="fs-brand-subtitle">Rule-governed analytics</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    labels = [item[0] for item in NAV_ITEMS]
    display_labels = [f"{icon} {label}" for label, icon in NAV_ITEMS]
    label_by_display = dict(zip(display_labels, labels, strict=True))
    display_by_label = dict(zip(labels, display_labels, strict=True))
    if active_tab not in labels:
        active_tab = "Overview"
    selected_display = st.sidebar.radio(
        "Navigation",
        display_labels,
        index=display_labels.index(display_by_label[active_tab]),
        label_visibility="collapsed",
        key="active_tab_display",
    )

    st.sidebar.markdown(
        f"""
        <div class="fs-sidebar-card">
          <div class="fs-sidebar-kicker">Dataset</div>
          <div class="fs-sidebar-value">{_html(source_name)}</div>
        </div>
        <div class="fs-sidebar-card">
          <div class="fs-sidebar-kicker">Analysis Mode</div>
          <div class="fs-sidebar-value">{_html(mode)}</div>
        </div>
        <div class="fs-sidebar-card">
          <div class="fs-sidebar-kicker">System</div>
          <div class="fs-sidebar-value">All systems operational</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    return label_by_display[selected_display]


def render_topbar(title: str, subtitle: str, active_tab: str, source_name: str, date_range: str) -> None:
    st.markdown(
        f"""
        <div class="fs-topbar">
          <div>
            <h1 class="fs-page-title">{_html(title)}</h1>
            <div class="fs-page-subtitle">{_html(subtitle)}</div>
            <div class="fs-badge-row">
              <span class="fs-badge">Rule-Governed</span>
              <span class="fs-badge fs-badge-muted">Generated from Skills.md</span>
              <span class="fs-badge fs-badge-muted">{_html(active_tab)}</span>
            </div>
          </div>
          <div class="fs-badge-row">
            <span class="fs-badge fs-badge-muted">Dataset · {_html(source_name)}</span>
            <span class="fs-badge fs-badge-muted">Range · {_html(date_range)}</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_topbar_controls(sample_files: Sequence[str]) -> dict[str, object]:
    """Render dataset, mode, rate, and action controls in the main app shell."""

    st.markdown(
        """
        <div class="fs-control-panel">
          <div class="fs-control-caption">Analysis Controls</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    row1 = st.columns([1.25, 1.65, 1.1, 0.85, 0.8], vertical_alignment="bottom")
    uploaded_file = row1[0].file_uploader("CSV Upload", type=["csv"], label_visibility="collapsed")
    sample_name = row1[1].selectbox("Dataset", ["샘플 없음", *sample_files], label_visibility="collapsed")
    mode = row1[2].selectbox(
        "Analysis Mode",
        ["Auto Detect", "Single Asset", "Multi Asset", "Allocation"],
        label_visibility="collapsed",
    )
    risk_free_rate = row1[3].number_input(
        "Risk-Free Rate",
        min_value=-1.0,
        max_value=1.0,
        value=0.0,
        step=0.005,
        format="%.4f",
        label_visibility="collapsed",
    )
    run_analysis = row1[4].button("Run Analysis", type="primary", use_container_width=True)

    caption_cols = st.columns([1.25, 1.65, 1.1, 0.85, 0.8])
    caption_cols[0].caption("Upload CSV")
    caption_cols[1].caption("Sample Dataset")
    caption_cols[2].caption("Mode")
    caption_cols[3].caption("Risk-Free Rate")
    caption_cols[4].caption("Refresh")

    return {
        "uploaded_file": uploaded_file,
        "sample_name": sample_name,
        "mode": mode,
        "risk_free_rate": risk_free_rate,
        "run_analysis": run_analysis,
        "export_requested": False,
    }


def date_range_label(profile: dict[str, object] | None) -> str:
    if not profile:
        return "Awaiting data"
    start = profile.get("start_date")
    end = profile.get("end_date")
    if start and end:
        return f"{start} - {end}"
    return str(profile.get("frequency", "Detected after load")).title()
