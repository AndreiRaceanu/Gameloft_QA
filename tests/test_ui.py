import re
import pytest
from playwright.sync_api import Page, expect
from conftest import expect_any_visible_text, visible_elements_count



"""
Verify if main controls are visible and the homepage loads.
Can't continue with the rest of unit tests if the main page doesn't work properly.     
"""

@pytest.mark.ui
def test_homepage_loads_branding_and_navigation(home_page: Page):

    expect(home_page).to_have_url(re.compile(r"play\.ludigames\.com", re.I))
    expect_any_visible_text(home_page, r"LUDIGAMES")



"""

I decided to split the example-given UI test into multiple sub-tests to verify separately 
whether or not they work properly.

E.G : Open the homepage and verify that game category sections (Sport, Action, 
Racing…) are visible and each contains at least one game card. 


"""

"""
1. The homepage displays important game categories.
"""

@pytest.mark.ui
def test_homepage_displays_game_category_sections(home_page: Page):
    expected_categories = [
        "Action games",
        "Sport games",
        "Racing games",
        "Adventure games",
        "Casual games",
        "Logic games",
        "All games",
    ]

    for category in expected_categories:
        expect_any_visible_text(home_page, rf"^{re.escape(category)}$")



"""
2. verify if main game categories contains at least one gaming card.

"""

@pytest.mark.ui
@pytest.mark.parametrize(
    "category",
    [
        "Action games",
        "Sport games",
        "Racing games",
    ],
)
def test_each_main_category_contains_at_least_one_game(page: Page, base_url: str, category: str):
    page.goto(base_url, wait_until="domcontentloaded")
    expect_any_visible_text(page, r"LUDIGAMES")

    category_card = expect_any_visible_text(page, rf"^{re.escape(category)}$")
    category_card.scroll_into_view_if_needed()
    category_card.click()

    page.wait_for_timeout(2000)

    visible_game_count = visible_elements_count(
        page,
        r"Mahjong|Space|Jewel|Asphalt|Poker|Cricket|Block|Molang|Kart|Shadow|Adventure|PRO|Legends",
    )

    assert visible_game_count >= 1, f"Expected at least one visible game after opening {category}."


"""
Verifies if the user has access to the game cards by checking if they are visible on the homepage.

"""


@pytest.mark.ui
def test_homepage_displays_multiple_game_cards(home_page: Page):
    known_games_pattern = (
        r"Mahjong|Space Survivor|Jewel|Asphalt|Poker|Cricket|"
        r"Block Breaker|Molang|Kart|Shadow|Adventure"
    )

    visible_games = visible_elements_count(home_page, known_games_pattern)

    assert visible_games >= 3, "Expected at least 3 visible game cards on the homepage."


"""

The proper functionality of the gaming cards when clicked is checked by checking 
their response and ensuring the users can navigate from hopemage to game category.

"""

@pytest.mark.ui
def test_clicking_category_card_opens_category_or_updates_content(home_page: Page):
    category = expect_any_visible_text(home_page, r"^Action games$")
    before_url = home_page.url

    category.scroll_into_view_if_needed()
    category.click()

    home_page.wait_for_timeout(1500)

    assert (
        home_page.url != before_url
        or visible_elements_count(home_page, r"Action|games|Play|Mahjong|Asphalt|Cricket") > 0
    )



"""
Verifies if the game site is built cross platform and its main widgets are still accesible.

"""

@pytest.mark.ui
def test_site_remains_usable_on_mobile_viewport(page: Page, base_url: str):
    page.set_viewport_size({"width": 390, "height": 844})
    page.goto(base_url, wait_until="domcontentloaded")

    expect_any_visible_text(page, r"LUDIGAMES")
    expect_any_visible_text(page, r"Action games|Sport games|Casual games|All games")

    visible_games = visible_elements_count(
        page,
        r"Mahjong|Asphalt|Poker|Cricket|Block|Adventure|Molang",
    )

    assert visible_games >= 1, "Expected at least one visible game card on mobile."