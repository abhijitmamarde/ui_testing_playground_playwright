import time
from playwright.sync_api import Page, expect, Dialog, TimeoutError


def goto_home(page: Page):
    page.goto("https://uitestingplayground.com/home")
    expect(page).to_have_title("UI Test Automation Playground")

    expect(page.locator("#title")).to_have_text(
        "UI Test Automation Playground", use_inner_text=True
    )


def get_html(page: Page, locator: str) -> str:
    return page.locator(locator).inner_html()


def get_input_text(page: Page, locator: str) -> str:
    return page.locator(locator).input_value().strip()


def click_home_link(page: Page, link_name: str) -> None:
    page.locator(f"//a[contains(text(), '{link_name}')]").click()

    home_page_link_url_map = {
        "Dynamic ID": "**/dynamicid",
        "Class Attribute": "**/classattr",
        "Hidden Layers": "**/hiddenlayers",
        "Load Delay": "**/loaddelay",
        "AJAX Data": "**/ajax",
        "Client Side Delay": "**/clientdelay",
        "Click": "**/click",
        "Text Input": "**/textinput",
        "Scrollbars": "**/scrollbars",
        "Dynamic Table": "**/dynamictable",
        "Verify Text": "**/verifytext",
        "Progress Bar": "**/progressbar",
        "Visibility": "**/visibility",
        "Sample App": "**/sampleapp",
        "Mouse Over": "**/mouseover",
        "Non-Breaking Space": "**/nbsp",
        "Overlapped Element": "**/overlapped",
        "Shadow DOM": "**/shadowdom",
    }
    url = home_page_link_url_map[link_name]
    page.wait_for_url(url)


def check_if_opaque(page: Page, locator) -> bool:
    e = page.locator(locator)
    style = e.get_attribute("style")
    if not style:
        return False
    styles = [x for x in style.split(";") if x]
    css_styles = {}
    for style in styles:
        k, v = style.split(":")
        k = k.strip()
        v = v.strip()
        css_styles[k] = v

    return css_styles.get("opacity", "1") == "0"


def click_btn_named(page: Page, btn_name: str) -> None:
    page.locator(f"//button[contains(text(), '{btn_name}')]")


def click_button_using_locator(page: Page, locator: str, timeout=30000) -> None:
    page.locator(locator).click(timeout=timeout)
    time.sleep(0.5)


def button_not_visible(page: Page, locator: str) -> bool:
    return (not page.locator(locator).is_visible()) or (check_if_opaque(page, locator))


def monitor_progress_till_percent(page: Page, percent: int) -> bool:
    for _ in range(100):
        time.sleep(1)
        e = page.locator("#progressBar")
        percent_now = e.get_attribute("aria-valuenow")
        percent_now = int(percent_now)
        if percent_now >= percent:
            return True
    return False


def input_text(page: Page, locator: str, text: str) -> None:
    page.locator(locator).fill(text)
    time.sleep(0.5)


def handle_dialog_class_attribute(dialog: Dialog) -> None:
    assert dialog.type == "alert"
    assert dialog.message == "Primary button pressed"
    dialog.accept()


def wait_for_ajax_text_to_visible(page: Page, ajax_text: str, timeout=30000) -> None:
    element = page.locator("p.bg-success")
    element.wait_for(state="visible", timeout=timeout)
    assert element.text_content() == ajax_text


def get_text_content(page: Page, locator: str) -> str:
    element = page.locator(locator)
    return element.text_content().strip()


def click_click_me_link(page: Page) -> None:
    e = page.locator("//a[@title='Click me']")
    box = e.bounding_box()
    page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)

    e = page.locator(".container h3")
    box = e.bounding_box()
    page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
