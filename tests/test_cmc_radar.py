import io
import json
import pathlib
import sys
import unittest
from unittest.mock import patch
import urllib.error

sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from cmc_market_radar import STABLECOINS, _number, get_keyless_listings, render_html, summarize


def sample():
    return {"status":{"timestamp":"2026-11-20T14:26:22.165Z","error_code":"0"},"data":[
        {"id":1,"cmc_rank":1,"name":"Bitcoin","symbol":"BTC","quote":[{"symbol":"USD","price":60000,"market_cap":1200e9,"percent_change_24h":-3,"percent_change_7d":-10,"volume_24h":30e9}]},
        {"id":1027,"cmc_rank":2,"name":"Ethereum","symbol":"ETH","quote":[{"symbol":"USD","price":1700,"market_cap":200e9,"percent_change_24h":4,"percent_change_7d":-5,"volume_24h":20e9}]},
        {"id":825,"cmc_rank":3,"name":"Tether USDt","symbol":"USDT","quote":[{"symbol":"USD","price":1,"market_cap":180e9,"percent_change_24h":0,"volume_24h":2e9}]}
    ]}


class MarketRadarTest(unittest.TestCase):
    def test_breadth_excludes_stables(self):
        r=summarize(sample()); self.assertEqual(r["coverage"]["nonstable_with_change"],2)
        self.assertEqual((r["breadth"]["up_24h"],r["breadth"]["down_24h"]),(1,1))
        self.assertEqual(r["coverage"]["excluded_stablecoins"],1)
    def test_sample_dominance_not_official(self):
        r=summarize(sample());self.assertAlmostEqual(r["btc_sample_cap_share_pct"],100*1200/1400)
        self.assertIn("NOT the official",r["caveats"][0])
    def test_quote_dict_supported(self):
        s=sample();s["data"][0]["quote"]={"USD":s["data"][0]["quote"][0]};self.assertEqual(summarize(s)["assets"][0]["symbol"],"BTC")
    def test_invalid_data_rejected(self):
        with self.assertRaises(ValueError):summarize({"data":[{"name":"Foo"}]})
    def test_html_escapes_untrusted_symbols(self):
        s=sample();s["data"][0]["symbol"]="<img onerror='alert(1)'>";s["data"][1]["name"]="<script>alert(1)</script>"
        out=render_html(summarize(s));self.assertNotIn("<script>alert",out);self.assertIn("&lt;script&gt;",out)
    def test_finite_number_checks(self):
        self.assertIsNone(_number("nan"));self.assertIsNone(_number(float("inf")));self.assertIsNone(_number(True))
    def test_limit_is_enforced(self):
        for n in [0,101,-1,"20"]:
            with self.assertRaises(ValueError):get_keyless_listings(n)
    def test_api_status_error_rejected(self):
        class Response:
            def __enter__(self):return io.BytesIO(json.dumps({"status":{"error_code":429,"error_message":"rate limit"},"data":[]}).encode())
            def __exit__(self,*args):pass
        with self.assertRaises(ValueError):get_keyless_listings(fetcher=lambda *a,**k:Response())
    def test_url_is_keyless_and_uses_no_auth_header(self):
        seen=[]
        class Response:
            def __enter__(self):return io.BytesIO(json.dumps(sample()).encode())
            def __exit__(self,*args):pass
        get_keyless_listings(10,fetcher=lambda req,**kw:(seen.append(req) or Response()))
        self.assertIn("/public-api/",seen[0].full_url)
        self.assertNotIn("X-CMC_PRO_API_KEY",dict(seen[0].header_items()))
    def test_live_fixture_report_html_has_provenance(self):
        s=summarize(sample());h=render_html(s);self.assertIn("2026-11-20T14:26",h);self.assertIn("CoinMarketCap",h)

if __name__=="__main__":unittest.main()
