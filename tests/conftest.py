import os
import re
import time
from urllib.parse import urljoin, urlparse

import httpx
import pytest
from bs4 import BeautifulSoup
from playwright.sync_api import Page

BASE_URL = os.getenv("BASE_URL", "https://play.ludigames.com/").rstrip("/") + "/"
TIMEOUT_MS = int(os.getenv("PW_TIMEOUT_MS", "15000"))
MAX_RESPONSE_MS = float(os.getenv("MAX_RESPONSE_MS", "3.0"))


@pytest.fixture(scope="session")
def base_url() -> str:
    return BASE_URL


@pytest.fixture(scope="session")
def http_client() -> httpx.Client:
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; QA-Automation-Challenge/1.0)",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }

    with httpx.Client(headers=headers, follow_redirects=True, timeout=20.0) as client:
        yield client


@pytest.fixture()
def configure_page(page: Page):
    page.set_default_timeout(TIMEOUT_MS)
    page.set_viewport_size({"width": 1366, "height": 900})


@pytest.fixture()
def home_page(page: Page, base_url: str, configure_page) -> Page:
    page.goto(base_url, wait_until="domcontentloaded")
    expect_any_visible_text(page, r"LUDIGAMES")
    return page


def same_host(url: str, base_url: str) -> bool:
    return urlparse(url).netloc == urlparse(base_url).netloc


def absolute_url(base_url: str, maybe_url: str) -> str:
    return urljoin(base_url, maybe_url)


def extract_asset_urls(html: str, base_url: str, limit: int = 20) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    urls: list[str] = []

    selectors = [
        ("script[src]", "src"),
        ("link[href]", "href"),
        ("img[src]", "src"),
        ("source[src]", "src"),
    ]

    for selector, attr in selectors:
        for tag in soup.select(selector):
            raw = (tag.get(attr) or "").strip()

            if not raw or raw.startswith("data:"):
                continue

            url = absolute_url(base_url, raw)

            if urlparse(url).scheme in {"http", "https"} and url not in urls:
                urls.append(url)

            if len(urls) >= limit:
                return urls

    return urls


def expect_any_visible_text(page: Page, pattern: str, timeout_ms: int = TIMEOUT_MS):
    locator = page.get_by_text(re.compile(pattern, re.I))
    deadline = time.monotonic() + timeout_ms / 1000

    while time.monotonic() < deadline:
        for index in range(locator.count()):
            candidate = locator.nth(index)

            if candidate.is_visible():
                return candidate

        page.wait_for_timeout(250)

    raise AssertionError(f"No visible element found for text pattern: {pattern}")


def visible_elements_count(page: Page, pattern: str) -> int:
    locator = page.get_by_text(re.compile(pattern, re.I))
    visible_count = 0

    for index in range(locator.count()):
        if locator.nth(index).is_visible():
            visible_count += 1

    return visible_count