from datetime import datetime


def get_now_time() -> float:
    return datetime.now().timestamp()


def get_now_datetime() -> datetime:
    return datetime.now()
