#!/usr/bin/env python3
"""LuxeDigitalNest / CMC Market Radar.

A no-wallet, no-API-key CLI for viewing CoinMarketCap Keyless Public API market breadth.
Only reads public information and writes local JSON/HTML files.
Not financial advice and not a trading bot.
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import math
import pathlib
import statistics
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = "https://pro-api.coinmarketcap.com/public-api"
ENDPOINT = "/v3/cryptocurrency/listings/latest"
STABLECOINS = {
    "USDT", "USDC", "DAI", "FDUSD", "USDE", "USDD", "TUSD", "PYUSD",
    "USDP", "USD1", "RLUSD", "EURC", "FRAX", "EURCV", "SUSD", "GUSD",
}


def _number(value):
    """Return a finite float or None; reject booleans and missing values."""
    if value is None or isinstance(value, bool):
        return None
    try:
        out = float(value)
    except (TypeError, ValueError, OverflowError):
        return None
    return out if math.isfinite(out) else None


def get_keyless_listings(limit=100, fetcher=None, attempts=3):
    """Fetch 10–100 public listings. Only rate-limit/server errors retry."""
    if not isinstance(limit, int) or not (10 <= limit <= 100):
        raise ValueError("Limit must be an integer between 10 and 100")
    if fetcher is None:
        fetcher = urllib.request.urlopen
    qs = urllib.parse.urlencode({"start": 1, "limit": limit, "convert": "USD"})
    url = f"{BASE_URL}{ENDPOINT}?{qs}"
    request = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "LDN-MarketRadar/0.1 (+research demo)"})
    for n in range(attempts):
        try:
            with fetcher(request, timeout=20) as response:
                payload = json.load(response)
            status = payload.get("status", {})
            if str(status.get("error_code", "0")) != "0":
                raise ValueError(f"CMC API error: {status.get('error_code')} {status.get('error_message')}")
            if not isinstance(payload.get("data"), list):
                raise ValueError("CMC returned no listings array")
            return payload
        except urllib.error.HTTPError as err:
            if err.code in (429, 500, 502, 503, 504) and n < attempts - 1:
                time.sleep(2 ** n)
                continue
            raise
    raise RuntimeError("No response")


def _usd_quote(asset):
    quotes = asset.get("quote")
    if isinstance(quotes, list):
        return next((x for x in quotes if isinstance(x, dict) and x.get("symbol") == "USD"), {})
    if isinstance(quotes, dict):
        return quotes.get("USD", {}) if isinstance(quotes.get("USD"), dict) else {}
    return {}


def summarize(payload):
    if not isinstance(payload, dict) or not isinstance(payload.get("data"), list):
        raise ValueError("Expected a CMC object with a data list")
    out = []
    for asset in payload["data"]:
        if not isinstance(asset, dict):
            continue
        q = _usd_quote(asset)
        rank = _number(asset.get("cmc_rank"))
        price = _number(q.get("price"))
        cap = _number(q.get("market_cap"))
        d24 = _number(q.get("percent_change_24h"))
        d7 = _number(q.get("percent_change_7d"))
        volume = _number(q.get("volume_24h"))
        if price is None or cap is None or cap < 0:
            continue
        out.append({
            "name": str(asset.get("name", "Unknown")),
            "symbol": str(asset.get("symbol", "?")),
            "rank": int(rank) if rank is not None else None,
            "price_usd": price,
            "market_cap_usd": cap,
            "volume_24h_usd": volume,
            "change_24h_pct": d24,
            "change_7d_pct": d7,
            "stablecoin_excluded": str(asset.get("symbol", "")).upper() in STABLECOINS,
        })
    if not out:
        raise ValueError("No valid USD quoted assets")
    tradeable = [a for a in out if not a["stablecoin_excluded"] and a["change_24h_pct"] is not None]
    if not tradeable:
        raise ValueError("No non-stablecoin assets have 24h changes")
    positives = sum(a["change_24h_pct"] > 0 for a in tradeable)
    negatives = sum(a["change_24h_pct"] < 0 for a in tradeable)
    flat = len(tradeable) - positives - negatives
    med = statistics.median(a["change_24h_pct"] for a in tradeable)
    means = statistics.mean(a["change_24h_pct"] for a in tradeable)
    total_cap = sum(a["market_cap_usd"] for a in tradeable)
    btc = next((a for a in out if a["symbol"] == "BTC"), None)
    btc_sample_share = 100 * btc["market_cap_usd"] / total_cap if btc and total_cap else None
    ranked = sorted(tradeable, key=lambda a: a["change_24h_pct"])
    # Descriptive classification, never a trading signal.
    if positives / len(tradeable) < 0.25:
        regime = "Broad 24h declines (sample)"
    elif positives / len(tradeable) > 0.75:
        regime = "Broad 24h advances (sample)"
    else:
        regime = "Mixed market breadth (sample)"
    return {
        "title": "LDN CoinMarketCap Market Radar",
        "source": f"{BASE_URL}{ENDPOINT}",
        "source_timestamp_utc": str(payload.get("status", {}).get("timestamp") or "Unknown"),
        "processed_timestamp_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "coverage": {"listings_received": len(payload["data"]), "valid_assets": len(out), "nonstable_with_change": len(tradeable), "excluded_stablecoins": len(out) - len([a for a in out if not a["stablecoin_excluded"]])},
        "breadth": {"up_24h": positives, "down_24h": negatives, "flat_24h": flat, "up_fraction": positives / len(tradeable), "median_change_24h_pct": med, "mean_change_24h_pct": means},
        "btc_sample_cap_share_pct": btc_sample_share,
        "regime_description": regime,
        "decliners": ranked[:5],
        "advancers": list(reversed(ranked[-5:])),
        "assets": sorted(out, key=lambda a: a["rank"] if a["rank"] is not None else 999999),
        "caveats": [
            "This is a top-N sample, NOT the full market. Sample BTC cap share is NOT the official BTC dominance figure.",
            "Stablecoins excluded from breadth by ticker; classification is a heuristic, not a complete peg registry.",
            "Data freshness comes from the original CMC response timestamp; numbers change between calls.",
            "Descriptive tool only; no buy/sell signals, account credentials, positions or order placement.",
        ],
    }


def _fmt_number(x, decimals=2):
    return "—" if x is None else f"{x:,.{decimals}f}"


def render_html(summary):
    def esc(x):
        return html.escape(str(x), quote=True)
    rows = []
    for a in summary["assets"]:
        change = a["change_24h_pct"]
        state = "positive" if change is not None and change > 0 else "negative" if change is not None and change < 0 else "neutral"
        rows.append(f"<tr><td>{esc(a['rank'] or '—')}</td><td><b>{esc(a['symbol'])}</b><small>{esc(a['name'])}</small></td>"
                    f"<td class='num'>${_fmt_number(a['price_usd'], 4)}</td>"
                    f"<td class='num {state}'>{'—' if change is None else f'{change:+.2f}%'}</td>"
                    f"<td class='num'>${_fmt_number(a['market_cap_usd']/1e9)}B</td>"
                    f"<td class='num'>{'Stablecoin' if a['stablecoin_excluded'] else 'Market'}</td></tr>")
    br = summary["breadth"]
    up_pct = br["up_fraction"]*100
    btc_share = "—" if summary["btc_sample_cap_share_pct"] is None else f"{summary['btc_sample_cap_share_pct']:.1f}%"
    caveat = "".join(f"<li>{esc(x)}</li>" for x in summary["caveats"])
    template = """<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>LDN Market Radar</title><style>
:root{color-scheme:dark}body{margin:0;background:#0c111a;color:#e8edf6;font:15px/1.5 system-ui,-apple-system,Segoe UI,sans-serif}
main{max-width:1050px;margin:auto;padding:34px 22px}header{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px}
h1{font-size:27px;margin:4px 0}p,.muted,small{color:#abb7c8}a{color:#8abdf8}.pill{border:1px solid #34465d;border-radius:30px;padding:7px 13px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin:28px 0}.stat{background:#161f2c;border:1px solid #26384c;border-radius:13px;padding:17px}.value{font-size:25px;font-weight:750}.label{font-size:12px;color:#a9b5c5}.positive{color:#69d5a8}.negative{color:#f696a6}
.bar{height:18px;background:#994051;border-radius:12px;overflow:hidden}.bar span{display:block;height:100%;background:#31886b}
.table{overflow-x:auto}table{border-collapse:collapse;width:100%;min-width:650px}th,td{padding:11px;border-bottom:1px solid #2d3848;text-align:left}th{font-size:12px;color:#a9b5c5}td small{display:block;font-size:12px}.num{text-align:right;font-variant-numeric:tabular-nums}section{margin-top:32px}footer{margin-top:28px;font-size:12px;color:#a9b5c5}li{margin:6px 0}
</style></head><body><main><header><div><div class='muted'>LUXEDIGITALNEST / RESEARCH</div><h1>Crypto Market Radar</h1><p>Source timestamp: {TIMESTAMP}</p></div><div class='pill'>CMC Keyless API · read-only</div></header>
<div class='grid'><div class='stat'><div class='label'>Market breadth · up 24h</div><div class='value'>{BREADTH}%</div></div><div class='stat'><div class='label'>Median 24h · ex stablecoins</div><div class='value'>{MEDIAN}%</div></div><div class='stat'><div class='label'>Assets · ex stablecoins</div><div class='value'>{COUNT}</div></div><div class='stat'><div class='label'>BTC share of sampled cap</div><div class='value'>{BTC}</div></div></div>
<section><h2>{REGIME}</h2><div class='bar'><span style='width:{BAR}%'></span></div><p>{UP} up · {DOWN} down · {FLAT} flat. This is a sample, not a trade recommendation.</p></section>
<section><h2>Observed assets</h2><div class='table'><table><thead><tr><th>#</th><th>Coin</th><th class='num'>Price (USD)</th><th class='num'>24h</th><th class='num'>Market cap</th><th class='num'>Type</th></tr></thead><tbody>{ROWS}</tbody></table></div></section>
<section><h2>Data limitations</h2><ul>{CAVEATS}</ul></section><footer>CoinMarketCap API source: <a href='{SOURCE}'>{SOURCE}</a>. Generated locally. No wallet or API key used.</footer></main></body></html>"""
    for k, v in {
        "TIMESTAMP":esc(summary["source_timestamp_utc"]),"BREADTH":f"{up_pct:.1f}",
        "MEDIAN":f"{br['median_change_24h_pct']:+.2f}","COUNT":str(summary["coverage"]["nonstable_with_change"]),
        "BTC":btc_share,"REGIME":esc(summary["regime_description"]),"BAR":f"{up_pct:.1f}",
        "UP":str(br["up_24h"]),"DOWN":str(br["down_24h"]),"FLAT":str(br["flat_24h"]),
        "ROWS":"\n".join(rows),"CAVEATS":caveat,"SOURCE":esc(summary["source"])
    }.items():
        template=template.replace("{"+k+"}",v)
    return template


def main(argv=None):
    ap=argparse.ArgumentParser(description="Read-only, no-key CMC market breadth report")
    ap.add_argument("--limit",type=int,default=50,help="Number of largest coins, between 10 and 100")
    ap.add_argument("--out",default="cmc_radar.html",help="HTML output file")
    ap.add_argument("--from-json",default=None,help="Replay a saved CMC response (does not connect to web)")
    args=ap.parse_args(argv)
    try:
        payload=json.loads(pathlib.Path(args.from_json).read_text(encoding="utf8")) if args.from_json else get_keyless_listings(args.limit)
        report=summarize(payload)
        path=pathlib.Path(args.out)
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(render_html(report),encoding="utf-8")
        path.with_suffix(".json").write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding="utf-8")
        print(f"Saved {path} and {path.with_suffix('.json')} from CMC timestamp {report['source_timestamp_utc']}")
    except (ValueError,urllib.error.URLError,OSError,TypeError) as ex:
        print(f"Cannot generate verified report: {ex}",file=sys.stderr)
        return 1
    return 0


if __name__=="__main__":
    raise SystemExit(main())
