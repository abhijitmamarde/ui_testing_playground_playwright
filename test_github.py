import os
import re

from playwright.sync_api import Page, expect, Browser


def check_login_done(page: Page, username: str) -> bool:
    # to check if login done
    assert (
        page.locator(".AppHeader-context-item-label").text_content().strip()
        == "Dashboard"
    )

    # verify username with which login is done
    page.get_by_label("Open user account menu").click()
    page.get_by_text(username, exact=True).is_visible()
    page.get_by_role("button", name="Close").click()
    return True


def test_login_github(page: Page):
    page.goto("https://github.com")
    expect(page).to_have_title(re.compile("GitHub"))

    username = os.getenv("GITHUB_USERNAME")
    password = os.getenv("GITHUB_PASSWORD")

    page.get_by_role("link", name="Sign in").click()

    page.get_by_label("Username or email address").fill(username)
    page.get_by_label("Password").fill(password)
    page.locator("input.js-sign-in-button").click()

    try:
        page.locator("#session-otp-input-label").wait_for(state="visible", timeout=3000)
    except:
        pass

    auth_code_required = False
    try:
        auth_code_required = page.locator("#session-otp-input-label").is_visible()
    except:
        pass

    if auth_code_required:
        auth_code = os.getenv("GITHUB_AUTHCODE")
        page.locator("#app_totp").fill(auth_code)

    check_login_done(page, username)

    page.context.storage_state(path="github_login_state.json")


def test_check_session_login(browser: Browser):
    context = browser.new_context(storage_state="github_login_state.json")
    page = context.new_page()
    page.goto("https://github.com")
    expect(page).to_have_title(re.compile("GitHub"))
    check_login_done(page, os.getenv("GITHUB_USERNAME"))
