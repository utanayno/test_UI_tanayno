from playwright.sync_api import BrowserContext
import pytest
import allure

from pages.cart_page import CartPage
from pages.catalog_category_page import CatalogCatPage
from pages.item_page import ItemPage


@pytest.fixture
def cart_page(page):
    return CartPage(page)


@pytest.fixture
def catalog_category_page(page):
    return CatalogCatPage(page)


@pytest.fixture
def item_page(page):
    return ItemPage(page)


@pytest.fixture
def page(context: BrowserContext, playwright):
    page = context.new_page()
    page.set_viewport_size({"width": 1920, "height": 1080})
    return page

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")

        if page and not page.is_closed():
            screenshot = page.screenshot(full_page=True)

            allure.attach(
                screenshot,
                name=f"Screenshot_{item.name}",
                attachment_type=allure.attachment_type.PNG
            )
