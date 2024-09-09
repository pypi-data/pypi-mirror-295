# coding=utf-8
import time
import calendar
import datetime
from datetime import timezone, timedelta
# from dateutil.relativedelta import relativedelta


class DateUtil(object):

    @classmethod
    def generate_time(cls, hours: int = 0, minutes: int = 0, format='%Y-%m-%d %H:%M:%S') -> str:
        now = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)
        hours = int(hours)
        minutes = int(minutes)
        modified = now + datetime.timedelta(hours=hours, minutes=minutes)
        return str(modified.strftime(format))

    @classmethod
    def get_time_now(cls):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    @classmethod
    def get_now_epoch(cls, is_ms=True) -> int:
        if not is_ms:
            return int(calendar.timegm(time.localtime()))
        return int(calendar.timegm(time.localtime()) * 1000)

    @classmethod
    def get_now_epoch_without_hms(cls) -> int:
        return calendar.timegm([datetime.datetime.now().year, datetime.datetime.now().month,
                                datetime.datetime.now().day, 0, 0, 0]) * 1000

    @classmethod
    def convert_epoch_time_to_datetime(cls, epoch, zone=timezone(timedelta(hours=0)), format='%Y-%m-%d %H:%M:%S'):
        return datetime.datetime.fromtimestamp(int(epoch) / 1000, zone).strftime(format)

    @classmethod
    def generate_epoch_time(cls, hours_delta: int = 0, minutes_delta: int = 0, days_delta: int = 0) -> int:
        now = datetime.datetime.now()
        hours = int(hours_delta)
        minutes = int(minutes_delta)
        days = int(days_delta)
        modified = now + \
                   datetime.timedelta(hours=hours, minutes=minutes, days=days)
        return int(time.mktime(modified.timetuple())) * 1000

    # cur_time type :datetime
    @classmethod
    def add_day_time(cls, cur_time: datetime.date, add_day: int) -> datetime.date:
        required_day = cur_time + datetime.timedelta(int(add_day))
        return required_day

    @classmethod
    def update_date(cls, date_str, add_day, format='%Y-%m-%d %H:%M:%S'):
        d = datetime.datetime.strptime(str(date_str), format)
        d1 = datetime.timedelta(days=int(add_day))
        return str(d + d1)

    @classmethod
    def update_days(cls, latest_date: str, day_num: int, format_date: bool = False) -> str:
        if not isinstance(latest_date, str):
            latest_date = str(latest_date)
        if '-' in latest_date:
            latest_date = ''.join(latest_date.split('-'))
        d = datetime.datetime.strptime(latest_date, '%Y%m%d')
        d1 = datetime.timedelta(days=int(day_num))
        date_str = str(d + d1).split()[0]
        if not format_date:
            return date_str.replace("-", "")
        else:
            return date_str

    @classmethod
    def update_hours(cls, date_str, add_hours):
        d = datetime.datetime.strptime(str(date_str), '%Y-%m-%d %H:%M:%S')
        d1 = datetime.timedelta(hours=int(add_hours))
        return str(d + d1)

    @classmethod
    def update_minutes(cls, date_str, add_minutes):
        d = datetime.datetime.strptime(str(date_str), '%Y-%m-%d %H:%M:%S')
        d1 = datetime.timedelta(minutes=int(add_minutes))
        return str(d + d1)

    @classmethod
    def gen_epoch_by_specified_date(cls, year, month, day, add_day=0):
        return calendar.timegm([year, month, day + add_day, 0, 0, 0]) * 1000

    @classmethod
    def generate_today(cls, format=True) -> str:
        today = datetime.date.today()
        if not format:
            return str(today.strftime('%Y%m%d'))
        return str(today.strftime('%Y-%m-%d'))

    @classmethod
    def get_required_epoch(cls, required_date: str, date_formate: str = "%Y-%m-%d") -> int:
        time_array = time.strptime(str(required_date), date_formate)
        required_epoch = int(time.mktime(time_array))
        return required_epoch * 1000

    @classmethod
    def add_minute_time(cls, cur_time: datetime.date, minute: int) -> datetime.date:
        required_time = cur_time + datetime.timedelta(minutes=int(minute))
        return required_time

    @classmethod
    def add_hour_time(cls, cur_time: datetime.date, hour: int) -> datetime.date:
        required_time = cur_time + datetime.timedelta(hours=int(hour))
        return required_time

    @classmethod
    def convert_date_to_str(cls, required_date: datetime.date, format="%Y-%m-%d") -> str:
        return str(required_date.strftime(format))

    @classmethod
    def get_toady_without_time_zone(cls, format="%Y-%m-%d %H:%M:%S", add_days=0):
        today_epoch = DateUtil().get_now_epoch_without_hms()
        day_str = str(DateUtil().convert_epoch_time_to_datetime(today_epoch,
                                                                timezone(timedelta(hours=8)),
                                                                format))
        if add_days != 0:
            day_str = DateUtil().update_date(day_str, add_days, format)
        return day_str

    @classmethod
    def get_datetime(cls):
        now = datetime.datetime.now()
        return now.strftime('%Y-%m-%d %H:%M:%S')

    @classmethod
    def get_total_seconds(cls, t2):
        t1 = datetime.datetime.now()
        return (t1 - t2).total_seconds()
