import pytest

pytest_plugins = [
    'tests.fixtures.api_client',
    'tests.fixtures.rcc_response',
    'tests.fixtures.mr_response',
    'tests.fixtures.db_session',
]


def pytest_configure(config):
    config.addinivalue_line('markers', 'online: mark test which needed internet connection')


def pytest_addoption(parser):
    parser.addoption(
        '--online',
        action='store_true',
        default=False,
        help='Run test which nedeed a internet connection',
    )


def pytest_runtest_setup(item):
    if ('online' in item.keywords) and not (item.config.getoption('--online')):
        pytest.skip('Need --with-env to run')
