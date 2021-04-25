from datetime import datetime, date, time, timedelta


def rolloverDate(dt: datetime, rollover: time) -> date:
    given_time = dt.time()
    if given_time < rollover:
        return dt.date() - timedelta(days=1)
    else:
        return dt.date()
