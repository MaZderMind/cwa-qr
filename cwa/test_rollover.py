from datetime import datetime, time, date

from . import rollover


def test_rollover():
    rollover_time = time(13, 0)

    # before 13:00 it's the given day
    assert rollover.rolloverDate(datetime(2021, 1, 1, 0, 0), rollover_time) == date(2021, 1, 1)
    assert rollover.rolloverDate(datetime(2021, 1, 1, 6, 0), rollover_time) == date(2021, 1, 1)
    assert rollover.rolloverDate(datetime(2021, 1, 1, 12, 0), rollover_time) == date(2021, 1, 1)

    # after 13:00 it's the next day
    assert rollover.rolloverDate(datetime(2021, 1, 1, 13, 0), rollover_time) == date(2021, 1, 2)
    assert rollover.rolloverDate(datetime(2021, 1, 1, 16, 0), rollover_time) == date(2021, 1, 2)
    assert rollover.rolloverDate(datetime(2021, 1, 1, 20, 0), rollover_time) == date(2021, 1, 2)
    assert rollover.rolloverDate(datetime(2021, 1, 1, 23, 0), rollover_time) == date(2021, 1, 2)
    assert rollover.rolloverDate(datetime(2021, 1, 1, 23, 59), rollover_time) == date(2021, 1, 2)

    # and it continues to be the next day until 13:00
    assert rollover.rolloverDate(datetime(2021, 1, 2, 0, 0), rollover_time) == date(2021, 1, 2)
    assert rollover.rolloverDate(datetime(2021, 1, 2, 6, 0), rollover_time) == date(2021, 1, 2)
    assert rollover.rolloverDate(datetime(2021, 1, 2, 12, 0), rollover_time) == date(2021, 1, 2)

    # then it's the day after
    assert rollover.rolloverDate(datetime(2021, 1, 2, 13, 0), rollover_time) == date(2021, 1, 3)
