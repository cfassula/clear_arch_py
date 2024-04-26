import os
from typing import List
import pytest
from colorama import Fore, Style


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--env",
        action="store",
        default="test",
        help="Environment to run tests against. Default is 'test'.",
    )
    parser.addoption(
        "--group",
        action="store",
        default=None,
        help="Run test only from a specific group.",
    )


@pytest.hookimpl(tryfirst=True)
def pytest_load_initial_conftests(
    early_config: pytest.Config,  # pylint: disable=unused-argument
    parser: pytest.Parser,
    args: List[str]
) -> None:
    parser_args = parser.parse_known_args(args)
    env = parser_args.env
    os.environ.setdefault('APP_ENV', env)
    print(
        f"{Fore.BLUE}\n\n**** Running tests using .env.{env} *****\n\n{Style.RESET_ALL}"
    )


def pytest_runtest_setup(item: pytest.Item) -> None:
    group_mark = item.get_closest_marker("group")

    group_option = item.config.getoption("--group")

    if group_option:
        if group_mark is None or group_option not in group_mark.args:
            pytest.skip(f"Test requires  group {group_option}")
