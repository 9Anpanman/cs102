from hw06 import hackernews


def test_clear() -> None:
    assert hackernews.clean("ALEKSEY") == "ALEKSEY"
    assert hackernews.clean("A, L, E, X") == "A L E X"
    assert hackernews.clean("ALEK.sey()") == "ALEKsey"
