# stock-price-fetcher

A zero-infrastructure, self-updating daily market data pipeline. A GitHub
Actions workflow runs every US trading day after market close, pulls the
latest closing price via [yfinance](https://github.com/ranaroussi/yfinance),
and commits it straight back into this repo -- no server, no database, no
cloud account, no cron job to babysit. The data just accumulates in
version-controlled history, one commit per trading day, forever.

Currently tracks: **QQQM** (Invesco NASDAQ 100 ETF).

> Data is sourced via the unofficial, open-source [`yfinance`](https://github.com/ranaroussi/yfinance)
> library for personal/educational use. This project is not affiliated with
> or endorsed by Yahoo Finance.

## Why this exists

Most personal trading/quant projects either pay for a market data API or
depend on a script you have to remember to run yourself. This repo is the
free, boring, always-on alternative: GitHub's own compute and cron
infrastructure does the fetching, GitHub's own storage (git history) does
the persistence, and the only "infra" is a public repo. Anyone -- including
downstream tools that just need daily closing prices -- can `git pull` this
repo and get an always-current, fully-auditable price history with a commit
log showing exactly when each data point was captured.

## What's in here

- `market_data.json` -- the accumulated price history. Each entry is
  strictly `{"date": "YYYY-MM-DD", "close": <float>}`. Nothing else lives in
  this file, ever -- no personal data, no account info, no positions. That's
  a deliberate boundary: this repo is a dumb, public, reusable data source,
  decoupled from anything private that might consume it.
- `fetch_price.py` -- the fetch/append logic. Idempotent: safe to re-run,
  skips dates already recorded, and catches up automatically on any missed
  trading day (it always checks the last 5 days, not just "today").
- `.github/workflows/fetch_price.yml` -- the schedule. Runs Mon-Fri after
  the US market close, with a manual trigger available too.

## Extending it

The fetch/append pattern here isn't QQQM-specific -- swap the ticker, add a
loop over multiple tickers, or track additional fields (volume, dividends)
without changing the underlying design: fetch, dedupe by date, append,
commit only if something actually changed. The same zero-infrastructure
pattern scales to tracking an entire watchlist just as easily as one ticker.
