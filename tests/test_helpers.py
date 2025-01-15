from connectaboard.helpers import SeenCounter


def test_seen_counter():
    seen_counter = SeenCounter(3)

    assert not seen_counter.has_been_seen_n_times("a")
    assert not seen_counter.has_been_seen_n_times("a")
    assert seen_counter.has_been_seen_n_times("a")

    assert not seen_counter.has_been_seen_n_times("b")
    assert not seen_counter.has_been_seen_n_times("b")
    assert seen_counter.has_been_seen_n_times("b")
