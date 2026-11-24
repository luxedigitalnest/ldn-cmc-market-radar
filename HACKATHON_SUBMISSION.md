# Build with CMC — Round 2 submission dossier

**Project:** LDN Crypto Market Radar  
**Team:** LuxeDigitalNest (independent builder)  
**Track:** Data and Visualisation  
**Status (2026-11-21):** Public, working historical-data demonstration and source code; **REGISTERED AND SUBMITTED** to the CoinMarketCap Round 2 DoraHacks hackathon. The official entry is **Under Review**. No award or judging acceptance claimed.

## Project summary (submitted)

LDN Crypto Market Radar is a small, open-source, reproducible market-breadth research tool built around the official CoinMarketCap Keyless Public API. Instead of implying that top-coin prices constitute financial advice, it calculates an explicitly sample-based market view: the proportion of non-stablecoin assets up or down over the previous 24 hours, median daily change, asset ranking and a BTC market-cap share *within the fetched sample*. It can fetch a current API response through a Python standard-library CLI, or replay a saved authentic API response to make testing and reviewing deterministic.

The published GitHub Pages demo is a timestamped **20 November 2026 snapshot**, not a live browser feed. For current data, run the CLI on a machine with internet access.

## Submission confirmation (November 21, 2026)

- **DoraHacks Build (Under Review):** https://dorahacks.io/build/51492
- **Official Round 2 event:** https://dorahacks.io/hackathon/coinmarketcap-api-202611/build
- **Original demo video:** https://github.com/luxedigitalnest/ldn-cmc-market-radar/blob/main/media/LDN_Crypto_Market_Radar_Genuine_Demo.mp4
- **Original X announcement:** https://x.com/LuxeDigitalNest/status/2124085478773182854
- **Confirmation:** authenticated DoraHacks says `Build Submitted!` and `Under Review`; successful event publish-buidl HTTP 200. This is **submission**, not a win.

## Links

- Source: https://github.com/luxedigitalnest/ldn-cmc-market-radar
- Published historical sample demo: https://luxedigitalnest.github.io/ldn-cmc-market-radar/
- Original recorded API response (public data): https://github.com/luxedigitalnest/ldn-cmc-market-radar/blob/main/examples/live_10_coinmarketcap_2026-11-20.json
- Browser-ready verified sample HTML: https://github.com/luxedigitalnest/ldn-cmc-market-radar/blob/main/demo_verified_10.html
- Official challenge: https://coinmarketcap.com/api/resources/api-hackathon-2026-11/
- DoraHacks event: https://dorahacks.io/hackathon/coinmarketcap-api-202611
- DoraHacks build entry: https://dorahacks.io/hackathon/coinmarketcap-api-202611/build

## 25 November 2026 CET verification

The signed-in [official event Builds page](https://dorahacks.io/hackathon/coinmarketcap-api-202611/build) lists BUIDL #51492 as **Under Review**. A direct browser GET to the ten-listing keyless endpoint returned HTTP 200, CMC error code `0`, ten listings and ten finite numeric USD price quotes in the quote arrays. CMC source timestamp: `2026-11-24T23:41:26.037Z`. This was a read-only endpoint check; the existing static Pages dashboard and original video were not refreshed, no API key or reward was obtained, and no new submission was made.

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
- [x] Match the registered CMC API account email to the event registration. Startup-tier promotional upgrade remains unverified.
- [x] Register existing @luxedigitalnest DoraHacks account for **CMC Round 2**, confirmation from authenticated event UI and HTTP 200
- [ ] If the judges require an **account-specific Pro API key**, implement a *server-side, secret-protected* call; never publish the key. Do not misrepresent the keyless API as the authenticated Pro API.
- [x] Produce original 72-second browser-capture video with actual data replay, rendered dashboard and 10 passing tests; male synthetic narration (Microsoft David), no third-party music
- [x] Create public DoraHacks BUIDL at https://dorahacks.io/build/51492 including GitHub, GitHub Pages and original video
- [x] Publish the original @LuxeDigitalNest X post linking the BUIDL and demo video, tagged `#BuildwithCMC`; verify post URL https://x.com/LuxeDigitalNest/status/2124085478773182854
- [x] Submit BUIDL under **Data and Visualisation** and verify DoraHacks response **Build Submitted! / Under Review**, HTTP 200 (November 21, 2026), ahead of the organizer's Dec 9 deadline.
- [x] Record final entry link and submitted/Under Review status, with independent GitHub and X evidence.
- [ ] Await judging/award decision: no prize, ranking, or prize eligibility has yet been verified.

**Prizes:** The headline value is mainly API subscriptions and physical merchandise, not a $10,000 cash prize. Registration alone does not imply a prize or an accepted entry.

## Suggested DoraHacks short description

> An open-source CoinMarketCap-powered research dashboard and reproducible Python CLI showing **market breadth and median change within a clearly disclosed top-asset sample**. It provides a timestamped real API data fixture, robust input validation, source attribution, and a static proof-of-concept demo. It intentionally avoids trading advice, wallet permissions, and mislabeling sample statistics as whole-market indicators.
