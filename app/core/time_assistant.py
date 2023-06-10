from datetime import datetime, timedelta

from app.core import settings

FRIDAY = 4
MONDAY = 0


class TimeAssistant:
    def get_next_wipe_day(self) -> datetime:
        time_now = datetime.now(tz=settings.TIMEZONE)
        if time_now.weekday() > FRIDAY:
            print('monday wipe')
            return self._monday_wipe_date(time_now)
        else:
            return self._friday_wipe_date(time_now)

    def _monday_wipe_date(self, time_now: datetime) -> datetime:
        days_to_monday = self._days_to_next_day(time_now, MONDAY)
        print(days_to_monday)  # 1
        wipe_day = time_now + timedelta(days=days_to_monday)
        return datetime(
            year=wipe_day.year,
            month=wipe_day.month,
            day=wipe_day.day,
            hour=settings.WIPE_TIME,
            tzinfo=settings.TIMEZONE,
        )

    def _friday_wipe_date(self, time_now: datetime) -> datetime:
        days_to_friday = self._days_to_next_day(time_now, FRIDAY)
        wipe_day = time_now + timedelta(days=days_to_friday)
        return datetime(
            year=wipe_day.year,
            month=wipe_day.month,
            day=wipe_day.day,
            hour=settings.WIPE_TIME,
            tzinfo=settings.TIMEZONE,
        )

    def _days_to_next_day(self, date_now: datetime, day_of_week: int) -> int:
        days_to_day_of_week = day_of_week - date_now.weekday()
        if days_to_day_of_week <= 0:
            days_to_day_of_week += 7
        return days_to_day_of_week


time_assistant = TimeAssistant()
