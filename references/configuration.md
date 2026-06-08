# TradingAgents Configuration Reference

Use this reference for provider, ticker, environment, output, and persistence questions.

## Contents

- [Defaults](#defaults)
- [Environment Overrides](#environment-overrides)
- [Providers And Keys](#providers-and-keys)
- [Tickers And Asset Types](#tickers-and-asset-types)
- [Output Language](#output-language)
- [Benchmarks](#benchmarks)

## Defaults

`DEFAULT_CONFIG` includes:

- `llm_provider`: `openai`
- `deep_think_llm`: `gpt-5.5`
- `quick_think_llm`: `gpt-5.4-mini`
- `output_language`: `English`
- `max_debate_rounds`: `1`
- `max_risk_discuss_rounds`: `1`
- `analyst_concurrency_limit`: `1`
- `data_vendors`: yfinance for stock, indicators, fundamentals, and news
- `results_dir`: `~/.tradingagents/logs`
- `data_cache_dir`: `~/.tradingagents/cache`
- `memory_log_path`: `~/.tradingagents/memory/trading_memory.md`

## Environment Overrides

The project applies these `TRADINGAGENTS_*` variables directly to config:

- `TRADINGAGENTS_LLM_PROVIDER`
- `TRADINGAGENTS_DEEP_THINK_LLM`
- `TRADINGAGENTS_QUICK_THINK_LLM`
- `TRADINGAGENTS_LLM_BACKEND_URL`
- `TRADINGAGENTS_OUTPUT_LANGUAGE`
- `TRADINGAGENTS_MAX_DEBATE_ROUNDS`
- `TRADINGAGENTS_MAX_RISK_ROUNDS`
- `TRADINGAGENTS_CHECKPOINT_ENABLED`
- `TRADINGAGENTS_BENCHMARK_TICKER`
- `TRADINGAGENTS_TEMPERATURE`

The path variables are handled separately:

- `TRADINGAGENTS_RESULTS_DIR`
- `TRADINGAGENTS_CACHE_DIR`
- `TRADINGAGENTS_MEMORY_LOG_PATH`

## Providers And Keys

Supported provider keys include:

- `openai`
- `google`
- `anthropic`
- `xai`
- `deepseek`
- `qwen`
- `qwen-cn`
- `glm`
- `glm-cn`
- `minimax`
- `minimax-cn`
- `openrouter`
- `ollama`
- `azure`

Common API key variables:

- `OPENAI_API_KEY`
- `GOOGLE_API_KEY`
- `ANTHROPIC_API_KEY`
- `XAI_API_KEY`
- `DEEPSEEK_API_KEY`
- `DASHSCOPE_API_KEY`
- `DASHSCOPE_CN_API_KEY`
- `ZHIPU_API_KEY`
- `ZHIPU_CN_API_KEY`
- `MINIMAX_API_KEY`
- `MINIMAX_CN_API_KEY`
- `OPENROUTER_API_KEY`
- `ALPHA_VANTAGE_API_KEY`

Ollama does not require a provider API key. Use `OLLAMA_BASE_URL` or `TRADINGAGENTS_LLM_BACKEND_URL` for a non-default endpoint.

## Tickers And Asset Types

The CLI preserves exchange suffixes and uppercases input:

- US: `AAPL`, `SPY`
- Hong Kong: `0700.HK`
- Tokyo: `7203.T`
- London: `AZN.L`
- India: `RELIANCE.NS`, `.BO`
- Canada: `.TO`
- Australia: `.AX`
- China A-shares: `.SS`, `.SZ`
- Crypto: `BTC-USD`, `ETH-USD`

Tickers ending in `-USD`, `-USDT`, `-USDC`, `-BTC`, or `-ETH` are treated as crypto. For crypto, fundamentals are normally omitted.

## Output Language

`output_language` controls analyst reports and final decision language. Internal debate remains optimized for model reasoning. The CLI offers English, Chinese, Japanese, Korean, Hindi, Spanish, Portuguese, French, German, Arabic, Russian, and custom language names.

## Benchmarks

If `benchmark_ticker` is set, it overrides all automatic benchmark detection. Otherwise the suffix map picks regional benchmarks such as `^HSI` for `.HK`, `^N225` for `.T`, `^NSEI` for `.NS`, and `SPY` for US/no suffix.
