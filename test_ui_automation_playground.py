import time

import pytest
from playwright.sync_api import Page, expect, Dialog, TimeoutError
from html_table import Table
from steps import *


def test_1_btn_with_dynamic_id(page: Page):
    goto_home(page)
    click_home_link(page, "Dynamic ID")
    click_btn_named(page, "Button with Dynamic ID")


def test_2_class_attribute(page: Page):
    goto_home(page)
    click_home_link(page, "Class Attribute")
    page.on("dialog", handle_dialog_class_attribute)
    click_button_using_locator(page, "button.btn-primary")


def test_3_hidden_layers(page: Page):
    goto_home(page)
    click_home_link(page, "Hidden Layers")
    click_button_using_locator(page, "#greenButton")
    with pytest.raises(TimeoutError):
        click_button_using_locator(page, "#greenButton", timeout=1000)


def test_4_load_delay(page: Page):
    goto_home(page)
    click_home_link(page, "Load Delay")
    click_btn_named(page, "Button Appearing After Delay")


def test_5_ajax_data(page: Page):
    goto_home(page)
    click_home_link(page, "AJAX Data")
    click_btn_named(page, "Button Triggering AJAX Request")
    click_button_using_locator(page, "#ajaxButton")
    # 15secs req
    wait_for_ajax_text_to_visible(
        page, "Data loaded with AJAX get request.", timeout=16000
    )


def test_6_client_side_delay(page: Page):
    goto_home(page)
    click_home_link(page, "Client Side Delay")
    click_button_using_locator(page, "#ajaxButton")
    # 15secs req
    wait_for_ajax_text_to_visible(
        page, "Data calculated on the client side.", timeout=16000
    )


def test_7_click(page: Page):
    goto_home(page)
    click_home_link(page, "Click")
    click_button_using_locator(page, "#badButton")
    click_button_using_locator(page, "button.btn.btn-success")


def test_8_text_input(page: Page):
    goto_home(page)
    click_home_link(page, "Text Input")
    new_button_name = "the-special-btn-name"
    input_text(page, "#newButtonName", new_button_name)
    click_button_using_locator(page, "#updatingButton")
    click_button_using_locator(page, f"//button[contains(text(), '{new_button_name}')]")


def test_9_scrollbars(page: Page):
    goto_home(page)
    click_home_link(page, "Scrollbars")
    # This works without any special Handling; supported at framework level
    click_button_using_locator(page, "#hidingButton")


def test_10_dynamic_table(page: Page):
    goto_home(page)
    click_home_link(page, "Dynamic Table")
    expected_text = get_text_content(page, "p.bg-warning")

    table_html = get_html(page, "//div[@role='table']")
    table = Table(table_html)
    chrome_cpu_data = table.get_data("Name", "Chrome", "CPU")

    assert expected_text == f"Chrome CPU: {chrome_cpu_data}"


def test_11_verify_text(page: Page):
    goto_home(page)
    click_home_link(page, "Verify Text")
    text = get_text_content(page, ".bg-primary")
    assert text == "Welcome UserName!"


def test_12_progress_bar(page: Page):
    goto_home(page)
    click_home_link(page, "Progress Bar")
    click_button_using_locator(page, "#startButton")
    assert monitor_progress_till_percent(page, 75)
    click_button_using_locator(page, "#stopButton")
    result = get_text_content(page, "#result")
    print(f"{result=}")
    assert result.startswith("Result:")


def test_13_visibility(page: Page):
    goto_home(page)
    click_home_link(page, "Visibility")

    click_button_using_locator(page, "#hideButton")

    assert button_not_visible(page, "#removedButton")
    assert button_not_visible(page, "#zeroWidthButton")
    # assert button_not_visible(page, "#overlappedButton")
    assert button_not_visible(
        page, "#transparentButton"
    )  # works because of check - check_if_opaque
    assert button_not_visible(page, "#invisibleButton")
    assert button_not_visible(page, "#notdisplayedButton")
    # assert button_not_visible(page, "#offscreenButton")

    # check if buttons could be clicked!!! Expected, should raise exception
    with pytest.raises(Exception):
        click_button_using_locator(page, "#overlappedButton", timeout=500)
    # with pytest.raises(Exception):
    #     # transparentButton are able to clicked!!!
    #     click_button_using_locator(page, "#transparentButton", timeout=500)
    with pytest.raises(Exception):
        click_button_using_locator(page, "#offscreenButton", timeout=500)

    assert check_if_opaque(page, "#transparentButton")


def test_14_sample_app(page: Page):
    goto_home(page)
    click_home_link(page, "Sample App")
    assert get_text_content(page, "#loginstatus") == "User logged out."
    input_text(page, "//input[@name='UserName']", "abhijit")
    input_text(page, "//input[@name='Password']", "pwd")
    click_button_using_locator(page, "#login")
    assert get_text_content(page, "#loginstatus") == "Welcome, abhijit!"

    # TODO: this is not working; need to check further!
    # click_btn_named(page, "Log Out")

    click_button_using_locator(page, "#login")
    time.sleep(0.5)
    assert get_text_content(page, "#loginstatus") == "User logged out."


def test_15_mouse_over(page: Page):
    goto_home(page)
    click_home_link(page, "Mouse Over")

    assert get_text_content(page, "#clickCount") == "0"

    click_click_me_link(page)
    click_click_me_link(page)

    assert get_text_content(page, "#clickCount") == "2"


def test_16_nbsp_btn_click(page: Page):
    goto_home(page)
    click_home_link(page, "Non-Breaking Space")

    with pytest.raises(TimeoutError):
        click_button_using_locator(page, "//button[text()='My Button']", timeout=1000)

    # this has special space char; check below url
    # https://stackoverflow.com/questions/247135/using-xpath-to-search-text-containing-nbsp
    nbsp = "\u00a0"
    click_button_using_locator(page, f"//button[text()='My{nbsp}Button']", timeout=1000)


def test_16_overlapped_element(page: Page):
    goto_home(page)
    click_home_link(page, "Overlapped Element")

    assert get_input_text(page, "#id") == ""
    assert get_input_text(page, "#name") == ""

    input_text(page, "#id", "sample_id")

    # needed for scrolling, else input text is failing!
    page.keyboard.press("PageDown")
    # or could use this element level PageDown key press!
    # page.locator("#id").press("PageDown")
    time.sleep(0.3)

    input_text(page, "#name", "sample_name")

    assert get_input_text(page, "#id") == "sample_id"
    assert get_input_text(page, "#name") == "sample_name"


@pytest.mark.onlyheaded
def test_17_shadow_dom(page: Page, is_headless):
    if is_headless:
        pytest.skip("Copy to clipboard does not work with headless mode!")
    goto_home(page)
    click_home_link(page, "Shadow DOM")

    assert get_input_text(page, "#editField") == ""

    click_button_using_locator(page, "#buttonGenerate")
    time.sleep(0.3)

    assert get_input_text(page, "#editField") != ""

    click_button_using_locator(page, "#buttonCopy")
    generated_guid = get_input_text(page, "#editField")

    print(f"{generated_guid=}")

    input_text(page, "#editField", "abc")
    page.keyboard.press("Control+C")
    page.keyboard.press("Control+V")
    assert get_input_text(page, "#editField") == f"abc{generated_guid}"
