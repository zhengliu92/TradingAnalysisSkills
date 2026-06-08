#!/usr/bin/env python3
"""Run TradingAgents programmatically without launching the interactive CLI."""

from __future__ import annotations

import argparse
import copy
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


ANALYST_ORDER = ("market", "social", "news", "fundamentals")
CRYPTO_SUFFIXES = ("-USD", "-USDT", "-USDC", "-BTC", "-ETH")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a non-interactive TradingAgents analysis from a checkout."
    )
    parser.add_argument("--project-dir", default=os.environ.get("TRADINGAGENTS_PROJECT_DIR", "."))
    parser.add_argument("--ticker", required=True)
    parser.add_argument("--date", required=True, help="Analysis date in YYYY-MM-DD format")
    parser.add_argument("--asset-type", choices=("auto", "stock", "crypto"), default="auto")
    parser.add_argument("--analysts", default="market,social,news,fundamentals")
    parser.add_argument("--provider", default=None, help="Optional explicit TradingAgents runtime provider; omit for ordinary skill use")
    parser.add_argument("--quick-model", default=None, help="Optional explicit TradingAgents quick model; omit for ordinary skill use")
    parser.add_argument("--deep-model", default=None, help="Optional explicit TradingAgents deep model; omit for ordinary skill use")
    parser.add_argument("--backend-url", default=None)
    parser.add_argument("--output-language", default=None)
    parser.add_argument("--debate-rounds", type=int, default=None)
    parser.add_argument("--risk-rounds", type=int, default=None)
    parser.add_argument("--temperature", type=float, default=None)
    parser.add_argument("--results-dir", default=None)
    parser.add_argument("--cache-dir", default=None)
    parser.add_argument("--memory-log-path", default=None)
    parser.add_argument("--data-vendors", default=None, help="Comma form: category=vendor,category=vendor")
    parser.add_argument("--tool-vendors", default=None, help="Comma form: tool=vendor,tool=vendor")
    parser.add_argument("--checkpoint", action="store_true")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--output-dir", default="tradingagents-output")
    parser.add_argument("--json-out", default=None)
    parser.add_argument("--markdown-out", default=None)
    parser.add_argument("--dry-run", action="store_true", help="Validate import/config and print the planned run")
    return parser.parse_args()


def normalize_ticker(ticker: str) -> str:
    return ticker.strip().upper()


def detect_asset_type(ticker: str) -> str:
    return "crypto" if normalize_ticker(ticker).endswith(CRYPTO_SUFFIXES) else "stock"


def parse_mapping(raw: str | None) -> dict[str, str]:
    if not raw:
        return {}
    result: dict[str, str] = {}
    for item in raw.split(","):
        if not item.strip():
            continue
        if "=" not in item:
            raise ValueError(f"Expected key=value mapping, got {item!r}")
        key, value = item.split("=", 1)
        result[key.strip()] = value.strip()
    return result


def parse_analysts(raw: str, asset_type: str) -> list[str]:
    analysts = [part.strip().lower() for part in raw.split(",") if part.strip()]
    unknown = [name for name in analysts if name not in ANALYST_ORDER]
    if unknown:
        raise ValueError(f"Unknown analyst(s): {', '.join(unknown)}")
    if not analysts:
        raise ValueError("At least one analyst is required")
    if asset_type == "crypto":
        analysts = [name for name in analysts if name != "fundamentals"]
    return [name for name in ANALYST_ORDER if name in set(analysts)]


def add_project_to_path(project_dir: Path) -> Path:
    project_dir = project_dir.resolve()
    if not project_dir.exists():
        raise FileNotFoundError(f"Project directory does not exist: {project_dir}")
    sys.path.insert(0, str(project_dir))
    return project_dir


def import_default_config(project_dir: Path) -> dict[str, Any]:
    add_project_to_path(project_dir)
    from tradingagents.default_config import DEFAULT_CONFIG

    return DEFAULT_CONFIG


def import_graph(project_dir: Path) -> Any:
    add_project_to_path(project_dir)
    from tradingagents.graph.trading_graph import TradingAgentsGraph

    return TradingAgentsGraph


def apply_overrides(config: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    updates = {
        "llm_provider": args.provider,
        "quick_think_llm": args.quick_model,
        "deep_think_llm": args.deep_model,
        "backend_url": args.backend_url,
        "output_language": args.output_language,
        "max_debate_rounds": args.debate_rounds,
        "max_risk_discuss_rounds": args.risk_rounds,
        "temperature": args.temperature,
        "results_dir": args.results_dir,
        "data_cache_dir": args.cache_dir,
        "memory_log_path": args.memory_log_path,
    }
    for key, value in updates.items():
        if value is not None:
            config[key] = value
    config["checkpoint_enabled"] = bool(args.checkpoint)

    data_vendors = parse_mapping(args.data_vendors)
    if data_vendors:
        config.setdefault("data_vendors", {}).update(data_vendors)

    tool_vendors = parse_mapping(args.tool_vendors)
    if tool_vendors:
        config.setdefault("tool_vendors", {}).update(tool_vendors)

    return config


def render_markdown(ticker: str, trade_date: str, asset_type: str, final_state: dict[str, Any], decision: Any) -> str:
    lines = [
        f"# TradingAgents Analysis: {ticker}",
        "",
        f"Analysis date: {trade_date}",
        f"Asset type: {asset_type}",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        "Disclaimer: Research analysis only; not financial advice.",
        "",
    ]

    analyst_sections = [
        ("Market Analyst", "market_report"),
        ("Sentiment Analyst", "sentiment_report"),
        ("News Analyst", "news_report"),
        ("Fundamentals Analyst", "fundamentals_report"),
    ]
    if any(final_state.get(key) for _, key in analyst_sections):
        lines.append("## I. Analyst Team Reports")
        for title, key in analyst_sections:
            if final_state.get(key):
                lines.extend(["", f"### {title}", str(final_state[key]).strip()])
        lines.append("")

    debate = final_state.get("investment_debate_state") or {}
    if debate:
        lines.append("## II. Research Team Decision")
        for title, key in (
            ("Bull Researcher", "bull_history"),
            ("Bear Researcher", "bear_history"),
            ("Research Manager", "judge_decision"),
        ):
            if debate.get(key):
                lines.extend(["", f"### {title}", str(debate[key]).strip()])
        lines.append("")

    if final_state.get("trader_investment_plan"):
        lines.extend([
            "## III. Trading Team Plan",
            "",
            "### Trader",
            str(final_state["trader_investment_plan"]).strip(),
            "",
        ])

    risk = final_state.get("risk_debate_state") or {}
    if risk:
        lines.append("## IV. Risk Management Team Decision")
        for title, key in (
            ("Aggressive Analyst", "aggressive_history"),
            ("Conservative Analyst", "conservative_history"),
            ("Neutral Analyst", "neutral_history"),
        ):
            if risk.get(key):
                lines.extend(["", f"### {title}", str(risk[key]).strip()])
        lines.append("")

    final_decision = risk.get("judge_decision") or final_state.get("final_trade_decision")
    if final_decision:
        lines.extend([
            "## V. Portfolio Manager Decision",
            "",
            "### Portfolio Manager",
            str(final_decision).strip(),
            "",
        ])

    lines.extend(["## Extracted Decision", "", str(decision).strip(), ""])
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    ticker = normalize_ticker(args.ticker)
    datetime.strptime(args.date, "%Y-%m-%d")
    asset_type = detect_asset_type(ticker) if args.asset_type == "auto" else args.asset_type
    analysts = parse_analysts(args.analysts, asset_type)

    project_dir = Path(args.project_dir)
    DEFAULT_CONFIG = import_default_config(project_dir)
    config = apply_overrides(copy.deepcopy(DEFAULT_CONFIG), args)

    plan = {
        "ticker": ticker,
        "date": args.date,
        "asset_type": asset_type,
        "analysts": analysts,
        "provider": config.get("llm_provider"),
        "quick_model": config.get("quick_think_llm"),
        "deep_model": config.get("deep_think_llm"),
        "results_dir": config.get("results_dir"),
        "cache_dir": config.get("data_cache_dir"),
        "checkpoint_enabled": config.get("checkpoint_enabled"),
    }

    if args.dry_run:
        print(json.dumps({"dry_run": True, "plan": plan}, indent=2, ensure_ascii=False))
        return 0

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    TradingAgentsGraph = import_graph(project_dir)
    graph = TradingAgentsGraph(
        selected_analysts=analysts,
        debug=args.debug,
        config=config,
    )
    final_state, decision = graph.propagate(ticker, args.date, asset_type=asset_type)

    json_path = Path(args.json_out) if args.json_out else output_dir / f"{ticker}_{args.date}_state.json"
    markdown_path = Path(args.markdown_out) if args.markdown_out else output_dir / f"{ticker}_{args.date}_report.md"
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)

    with json_path.open("w", encoding="utf-8") as f:
        json.dump(
            {"plan": plan, "decision": decision, "final_state": final_state},
            f,
            indent=2,
            ensure_ascii=False,
            default=str,
        )

    markdown_path.write_text(
        render_markdown(ticker, args.date, asset_type, final_state, decision),
        encoding="utf-8",
    )

    print(json.dumps({"json": str(json_path), "markdown": str(markdown_path), "decision": decision}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
