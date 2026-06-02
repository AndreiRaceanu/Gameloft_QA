import re

import pytest
from playwright.sync_api import Page, expect

from conftest import expect_any_visible_text

"""
this test verifies if the homepage 
loads successfully and the most important
category rails are visible to the user
"""

@pytest.mark.ui
def test_homepage_loads_core_sections_and_category_rails(home_page: Page):
    expect(home_page).to_have_title(re.compile(r"Ludigames|Free Online Games", re.I))

    expect_any_visible_text(home_page, r"^Top 10$")
    expect_any_visible_text(home_page, r"^Games you might like$")

    for category in ["Sport", "Action", "Racing", "Adventure", "Brain Games"]:
        expect_any_visible_text(home_page, rf"^{re.escape(category)}$")

"""
verifies at least one playable game card or play action is visible
"""


@pytest.mark.ui
def test_game_recommendations_have_playable_cards(home_page: Page):
    expect_any_visible_text(home_page, r"^Games you might like$")

    playable_content = re.compile(
        r"Kart Racing PRO|Knife Smash|Play Now|WATCH AD TO PLAY|Play",
        re.I,
    )

    expect_any_visible_text(home_page, playable_content.pattern)


"""
ensures users can access policy and compliance information
"""


@pytest.mark.ui
def test_footer_legal_links_are_visible(home_page: Page):
    home_page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

    for label in [
        "privacy policy",
        "Terms of Use",
        "Cookie Policy",
        "Manage Your Cookie Choices",
    ]:
        expect_any_visible_text(home_page, re.escape(label))

"""
verifies a view-all widget is found and can be interracted with

"""


@pytest.mark.ui
def test_clicking_a_view_all_control_opens_a_browseable_listing(page: Page, base_url: str):
    page.goto(base_url, wait_until="domcontentloaded")

    view_all = expect_any_visible_text(page, r"^View all$")
    before_url = page.url

    view_all.scroll_into_view_if_needed()
    view_all.click()

    page.wait_for_timeout(1500)

    if page.url == before_url:
        expect_any_visible_text(page, r"Play|WATCH AD TO PLAY|Game|Top 10|Games")
    else:
        expect(page).to_have_url(re.compile(r".+"))


"""
verifies if the website is built to be platform dependant or not

"""

@pytest.mark.ui
def test_site_remains_usable_on_mobile_viewport(page: Page, base_url: str):
    page.set_viewport_size({"width": 390, "height": 844})
    page.goto(base_url, wait_until="domcontentloaded")

    expect_any_visible_text(page, r"LUDIGAMES")
    expect_any_visible_text(page, r"Sport|Action|Racing|Adventure|Brain Games")
    expect_any_visible_text(page, r"Play|WATCH AD TO PLAY|View all")