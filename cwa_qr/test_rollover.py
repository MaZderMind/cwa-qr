from datetime import datetime, time, date

from . import rollover


def test_rollover():
    rollover_time = time(4, 0)

    # between 4:00 and 23:59 it's the given day
    assert rollover.rollover_date(datetime(2021, 1, 1, 6, 0), rollover_time) == date(2021, 1, 1)
    assert rollover.rollover_date(datetime(2021, 1, 1, 12, 0), rollover_time) == date(2021, 1, 1)
    assert rollover.rollover_date(datetime(2021, 1, 1, 20, 0), rollover_time) == date(2021, 1, 1)
    assert rollover.rollover_date(datetime(2021, 1, 1, 22, 0), rollover_time) == date(2021, 1, 1)
    assert rollover.rollover_date(datetime(2021, 1, 1, 23, 59), rollover_time) == date(2021, 1, 1)

    # between 0:00 and 4:00 on the following day, it's still the day before
    assert rollover.rollover_date(datetime(2021, 1, 2, 0, 0), rollover_time) == date(2021, 1, 1)
    assert rollover.rollover_date(datetime(2021, 1, 2, 2, 0), rollover_time) == date(2021, 1, 1)
    assert rollover.rollover_date(datetime(2021, 1, 2, 3, 0), rollover_time) == date(2021, 1, 1)
    assert rollover.rollover_date(datetime(2021, 1, 2, 3, 59), rollover_time) == date(2021, 1, 1)

    # after 4:00 it's the next day
    assert rollover.rollover_date(datetime(2021, 1, 2, 4, 0), rollover_time) == date(2021, 1, 2)
    assert rollover.rollover_date(datetime(2021, 1, 2, 12, 0), rollover_time) == date(2021, 1, 2)
    assert rollover.rollover_date(datetime(2021, 1, 2, 20, 0), rollover_time) == date(2021, 1, 2)
    assert rollover.rollover_date(datetime(2021, 1, 2, 23, 0), rollover_time) == date(2021, 1, 2)
    assert rollover.rollover_date(datetime(2021, 1, 2, 23, 59), rollover_time) == date(2021, 1, 2)

    # and it continues to be the next day until 4:00
    assert rollover.rollover_date(datetime(2021, 1, 3, 0, 0), rollover_time) == date(2021, 1, 2)
    assert rollover.rollover_date(datetime(2021, 1, 3, 2, 0), rollover_time) == date(2021, 1, 2)
    assert rollover.rollover_date(datetime(2021, 1, 3, 3, 59), rollover_time) == date(2021, 1, 2)

    # then it's the day after
    assert rollover.rollover_date(datetime(2021, 1, 3, 4, 0), rollover_time) == date(2021, 1, 3)
