from connectaboard.helpers import SeenCounter


def test_seen_counter():
    initial = "a"
    new = "b"
    seen_counter = SeenCounter(initial, 3)

    assert not seen_counter.has_been_seen_n_times(initial)
    assert not seen_counter.has_been_seen_n_times(initial)
    assert seen_counter.has_been_seen_n_times(initial)

    assert not seen_counter.has_been_seen_n_times(new)
    assert not seen_counter.has_been_seen_n_times(new)
    assert seen_counter.has_been_seen_n_times(new)
