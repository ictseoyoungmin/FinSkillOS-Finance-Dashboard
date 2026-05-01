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


def render_missing_values_chart(profile: dict[str, Any] | None, height: int = 250) -> None:
    if not profile:
        empty_state("Missingness Unavailable", "Run an analysis to inspect missing values.")
        return
    missing = profile.get("missing_rates", {})
    if not missing:
        empty_state("Missingness Unavailable", "No column missingness profile was produced.")
        return
    plot_df = pd.DataFrame(
        [{"column": column, "missing_rate": rate} for column, rate in missing.items()]
    ).sort_values("missing_rate", ascending=False)
    fig = px.bar(plot_df, x="column", y="missing_rate")
    fig.update_layout(height=height)
    fig.update_yaxes(tickformat=".1%", title="Missing Rate")
    fig.update_xaxes(title="")
    st.plotly_chart(style_plotly_figure(fig), use_container_width=True)


def render_frequency_coverage_chart(schema: dict[str, Any] | None, height: int = 250) -> None:
    std_df = schema.get("standardized_df") if schema else None
    if not isinstance(std_df, pd.DataFrame) or "date" not in std_df.columns:
        empty_state("Coverage Unavailable", "Coverage requires a standardized date column.")
        return
    coverage = (
        std_df.assign(date=pd.to_datetime(std_df["date"], errors="coerce"))
        .dropna(subset=["date"])
        .groupby("date", as_index=False)
        .size()
        .rename(columns={"size": "observations"})
    )
    if coverage.empty:
        empty_state("Coverage Unavailable", "No valid dates were available after standardization.")
        return
    fig = px.bar(coverage, x="date", y="observations")
    fig.update_layout(height=height)
    fig.update_xaxes(title="")
    fig.update_yaxes(title="Rows")
    st.plotly_chart(style_plotly_figure(fig), use_container_width=True)


def render_return_distribution(metrics: dict[str, Any] | None, height: int = 270) -> None:
    if not metrics:
        empty_state("Return Distribution Unavailable", "Run an analysis to generate return observations.")
        return
    returns = metrics.get("returns")
    if not isinstance(returns, pd.DataFrame) or returns.empty or "return" not in returns.columns:
        empty_state("Return Distribution Unavailable", "Return distribution requires period return observations.")
        return
    fig = px.histogram(returns.dropna(subset=["return"]), x="return", nbins=36, color="asset" if "asset" in returns.columns else None)
    fig.update_layout(height=height, bargap=0.04)
    fig.update_xaxes(tickformat=".1%", title="Period Return")
    fig.update_yaxes(title="Frequency")
    st.plotly_chart(style_plotly_figure(fig), use_container_width=True)


def render_rolling_return_chart(metrics: dict[str, Any] | None, window: int = 63, height: int = 270) -> None:
    if not metrics:
        empty_state("Rolling Return Unavailable", "Run an analysis to generate returns.")
        return
    returns = metrics.get("returns")
    if not isinstance(returns, pd.DataFrame) or returns.empty or not {"date", "return"}.issubset(returns.columns):
        empty_state("Rolling Return Unavailable", "Rolling return requires dated return observations.")
        return
    working = returns.copy()
    working["date"] = pd.to_datetime(working["date"], errors="coerce")
    working = working.dropna(subset=["date", "return"]).sort_values(["asset", "date"] if "asset" in working.columns else ["date"])
    if "asset" not in working.columns:
        working["asset"] = "Portfolio"
    working["rolling_return"] = working.groupby("asset")["return"].transform(
        lambda series: (1.0 + series).rolling(window=min(window, max(len(series), 1)), min_periods=5).apply(lambda values: values.prod() - 1.0, raw=True)
    )
    plot_df = working.dropna(subset=["rolling_return"])
    if plot_df.empty:
        empty_state("Rolling Return Unavailable", "Not enough observations for the selected rolling window.")
        return
    fig = px.line(plot_df, x="date", y="rolling_return", color="asset")
    fig.update_layout(height=height)
    fig.update_yaxes(tickformat=".0%", title=f"Rolling {window} Period Return")
    st.plotly_chart(style_plotly_figure(fig), use_container_width=True)


def render_rolling_volatility_chart(metrics: dict[str, Any] | None, periods_per_year: int = 252, window: int = 63, height: int = 300) -> None:
    if not metrics:
        empty_state("Rolling Volatility Unavailable", "Run an analysis to generate returns.")
        return
    returns = metrics.get("returns")
    if not isinstance(returns, pd.DataFrame) or returns.empty or not {"date", "return"}.issubset(returns.columns):
        empty_state("Rolling Volatility Unavailable", "Rolling volatility requires dated return observations.")
        return
    working = returns.copy()
    working["date"] = pd.to_datetime(working["date"], errors="coerce")
    working = working.dropna(subset=["date", "return"]).sort_values(["asset", "date"] if "asset" in working.columns else ["date"])
    if "asset" not in working.columns:
        working["asset"] = "Portfolio"
    effective_window = min(window, max(len(working), 1))
    working["rolling_volatility"] = working.groupby("asset")["return"].transform(
        lambda series: series.rolling(window=effective_window, min_periods=5).std() * (periods_per_year ** 0.5)
    )
    plot_df = working.dropna(subset=["rolling_volatility"])
    if plot_df.empty:
        empty_state("Rolling Volatility Unavailable", "Not enough observations for the selected rolling window.")
        return
    fig = px.line(plot_df, x="date", y="rolling_volatility", color="asset")
    fig.update_layout(height=height)
    fig.update_yaxes(tickformat=".0%", title="Annualized Volatility")
    st.plotly_chart(style_plotly_figure(fig), use_container_width=True)


def render_allocation_chart(schema: dict[str, Any] | None, height: int = 280) -> None:
    std_df = schema.get("standardized_df") if schema else None
    if not isinstance(std_df, pd.DataFrame) or not {"asset", "weight"}.issubset(std_df.columns):
        empty_state("Allocation Unavailable", "Allocation chart requires standardized asset and weight fields.")
        return
    plot_df = std_df.dropna(subset=["asset", "weight"])
    if plot_df.empty:
        empty_state("Allocation Unavailable", "No valid asset weights were available.")
        return
    fig = px.pie(plot_df, names="asset", values="weight", hole=0.48)
    fig.update_layout(height=height)
    st.plotly_chart(style_plotly_figure(fig), use_container_width=True)


def render_risk_contribution_chart(metrics: dict[str, Any] | None, height: int = 280) -> None:
    if not metrics:
        empty_state("Risk Contribution Unavailable", "Run an analysis to generate asset metrics.")
        return
    asset_metrics = pd.DataFrame(metrics.get("asset_metrics", []))
    if asset_metrics.empty or not {"asset", "annualized_volatility"}.issubset(asset_metrics.columns):
        empty_state("Risk Contribution Unavailable", "Risk contribution requires asset-level volatility metrics.")
        return
    plot_df = asset_metrics.dropna(subset=["annualized_volatility"]).copy()
    total = plot_df["annualized_volatility"].sum()
    if total == 0 or plot_df.empty:
        empty_state("Risk Contribution Unavailable", "Asset volatility values are unavailable or zero.")
        return
    plot_df["risk_contribution"] = plot_df["annualized_volatility"] / total
    fig = px.bar(plot_df.sort_values("risk_contribution"), x="risk_contribution", y="asset", orientation="h")
    fig.update_layout(height=height)
    fig.update_xaxes(tickformat=".0%", title="Share of Asset Volatility")
    fig.update_yaxes(title="")
    st.plotly_chart(style_plotly_figure(fig), use_container_width=True)
