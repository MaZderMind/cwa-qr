from datetime import datetime

from . import seed


def assert_accepts_seed(value):
    seedA = seed.constructSeed(value)
    seedB = seed.constructSeed(value)
    assert len(seedA) == 16
    assert seedA == seedB


def test_accepts_int_seed():
    assert_accepts_seed(42)


def test_accepts_float_seed():
    assert_accepts_seed(3.1415)


def test_accepts_str_seed():
    assert_accepts_seed('foo')


def test_accepts_datetime_seed():
    assert_accepts_seed(datetime(2021, 4, 21, 10, 0))


def test_accepts_bytes_seed():
    assert_accepts_seed(b'\xDE\xAD\xBE\xEF')


def test_accepts_none_seed():
    assert_accepts_seed(None)
