#!/usr/bin/env python3
"""Cheap correctness checks for the static product selection site."""

from __future__ import annotations

import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
PAGES = (
    Path("index.html"),
    Path("watch/index.html"),
    Path("osprey/index.html"),
    Path("osprey/series/index.html"),
    Path("iphone/index.html"),
    Path("iphone/trade-in-guide/index.html"),
    Path("mac/index.html"),
    Path("mac/macbook-pro/index.html"),
    Path("mac/mac-mini/index.html"),
    Path("mac/storage/index.html"),
)

HKD = 0.8556
SGD = 5.2556
USD = 6.7114


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []
        self.title_depth = 0
        self.title_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "a":
            for key, value in attrs:
                if key == "href" and value:
                    self.hrefs.append(value)
        if tag == "title":
            self.title_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag == "title" and self.title_depth:
            self.title_depth -= 1

    def handle_data(self, data: str) -> None:
        if self.title_depth:
            self.title_text.append(data)


def fail(message: str) -> None:
    raise SystemExit(message)


def require(text: str, fragment: str, label: str) -> None:
    if fragment not in text:
        fail(f"{label}: missing {fragment!r}")


def yen(amount: int, rate: float) -> int:
    # Site policy: positive CNY conversions round to the nearest whole yuan.
    return int(amount * rate + 0.5)


def internal_target(href: str) -> Path | None:
    if not href.startswith("/") or href.startswith("//"):
        return None
    path = urlsplit(href).path
    if path == "/":
        return Path("index.html")
    if path.endswith("/"):
        return Path(path.lstrip("/")) / "index.html"
    return Path(path.lstrip("/"))


def validate_routes() -> None:
    expected = {page.as_posix() for page in PAGES}
    for page in PAGES:
        full = ROOT / page
        if not full.is_file():
            fail(f"missing required page: {page}")
        text = full.read_text(encoding="utf-8")
        parser = LinkParser()
        parser.feed(text)
        if not "".join(parser.title_text).strip():
            fail(f"{page}: missing non-empty <title>")
        for href in parser.hrefs:
            target = internal_target(href)
            if target is None:
                continue
            if target.as_posix() not in expected or not (ROOT / target).is_file():
                fail(f"{page}: broken internal route {href!r} -> {target}")


def validate_osprey() -> None:
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    page = (ROOT / "osprey/index.html").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    require(home, "<h1>选购商品</h1>", "product selection site title")
    require(home, 'href="/osprey/"', "backpack homepage entry")
    require(readme, "# 选购商品", "product selection readme")
    for fragment in (
        'data-choice="daily"',
        'data-choice="hike"',
        'data-choice="travel"',
        'data-choice="trek"',
        "Daylite™ Plus",
        "Talon™ 22",
        "Farpoint™ 40",
        "Kestrel™ 48",
        "https://www.osprey.com/expert-advice/size-fit",
        "aria-pressed",
    ):
        require(page, fragment, "Osprey chooser")


def validate_osprey_series() -> None:
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    chooser = (ROOT / "osprey/index.html").read_text(encoding="utf-8")
    series_page = (ROOT / "osprey/series/index.html").read_text(encoding="utf-8")
    app = (ROOT / "osprey/series/app.js").read_text(encoding="utf-8")
    require(home, "18 个常见系列", "Osprey homepage overview")
    require(chooser, 'href="/osprey/series/"', "Osprey two-way navigation")
    require(chooser, 'id="series-detail"', "Osprey deep link from use case")
    for fragment in ('id="family-list"', 'id="family-detail"', 'data-filter="backpacking"',
                     'id="series-search"', 'src="./app.js"', '2026-10-14'):
        require(series_page, fragment, "Osprey series browser")
    for fragment in ('fetch("./catalog.json"', 'aria-pressed', 'priceUsd',
                     'seriesUrl', 'visibleFamilies', 'currentFamily'):
        require(app, fragment, "Osprey series app")
    catalogue = json.loads((ROOT / "osprey/series/catalog.json").read_text(encoding="utf-8"))
    if catalogue.get("checkedAt") != "2026-10-14" or catalogue.get("currency") != "USD":
        fail("Osprey snapshot date/market/currency must remain explicit")
    families = catalogue.get("families", [])
    if len(families) != 18 or sum(len(f.get("products", [])) for f in families) != 36:
        fail("Osprey documented 18 series / 36 representative products contract")
    ids = [family.get("id") for family in families]
    if len(ids) != len(set(ids)):
        fail("Duplicate Osprey series id")
    allowed = set(catalogue.get("categoryLabels", {}))
    for family in families:
        if family.get("category") not in allowed:
            fail(f"Osprey family category missing: {family.get('id')}")
        if not all(isinstance(family.get(k), str) and family[k].strip()
                   for k in ("name", "tagline", "intro", "bestFor", "caution")):
            fail(f"Osprey family incomplete: {family.get('id')}")
        if not family.get("seriesUrl", "").startswith("https://www.osprey.com/"):
            fail(f"Osprey series link not official: {family.get('id')}")
        for product in family["products"]:
            if (not isinstance(product.get("priceUsd"), (int, float))
                    or isinstance(product.get("priceUsd"), bool) or product["priceUsd"] <= 0):
                fail(f"Missing positive Osprey USD snapshot price: {product.get('name')}")
            if not all(isinstance(product.get(k), str) and product[k].strip()
                       for k in ("name", "volume", "description")):
                fail(f"Incomplete Osprey product: {product.get('name')}")
            if not product.get("url", "").startswith("https://www.osprey.com/"):
                fail(f"Osprey product link not official: {product.get('name')}")


def validate_rates() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for fragment in (
        "1 HKD ≈ 0.8556 CNY",
        "1 SGD ≈ 5.2556 CNY",
        "1 USD ≈ 6.7114 CNY",
    ):
        require(readme, fragment, "README exchange-rate snapshot")


def validate_watch() -> None:
    text = (ROOT / "watch/index.html").read_text(encoding="utf-8")
    require(text, "页面默认按 46 mm 比较", "Watch fixed-size policy")
    require(text, "<h2>46 mm</h2>", "Watch heading")
    require(text, "46mm-cellular-natural-titanium", "Watch titanium purchase URL")
    require(text, "46mm-cellular-pearl-white-ceramic", "Watch ceramic purchase URL")

    ti_hk = yen(5599, HKD)
    ti_sg = yen(1009, SGD)
    ti_us = yen(749, USD)
    ce_hk = yen(7199, HKD)
    ce_sg = yen(1259, SGD)
    ce_us = yen(949, USD)

    fragments = (
        f"约 ¥{ti_hk:,}",
        f"¥5,599 · 比香港贵 ¥{5599 - ti_hk:,}",
        f"S$1,009 · 约 ¥{ti_sg:,} · 比香港贵 ¥{ti_sg - ti_hk:,}",
        f"$749 · 约 ¥{ti_us:,} · 比香港贵 ¥{ti_us - ti_hk:,}",
        f"约 ¥{ce_hk:,}",
        f"¥7,099 · 比香港贵 ¥{7099 - ce_hk:,}",
        f"S$1,259 · 约 ¥{ce_sg:,} · 比香港贵 ¥{ce_sg - ce_hk:,}",
        f"$949 · 约 ¥{ce_us:,} · 比香港贵 ¥{ce_us - ce_hk:,}",
        f"陶瓷多 HK$1,600，约 ¥{yen(1600, HKD):,}",
    )
    for fragment in fragments:
        require(text, fragment, "Watch price logic")


def validate_iphone() -> None:
    text = (ROOT / "iphone/index.html").read_text(encoding="utf-8")
    require(text, "iPhone 18 Pro Max 256GB", "iPhone fixed model")

    hk = yen(11499, HKD)
    sg = yen(2099, SGD)
    us = yen(1299, USD)
    direct_delta = int((11499 * HKD - 1299 * USD) + 0.5)

    for fragment in (
        "¥10,999",
        f"约 ¥{hk:,}",
        f"约 ¥{sg:,}",
        f"约 ¥{us:,}",
        f"美国免税州比香港约低 ¥{direct_delta:,}",
    ):
        require(text, fragment, "iPhone price logic")




def validate_iphone_tradein_applecare() -> None:
    text = (ROOT / "iphone/index.html").read_text(encoding="utf-8")
    for fragment in (
        'id="tradein-applecare"',
        "HK$4,499",
        "2027-09-28",
        "353 / 730",
        "60 天内",
        "HK$172.49",
        "以旧换新可能令之前的银行卡回赠计算失效",
        "250909_applecareplusch.pdf",
        "https://www.apple.com/hk/shop/trade-in",
    ):
        require(text, fragment, "iPhone HK trade-in / AppleCare")
    assert 11499 - 7000 == 4499
    assert abs(353 / 730 * 100 - 48.356) < .01


def validate_iphone_payment() -> None:
    text = (ROOT / "iphone/index.html").read_text(encoding="utf-8")
    # Protect the dated Hong Kong payment decision without making live-bank claims in CI.
    for fragment in (
        'id="hk-payment" class="payment" data-price="11499"',
        'id="za-stock"',
        'id="chill-reward"',
        'id="chill-channel"',
        'id="chill-left"',
        'id="stock-change"',
        'price*.015*(1+growth/100)',
        'Math.min(150,left,round(price*.036))',
        "HK$21,999 ≠ HK$21,999 立减",
        "2026-10-10",
        "https://bank.za.group/za-card",
        "chill_offer_tnc_sc.pdf",
    ):
        require(text, fragment, "iPhone HK payment decision")

    # Derived default figures: round monetary rewards to cents, then split Chill 50/50.
    price_cents = 11499 * 100
    za_reward_cents = int(11499 * 1.5 + 0.5)
    chill_points_cents = int(11499 * 0.4 + 0.5)
    chill_extra_cents = 150 * 100
    chill_share_cents = (chill_points_cents + chill_extra_cents) // 2
    if (za_reward_cents, chill_points_cents, chill_share_cents) != (17249, 4600, 9800):
        fail("iPhone HK payment calculation drift")
    if price_cents - za_reward_cents != 1132651 or price_cents - chill_share_cents != 1140100:
        fail("iPhone HK personal net cost drift")
    if (price_cents - chill_share_cents) - (price_cents - za_reward_cents) != 7449:
        fail("iPhone HK expected difference drift")



def validate_iphone_tradein_routes() -> None:
    text = (ROOT / "iphone/index.html").read_text(encoding="utf-8")
    for fragment in (
        'id="trade-flow-simulator" data-price="11499" data-balance="5080" data-care="1799"',
        'data-route="A"',
        'data-route="B"',
        'id="tf2-appraise"',
        'id="tf2-care-when"',
        'id="tf2-day-topup"',
        'id="tf2-total-topup"',
        'id="tf2-final-bank"',
        'id="tf2-refund"',
        'id="tf2-stockback"',
        'id="tf2-raffle"',
        'var laterTopup=Math.max(0,laterCare-cashBeforeLaterCare)',
        "C 是「先领礼品卡再付款」",
        "不考虑礼品卡和私人出售",
        "银行尚未正式保证",
    ):
        require(text, fragment, "iPhone two active HK Trade In routes")

    if 'data-route="C"' in text or 'data-tf-route="E"' in text:
        fail("retired purchase routes must not be active")

    balance, price, trade, care = 1180 + 3900, 11499, 7000, 1799
    immediate = price - trade
    assert balance == 5080 and immediate == 4499
    # Route A, AppleCare+ paid later: no extra money for phone, HK$1,218 later.
    assert max(0, immediate - balance) == 0
    assert care - (balance - immediate) == 1218
    # Route A, AppleCare+ paid same day: full HK$6,298 charge, HK$1,218 top-up.
    assert immediate + care == 6298
    assert immediate + care - balance == 1218
    # Route B, AppleCare+ bought after confirmed HK$7,000 refund.
    assert price - balance == 6419
    assert trade - care == 5201
    # Route B, AppleCare+ bought upfront: HK$13,298 needs HK$8,218 top-up,
    # then HK$7,000 later becomes bank balance, not a second discount.
    assert price + care == 13298
    assert price + care - balance == 8218
    assert trade == 7000
    # Stocks are value approximations, not checkout price reductions.
    assert int(immediate * .015 * 100 + .5) == 6749
    assert int(price * .015 * 100 + .5) == 17249
    assert immediate < 10000 <= price


def validate_tradein_dialogue() -> None:
    """The guided conversation is a separate subroute; do not overwrite finance logic."""
    guide = (ROOT / "iphone/trade-in-guide/index.html").read_text(encoding="utf-8")
    main_page = (ROOT / "iphone/index.html").read_text(encoding="utf-8")
    ui = (ROOT / "iphone/trade-in-guide/ui.js").read_text(encoding="utf-8")
    app = (ROOT / "iphone/trade-in-guide/app.js").read_text(encoding="utf-8")
    model = (ROOT / "iphone/trade-in-guide/model.js").read_text(encoding="utf-8")
    require(main_page, 'href="/iphone/trade-in-guide/#actual-route-20261013"', "iPhone actual route link")
    for fragment in ('src="./model.js"', 'src="./ui.js"', 'src="./app.js"', "HK$11,500", "HK$11,499"):
        require(guide, fragment, "trade-in guide entry and source")
    for fragment in ('能抵 7,000', '只能抵更少', '要收 228', '要寄走检查', '不能折抵', '上门收件', '指定网点'):
        require(app, fragment, "original option preserved")
    for fragment in ("那我该怎么寄旧手机？", "最后报价变低", "旧手机拿回来吗？", "factoryAccept"):
        require(app, fragment, "courier / returned-device follow-up")
    for fragment in ("bought-return-old", "not-buy", "readyMail", "readyShop", "careBlocked"):
        require(model, fragment, "gated purchase states")
    require(ui, "check-circle-2", "original icon family")


def validate_actual_purchase_route() -> None:
    """Actual purchase path is immutable evidence, not a guessed successful Trade In."""
    page = (ROOT / "iphone/trade-in-guide/index.html").read_text(encoding="utf-8")
    main_page = (ROOT / "iphone/index.html").read_text(encoding="utf-8")
    style = (ROOT / "iphone/trade-in-guide/style.css").read_text(encoding="utf-8")
    record = (ROOT / "docs/decisions/2026-10-13-iphone-hk-actual-route.md").read_text(encoding="utf-8")

    for fragment in (
        'id="actual-route-20261013"',
        'data-purchase="completed"',
        'data-tradein="pending"',
        'data-courier="shipped"',
        'data-source="customer-recollection"',
        "2026 年 10 月 13 日",
        "冰川蓝 · 256GB",
        "8 位验证码",
        "已到香港顺丰网点寄出旧机",
        "已交寄",
        "HK$7,000",
        "并没有确认",
        "结果未知",
        "门店通常是折抵换购新产品",
        'id="tradein-app"',
        'src="./model.js"',
        'src="./ui.js"',
        'src="./app.js"',
    ):
        require(page, fragment, "dated actual purchase timeline")

    if page.count('data-stage-state="done"') != 5:
        fail("actual route must have five witnessed or prepared stages, including SF handover")
    if page.count('data-stage-state="pending"') != 1:
        fail("only final valuation should remain pending")
    require(page, 'data-route-stage="courier" data-stage-state="done"', "courier handover completed")
    if "旧手机还没确认寄出" in page or "尚未寄出" in page:
        fail("stale unshipped claim must not survive in actual-route page")
    if "不臆测验证码是否使用" not in record:
        fail("actual route must not pretend the 8-digit code was used")
    if "2026-10-13" not in record or "香港店员" not in record:
        fail("actual record must preserve witnessed testimony and uncertainty")
    if "2026-10-13 真实结局" not in main_page or "冰川蓝" not in main_page:
        fail("iPhone landing page must report purchase complete")
    require(style, ".actual-steps", "connected actual route timeline")
    require(style, ".actual-side", "unverified side branch styles")


def main() -> int:
    validate_routes()
    validate_osprey()
    validate_osprey_series()
    validate_rates()
    validate_watch()
    validate_iphone()
    validate_iphone_payment()
    validate_iphone_tradein_applecare()
    validate_iphone_tradein_routes()
    validate_tradein_dialogue()
    validate_actual_purchase_route()
    print("PASS: static routes, fixed models, exchange rates and price deltas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
