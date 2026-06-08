# Trading Analysis Skills

TradingAgents-style multi-agent financial analysis as an installable agent skill.

This repository packages the `tradingagents-analysis` skill. It lets Codex or another compatible agent reproduce the main TradingAgents workflow without launching the interactive TradingAgents CLI: analyst reports, bull/bear research debate, trader proposal, risk debate, and final portfolio decision.

> Research analysis only. This skill is not financial, investment, or trading advice.

## Install

Install with the open skills CLI:

```bash
npx skills add zhengliu92/TradingAnalysisSkills
```

Install globally:

```bash
npx skills add zhengliu92/TradingAnalysisSkills -g
```

List available skills in this repository:

```bash
npx skills add zhengliu92/TradingAnalysisSkills --list
```

## Use

Ask your agent to use the skill:

```text
Use $tradingagents-analysis to analyze NVDA for 2026-01-15 with the current Codex model and write a concise trading decision.
```

The skill defaults to the model already running your agent. It does not ask the agent to switch to Qwen, OpenAI, Claude, Gemini, or another provider-specific model.

## What It Provides

- A root `SKILL.md` with the TradingAgents-style workflow.
- `references/architecture.md` for the TradingAgents graph, data tools, and output contracts.
- `references/configuration.md` for tickers, asset types, environment variables, providers, and persistence.
- `scripts/run_tradingagents_analysis.py` for optional non-interactive execution against a local TradingAgents checkout.
- `agents/openai.yaml` metadata for compatible skill UIs.

## Optional Project Runtime

For ordinary skill use, the current agent model performs the analysis directly.

If you explicitly want to run a real TradingAgents checkout, use the bundled runner:

```bash
python scripts/run_tradingagents_analysis.py \
  --project-dir /path/to/TradingAgents \
  --ticker NVDA \
  --date 2026-01-15 \
  --analysts market,social,news,fundamentals \
  --output-dir ./tradingagents-output
```

Dry-run first:

```bash
python scripts/run_tradingagents_analysis.py \
  --project-dir /path/to/TradingAgents \
  --ticker NVDA \
  --date 2026-01-15 \
  --dry-run
```

Only pass `--provider`, `--quick-model`, or `--deep-model` when you explicitly want the TradingAgents project runtime to call a named external model.

## Skill Structure

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── architecture.md
│   └── configuration.md
└── scripts/
    └── run_tradingagents_analysis.py
```

## Development

Validate the skill:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run --no-project --with pyyaml \
  python ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
```

Compile the helper script:

```bash
python -m py_compile scripts/run_tradingagents_analysis.py
rm -rf scripts/__pycache__
```

## License

MIT
