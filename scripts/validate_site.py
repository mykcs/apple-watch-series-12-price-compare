#!/usr/bin/env python3
"""Cheap correctness checks for the static Apple comparison site."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
PAGES = (
    Path("index.html"),
    Path("watch/index.html"),
    Path("iphone/index.html"),
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
        'id="trade-flow-simulator" data-price="11499" data-balance="5080"',
        'data-tf-route="A"',
        'data-tf-route="B"',
        'data-tf-route="C"',
        'data-tf-route="D"',
        'data-tf-route="E"',
        'data-tf-route="F"',
        'id="tf-apple-value"',
        'id="tf-private-value"',
        'id="tf-stat-topup"',
        'id="tf-stat-final"',
        'id="tf-stat-gift"',
        'id="tf-stat-quest"',
        'id="tf-stat-care-topup"',
        'id="tf-stat-alltopup"',
        'id="tf-stat-postcare"',
        "var carePrice=1799",
        "var allTopup=topup+careTopup",
        'active="A"',
        'var charge=["A","C"].indexOf(active)>=0?',
        'var cashBefore=balance+(active==="E"?privateCash:0)',
        'var futureCash=(active==="B"?apple:active==="F"?privateCash:0)',
        'var gift=(active==="D"?apple:0)',
        "先把旧机价值用起来",
        "ZA 全额刷",
        "礼品卡不可直接换港币",
        "新机可否使用 Apple Store 礼品卡",
        "需要真实买家",
    ):
        require(text, fragment, "iPhone six-route HKD5080 decision tree")

    # HK$1,180 + HK$3,900 = HK$5,080, now fixed rather than a slider.
    balance, new_price, trade, sale = 1180 + 3900, 11499, 7000, 7000
    net = new_price - trade
    assert balance == 5080 and net == 4499
    # A: on-site HK$4,499, no top-up, cash left HK$581.
    assert max(0, net - balance) == 0 and balance - net == 581
    # B: HK$11,499 authorized; HK$6,419 top-up; refund HK$7,000 later.
    assert new_price - balance == 6419 and trade == 7000
    # C: apply HK$7,000 Apple Gift Card, ZA pays remaining HK$4,499.
    assert new_price - trade == net and balance - net == 581
    # D: HK$6,419 top-up, no bank refund; later Apple Gift Card HK$7,000.
    assert new_price - (balance + 6419) == 0 and trade == 7000
    # E: sell for HK$7,000 first, then pay full, with zero top-up.
    assert max(0, new_price - balance - sale) == 0
    assert balance + sale - new_price == 581
    # F: pay full first, sell later, temporarily top up HK$6,419.
    assert new_price - balance == 6419
    # Initial 1.5% stock awards, not checkout price reductions.
    assert int(new_price * .015 * 100 + .5) == 17249
    assert int(net * .015 * 100 + .5) == 6749
    assert net < 10000 <= new_price
    # Additional required two-year HK AppleCare+ (2026-10-10 official HK price).
    care = 1799
    # A/C: on-site net purchase HK$4,499 leaves HK$581; then HK$1,218 short.
    assert care - (balance - net) == 1218
    # B/F: after HK$7,000 arrives, cash remains HK$5,201 after care.
    assert 7000 - care == 5201
    # D: HK$7,000 Apple gift card is not cash; care needs HK$1,799 more.
    assert 6419 + care == 8218
    # E: HK$7,000 independent pre-sale leaves HK$581, then care shortfall HK$1,218.
    assert care - (balance + sale - new_price) == 1218


def main() -> int:
    validate_routes()
    validate_rates()
    validate_watch()
    validate_iphone()
    validate_iphone_payment()
    validate_iphone_tradein_applecare()
    validate_iphone_tradein_routes()
    print("PASS: static routes, fixed models, exchange rates and price deltas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
