"""Application shell and controls for FinSkillOS."""

from __future__ import annotations

from html import escape
from typing import Sequence

import streamlit as st

from ui.components import panel


NAV_ITEMS = [
    ("Overview", "⌂"),
    ("Data Profile", "◎"),
    ("Return Analysis", "↗"),
    ("Risk Analysis", "◇"),
    ("Diversification", "◌"),
    ("Insights", "✦"),
    ("Applied Rules", "▣"),
    ("Reports", "▤"),
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
        <div class="fs-nav-label">Workspace</div>
        """,
        unsafe_allow_html=True,
    )

    labels = [item[0] for item in NAV_ITEMS]
    display_labels = [f"{icon}  {label}" for label, icon in NAV_ITEMS]
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
        <div class="fs-sidebar-footer">
          <div class="fs-portfolio-card">
            <div class="fs-sidebar-kicker">Dataset</div>
            <div class="fs-sidebar-value">{_html(source_name)}</div>
          </div>
          <div class="fs-portfolio-card">
            <div class="fs-sidebar-kicker">Analysis Mode</div>
            <div class="fs-sidebar-value">{_html(mode)}</div>
          </div>
          <div class="fs-sidebar-card">
            <div class="fs-sidebar-kicker">System</div>
            <div class="fs-sidebar-value"><span class="fs-status-dot"></span>All systems operational</div>
          </div>
          <div class="fs-user-row">
            <div class="fs-user-avatar">FS</div>
            <div class="fs-user-copy">
              <div class="fs-user-name">FinSkillOS Console</div>
              <div class="fs-user-plan">Reference layout synced</div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    return label_by_display[selected_display]


def render_topbar(title: str, subtitle: str, active_tab: str, source_name: str, date_range: str) -> None:
    st.markdown(
        f"""
        <div class="fs-topbar-shell">
          <div class="fs-topbar">
            <div>
              <h1 class="fs-page-title">{_html(title)}</h1>
              <div class="fs-page-subtitle">{_html(subtitle)}</div>
              <div class="fs-badge-row">
                <span class="fs-badge fs-badge-live">Rule-Governed</span>
                <span class="fs-badge fs-badge-muted">Generated from Skills.md</span>
                <span class="fs-badge fs-badge-muted">{_html(active_tab)}</span>
              </div>
            </div>
            <div class="fs-badge-row">
              <span class="fs-badge fs-badge-muted">Dataset · {_html(source_name)}</span>
              <span class="fs-badge fs-badge-muted">Range · {_html(date_range)}</span>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_topbar_controls(sample_files: Sequence[str]) -> dict[str, object]:
    """Render dataset, mode, rate, and action controls in the main app shell."""

    sample_options = list(sample_files)
    if sample_options:
        default_sample = "multi_asset_portfolio.csv"
        default_index = sample_options.index(default_sample) if default_sample in sample_options else 0
    else:
        sample_options = ["샘플 없음"]
        default_index = 0

    with panel("Analysis Controls", None, height=176, body_class="fs-control-shell"):
        row = st.columns([1.5, 0.9, 0.72, 1.35, 0.72, 0.82], vertical_alignment="bottom")
        sample_name = row[0].selectbox(
            "Sample Dataset",
            sample_options,
            index=default_index,
            key="sample_dataset_select",
        )
        mode = row[1].selectbox(
            "Mode",
            ["Auto Detect", "Single Asset", "Multi Asset", "Allocation"],
            key="analysis_mode_select",
        )
        risk_free_rate = row[2].number_input(
            "Risk-Free Rate",
            min_value=-1.0,
            max_value=1.0,
            value=0.0,
            step=0.005,
            format="%.4f",
            key="risk_free_rate_input",
        )
        with row[3]:
            uploaded_file = st.file_uploader(
                "CSV Upload",
                type=["csv"],
                accept_multiple_files=False,
                key="csv_upload",
            )
            if uploaded_file is not None:
                st.caption(uploaded_file.name)
        theme = row[4].selectbox(
            "Theme",
            ["Dark", "Light"],
            index=0,
            key="dashboard_theme",
        )
        run_analysis = row[5].button("Apply Settings", type="primary", use_container_width=True)

    return {
        "uploaded_file": uploaded_file,
        "sample_name": sample_name,
        "mode": mode,
        "risk_free_rate": risk_free_rate,
        "theme": theme,
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
