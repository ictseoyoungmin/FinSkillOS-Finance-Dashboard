"""Design tokens and theme helpers for FinSkillOS."""

from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st


PLOTLY_COLORS = [
    "#25f2c7",
    "#38a3ff",
    "#f4b740",
    "#a874ff",
    "#ff5b73",
    "#6ef3ff",
    "#7bd88f",
]


def apply_dashboard_style() -> None:
    """Apply the FinSkillOS dark product shell theme."""

    st.markdown(
        """
        <style>
        :root {
            --fs-bg: #020812;
            --fs-bg-soft: #07111f;
            --fs-sidebar: #04101d;
            --fs-panel: rgba(12, 26, 43, 0.88);
            --fs-panel-strong: rgba(14, 32, 52, 0.96);
            --fs-panel-hover: rgba(18, 42, 66, 0.98);
            --fs-line: rgba(129, 166, 202, 0.22);
            --fs-line-strong: rgba(37, 242, 199, 0.48);
            --fs-ink: #eef7ff;
            --fs-muted: #9db0c6;
            --fs-soft: #c7d5e6;
            --fs-teal: #25f2c7;
            --fs-cyan: #38d7ff;
            --fs-blue: #38a3ff;
            --fs-red: #ff5b73;
            --fs-amber: #f4b740;
            --fs-purple: #a874ff;
            --fs-green: #35d990;
            --fs-radius: 8px;
            --fs-shadow: 0 18px 60px rgba(0, 0, 0, 0.34);
            --fs-glow: 0 0 0 1px rgba(37, 242, 199, 0.36), 0 0 28px rgba(37, 242, 199, 0.1);
        }

        html, body, [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(circle at 18% 0%, rgba(25, 117, 154, 0.18), transparent 26rem),
                radial-gradient(circle at 90% 18%, rgba(37, 242, 199, 0.08), transparent 24rem),
                linear-gradient(135deg, #020812 0%, #06111f 48%, #03101b 100%) !important;
            color: var(--fs-ink);
        }

        [data-testid="stHeader"] {
            background: rgba(2, 8, 18, 0.72);
            border-bottom: 1px solid rgba(129, 166, 202, 0.12);
            backdrop-filter: blur(16px);
        }

        [data-testid="stSidebar"] {
            background:
                linear-gradient(180deg, rgba(3, 15, 28, 0.98), rgba(4, 14, 24, 0.98)),
                var(--fs-sidebar);
            border-right: 1px solid var(--fs-line);
        }

        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] label {
            color: var(--fs-soft);
        }

        .main .block-container {
            padding: 1.15rem 1.8rem 3rem 1.8rem;
            max-width: 1640px;
        }

        h1, h2, h3, h4 {
            color: var(--fs-ink);
            letter-spacing: 0;
        }

        div[data-testid="stMetric"] {
            border: 1px solid var(--fs-line);
            border-radius: var(--fs-radius);
            padding: 0.9rem 1rem;
            background: linear-gradient(180deg, rgba(15, 33, 54, 0.92), rgba(8, 20, 36, 0.92));
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.03);
        }

        div[data-testid="stMetricLabel"] {
            color: var(--fs-muted);
            font-size: 0.76rem;
        }

        div[data-testid="stMetricValue"] {
            color: var(--fs-teal);
        }

        div[data-testid="stDataFrame"],
        div[data-testid="stTable"] {
            border-radius: var(--fs-radius);
            overflow: hidden;
        }

        .stButton > button,
        .stDownloadButton > button {
            border-radius: var(--fs-radius);
            border: 1px solid rgba(37, 242, 199, 0.42);
            background: linear-gradient(135deg, rgba(0, 128, 126, 0.86), rgba(20, 182, 169, 0.82));
            color: #f3fffd;
            font-weight: 700;
            min-height: 2.6rem;
            transition: transform 160ms ease, border-color 160ms ease, box-shadow 160ms ease;
        }

        .stButton > button:hover,
        .stDownloadButton > button:hover {
            border-color: var(--fs-teal);
            box-shadow: var(--fs-glow);
            transform: translateY(-1px);
        }

        .stButton > button:focus-visible,
        .stDownloadButton > button:focus-visible,
        button:focus-visible,
        input:focus-visible,
        [role="button"]:focus-visible {
            outline: 2px solid var(--fs-teal) !important;
            outline-offset: 2px;
        }

        [data-baseweb="select"] > div,
        [data-testid="stNumberInput"] input,
        [data-testid="stFileUploader"] section {
            background: rgba(7, 17, 31, 0.95);
            border-color: var(--fs-line);
            border-radius: var(--fs-radius);
            color: var(--fs-ink);
        }

        .fs-brand {
            display: flex;
            align-items: center;
            gap: 0.8rem;
            margin: 0.6rem 0 1.5rem 0;
            padding: 0.6rem 0.2rem;
        }
        .fs-logo-mark {
            width: 42px;
            height: 42px;
            display: grid;
            place-items: center;
            border-radius: 12px;
            color: #021019;
            font-weight: 900;
            background: linear-gradient(135deg, var(--fs-teal), var(--fs-blue));
            box-shadow: 0 0 28px rgba(37, 242, 199, 0.2);
        }
        .fs-brand-title {
            color: var(--fs-ink);
            font-size: 1.45rem;
            font-weight: 830;
            line-height: 1;
        }
        .fs-brand-title span {
            color: var(--fs-blue);
        }
        .fs-brand-subtitle {
            color: var(--fs-muted);
            font-size: 0.74rem;
            margin-top: 0.25rem;
        }

        .fs-nav-item {
            display: flex;
            align-items: center;
            gap: 0.65rem;
            padding: 0.78rem 0.82rem;
            margin: 0.22rem 0;
            border: 1px solid transparent;
            border-radius: var(--fs-radius);
            color: var(--fs-soft);
            background: transparent;
        }
        .fs-nav-item-active {
            color: var(--fs-teal);
            border-color: rgba(37, 242, 199, 0.42);
            background: linear-gradient(90deg, rgba(37, 242, 199, 0.15), rgba(56, 163, 255, 0.06));
            box-shadow: inset 3px 0 0 var(--fs-teal);
        }
        [data-testid="stSidebar"] [role="radiogroup"] {
            display: flex;
            flex-direction: column;
            gap: 0.18rem;
            margin-bottom: 1.2rem;
        }
        [data-testid="stSidebar"] [role="radiogroup"] label {
            border: 1px solid transparent;
            border-radius: var(--fs-radius);
            padding: 0.45rem 0.5rem;
            background: transparent;
            transition: border-color 160ms ease, background 160ms ease, color 160ms ease;
        }
        [data-testid="stSidebar"] [role="radiogroup"] label:hover {
            border-color: rgba(37, 242, 199, 0.22);
            background: rgba(37, 242, 199, 0.06);
        }
        [data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
            border-color: rgba(37, 242, 199, 0.42);
            background: linear-gradient(90deg, rgba(37, 242, 199, 0.15), rgba(56, 163, 255, 0.06));
            box-shadow: inset 3px 0 0 var(--fs-teal);
            color: var(--fs-teal);
        }
        .fs-nav-icon {
            width: 1.35rem;
            color: inherit;
            text-align: center;
        }
        .fs-sidebar-card {
            border: 1px solid var(--fs-line);
            border-radius: var(--fs-radius);
            background: rgba(13, 29, 48, 0.84);
            padding: 0.9rem;
            margin-top: 1rem;
        }
        .fs-sidebar-kicker {
            color: var(--fs-muted);
            font-size: 0.76rem;
        }
        .fs-sidebar-value {
            color: var(--fs-ink);
            font-size: 0.98rem;
            font-weight: 760;
            margin-top: 0.15rem;
        }

        .fs-topbar {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 1rem;
            margin-bottom: 1rem;
        }
        .fs-page-title {
            margin: 0;
            font-size: 1.72rem;
            font-weight: 820;
            line-height: 1.08;
        }
        .fs-page-subtitle {
            color: var(--fs-soft);
            margin-top: 0.35rem;
            font-size: 0.92rem;
        }
        .fs-badge-row {
            display: flex;
            align-items: center;
            gap: 0.45rem;
            flex-wrap: wrap;
            margin-top: 0.45rem;
        }
        .fs-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.32rem;
            border: 1px solid rgba(37, 242, 199, 0.36);
            background: rgba(37, 242, 199, 0.08);
            color: var(--fs-teal);
            border-radius: 999px;
            padding: 0.25rem 0.55rem;
            font-size: 0.75rem;
            font-weight: 730;
        }
        .fs-badge-muted {
            color: var(--fs-soft);
            border-color: var(--fs-line);
            background: rgba(129, 166, 202, 0.08);
        }

        .fs-control-panel {
            border: 1px solid var(--fs-line);
            border-radius: var(--fs-radius);
            background: linear-gradient(180deg, rgba(12, 26, 43, 0.78), rgba(7, 17, 31, 0.86));
            padding: 0.85rem;
            margin: 0.6rem 0 1rem 0;
            box-shadow: var(--fs-shadow);
        }
        .fs-control-caption {
            color: var(--fs-muted);
            font-size: 0.72rem;
            font-weight: 760;
            text-transform: uppercase;
            letter-spacing: 0.03em;
            margin-bottom: 0.35rem;
        }

        .fs-card-grid {
            display: grid;
            gap: 0.72rem;
            grid-template-columns: repeat(auto-fit, minmax(178px, 1fr));
            margin: 0.85rem 0 0.75rem 0;
        }
        .fs-metric-card,
        .fs-panel,
        .fs-rule-card,
        .fs-insight-card,
        .fs-empty-state {
            border: 1px solid var(--fs-line);
            border-radius: var(--fs-radius);
            background: linear-gradient(180deg, rgba(14, 32, 52, 0.92), rgba(7, 17, 31, 0.94));
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.035);
            transition: transform 160ms ease, border-color 160ms ease, background 160ms ease, box-shadow 160ms ease;
        }
        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-color: var(--fs-line) !important;
            border-radius: var(--fs-radius) !important;
            background: linear-gradient(180deg, rgba(14, 32, 52, 0.72), rgba(7, 17, 31, 0.78));
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.025);
        }
        @keyframes fs-card-in {
            from { opacity: 0; transform: translateY(8px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .fs-metric-card:hover,
        .fs-panel:hover,
        .fs-rule-card:hover,
        .fs-insight-card:hover {
            border-color: rgba(37, 242, 199, 0.38);
            background: var(--fs-panel-hover);
            transform: translateY(-1px);
        }
        .fs-metric-card {
            min-height: 112px;
            padding: 1rem;
            display: flex;
            gap: 0.8rem;
            align-items: flex-start;
            animation: fs-card-in 240ms ease both;
        }
        .fs-metric-icon {
            width: 42px;
            height: 42px;
            border-radius: 12px;
            display: grid;
            place-items: center;
            background: rgba(37, 242, 199, 0.1);
            color: var(--fs-teal);
            flex: 0 0 auto;
            font-weight: 900;
        }
        .fs-metric-card[data-tone="blue"] .fs-metric-icon,
        .fs-metric-card[data-tone="blue"] .fs-metric-value { color: var(--fs-blue); }
        .fs-metric-card[data-tone="red"] .fs-metric-icon,
        .fs-metric-card[data-tone="red"] .fs-metric-value { color: var(--fs-red); }
        .fs-metric-card[data-tone="amber"] .fs-metric-icon,
        .fs-metric-card[data-tone="amber"] .fs-metric-value { color: var(--fs-amber); }
        .fs-metric-card[data-tone="purple"] .fs-metric-icon,
        .fs-metric-card[data-tone="purple"] .fs-metric-value { color: var(--fs-purple); }
        .fs-metric-label {
            color: var(--fs-soft);
            font-size: 0.78rem;
            font-weight: 760;
            margin-bottom: 0.35rem;
        }
        .fs-metric-value {
            color: var(--fs-teal);
            font-size: 1.45rem;
            font-weight: 850;
            line-height: 1.05;
        }
        .fs-metric-caption {
            color: var(--fs-muted);
            margin-top: 0.45rem;
            font-size: 0.76rem;
        }
        .fs-panel {
            padding: 1rem;
            margin: 0.75rem 0;
        }
        .fs-panel-header {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 0.7rem;
            margin-bottom: 0.8rem;
        }
        .fs-panel-title {
            color: var(--fs-ink);
            font-size: 1rem;
            font-weight: 800;
        }
        .fs-panel-subtitle {
            color: var(--fs-muted);
            font-size: 0.8rem;
            margin-top: 0.15rem;
        }
        .fs-section {
            border-top: 1px solid var(--fs-line);
            padding-top: 1rem;
            margin-top: 1.4rem;
        }
        .fs-section-kicker {
            color: var(--fs-teal);
            font-size: 0.72rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }
        .fs-section-title {
            color: var(--fs-ink);
            font-size: 1.18rem;
            font-weight: 820;
            margin: 0.12rem 0 0.7rem 0;
        }
        .fs-rule-card {
            padding: 0.9rem;
            min-height: 122px;
        }
        .fs-rule-top {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 0.6rem;
            margin-bottom: 0.55rem;
        }
        .fs-rule-id {
            color: var(--fs-ink);
            font-weight: 850;
        }
        .fs-rule-description,
        .fs-insight-body {
            color: var(--fs-soft);
            font-size: 0.8rem;
        }
        .fs-status {
            display: inline-flex;
            border-radius: 999px;
            padding: 0.18rem 0.5rem;
            font-size: 0.7rem;
            font-weight: 820;
            border: 1px solid rgba(37, 242, 199, 0.38);
            color: var(--fs-teal);
            background: rgba(37, 242, 199, 0.1);
        }
        .fs-status-warning {
            border-color: rgba(244, 183, 64, 0.5);
            color: var(--fs-amber);
            background: rgba(244, 183, 64, 0.1);
        }
        .fs-status-danger {
            border-color: rgba(255, 91, 115, 0.5);
            color: var(--fs-red);
            background: rgba(255, 91, 115, 0.1);
        }
        .fs-insight-card {
            padding: 0.9rem;
            border-left: 3px solid var(--fs-teal);
            margin-bottom: 0.55rem;
        }
        .fs-insight-card[data-category="caution"],
        .fs-insight-card[data-category="data_quality"] {
            border-left-color: var(--fs-amber);
        }
        .fs-insight-card[data-severity="HIGH"],
        .fs-insight-card[data-severity="WARNING"] {
            border-left-color: var(--fs-red);
        }
        .fs-insight-title {
            color: var(--fs-ink);
            font-weight: 820;
            margin-bottom: 0.35rem;
        }
        .fs-empty-state {
            padding: 1.25rem;
            text-align: left;
        }
        .fs-empty-title {
            color: var(--fs-ink);
            font-weight: 830;
            font-size: 1.05rem;
        }
        .fs-empty-message {
            color: var(--fs-muted);
            margin-top: 0.3rem;
            font-size: 0.86rem;
        }

        @media (max-width: 980px) {
            .main .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }
            .fs-topbar {
                display: block;
            }
            .fs-page-title {
                font-size: 1.38rem;
            }
            .fs-card-grid {
                grid-template-columns: repeat(auto-fit, minmax(148px, 1fr));
            }
        }

        @media (prefers-reduced-motion: reduce) {
            *, *::before, *::after {
                animation-duration: 0.001ms !important;
                transition-duration: 0.001ms !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def style_plotly_figure(fig: go.Figure) -> go.Figure:
    """Apply the shared dark chart treatment."""

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(2, 8, 18, 0.18)",
        font=dict(color="#c7d5e6", family="Arial, sans-serif"),
        colorway=PLOTLY_COLORS,
        margin=dict(l=20, r=20, t=44, b=24),
        legend_title_text="",
        hovermode="x unified",
    )
    fig.update_xaxes(gridcolor="rgba(129, 166, 202, 0.14)", zerolinecolor="rgba(129, 166, 202, 0.22)")
    fig.update_yaxes(gridcolor="rgba(129, 166, 202, 0.14)", zerolinecolor="rgba(129, 166, 202, 0.22)")
    return fig
