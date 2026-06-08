---
name: tradingagents-analysis
description: Use when Codex needs to perform or reproduce TradingAgents-style multi-agent financial market analysis with the current Codex model, without launching the interactive TradingAgents project or selecting another LLM model. Supports ticker/date trading decisions, stock or crypto analysis, analyst/research/trader/risk/portfolio report generation, running a TradingAgents checkout programmatically when explicitly requested, or producing a standalone TradingAgents-like report from fresh market/news evidence.
---

# TradingAgents Analysis

## Goal

Use this skill to produce the main TradingAgents result without starting the interactive CLI: a multi-stage market analysis and final portfolio decision for a ticker/date.

TradingAgents is research software, not financial advice. Always state that outputs are analytical/research material and not a recommendation to trade real money.

## Model Policy

Use the current Codex model to perform the standalone/manual TradingAgents-style workflow. Do not suggest, select, or pass another model such as Qwen, GPT, Claude, Gemini, or provider-specific model IDs unless the user explicitly asks to run the actual TradingAgents checkout with a specific runtime provider/model configuration.

When using the bundled runner, omit `--provider`, `--quick-model`, and `--deep-model` by default. Those flags exist only for explicit project-runtime configuration, not for ordinary skill use.

## Choose The Execution Path

1. If a TradingAgents checkout or installed package is available and the user wants an actual project run, use `scripts/run_tradingagents_analysis.py`.
2. If the user wants a report but no checkout/API keys/runtime is available, reproduce the workflow manually with current market, fundamentals, technical, sentiment, and news evidence.
3. If the user asks how the project works, read `references/architecture.md`.
4. If the user asks about configuration, providers, tickers, outputs, or persistence, read `references/configuration.md`.

## Quick Runner

Run a non-interactive analysis from a checkout:

```bash
python ~/.codex/skills/tradingagents-analysis/scripts/run_tradingagents_analysis.py \
  --project-dir /path/to/TradingAgents \
  --ticker NVDA \
  --date 2026-01-15 \
  --analysts market,social,news,fundamentals \
  --output-dir ./tradingagents-output
```

Use `--dry-run` first to validate imports/config without making market or LLM calls:

```bash
python ~/.codex/skills/tradingagents-analysis/scripts/run_tradingagents_analysis.py \
  --project-dir /path/to/TradingAgents \
  --ticker NVDA \
  --date 2026-01-15 \
  --dry-run
```

The runner imports `TradingAgentsGraph`, applies env/config overrides, calls `propagate()`, and writes JSON plus markdown artifacts. Only add provider/model flags when the user explicitly wants the project runtime to call a named external model.

## Manual TradingAgents Workflow

When producing a TradingAgents-like report manually, follow this order:

1. Normalize the instrument:
   - Preserve exchange suffixes such as `0700.HK`, `7203.T`, `RELIANCE.NS`, `600519.SS`.
   - Treat tickers ending in `-USD`, `-USDT`, `-USDC`, `-BTC`, or `-ETH` as crypto.
   - For crypto, skip fundamentals if company fundamentals are unavailable.
2. Gather evidence:
   - Market/technical: recent OHLCV, trend, volatility, volume, support/resistance, momentum indicators when available.
   - Fundamentals: valuation, growth, margins, balance sheet, cash flow, earnings signals for equities.
   - Sentiment: news headlines, social/reddit/StockTwits-like signals when available.
   - Macro/news: sector, rates, regulation, geopolitics, and broad-market context.
3. Produce analyst team reports:
   - Market Analyst
   - Sentiment Analyst
   - News Analyst
   - Fundamentals Analyst for equities only
4. Produce research debate:
   - Bull Researcher: strongest upside case.
   - Bear Researcher: strongest downside case.
   - Research Manager: choose one of `Buy`, `Overweight`, `Hold`, `Underweight`, `Sell`.
5. Produce Trader proposal:
   - Choose `Buy`, `Hold`, or `Sell`.
   - Include reasoning, optional entry price, stop loss, and sizing.
   - End with `FINAL TRANSACTION PROPOSAL: **BUY|HOLD|SELL**`.
6. Produce risk debate:
   - Aggressive Analyst
   - Conservative Analyst
   - Neutral Analyst
7. Produce Portfolio Manager decision:
   - Rating: exactly one of `Buy`, `Overweight`, `Hold`, `Underweight`, `Sell`.
   - Executive summary.
   - Investment thesis.
   - Optional price target and time horizon.

## Output Shape

Use this markdown structure unless the user asks otherwise:

```markdown
# TradingAgents Analysis: <TICKER>

Analysis date: <YYYY-MM-DD>
Asset type: <stock|crypto>
Evidence cutoff: <date/time or source dates>
Disclaimer: Research analysis only; not financial advice.

## I. Analyst Team Reports
### Market Analyst
### Sentiment Analyst
### News Analyst
### Fundamentals Analyst

## II. Research Team Decision
### Bull Researcher
### Bear Researcher
### Research Manager

## III. Trading Team Plan
### Trader

## IV. Risk Management Team Decision
### Aggressive Analyst
### Conservative Analyst
### Neutral Analyst

## V. Portfolio Manager Decision
```

For short answers, include only the final rating, transaction proposal, top evidence, and main risks.

## Configuration Notes

The real project accepts these common environment overrides: `TRADINGAGENTS_LLM_PROVIDER`, `TRADINGAGENTS_DEEP_THINK_LLM`, `TRADINGAGENTS_QUICK_THINK_LLM`, `TRADINGAGENTS_LLM_BACKEND_URL`, `TRADINGAGENTS_OUTPUT_LANGUAGE`, `TRADINGAGENTS_MAX_DEBATE_ROUNDS`, `TRADINGAGENTS_MAX_RISK_ROUNDS`, `TRADINGAGENTS_CHECKPOINT_ENABLED`, `TRADINGAGENTS_BENCHMARK_TICKER`, and `TRADINGAGENTS_TEMPERATURE`.

Common provider API key variables include `OPENAI_API_KEY`, `GOOGLE_API_KEY`, `ANTHROPIC_API_KEY`, `XAI_API_KEY`, `DEEPSEEK_API_KEY`, `DASHSCOPE_API_KEY`, `DASHSCOPE_CN_API_KEY`, `ZHIPU_API_KEY`, `ZHIPU_CN_API_KEY`, `MINIMAX_API_KEY`, `MINIMAX_CN_API_KEY`, `OPENROUTER_API_KEY`, and `ALPHA_VANTAGE_API_KEY`.

Read `references/configuration.md` before changing provider/model/data-vendor behavior.
