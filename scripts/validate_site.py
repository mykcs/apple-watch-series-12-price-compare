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


def main() -> int:
    validate_routes()
    validate_rates()
    validate_watch()
    validate_iphone()
    print("PASS: static routes, fixed models, exchange rates and price deltas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
