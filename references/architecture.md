# TradingAgents Architecture Reference

Use this reference when explaining or reproducing the project workflow.

## Entry Points

- `tradingagents` console script maps to `cli.main:app`.
- `python -m cli.main` launches the same Typer CLI.
- Programmatic usage imports `TradingAgentsGraph` and calls `propagate(ticker, trade_date, asset_type="stock")`.

## Core Orchestrator

`TradingAgentsGraph` initializes:

- config from `DEFAULT_CONFIG`
- global dataflow config via `set_config(config)`
- results/cache directories
- deep and quick LLM clients via `create_llm_client`
- persistent decision memory via `TradingMemoryLog`
- LangGraph tool nodes for market, social, news, and fundamentals tools
- graph setup, propagation, reflection, and signal processing helpers

The main call path is:

1. `TradingAgentsGraph.propagate()`
2. `_resolve_pending_entries()` for prior same-ticker decisions
3. optional checkpoint setup
4. `_run_graph()`
5. `Propagator.create_initial_state()`
6. LangGraph invoke/stream
7. `_log_state()` to JSON
8. `memory_log.store_decision()`
9. `process_signal()` to extract the final decision

## Graph Order

The LangGraph workflow is:

1. Selected analyst nodes in configured order:
   - `market`
   - `social`
   - `news`
   - `fundamentals`
2. Bull Researcher
3. Bear Researcher
4. Research Manager
5. Trader
6. Aggressive Analyst
7. Conservative Analyst
8. Neutral Analyst
9. Portfolio Manager

Each analyst can call its tool node until conditional logic routes through its clear-message node. Research and risk teams debate for the configured number of rounds, then managers judge.

## Data Tools

Tool nodes map to:

- Market: `get_stock_data`, `get_indicators`
- Social: `get_news`
- News: `get_news`, `get_global_news`, `get_insider_transactions`
- Fundamentals: `get_fundamentals`, `get_balance_sheet`, `get_cashflow`, `get_income_statement`

Vendor routing lives in `tradingagents/dataflows/interface.py`. Supported vendors are `yfinance` and `alpha_vantage`; category defaults come from `DEFAULT_CONFIG["data_vendors"]`, and per-tool overrides come from `DEFAULT_CONFIG["tool_vendors"]`.

## Output Contracts

The final state includes:

- `market_report`
- `sentiment_report`
- `news_report`
- `fundamentals_report`
- `investment_debate_state`
- `investment_plan`
- `trader_investment_plan`
- `risk_debate_state`
- `final_trade_decision`

Structured decision agents render markdown back from Pydantic schemas:

- Research Manager: rating plus rationale and strategic actions.
- Trader: `Buy`, `Hold`, or `Sell`, ending with `FINAL TRANSACTION PROPOSAL: **...**`.
- Portfolio Manager: final five-tier rating, executive summary, investment thesis, optional price target, optional time horizon.

## Persistence

The project writes:

- full state JSON under `<results_dir>/<ticker>/TradingAgentsStrategy_logs/full_states_log_<date>.json`
- CLI report folders under the selected report directory
- decision memory to `~/.tradingagents/memory/trading_memory.md` unless overridden
- optional checkpoints under `~/.tradingagents/cache/checkpoints/<ticker>.db`
