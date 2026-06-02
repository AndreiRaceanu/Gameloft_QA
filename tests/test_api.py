import time

import pytest

from conftest import MAX_RESPONSE_MS, extract_asset_urls

"""
verifies if the homepage is reachable and responds successfully.
"""


@pytest.mark.api
def test_homepage_returns_200_fast_and_contains_expected_content(http_client, base_url):
    start = time.perf_counter()
    response = http_client.get(base_url)
    elapsed = time.perf_counter() - start

    assert response.status_code == 200
    assert elapsed <= MAX_RESPONSE_MS

    html = response.text.lower()
    assert "ludigames" in html
    assert "<html" in html
    assert "</html>" in html

"""
verifies if the assets referenced by the homepage can be downloaded
"""
@pytest.mark.api
def test_homepage_static_assets_are_reachable(http_client, base_url):
    response = http_client.get(base_url)
    assert response.status_code == 200

    asset_urls = extract_asset_urls(response.text, base_url, limit=10)
    assert asset_urls, "No static assets found on the homepage."

    failures = []

    for url in asset_urls:
        asset_response = http_client.get(url)

        if asset_response.status_code >= 400:
            failures.append((url, asset_response.status_code))

    assert not failures, f"Static assets with error responses: {failures}"
"""
verifies the server returns a non-empty and valid HTML document.
"""

@pytest.mark.api
def test_homepage_html_is_not_empty_and_has_document_structure(http_client, base_url):
    response = http_client.get(base_url)

    assert response.status_code == 200
    assert response.text.strip(), "Homepage response body is empty."

    html = response.text.lower()
    assert "<html" in html, "Homepage response does not look like an HTML document."
    assert "</html>" in html, "Homepage HTML document is not closed properly."
    assert "ludigames" in html, "Homepage HTML does not mention Ludigames."