# Build with CMC — Round 2 submission dossier

**Project:** LDN Crypto Market Radar  
**Team:** LuxeDigitalNest (independent builder)  
**Track:** Data and Visualisation  
**Status (2026-11-21):** Public, working historical-data demonstration and source code; **NOT YET REGISTERED OR SUBMITTED** to the CoinMarketCap Round 2 DoraHacks hackathon. No award claimed.

## Project summary (submission-ready draft)

LDN Crypto Market Radar is a small, open-source, reproducible market-breadth research tool built around the official CoinMarketCap Keyless Public API. Instead of implying that top-coin prices constitute financial advice, it calculates an explicitly sample-based market view: the proportion of non-stablecoin assets up or down over the previous 24 hours, median daily change, asset ranking and a BTC market-cap share *within the fetched sample*. It can fetch a current API response through a Python standard-library CLI, or replay a saved authentic API response to make testing and reviewing deterministic.

The published GitHub Pages demo is a timestamped **20 November 2026 snapshot**, not a live browser feed. For current data, run the CLI on a machine with internet access.

## Links

- Source: https://github.com/luxedigitalnest/ldn-cmc-market-radar
- Published historical sample demo: https://luxedigitalnest.github.io/ldn-cmc-market-radar/
- Original recorded API response (public data): https://github.com/luxedigitalnest/ldn-cmc-market-radar/blob/main/examples/live_10_coinmarketcap_2026-11-20.json
- Browser-ready verified sample HTML: https://github.com/luxedigitalnest/ldn-cmc-market-radar/blob/main/demo_verified_10.html
- Official challenge: https://coinmarketcap.com/api/resources/api-hackathon-2026-11/
- DoraHacks event: https://dorahacks.io/hackathon/coinmarketcap-api-202611
- DoraHacks build entry: https://dorahacks.io/hackathon/coinmarketcap-api-202611/build

## Exact CMC API usage

Provider: CoinMarketCap **Keyless Public API**.  
Endpoint: `GET https://pro-api.coinmarketcap.com/public-api/v3/cryptocurrency/listings/latest?start=1&limit=50&convert=USD`

For the saved reproducible ten-coin example, `limit=10`. Source timestamps are read from the actual API response's `status.timestamp`. Input response shape and numeric fields are checked; malformed or unavailable data raises an explicit error. The JSON fixture is a historical source observation, not a simulated or predicted price feed. No API keys are stored or required by this implementation.

### Reproduce with no API credentials

Python 3.10+ standard library:

```sh
python -m unittest discover -s tests -v
python cmc_market_radar.py --from-json examples/live_10_coinmarketcap_2026-11-20.json --out offline_demo.html
```

To request **fresh** CMC data (internet and available public endpoint required):

```sh
python cmc_market_radar.py --limit 50 --out latest_cmc_market_radar.html
```

Open the generated HTML file in a browser. Tests cover response parsing, missing/invalid values, breadth calculations and HTML rendering. These commands describe how to reproduce; they are **not** a claim that the entire test suite was rerun during this dossier update.

## Why this is useful

Market-breadth snapshots often hide their selection bias. This demo makes the sample definition, stablecoin heuristics and source timestamp explicit. It uses a read-only data path; there is no trading, wallet custody or investment advice.

## What the API enables, and where it gets in the way

**Made possible:** a simple top-asset data feed with USD price, capitalization and daily price-change fields, so the project does not rely on hand-entered figures. The saved response allows offline independent verification.

**Limits / product feedback:** the keyless endpoint is rate-limited; network, data-shape and missing-value errors need clear handling. The deployed static Pages dashboard intentionally serves a dated snapshot. A direct cross-origin browser request from GitHub Pages was **not confirmed to work** (a browser-side `TypeError: Failed to fetch` occurred on 21 Nov), so no false “refresh live” button was added. For a live public web experience without leaking credentials, a reliable server-side proxy with explicit quotas and caching would be needed. Sample-based BTC market-cap share must not be labeled official market dominance.

## Honest readiness checklist (as of Nov 21, 2026)

- [x] Original public GitHub repository and readable code
- [x] Original CMC keyless API endpoint identified in source and README
- [x] Actual timestamped API response fixture with real response fields
- [x] Published GitHub Pages demonstration of historical snapshot
- [x] Local reproduction and unit-test commands
- [ ] Verify the target CMC account email for temporary Startup API access
- [ ] Register existing @luxedigitalnest DoraHacks account for **CMC Round 2**, confirm registration receipt
- [ ] If the judges require an **account-specific Pro API key**, implement a *server-side, secret-protected* call; never publish the key. Do not misrepresent the keyless API as the authenticated Pro API.
- [ ] Capture an original, audible/readable, short screencast showing the code, one real API response, and the working rendered dashboard
- [ ] Create the DoraHacks BUIDL draft and obtain a public submission URL
- [ ] Publish one original X post linking the **actual DoraHacks submission and demo recording**, tagged `#BuildwithCMC`; copy its verified URL into DoraHacks
- [ ] Submit and verify DoraHacks receipt before the organizer's stricter **2026-12-09 23:59 UTC** deadline (DoraHacks displays 19:00 UTC−5, exactly 2026-12-10 00:00 UTC; do not rely on that extra minute)
- [ ] Record final entry link, submitted status and judged result, without inventing prizes

**Prizes:** The headline value is mainly API subscriptions and physical merchandise, not a $10,000 cash prize. Registration alone does not imply a prize or an accepted entry.

## Suggested DoraHacks short description

> An open-source CoinMarketCap-powered research dashboard and reproducible Python CLI showing **market breadth and median change within a clearly disclosed top-asset sample**. It provides a timestamped real API data fixture, robust input validation, source attribution, and a static proof-of-concept demo. It intentionally avoids trading advice, wallet permissions, and mislabeling sample statistics as whole-market indicators.
