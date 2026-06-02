Ludigames QA Tests

This repository is the intended solution for assessing some of the edge-case scenarios, basic functioning and
requirements for the online gaming portal powered by Gameloft, Ludigames.


To ensure the proper replication of results across machines in the absence of containerization,
please ensure the req.txt file is fulfilled locally by downloading its dependencies.

The solution uses : 

- Python 3.12
- Pytest
- Playwright
- HTTPX
- BeautifulSoup

The automated suite covers both browser-based validation and HTTP/API validation.

Installation : 

1. Clone the repository :

git cline <repo's url>
cd gameloft_solution

2. Create and activate virtual environment :

python -m venv .venv
source .venv/Scripts/activate

3. Install project dependencies :
pip install -r req.txt


5. Run the tests :

python -m pytest -v --> to be used to run all the tests
python -m pytest -m api -v --> to be used to run only API tests
python -m pytest -m ui -v --> to be used to run only UI tests


Since in the task it was specified to test for at least 5 cases, combining UI and API, the follwing
breakdown is broken into API scenarios and UI scenarios :

API Scenario 1 : Homepage Availability & Performance

If the main product, the homepage, is not available to the users, then the rest of the unit tests
lost their meaning, since the user experience is ruined. Therefore, to ensure that the basics work
i created a unit test to check if the :

- Homepage returns HTTP 200
- Homepage responds withing threshold

API Scenario 2 : Static Asset Availability

Missing CSS, JS or image resources will break the UX. --> Validation :

1. Extract assets from homepage HTML
2. Verify assets are reachable
3. Verify assets do not return HTTP errors.


API Scenario 3 : Homepage integrity : 

The homepage should always return a valid, non-empty HTML document.

Validation :

1.Response body is not empty.
2.HTML document structure exists.


UI Scenarios : 

I) Homepage Branding & Navigation : 

Users should immediately recognize the platform and access navigation controls.

-> Homepage loads successfully
-> Ludigames branding is visible
-> navigation area is displayed

II) Category Sections Visibility and Contains Games : 

This section satisfies the challenge example :
Open the homepage and verify that game category sections are visible and 
each contains at least one game card.

A category without any games would represent a broken implementation and user experience, 
while game discovery is one of the primary functions of the website.

III) Category Navigation : 

Users have to be able to navigate from category cards to category content.

Validation : Click a category card, verify navigation or content update occurs.

IV) Mobile Responsiveness : 

Many users access gaming portals from mobile devices, to check if the solution is cross-platformed
or not is required.

A sample of tests passing is provided :


tests/test_api.py::test_homepage_returns_200_fast_and_contains_expected_content PASSED                                                                                 [  9%]
tests/test_api.py::test_homepage_static_assets_are_reachable PASSED                                                                                                    [ 18%]
tests/test_api.py::test_homepage_html_is_not_empty_and_has_ludigames_branding PASSED                                                                                   [ 27%]
tests/test_ui.py::test_homepage_loads_branding_and_navigation[chromium] PASSED                                                                                         [ 36%]
tests/test_ui.py::test_homepage_displays_game_category_sections[chromium] PASSED                                                                                       [ 45%]
tests/test_ui.py::test_each_main_category_contains_at_least_one_game[chromium-Action games] PASSED                                                                     [ 54%]
tests/test_ui.py::test_each_main_category_contains_at_least_one_game[chromium-Sport games] PASSED                                                                      [ 63%]
tests/test_ui.py::test_each_main_category_contains_at_least_one_game[chromium-Racing games] PASSED                                                                     [ 72%]
tests/test_ui.py::test_homepage_displays_multiple_game_cards[chromium] PASSED                                                                                          [ 81%]
tests/test_ui.py::test_clicking_category_card_opens_category_or_updates_content[chromium] PASSED                                                                       [ 90%]
tests/test_ui.py::test_site_remains_usable_on_mobile_viewport[chromium] PASSED                                                                                         [100%]

============================================================================ 11 passed in 35.34s =======================================================


