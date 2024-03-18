from time import sleep

import pytest


@pytest.fixture(scope="session")
def middleware():
    print("starting...")
    sleep(1)
    print("started.")
    yield "db connection"
    print("teardown...")
    sleep(1)
    print("teardown complete.")


@pytest.fixture
def f() -> list[int]:
    return [1, 3]


def test_asdf(middleware: str, f: list[int]):  # pylint: disable=W0621
    print(middleware)
    assert f[0] == 1
