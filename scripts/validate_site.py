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
