"""Reusable UI components for FinSkillOS."""

from __future__ import annotations

from contextlib import contextmanager
from html import escape
from typing import Iterator

import streamlit as st


TONE_BY_SEVERITY = {
    "INFO": "default",
    "LOW": "default",
    "MEDIUM": "warning",
    "MODERATE": "warning",
    "WARNING": "warning",
    "HIGH": "danger",
    "VERY HIGH": "danger",
    "ERROR": "danger",
}


def _html(value: object) -> str:
    return escape("" if value is None else str(value))


def status_badge(text: str, tone: str = "default") -> str:
    css_class = "fs-status"
    if tone == "warning":
        css_class += " fs-status-warning"
    elif tone == "danger":
        css_class += " fs-status-danger"
    return f'<span class="{css_class}">{_html(text)}</span>'


def metric_card(label: str, value: str, caption: str, tone: str = "teal", icon: str = "◇") -> None:
    st.markdown(
        f"""
        <div class="fs-metric-card" data-tone="{_html(tone)}">
          <div class="fs-metric-icon">{_html(icon)}</div>
          <div>
            <div class="fs-metric-label">{_html(label)}</div>
            <div class="fs-metric-value">{_html(value)}</div>
            <div class="fs-metric-caption">{_html(caption)}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


@contextmanager
def panel(title: str, subtitle: str | None = None, action: str | None = None) -> Iterator[None]:
    action_html = f"<div>{action}</div>" if action else ""
    subtitle_html = f'<div class="fs-panel-subtitle">{_html(subtitle)}</div>' if subtitle else ""
    st.markdown(
        f"""
        <div class="fs-panel">
          <div class="fs-panel-header">
            <div>
              <div class="fs-panel-title">{_html(title)}</div>
              {subtitle_html}
            </div>
            {action_html}
          </div>
        """,
        unsafe_allow_html=True,
    )
    try:
        yield
    finally:
        st.markdown("</div>", unsafe_allow_html=True)


def section_header(number: int, title: str, rule_id: str | None = None) -> None:
    label = f"Section {number:02d}"
    if rule_id:
        label = f"{label} · {rule_id}"
    st.markdown(
        f"""
        <div class="fs-section">
          <div class="fs-section-kicker">{_html(label)}</div>
          <div class="fs-section-title">{_html(title)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def rule_card(rule_id: str, title: str, description: str, status: str = "Passed", severity: str = "INFO") -> None:
    tone = TONE_BY_SEVERITY.get(str(severity).upper(), "default")
    st.markdown(
        f"""
        <div class="fs-rule-card">
          <div class="fs-rule-top">
            <div>
              <div class="fs-rule-id">{_html(rule_id)}</div>
              <div class="fs-panel-subtitle">{_html(title)}</div>
            </div>
            {status_badge(status, tone)}
          </div>
          <div class="fs-rule-description">{_html(description)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def insight_card(
    category: str,
    fact: str,
    interpretation: str,
    caution: str,
    severity: str = "INFO",
    selected: bool = False,
) -> None:
    selected_class = " fs-insight-selected" if selected else ""
    st.markdown(
        f"""
        <div class="fs-insight-card{selected_class}" data-category="{_html(category)}" data-severity="{_html(severity)}">
          <div class="fs-insight-title">{_html(category).title()} · {_html(severity)}</div>
          <div class="fs-insight-body"><strong>Fact:</strong> {_html(fact)}</div>
          <div class="fs-insight-body"><strong>Interpretation:</strong> {_html(interpretation)}</div>
          <div class="fs-insight-body"><strong>Caution:</strong> {_html(caution)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def empty_state(title: str, message: str) -> None:
    st.markdown(
        f"""
        <div class="fs-empty-state">
          <div class="fs-empty-title">{_html(title)}</div>
          <div class="fs-empty-message">{_html(message)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

