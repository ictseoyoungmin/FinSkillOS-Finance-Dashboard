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
            background: rgba(2, 8, 18, 0.72);
            border-bottom: 1px solid rgba(129, 166, 202, 0.12);
            backdrop-filter: blur(16px);
        }

        [data-testid="stSidebar"] {
            background:
                linear-gradient(180deg, rgba(17, 24, 39, 0.98), rgba(11, 15, 25, 0.98)),
                var(--fs-sidebar);
            border-right: 1px solid var(--fs-line);
            min-width: 260px !important;
            max-width: 260px !important;
        }

        [data-testid="stSidebar"] > div:first-child {
            width: 260px;
            padding: 1.45rem 0.85rem 1.1rem 0.85rem;
        }

        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] label {
            color: var(--fs-soft);
        }

        .main .block-container {
            padding: 0.78rem 1.25rem 2rem 1.25rem;
            max-width: 1540px;
            animation: fs-page-in var(--fs-medium) var(--fs-ease) both;
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
        div[data-testid="stPlotlyChart"] {
            min-height: 235px;
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
        [data-testid="stNumberInput"] input,
        [data-testid="stFileUploader"] section {
            background: rgba(7, 17, 31, 0.95);
            border-color: var(--fs-line);
            border-radius: var(--fs-radius);
            color: var(--fs-ink);
            min-height: 2.25rem;
            transition: border-color var(--fs-fast) var(--fs-ease), box-shadow var(--fs-fast) var(--fs-ease);
        }
        [data-baseweb="select"] > div:hover,
        [data-testid="stNumberInput"] input:hover,
        [data-testid="stFileUploader"] section:hover {
            border-color: rgba(37, 242, 199, 0.36);
        }

        .fs-brand {
            display: flex;
            align-items: center;
            gap: 0.64rem;
            margin: 0.25rem 0 1rem 0;
            padding: 0.35rem 0.15rem 0.85rem 0.15rem;
            border-bottom: 1px solid var(--fs-line);
        }
        .fs-logo-mark {
            width: 32px;
            height: 32px;
            display: grid;
            place-items: center;
            border-radius: 8px;
            color: #021019;
            font-weight: 900;
            background: linear-gradient(135deg, var(--fs-teal), var(--fs-blue));
            box-shadow: 0 0 22px rgba(0, 212, 160, 0.16);
        }
        .fs-brand-title {
            color: var(--fs-ink);
            font-size: 1.12rem;
            font-weight: 830;
            line-height: 1;
        }
        .fs-brand-title span {
            color: var(--fs-blue);
        }
        .fs-brand-subtitle {
            color: var(--fs-muted);
            font-size: 0.68rem;
            margin-top: 0.2rem;
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
            gap: 0.1rem;
            margin-bottom: 0.9rem;
        }
        [data-testid="stSidebar"] [role="radiogroup"] label {
            border: 1px solid transparent;
            border-radius: var(--fs-radius);
            padding: 0.48rem 0.62rem;
            background: transparent;
            transition: border-color var(--fs-fast) var(--fs-ease), background var(--fs-fast) var(--fs-ease), color var(--fs-fast) var(--fs-ease), transform var(--fs-fast) var(--fs-ease);
        }
        [data-testid="stSidebar"] [role="radiogroup"] label > div:first-child {
            display: none;
        }
        [data-testid="stSidebar"] [role="radiogroup"] label p {
            color: inherit;
            font-size: 0.82rem;
            font-weight: 650;
            line-height: 1.25;
        }
        [data-testid="stSidebar"] [role="radiogroup"] label:hover {
            border-color: rgba(37, 242, 199, 0.22);
            background: rgba(37, 242, 199, 0.06);
            transform: translateX(2px);
        }
        [data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
            border-color: rgba(37, 242, 199, 0.42);
            background: linear-gradient(90deg, rgba(37, 242, 199, 0.15), rgba(56, 163, 255, 0.06));
            box-shadow: inset 3px 0 0 var(--fs-teal);
            color: var(--fs-teal);
            animation: fs-nav-lock var(--fs-medium) var(--fs-ease) both;
        }
        .fs-nav-icon {
            width: 1.35rem;
            color: inherit;
            text-align: center;
        }
        .fs-sidebar-card {
            border: 1px solid var(--fs-line);
            border-radius: var(--fs-radius);
            background: rgba(21, 30, 45, 0.84);
            padding: 0.7rem 0.78rem;
            margin-top: 0.7rem;
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
        }

        .fs-topbar {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 0.8rem;
            margin-bottom: 0.72rem;
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
            padding: 0.85rem;
            margin: 0.6rem 0 1rem 0;
            box-shadow: var(--fs-shadow);
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
            margin: 0.1rem 0 0.28rem 0;
        }

        .fs-card-grid {
            display: grid;
            gap: 0.62rem;
            grid-template-columns: repeat(auto-fit, minmax(178px, 1fr));
            margin: 0.68rem 0 0.62rem 0;
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
            transition: transform var(--fs-fast) var(--fs-ease), border-color var(--fs-fast) var(--fs-ease), background var(--fs-fast) var(--fs-ease), box-shadow var(--fs-fast) var(--fs-ease);
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
        @keyframes fs-page-in {
            from { opacity: 0; transform: translateY(6px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes fs-nav-lock {
            from { box-shadow: inset 0 0 0 var(--fs-teal), 0 0 0 rgba(37, 242, 199, 0); }
            to { box-shadow: inset 3px 0 0 var(--fs-teal), 0 0 26px rgba(37, 242, 199, 0.08); }
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
            min-height: 92px;
            padding: 0.72rem 0.82rem;
            display: flex;
            gap: 0.68rem;
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
            margin-bottom: 0.28rem;
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
            margin-top: 0.34rem;
            font-size: 0.66rem;
        }
        .fs-kv-table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            margin: 0.65rem 0 0.8rem 0;
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
            gap: 0.5rem;
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
            padding: 0.85rem 0.95rem;
            margin: 0.62rem 0;
        }
        .fs-panel-header {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 0.62rem;
            margin-bottom: 0.62rem;
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
        .fs-section {
            border-top: 1px solid var(--fs-line);
            padding-top: 0.82rem;
            margin-top: 1.1rem;
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
            margin: 0.1rem 0 0.58rem 0;
        }
        .fs-rule-card {
            padding: 0.72rem;
            min-height: 104px;
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
            padding: 0.72rem 0.78rem;
            border-left: 3px solid var(--fs-teal);
            margin-bottom: 0.48rem;
            overflow-wrap: anywhere;
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
            margin-bottom: 0.28rem;
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
            .main .block-container {
                max-width: 1680px;
            }
            div[data-testid="column"] {
                min-width: 0;
            }
        }

        @media (max-width: 980px) {
            .main .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
                padding-top: 0.9rem;
            }
            .fs-topbar {
                display: block;
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
            .main .block-container {
                padding-left: 0.7rem;
                padding-right: 0.7rem;
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
