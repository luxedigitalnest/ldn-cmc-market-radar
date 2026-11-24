# LDN Crypto Market Radar — keyless CoinMarketCap proof of concept

**Status:** runnable, offline-testable, based on the official CoinMarketCap Keyless Public API. Source observations from a real browser API response at `2026-11-20T14:26:22.165Z`. **Submitted to CoinMarketCap Round 2 as [DoraHacks BUIDL #51492](https://dorahacks.io/build/51492); Under Review independently confirmed on 25 November 2026 CET. No award, financial advice or trading.**

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

**Hackathon submission verified.** The [official event Builds page](https://dorahacks.io/hackathon/coinmarketcap-api-202611/build) shows the existing LDN Crypto Market Radar entry as Under Review. The repository, demo, original X announcement and submission details are linked in the dossier. Most stated prizes are **API plans or merchandise, not cash**; no prize is guaranteed. Don't invent an account or sign in without owner approval. On 25 November CET, a fresh direct browser call to the documented keyless endpoint returned HTTP 200, CMC error code `0`, ten listings and ten numeric USD price quotes; CMC's source timestamp was `2026-11-24T23:41:26.037Z`. This confirms the public endpoint response, not a new live-browser dashboard or an account-specific Pro API key.

## Data safety

- No keys, authentication, wallet access, transfers, deposits, or private data.
- CMC keyless API is rate-limited; 429 retries are bounded and exponential.
- Treat inputs as untrusted. HTML rendering escapes values.
- Not the full market; top-N sample selection and stablecoin heuristics bias breadth.
- Stated BTC cap ratio is **sample** dominance only, not official CMC total-market dominance.
- JSON fixture was faithfully transcribed from the browser-visible public CMC API response. It contains only public market data; no login or keys.

## Public demonstration

- [Read-only GitHub Pages dashboard](https://luxedigitalnest.github.io/ldn-cmc-market-radar/) — a historical 20 November 2026 API snapshot, **not a live price feed**.
- Ten automated unit tests are available locally with `python -m unittest discover -s tests -v`. No GitHub Actions workflow is configured in this repository at this checkpoint; run the offline suite locally.

The submitted project remains under review. The original historical dashboard and recorded video remain unchanged; GitHub deployment and submission do not imply judging acceptance or a prize.

## Round 2 hackathon dossier

See [evidence-first submission pack and readiness checklist](HACKATHON_SUBMISSION.md). The dossier records the confirmed original entry, evidence and outstanding limitations.

## CMC Round 2 demo video (actual browser capture)

[Watch the 72-second original project demonstration](media/LDN_Crypto_Market_Radar_Genuine_Demo.mp4). It shows the real local generated dashboard, the recorded 2026-11-20 CMC data snapshot, and actual Python unit-test output. No live browser API call, award, or trading transaction is implied.

The reproducible recording pipeline is in [make_actual_demo.py](make_actual_demo.py), with offline replay and test verification; the male narration uses the built-in Windows Speech API in [make_narration.ps1](make_narration.ps1).

