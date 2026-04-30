"""Chart renderers used by FinSkillOS UI tabs."""

from __future__ import annotations

from typing import Any

import pandas as pd
import plotly.express as px
import streamlit as st

from ui.components import empty_state
from ui.theme import style_plotly_figure


def render_cumulative_return_chart(metrics: dict[str, Any] | None, height: int = 320) -> None:
    if not metrics:
        empty_state("Cumulative Return Unavailable", "Run an analysis to generate return series.")
        return
    cumulative = metrics.get("cumulative_returns")
    if not isinstance(cumulative, pd.DataFrame) or cumulative.empty:
        empty_state("Cumulative Return Unavailable", "No cumulative return series was produced for this schema.")
        return

    plot_df = cumulative.copy()
    plot_df["indexed_value"] = 100.0 * (1.0 + plot_df["cumulative_return"])
    fig = px.line(plot_df, x="date", y="indexed_value", color="asset")
    fig.update_layout(height=height)
    fig.update_yaxes(title="Indexed Value")
    st.plotly_chart(style_plotly_figure(fig), use_container_width=True)


def render_drawdown_chart(metrics: dict[str, Any] | None, height: int = 320) -> None:
    if not metrics:
        empty_state("Drawdown Unavailable", "Run an analysis to generate drawdown series.")
        return
    drawdowns = metrics.get("drawdowns")
    if not isinstance(drawdowns, pd.DataFrame) or drawdowns.empty:
        empty_state("Drawdown Unavailable", "Drawdown requires a valid price or return time series.")
        return

    fig = px.area(drawdowns, x="date", y="drawdown", color="asset")
    fig.update_layout(height=height)
    fig.update_yaxes(tickformat=".0%", title="Drawdown")
    st.plotly_chart(style_plotly_figure(fig), use_container_width=True)


def render_correlation_heatmap(metrics: dict[str, Any] | None, height: int = 280) -> None:
    if not metrics:
        empty_state("Correlation Unavailable", "Run an analysis to generate asset return correlations.")
        return
    corr = metrics.get("correlation_matrix")
    if not isinstance(corr, pd.DataFrame) or corr.empty:
        empty_state("Correlation Unavailable", "Correlation heatmap requires at least two assets with overlapping returns.")
        return

    fig = px.imshow(
        corr,
        text_auto=".2f",
        zmin=-1,
        zmax=1,
        color_continuous_scale="RdBu_r",
        aspect="auto",
    )
    fig.update_layout(height=height)
    st.plotly_chart(style_plotly_figure(fig), use_container_width=True)


def render_risk_return_scatter(metrics: dict[str, Any] | None, height: int = 280) -> None:
    if not metrics:
        empty_state("Risk vs. Return Unavailable", "Run an analysis to generate asset-level metrics.")
        return

    asset_metrics = pd.DataFrame(metrics.get("asset_metrics", []))
    required = {"annualized_volatility", "annualized_return", "asset"}
    if asset_metrics.empty or not required.issubset(asset_metrics.columns):
        empty_state("Risk vs. Return Unavailable", "This panel requires asset, annualized return, and volatility metrics.")
        return

    asset_metrics = asset_metrics.dropna(subset=["annualized_volatility", "annualized_return"])
    if asset_metrics.empty:
        empty_state("Risk vs. Return Unavailable", "No asset has both return and volatility available.")
        return

    size = asset_metrics["max_drawdown"].abs() if "max_drawdown" in asset_metrics.columns else None
    fig = px.scatter(
        asset_metrics,
        x="annualized_volatility",
        y="annualized_return",
        text="asset",
        size=size,
    )
    fig.update_layout(height=height)
    fig.update_traces(textposition="top center")
    fig.update_xaxes(tickformat=".0%", title="Volatility")
    fig.update_yaxes(tickformat=".0%", title="Annualized Return")
    st.plotly_chart(style_plotly_figure(fig), use_container_width=True)

