import time
import pytest
from conftest import MAX_RESPONSE_MS, extract_asset_urls


"""

The other UNIT test prescribed in the challenge : 

Open the homepage and verify that game category sections (Sport, Action, 
Racing…) are visible and each contains at least one game card. 

it verifies the homepage is reachable and responds successfully by checking response time and basic
content meet expected requirements.

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



"""

Ensures the critical static components are available, creating a better and user friendly experience for the end-user
by checking of the images and stylesheets are available. 

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
Verifies if the server returns a valid HTML response.

"""


@pytest.mark.api
def test_homepage_html_is_not_empty_and_has_ludigames_branding(http_client, base_url):
  
    response = http_client.get(base_url)

    assert response.status_code == 200
    assert response.text.strip(), "Homepage response body is empty."
    assert "ludigames" in response.text.lower()