# LDN Crypto Market Radar — keyless CoinMarketCap proof of concept

**Status:** runnable, offline-testable, based on the official CoinMarketCap Keyless Public API. Source observations from a real browser API response at `2026-11-20T14:26:22.165Z`. **Not submitted to any hackathon, not awarded, not financial advice, and does not trade.**

## What it does

- Fetches 10–100 top crypto assets using the official no-API-key CMC endpoint.
- Validates response shape and reports API failures instead of inventing prices.
- Computes 24-hour market breadth excluding known stablecoin tickers, median price change, worst/best sample performers, and BTC market-cap share **within the sample**.
- Generates a standalone HTML dashboard with escaped, source-attributed data and JSON output, without a wallet or paid account.
- Supports exact-data replay from a saved CMC response to keep demos reproducible.

## Install and run

Requires Python 3.10+ with standard library only; an internet connection for live queries.

```powershell
python cmc_market_radar.py --limit 50 --out cmc_radar.html
# Open cmc_radar.html locally in any browser.
```

To replay an **actual ten-coin browser response** captured on 20 November 2026 (these numbers are historical, not live):

```powershell
python cmc_market_radar.py --from-json examples/live_10_coinmarketcap_2026-11-20.json --out demo_verified_10.html
```

Run all offline tests:

```powershell
python -m unittest discover -s tests -v
```

## Source of truth

Official docs: https://coinmarketcap.com/api/documentation/pro-api-reference/keyless-public-api

Public endpoint: https://pro-api.coinmarketcap.com/public-api/v3/cryptocurrency/listings/latest?start=1&limit=50&convert=USD

CMC API Hackathon Round 2: https://coinmarketcap.com/api/resources/api-hackathon-2026-11/

**Hackathon not submitted.** Official rules require a public GitHub repository, a working demonstration, visible proof of a real CMC API call, API endpoint declaration, an original X post with #BuildwithCMC, and a DoraHacks application. Most stated prizes are **API plans or merchandise, not cash**; no prize is guaranteed. Don't invent an account or sign in without owner approval. Further development can add a verified live API demo video and improve analytics before review.

## Data safety

- No keys, authentication, wallet access, transfers, deposits, or private data.
- CMC keyless API is rate-limited; 429 retries are bounded and exponential.
- Treat inputs as untrusted. HTML rendering escapes values.
- Not the full market; top-N sample selection and stablecoin heuristics bias breadth.
- Stated BTC cap ratio is **sample** dominance only, not official CMC total-market dominance.
- JSON fixture was faithfully transcribed from the browser-visible public CMC API response. It contains only public market data; no login or keys.
