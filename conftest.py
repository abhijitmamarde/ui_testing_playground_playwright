import pytest


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "ignore_https_errors": True,
        # "viewport": {
        #     "width": 1920,
        #     "height": 1080,
        # },
    }


@pytest.fixture
def is_headless(request):
    headed = request.config.getoption("--headed")
    print(f"command line option {headed=}")
    return not headed
