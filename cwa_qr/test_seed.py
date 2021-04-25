from datetime import datetime, date

from . import seed


def assert_seed(input_value):
    seed_a = seed.construct_seed(input_value)
    seed_b = seed.construct_seed(input_value)
    assert len(seed_a) == 16
    assert seed_a == seed_b


def test_accepts_int_seed():
    assert_seed(42)


def test_accepts_float_seed():
    assert_seed(3.1415)


def test_accepts_str_seed():
    assert_seed('foo')


def test_accepts_datetime_seed():
    assert_seed(datetime(2021, 4, 21, 10, 0))


def test_accepts_date_seed():
    assert_seed(date(2021, 4, 21))


def test_accepts_bytes_seed():
    assert_seed(b'\xDE\xAD\xBE\xEF')


def test_accepts_none_seed():
    assert_seed(None)
