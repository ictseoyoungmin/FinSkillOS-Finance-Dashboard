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


def apply_dashboard_style(theme: str = "Dark") -> None:
    """Apply the FinSkillOS product shell theme."""

    st.markdown(
        """
        <style>
        *, *::before, *::after {
            box-sizing: border-box;
        }

        :root {
            --fs-bg: #0b0f19;
            --fs-bg-soft: #111827;
            --fs-sidebar: #111827;
            --fs-panel: rgba(21, 30, 45, 0.92);
            --fs-panel-strong: rgba(26, 37, 64, 0.96);
            --fs-panel-hover: rgba(31, 45, 69, 0.98);
            --fs-line: rgba(255, 255, 255, 0.08);
            --fs-line-strong: rgba(0, 212, 160, 0.44);
            --fs-ink: #e8edf5;
            --fs-muted: #7a8ba0;
            --fs-soft: #b8c4d4;
            --fs-teal: #00d4a0;
            --fs-cyan: #35d6ff;
            --fs-blue: #4f91e8;
            --fs-red: #f05151;
            --fs-amber: #f5a623;
            --fs-purple: #a874ff;
            --fs-green: #35d990;
            --fs-radius: 8px;
            --fs-shadow: 0 10px 34px rgba(0, 0, 0, 0.28);
            --fs-glow: 0 0 0 1px rgba(0, 212, 160, 0.3), 0 0 22px rgba(0, 212, 160, 0.09);
            --fs-ease: cubic-bezier(0.22, 1, 0.36, 1);
            --fs-fast: 140ms;
            --fs-medium: 240ms;
            --fs-sidebar-width: 240px;
            --fs-gap-xs: 4px;
            --fs-gap-sm: 8px;
            --fs-gap-md: 14px;
            --fs-gap-lg: 18px;
            --fs-gap-xl: 24px;
        }

        html, body, [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(circle at 18% 0%, rgba(0, 212, 160, 0.08), transparent 25rem),
                radial-gradient(circle at 92% 20%, rgba(79, 145, 232, 0.1), transparent 24rem),
                linear-gradient(135deg, #0b0f19 0%, #08111f 52%, #0b0f19 100%) !important;
            color: var(--fs-ink);
            font-family: "DM Sans", "Aptos", "Segoe UI", sans-serif;
        }

        [data-testid="stHeader"] {
            height: 0;
            background: transparent;
            border-bottom: 0;
            backdrop-filter: none;
        }

        [data-testid="stToolbar"],
        [data-testid="stDecoration"],
        [data-testid="stStatusWidget"] {
            display: none !important;
        }

        [data-testid="stAppViewContainer"] {
            display: flex;
        }

        [data-testid="stSidebar"] {
            background:
                linear-gradient(180deg, rgba(17, 24, 39, 0.98), rgba(11, 15, 25, 0.98)),
                var(--fs-sidebar);
            border-right: 1px solid var(--fs-line);
            width: var(--fs-sidebar-width) !important;
            min-width: var(--fs-sidebar-width) !important;
            max-width: var(--fs-sidebar-width) !important;
        }

        [data-testid="stSidebar"] > div:first-child {
            width: var(--fs-sidebar-width);
            padding: 20px 0 16px 0;
            overflow-x: hidden;
        }
        [data-testid="stSidebarContent"] {
            width: var(--fs-sidebar-width) !important;
            padding: 20px 0 16px 0 !important;
            overflow-x: hidden;
        }

        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] label {
            color: var(--fs-soft);
        }

        [data-testid="stMain"],
        section.main {
            min-width: 0;
            padding-left: 0 !important;
            padding-right: 0 !important;
        }

        [data-testid="stMainBlockContainer"],
        .main .block-container,
        section.main > div.block-container {
            padding: 18px 20px 28px 20px !important;
            max-width: none;
            width: 100%;
            animation: fs-page-in var(--fs-medium) var(--fs-ease) both;
        }
        [data-testid="stMainBlockContainer"] [data-testid="stVerticalBlock"],
        .main .block-container [data-testid="stVerticalBlock"] {
            gap: var(--fs-gap-md);
        }
        [data-testid="stMainBlockContainer"] [data-testid="stHorizontalBlock"],
        .main .block-container [data-testid="stHorizontalBlock"] {
            gap: var(--fs-gap-md);
            margin: 0;
            align-items: stretch;
        }
        [data-testid="column"] > [data-testid="stVerticalBlock"] {
            gap: var(--fs-gap-sm);
            height: 100%;
        }
        [data-testid="column"] {
            display: flex;
        }
        [data-testid="column"] > div {
            width: 100%;
        }
        [data-testid="stMainBlockContainer"] div[data-testid="stElementContainer"],
        .main .block-container div[data-testid="stElementContainer"] {
            margin: 0;
        }

        h1, h2, h3, h4 {
            color: var(--fs-ink);
            letter-spacing: 0;
        }

        div[data-testid="stMetric"] {
            border: 1px solid var(--fs-line);
            border-radius: var(--fs-radius);
            padding: 0.72rem 0.82rem;
            background: linear-gradient(180deg, rgba(21, 30, 45, 0.92), rgba(13, 21, 35, 0.94));
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.03);
        }

        div[data-testid="stMetricLabel"] {
            color: var(--fs-muted);
            font-size: 0.68rem;
        }

        div[data-testid="stMetricValue"] {
            color: var(--fs-teal);
        }

        div[data-testid="stDataFrame"],
        div[data-testid="stTable"] {
            border-radius: var(--fs-radius);
            overflow: auto;
        }
        div[data-testid="stDataFrame"] {
            border: 1px solid var(--fs-line);
            background: rgba(11, 18, 31, 0.72);
            max-width: 100%;
        }
        div[data-testid="stMarkdownContainer"] h3 {
            margin: 0 0 var(--fs-gap-xs) 0;
            line-height: 1.12;
            font-size: 1.38rem;
        }
        div[data-testid="stMarkdownContainer"] h4 {
            margin: 0 0 2px 0;
            line-height: 1.14;
            font-size: 1rem;
        }
        div[data-testid="stMarkdownContainer"] h5 {
            margin: var(--fs-gap-sm) 0 var(--fs-gap-xs) 0;
            line-height: 1.12;
            font-size: 0.86rem;
        }
        div[data-testid="stMarkdownContainer"] p {
            margin: 0;
        }
        div[data-testid="stPlotlyChart"] {
            min-height: 235px;
            background: transparent !important;
            border: 0 !important;
        }
        div[data-testid="stPlotlyChart"] .modebar {
            display: none !important;
        }
        div[data-testid="stPlotlyChart"] .js-plotly-plot,
        div[data-testid="stPlotlyChart"] .plot-container,
        div[data-testid="stPlotlyChart"] .svg-container {
            background: transparent !important;
        }

        .stButton > button,
        .stDownloadButton > button,
        [data-testid="stPopover"] > button {
            border-radius: var(--fs-radius);
            border: 1px solid rgba(37, 242, 199, 0.42);
            background: linear-gradient(135deg, rgba(0, 128, 126, 0.86), rgba(20, 182, 169, 0.82));
            color: #f3fffd;
            font-weight: 700;
            min-height: 2.25rem;
            font-size: 0.78rem;
            transition: transform var(--fs-fast) var(--fs-ease), border-color var(--fs-fast) var(--fs-ease), box-shadow var(--fs-fast) var(--fs-ease), filter var(--fs-fast) var(--fs-ease);
        }

        .stButton > button:hover,
        .stDownloadButton > button:hover,
        [data-testid="stPopover"] > button:hover {
            border-color: var(--fs-teal);
            box-shadow: var(--fs-glow);
            transform: translateY(-1px);
            filter: saturate(1.08);
        }

        .stButton > button:disabled,
        .stDownloadButton > button:disabled {
            opacity: 0.48;
            transform: none;
            box-shadow: none;
            cursor: not-allowed;
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
        [data-testid="stTextInput"] input,
        [data-testid="stTextArea"] textarea,
        [data-testid="stNumberInput"] input,
        [data-testid="stFileUploader"] section {
            background: rgba(7, 17, 31, 0.95);
            border-color: var(--fs-line);
            border-radius: var(--fs-radius);
            color: var(--fs-ink);
            min-height: 2.42rem;
            transition: border-color var(--fs-fast) var(--fs-ease), box-shadow var(--fs-fast) var(--fs-ease);
        }
        [data-testid="stWidgetLabel"] {
            min-height: 1rem;
            margin-bottom: var(--fs-gap-xs);
        }
        [data-testid="stWidgetLabel"] p {
            color: var(--fs-muted);
            font-size: 0.66rem;
            font-weight: 760;
            line-height: 1;
            letter-spacing: 0.01em;
            white-space: nowrap;
        }
        [data-baseweb="select"] > div:hover,
        [data-testid="stTextInput"] input:hover,
        [data-testid="stTextArea"] textarea:hover,
        [data-testid="stNumberInput"] input:hover,
        [data-testid="stFileUploader"] section:hover {
            border-color: rgba(37, 242, 199, 0.36);
        }
        [data-testid="stTextInput"] input:focus,
        [data-testid="stTextArea"] textarea:focus,
        [data-testid="stNumberInput"] input:focus {
            border-color: rgba(37, 242, 199, 0.48) !important;
            box-shadow: 0 0 0 1px rgba(37, 242, 199, 0.18);
        }
        [data-testid="stFileUploader"] {
            min-width: 0;
        }
        [data-testid="stFileUploader"] section {
            min-height: 2.42rem;
            max-height: 2.42rem;
            padding: 0.34rem 0.58rem;
            display: flex;
            align-items: center;
            overflow: hidden;
        }
        [data-testid="stFileUploader"] section > div {
            min-width: 0;
            width: 100%;
            gap: 0.42rem;
            align-items: center;
        }
        [data-testid="stFileUploader"] [data-testid="stFileUploaderDropzoneInstructions"] {
            min-width: 0;
            flex: 1 1 auto;
        }
        [data-testid="stFileUploader"] [data-testid="stFileUploaderDropzoneInstructions"] > div {
            display: none;
        }
        [data-testid="stFileUploader"] [data-testid="stFileUploaderDropzoneInstructions"]::before {
            content: "Drop or browse CSV";
            display: block;
            color: var(--fs-soft);
            font-size: 0.72rem;
            font-weight: 760;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        [data-testid="stFileUploader"] section button {
            min-height: 1.62rem;
            padding: 0.18rem 0.58rem;
            border-radius: var(--fs-radius);
            border-color: rgba(129, 166, 202, 0.22);
            background: rgba(21, 30, 45, 0.72);
            color: var(--fs-soft);
            font-size: 0.72rem;
            font-weight: 720;
        }
        [data-testid="stFileUploader"] input[type="file"] {
            width: 0.1px;
            height: 0.1px;
            opacity: 0;
            overflow: hidden;
            position: absolute;
            z-index: -1;
        }
        [data-testid="stFileUploader"] small,
        [data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] {
            display: none;
        }
        [data-testid="stCaptionContainer"] p {
            color: var(--fs-muted);
            font-size: 0.66rem;
            line-height: 1.18;
            margin: 0 0 var(--fs-gap-sm) 0;
        }

        .fs-brand {
            display: flex;
            align-items: center;
            gap: 8px;
            margin: 0 18px 10px 18px;
            padding: 0 0 18px 0;
            border-bottom: 1px solid var(--fs-line);
            min-width: 0;
        }
        .fs-logo-mark {
            width: 28px;
            height: 28px;
            display: grid;
            place-items: center;
            border-radius: 6px;
            color: #021019;
            font-weight: 900;
            font-size: 0.74rem;
            background: linear-gradient(135deg, var(--fs-teal), var(--fs-blue));
            box-shadow: 0 0 22px rgba(0, 212, 160, 0.16);
        }
        .fs-brand-title {
            color: var(--fs-ink);
            font-size: 0.94rem;
            font-weight: 830;
            line-height: 1;
            white-space: nowrap;
        }
        .fs-brand-title span {
            color: var(--fs-blue);
        }
        .fs-brand-subtitle {
            color: var(--fs-muted);
            font-size: 0.58rem;
            margin-top: 0.18rem;
            white-space: nowrap;
        }
        .fs-nav-label {
            color: var(--fs-muted);
            font-size: 0.6rem;
            font-weight: 760;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin: 0 18px 6px 18px;
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
            gap: 0;
            margin-bottom: 12px;
            width: 100%;
        }
        [data-testid="stSidebar"] [role="radiogroup"] label {
            border: 1px solid transparent;
            border-left: 2px solid transparent;
            border-radius: 0;
            padding: 10px 18px;
            margin: 0;
            background: transparent;
            width: 100%;
            min-height: 38px;
            transition: border-color var(--fs-fast) var(--fs-ease), background var(--fs-fast) var(--fs-ease), color var(--fs-fast) var(--fs-ease), transform var(--fs-fast) var(--fs-ease);
        }
        [data-testid="stSidebar"] [role="radiogroup"] label > div:first-child {
            display: none;
        }
        [data-testid="stSidebar"] [role="radiogroup"] label p {
            color: inherit;
            font-size: 0.78rem;
            font-weight: 650;
            line-height: 1.25;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        [data-testid="stSidebar"] [role="radiogroup"] label:hover {
            border-color: transparent;
            border-left-color: rgba(37, 242, 199, 0.32);
            background: rgba(37, 242, 199, 0.06);
        }
        [data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
            border-color: transparent;
            border-left-color: var(--fs-teal);
            background: rgba(37, 242, 199, 0.12);
            box-shadow: none;
            color: var(--fs-teal);
            animation: fs-nav-lock var(--fs-medium) var(--fs-ease) both;
        }
        .fs-nav-icon {
            width: 1rem;
            color: inherit;
            text-align: center;
        }
        .fs-sidebar-card {
            border: 1px solid var(--fs-line);
            border-radius: var(--fs-radius);
            background: rgba(21, 30, 45, 0.84);
            padding: 10px 12px;
            min-width: 0;
        }
        .fs-sidebar-footer {
            margin-top: auto;
            padding: 12px 18px 0 18px;
            border-top: 1px solid var(--fs-line);
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .fs-portfolio-card {
            border: 1px solid var(--fs-line);
            border-radius: var(--fs-radius);
            background: rgba(21, 30, 45, 0.84);
            padding: 10px 12px;
            min-width: 0;
        }
        .fs-sidebar-kicker {
            color: var(--fs-muted);
            font-size: 0.64rem;
        }
        .fs-sidebar-value {
            color: var(--fs-ink);
            font-size: 0.82rem;
            font-weight: 720;
            margin-top: 0.15rem;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        .fs-status-dot {
            width: 0.42rem;
            height: 0.42rem;
            border-radius: 999px;
            display: inline-block;
            margin-right: 0.32rem;
            background: var(--fs-teal);
            box-shadow: 0 0 0 3px rgba(37, 242, 199, 0.08);
        }
        .fs-user-row {
            display: flex;
            align-items: center;
            gap: 0.7rem;
            padding: 0.12rem 0;
        }
        .fs-user-avatar {
            width: 2rem;
            height: 2rem;
            border-radius: 999px;
            display: grid;
            place-items: center;
            background: linear-gradient(135deg, var(--fs-blue), var(--fs-purple));
            color: #f8fbff;
            font-size: 0.68rem;
            font-weight: 820;
            flex: 0 0 auto;
        }
        .fs-user-copy {
            min-width: 0;
        }
        .fs-user-name {
            color: var(--fs-ink);
            font-size: 0.78rem;
            font-weight: 760;
            white-space: nowrap;
        }
        .fs-user-plan {
            color: var(--fs-muted);
            font-size: 0.64rem;
            margin-top: 0.12rem;
            white-space: nowrap;
        }

        .fs-topbar-shell {
            border: 1px solid var(--fs-line);
            border-radius: 14px;
            background: linear-gradient(180deg, rgba(16, 34, 55, 0.88), rgba(12, 25, 42, 0.9));
            padding: 22px 24px 18px 24px;
            margin: 0 0 var(--fs-gap-lg) 0;
        }
        .fs-topbar {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 0.8rem;
            margin: 0;
        }
        .fs-page-title {
            margin: 0;
            font-size: 1.42rem;
            font-weight: 760;
            line-height: 1.08;
        }
        .fs-page-subtitle {
            color: var(--fs-soft);
            margin-top: 0.25rem;
            font-size: 0.78rem;
        }
        .fs-badge-row {
            display: flex;
            align-items: center;
            gap: 0.36rem;
            flex-wrap: wrap;
            margin-top: 0.36rem;
        }
        .fs-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.32rem;
            border: 1px solid rgba(37, 242, 199, 0.36);
            background: rgba(37, 242, 199, 0.08);
            color: var(--fs-teal);
            border-radius: 999px;
            padding: 0.18rem 0.44rem;
            font-size: 0.66rem;
            font-weight: 720;
        }
        .fs-badge-live {
            animation: fs-pulse 1800ms var(--fs-ease) infinite;
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
            padding: var(--fs-gap-md);
            margin: 0 0 var(--fs-gap-lg) 0;
            box-shadow: var(--fs-shadow);
        }
        .fs-control-shell {
            margin-bottom: var(--fs-gap-lg);
        }
        .fs-control-shell .fs-panel-header {
            margin-bottom: 0.9rem;
        }
        .fs-control-shell [data-testid="stHorizontalBlock"] {
            align-items: end;
        }
        .fs-control-caption {
            color: var(--fs-muted);
            font-size: 0.64rem;
            font-weight: 760;
            text-transform: uppercase;
            letter-spacing: 0.03em;
            margin-bottom: 0.28rem;
        }
        .fs-control-caption-compact {
            margin: 0 0 var(--fs-gap-xs) 0;
        }

        .fs-card-grid {
            display: grid;
            gap: var(--fs-gap-md);
            grid-template-columns: repeat(auto-fit, minmax(178px, 1fr));
            margin: var(--fs-gap-md) 0;
        }
        .fs-metric-card,
        .fs-summary-stat,
        .fs-panel,
        .fs-rule-card,
        .fs-insight-card,
        .fs-empty-state {
            border: 1px solid var(--fs-line);
            border-radius: var(--fs-radius);
            background: linear-gradient(180deg, rgba(14, 32, 52, 0.92), rgba(7, 17, 31, 0.94));
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.035);
            transition: transform var(--fs-fast) var(--fs-ease), border-color var(--fs-fast) var(--fs-ease), background var(--fs-fast) var(--fs-ease), box-shadow var(--fs-fast) var(--fs-ease);
        }
        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-color: transparent !important;
            border-radius: 0 !important;
            background: transparent !important;
            box-shadow: none !important;
            margin: 0;
        }
        div[data-testid="stVerticalBlockBorderWrapper"] > div {
            padding: 0 !important;
        }
        div[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stVerticalBlock"] {
            gap: var(--fs-gap-sm);
        }
        @keyframes fs-card-in {
            from { opacity: 0; transform: translateY(8px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes fs-page-in {
            from { opacity: 0; transform: translateY(6px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes fs-nav-lock {
            from { background: rgba(37, 242, 199, 0.04); }
            to { background: rgba(37, 242, 199, 0.12); }
        }
        @keyframes fs-pulse {
            0%, 100% { box-shadow: 0 0 0 0 rgba(37, 242, 199, 0.0); }
            50% { box-shadow: 0 0 0 4px rgba(37, 242, 199, 0.08); }
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
            min-height: 88px;
            padding: var(--fs-gap-md);
            display: flex;
            gap: var(--fs-gap-sm);
            align-items: flex-start;
            animation: fs-card-in 240ms ease both;
            overflow-wrap: anywhere;
        }
        .fs-metric-icon {
            width: 32px;
            height: 32px;
            border-radius: 8px;
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
            font-size: 0.68rem;
            font-weight: 680;
            margin-bottom: var(--fs-gap-xs);
        }
        .fs-metric-value {
            color: var(--fs-teal);
            font-size: 1.28rem;
            font-weight: 760;
            line-height: 1.05;
            overflow-wrap: anywhere;
        }
        .fs-metric-caption {
            color: var(--fs-muted);
            margin-top: var(--fs-gap-xs);
            font-size: 0.66rem;
        }
        .fs-summary-stat {
            min-height: 56px;
            padding: var(--fs-gap-sm) var(--fs-gap-md);
            display: flex;
            flex-direction: column;
            justify-content: center;
            overflow: hidden;
        }
        .fs-summary-label {
            color: var(--fs-ink);
            font-size: 0.82rem;
            font-weight: 760;
            line-height: 1.2;
            white-space: nowrap;
        }
        .fs-summary-value {
            color: var(--fs-soft);
            font-size: 0.86rem;
            line-height: 1.25;
            margin-top: var(--fs-gap-xs);
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        .fs-kv-table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            margin: var(--fs-gap-sm) 0 0 0;
            overflow: hidden;
            border: 1px solid var(--fs-line);
            border-radius: var(--fs-radius);
            background: rgba(6, 16, 30, 0.72);
            table-layout: fixed;
        }
        .fs-kv-table th,
        .fs-kv-table td {
            padding: 0.44rem 0.52rem;
            border-bottom: 1px solid rgba(129, 166, 202, 0.12);
            color: var(--fs-soft);
            font-size: 0.72rem;
            text-align: left;
            overflow-wrap: anywhere;
        }
        .fs-kv-table th {
            color: var(--fs-muted);
            background: rgba(129, 166, 202, 0.08);
            font-size: 0.66rem;
            text-transform: uppercase;
            letter-spacing: 0.03em;
        }
        .fs-kv-table td:last-child {
            color: var(--fs-ink);
            font-weight: 720;
        }
        .fs-kv-table tr:last-child td {
            border-bottom: 0;
        }
        .fs-table-scroll {
            width: 100%;
            overflow-x: auto;
            border: 1px solid var(--fs-line);
            border-radius: var(--fs-radius);
            background: rgba(6, 16, 30, 0.72);
        }
        .fs-data-table {
            width: 100%;
            min-width: 480px;
            border-collapse: collapse;
            table-layout: auto;
        }
        .fs-data-table th,
        .fs-data-table td {
            padding: 0.46rem 0.54rem;
            border-bottom: 1px solid rgba(129, 166, 202, 0.12);
            color: var(--fs-soft);
            font-size: 0.7rem;
            text-align: left;
            vertical-align: top;
            white-space: nowrap;
        }
        .fs-data-table th {
            color: var(--fs-muted);
            background: rgba(129, 166, 202, 0.08);
            font-size: 0.64rem;
            font-weight: 760;
            text-transform: uppercase;
            letter-spacing: 0.03em;
        }
        .fs-data-table td {
            max-width: 260px;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .fs-data-table tr:last-child td {
            border-bottom: 0;
        }
        .fs-validation-list {
            display: flex;
            flex-direction: column;
            gap: var(--fs-gap-sm);
        }
        .fs-validation-row {
            display: grid;
            grid-template-columns: 1.85rem minmax(0, 1fr) auto;
            align-items: start;
            gap: 0.62rem;
            padding: 0.64rem;
            border: 1px solid rgba(129, 166, 202, 0.18);
            border-radius: var(--fs-radius);
            background: linear-gradient(180deg, rgba(21, 30, 45, 0.88), rgba(12, 20, 34, 0.92));
        }
        .fs-validation-icon {
            width: 1.85rem;
            height: 1.85rem;
            border-radius: 8px;
            display: grid;
            place-items: center;
            color: var(--fs-teal);
            background: rgba(37, 242, 199, 0.1);
            font-weight: 850;
            flex: 0 0 auto;
        }
        .fs-validation-copy {
            min-width: 0;
        }
        .fs-validation-title {
            color: var(--fs-ink);
            font-size: 0.78rem;
            font-weight: 780;
            white-space: nowrap;
        }
        .fs-validation-step,
        .fs-validation-result {
            color: var(--fs-muted);
            font-size: 0.68rem;
            line-height: 1.35;
            overflow-wrap: anywhere;
        }
        .fs-validation-result {
            color: var(--fs-soft);
            margin-top: 0.18rem;
        }
        .fs-panel {
            padding: var(--fs-gap-md) var(--fs-gap-lg);
            margin: 0;
        }
        .fs-panel-shell {
            height: var(--fs-panel-height, auto);
            display: flex;
            flex-direction: column;
        }
        .fs-panel-header {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 0.62rem;
            margin-bottom: 0.62rem;
            flex: 0 0 auto;
        }
        .fs-panel-title {
            color: var(--fs-ink);
            font-size: 0.86rem;
            font-weight: 760;
        }
        .fs-panel-subtitle {
            color: var(--fs-muted);
            font-size: 0.7rem;
            margin-top: 0.15rem;
        }
        .fs-panel-body {
            display: flex;
            flex-direction: column;
            gap: var(--fs-gap-sm);
            min-height: 0;
        }
        .fs-panel-scroll .fs-panel-body {
            flex: 1 1 auto;
            overflow-y: auto;
            padding-right: 4px;
        }
        .fs-panel-scroll .fs-panel-body::-webkit-scrollbar {
            width: 5px;
        }
        .fs-panel-scroll .fs-panel-body::-webkit-scrollbar-track {
            background: transparent;
        }
        .fs-panel-scroll .fs-panel-body::-webkit-scrollbar-thumb {
            background: rgba(129, 166, 202, 0.28);
            border-radius: 999px;
        }
        .fs-section {
            border-top: 1px solid var(--fs-line);
            padding-top: var(--fs-gap-lg);
            margin-top: var(--fs-gap-lg);
        }
        .fs-section-kicker {
            color: var(--fs-teal);
            font-size: 0.64rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }
        .fs-section-title {
            color: var(--fs-ink);
            font-size: 1rem;
            font-weight: 760;
            margin: 2px 0 var(--fs-gap-md) 0;
        }
        .fs-rule-card {
            padding: var(--fs-gap-md);
            min-height: 100px;
            overflow-wrap: anywhere;
        }
        .fs-rule-top {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 0.6rem;
            margin-bottom: 0.42rem;
        }
        .fs-rule-id {
            color: var(--fs-ink);
            font-size: 0.8rem;
            font-weight: 780;
            white-space: nowrap;
        }
        .fs-rule-description,
        .fs-insight-body {
            color: var(--fs-soft);
            font-size: 0.7rem;
        }
        .fs-status {
            display: inline-flex;
            border-radius: 999px;
            padding: 0.13rem 0.42rem;
            font-size: 0.62rem;
            font-weight: 760;
            border: 1px solid rgba(37, 242, 199, 0.38);
            color: var(--fs-teal);
            background: rgba(37, 242, 199, 0.1);
            white-space: nowrap;
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
            padding: var(--fs-gap-md);
            border-left: 3px solid var(--fs-teal);
            margin-bottom: var(--fs-gap-sm);
            overflow-wrap: anywhere;
            display: flex;
            flex-direction: column;
            gap: var(--fs-gap-sm);
        }
        .fs-insight-selected {
            border-color: rgba(37, 242, 199, 0.5);
            box-shadow: var(--fs-glow);
            background: linear-gradient(180deg, rgba(20, 52, 74, 0.95), rgba(8, 22, 38, 0.95));
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
            font-size: 0.78rem;
            font-weight: 760;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 0.5rem;
            margin-bottom: 0;
        }
        .fs-insight-row {
            display: flex;
            align-items: flex-start;
            gap: 0.52rem;
            border: 1px solid rgba(255, 255, 255, 0.055);
            border-radius: var(--fs-radius);
            padding: 0.48rem 0.54rem;
            background: rgba(11, 18, 31, 0.44);
        }
        .fs-insight-row-fact {
            background: rgba(0, 212, 160, 0.08);
            border-color: rgba(0, 212, 160, 0.16);
        }
        .fs-insight-row-interpretation {
            background: rgba(79, 145, 232, 0.08);
            border-color: rgba(79, 145, 232, 0.16);
        }
        .fs-insight-row-caution {
            background: rgba(245, 166, 35, 0.08);
            border-color: rgba(245, 166, 35, 0.18);
        }
        .fs-insight-badge {
            flex: 0 0 auto;
            border-radius: 5px;
            padding: 0.12rem 0.42rem;
            font-size: 0.62rem;
            font-weight: 760;
            white-space: nowrap;
        }
        .fs-insight-row-fact .fs-insight-badge {
            color: var(--fs-teal);
            background: rgba(0, 212, 160, 0.14);
        }
        .fs-insight-row-interpretation .fs-insight-badge {
            color: var(--fs-blue);
            background: rgba(79, 145, 232, 0.14);
        }
        .fs-insight-row-caution .fs-insight-badge {
            color: var(--fs-amber);
            background: rgba(245, 166, 35, 0.14);
        }
        .fs-insight-row .fs-insight-body {
            min-width: 0;
            line-height: 1.45;
        }
        .fs-empty-state {
            padding: 1rem;
            text-align: left;
            min-height: 112px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            position: relative;
            overflow: hidden;
        }
        .fs-empty-state::before {
            content: "";
            position: absolute;
            inset: 0;
            background:
                linear-gradient(90deg, rgba(37, 242, 199, 0.06), transparent 34%),
                repeating-linear-gradient(135deg, rgba(129, 166, 202, 0.04) 0 1px, transparent 1px 9px);
            pointer-events: none;
        }
        .fs-empty-title {
            color: var(--fs-ink);
            font-weight: 760;
            font-size: 0.9rem;
            position: relative;
        }
        .fs-empty-message {
            color: var(--fs-muted);
            margin-top: 0.3rem;
            font-size: 0.74rem;
            position: relative;
        }

        @media (min-width: 1500px) {
            [data-testid="stMainBlockContainer"],
            .main .block-container,
            section.main > div.block-container {
                max-width: none;
                padding-left: 20px !important;
                padding-right: 20px !important;
            }
            div[data-testid="column"] {
                min-width: 0;
            }
        }

        @media (max-width: 980px) {
            :root {
                --fs-sidebar-width: 232px;
            }
            [data-testid="stMainBlockContainer"],
            .main .block-container,
            section.main > div.block-container {
                padding-left: 16px !important;
                padding-right: 16px !important;
                padding-top: 16px !important;
            }
            .fs-topbar {
                display: block;
            }
            .fs-topbar-shell {
                padding: 18px 18px 16px 18px;
            }
            .fs-page-title {
                font-size: 1.38rem;
            }
            .fs-control-panel {
                padding: 0.7rem;
            }
            .fs-card-grid {
                grid-template-columns: repeat(auto-fit, minmax(148px, 1fr));
            }
            .fs-metric-card {
                min-height: 96px;
                padding: 0.82rem;
            }
            .fs-metric-icon {
                width: 34px;
                height: 34px;
                border-radius: 10px;
            }
            .fs-metric-value {
                font-size: 1.16rem;
            }
        }

        @media (max-width: 760px) {
            [data-testid="stMainBlockContainer"],
            .main .block-container,
            section.main > div.block-container {
                padding-left: 12px !important;
                padding-right: 12px !important;
            }
            .fs-page-title {
                font-size: 1.16rem;
            }
            .fs-page-subtitle,
            .fs-badge,
            .fs-metric-caption,
            .fs-rule-description,
            .fs-insight-body {
                font-size: 0.72rem;
            }
            .fs-brand-title {
                font-size: 1.2rem;
            }
            .fs-sidebar-card {
                padding: 0.72rem;
            }
            .fs-sidebar-footer {
                padding: 10px 18px 0 18px;
            }
            div[data-testid="stPlotlyChart"] {
                min-height: 220px;
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

    if str(theme).lower() == "light":
        st.markdown(
            """
            <style>
            :root {
                --fs-bg: #f4f7fb;
                --fs-bg-soft: #eef4fb;
                --fs-sidebar: #edf3fa;
                --fs-panel: rgba(255, 255, 255, 0.94);
                --fs-panel-strong: rgba(255, 255, 255, 0.98);
                --fs-panel-hover: rgba(246, 250, 255, 0.98);
                --fs-line: rgba(36, 48, 68, 0.12);
                --fs-line-strong: rgba(0, 151, 124, 0.28);
                --fs-ink: #162033;
                --fs-muted: #64748b;
                --fs-soft: #334155;
                --fs-teal: #009b83;
                --fs-cyan: #047fa8;
                --fs-blue: #2563eb;
                --fs-red: #dc3545;
                --fs-amber: #b7791f;
                --fs-purple: #7c3aed;
                --fs-green: #168a52;
                --fs-shadow: 0 8px 22px rgba(15, 23, 42, 0.06);
                --fs-glow: 0 0 0 1px rgba(0, 151, 124, 0.18), 0 8px 18px rgba(0, 151, 124, 0.06);
            }

            html, body, [data-testid="stAppViewContainer"] {
                background:
                    radial-gradient(circle at 18% 0%, rgba(0, 151, 124, 0.08), transparent 26rem),
                    radial-gradient(circle at 92% 20%, rgba(37, 99, 235, 0.08), transparent 24rem),
                    linear-gradient(135deg, #f7fbff 0%, #eef4fb 56%, #f8fafc 100%) !important;
                color: var(--fs-ink);
            }
            [data-testid="stHeader"] {
                background: rgba(248, 250, 252, 0.82);
                border-bottom: 1px solid var(--fs-line);
            }
            [data-testid="stSidebar"] {
                background:
                    linear-gradient(180deg, rgba(239, 246, 255, 0.98), rgba(248, 250, 252, 0.98)),
                    var(--fs-sidebar);
                border-right: 1px solid var(--fs-line);
            }
            div[data-testid="stMetric"],
            div[data-testid="stVerticalBlockBorderWrapper"],
            .fs-topbar-shell,
            .fs-metric-card,
            .fs-summary-stat,
            .fs-panel,
            .fs-rule-card,
            .fs-insight-card,
            .fs-empty-state,
            .fs-portfolio-card,
            .fs-sidebar-card {
                background: linear-gradient(180deg, rgba(255, 255, 255, 0.95), rgba(247, 250, 252, 0.94)) !important;
                border-color: var(--fs-line) !important;
                box-shadow: var(--fs-shadow);
            }
            .fs-kv-table,
            .fs-table-scroll,
            div[data-testid="stDataFrame"] {
                background: rgba(255, 255, 255, 0.88);
                border-color: var(--fs-line);
            }
            .fs-kv-table th,
            .fs-data-table th {
                background: rgba(226, 232, 240, 0.68);
                color: var(--fs-muted);
            }
            .fs-kv-table td,
            .fs-data-table td,
            [data-testid="stSidebar"] [role="radiogroup"] label p {
                color: var(--fs-soft);
            }
            .fs-validation-row,
            .fs-insight-row,
            .fs-insight-selected {
                background: linear-gradient(180deg, rgba(255, 255, 255, 0.92), rgba(248, 250, 252, 0.9)) !important;
                border-color: var(--fs-line) !important;
            }
            .fs-insight-row-fact {
                background: rgba(0, 151, 124, 0.08) !important;
                border-color: rgba(0, 151, 124, 0.2) !important;
            }
            .fs-insight-row-interpretation {
                background: rgba(37, 99, 235, 0.08) !important;
                border-color: rgba(37, 99, 235, 0.18) !important;
            }
            .fs-insight-row-caution {
                background: rgba(183, 121, 31, 0.08) !important;
                border-color: rgba(183, 121, 31, 0.2) !important;
            }
            .fs-validation-icon,
            .fs-metric-icon {
                background: rgba(0, 151, 124, 0.1);
            }
            .fs-topbar,
            .fs-page-title,
            .fs-panel-title,
            .fs-section-title,
            .fs-metric-label,
            .fs-validation-title,
            .fs-rule-id,
            .fs-insight-title,
            h1, h2, h3, h4 {
                color: var(--fs-ink);
            }
            .fs-page-subtitle,
            .fs-panel-subtitle,
            .fs-metric-caption,
            .fs-validation-step,
            .fs-validation-result,
            .fs-rule-description,
            .fs-insight-body {
                color: var(--fs-muted);
            }
            [data-baseweb="select"] > div,
            [data-testid="stTextInput"] input,
            [data-testid="stTextArea"] textarea,
            [data-testid="stNumberInput"] input,
            [data-testid="stFileUploader"] section {
                background: rgba(255, 255, 255, 0.96);
                border-color: var(--fs-line);
                color: var(--fs-ink);
            }
            [data-testid="stFileUploader"] section button {
                background: rgba(239, 246, 255, 0.92);
                color: var(--fs-soft);
                border-color: var(--fs-line);
            }
            [data-testid="stFileUploader"] [data-testid="stFileUploaderDropzoneInstructions"]::before {
                color: var(--fs-soft);
            }
            [data-baseweb="popover"],
            [data-baseweb="menu"],
            [role="listbox"] {
                background: #ffffff !important;
                color: var(--fs-ink) !important;
                border-color: var(--fs-line) !important;
            }
            [data-baseweb="menu"] li,
            [role="option"] {
                color: var(--fs-ink) !important;
            }
            [data-baseweb="menu"] li:hover,
            [role="option"]:hover {
                background: rgba(0, 151, 124, 0.08) !important;
            }
            .stButton > button,
            .stDownloadButton > button {
                background: linear-gradient(135deg, rgba(0, 151, 124, 0.92), rgba(8, 145, 178, 0.88));
                color: #ffffff;
            }
            .fs-badge-muted {
                background: rgba(226, 232, 240, 0.74);
                color: var(--fs-soft);
            }
            </style>
            """,
            unsafe_allow_html=True,
        )


def style_plotly_figure(fig: go.Figure) -> go.Figure:
    """Apply the shared chart treatment for the selected shell theme."""

    is_light = str(st.session_state.get("dashboard_theme", "Dark")).lower() == "light"
    template = "plotly_white" if is_light else "plotly_dark"
    font_color = "#334155" if is_light else "#b8c4d4"
    muted_color = "#64748b" if is_light else "#7a8ba0"
    grid_color = "rgba(51, 65, 85, 0.12)" if is_light else "rgba(129, 166, 202, 0.12)"
    zero_color = "rgba(51, 65, 85, 0.18)" if is_light else "rgba(129, 166, 202, 0.2)"
    plot_bg = "rgba(0,0,0,0)"
    hover_bg = "#ffffff" if is_light else "#151e2d"
    hover_border = "rgba(51,65,85,0.18)" if is_light else "rgba(255,255,255,0.14)"

    fig.update_layout(
        template=template,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=plot_bg,
        font=dict(color=font_color, family="DM Sans, Aptos, Segoe UI, sans-serif", size=11),
        colorway=PLOTLY_COLORS,
        margin=dict(l=12, r=12, t=22, b=18),
        legend_title_text="",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
            font=dict(size=10, color=muted_color),
        ),
        hovermode="x unified",
        hoverlabel=dict(bgcolor=hover_bg, bordercolor=hover_border, font_size=11),
    )
    fig.update_xaxes(gridcolor=grid_color, zerolinecolor=zero_color, tickfont=dict(size=10, color=muted_color), title_font=dict(size=11, color=muted_color))
    fig.update_yaxes(gridcolor=grid_color, zerolinecolor=zero_color, tickfont=dict(size=10, color=muted_color), title_font=dict(size=11, color=muted_color))
    return fig
