#  Copyright (c) 2019. Steven@oddineers.co.uk

import datetime
import time
import operator
from decimal import Decimal


class TimeUtilities:
    format = "%Y-%m-%d %H:%M:%S"
    tz = datetime.timezone.utc

    def convert_todate(self, dt, custom_format=False):
        date_format = self.format

        if custom_format:
            date_format = custom_format

        if type(dt) == int:
            date_obj = datetime.datetime.fromtimestamp(dt)
        else:
            try:
                date_obj = datetime.datetime.strptime(dt, date_format)
            except ValueError:
                return False

        return date_obj

    def get_datetime_now(self, tz=False):
        if tz:
            now = datetime.datetime.now(self.tz)
        else:
            now = datetime.datetime.now()
        return now

    @staticmethod
    def get_first_day(dt, d_years=0, d_months=0):
        # d_years, d_months are "deltas" to apply to dt
        y, m = dt.year + d_years, dt.month + d_months
        a, m = divmod(m-1, 12)
        return datetime.date(y+a, m+1, 1)

    def get_last_day(self, dt):
        return self.get_first_day(dt, 0, 1) + datetime.timedelta(-1)

    @staticmethod
    def get_month_number(dt, date_format=format):
        dt = datetime.datetime.strptime(str(dt)[:-7], date_format)
        return dt.month

    def subtract_time(self, t, n, period="days"):
        subtract_period = datetime.timedelta(days=n)

        if period == "hours":
            subtract_period = datetime.timedelta(hours=n)

        earlier = t - subtract_period

        if period == "months":
            earlier = self.subtract_months(t, n)

        return earlier

    def subtract_months(self, date, months):
        # Calculate the number of years and months to subtract
        years = months // 12
        remaining_months = months % 12

        # Subtract the years
        new_date = date.replace(year=date.year - years)

        # Subtract the remaining months
        while remaining_months > 0:
            # Get the day of the month
            day = new_date.day

            # Calculate the last day of the previous month
            last_day_of_prev_month = new_date.replace(day=1) - datetime.timedelta(days=1)

            # Subtract the remaining months
            if day > last_day_of_prev_month.day:
                day = last_day_of_prev_month.day

            if new_date.month == 1:
                new_date = new_date.replace(year=new_date.year - 1, month=new_date.month + 11, day=day)
            else:
                new_date = new_date.replace(month=new_date.month - 1, day=day)

            remaining_months -= 1

        return new_date

    @staticmethod
    def time_of_day(x):
        if 7 <= x.hour < 19:
            return 'day'
        elif 19 <= x.hour <= 23:
            return 'eve'
        elif 00 <= x.hour < 7:
            return 'eve'

    @staticmethod
    def calculate_days(datein, op, day):
        if isinstance(datein, str):
            datein = datetime.datetime.strptime(datein, "%Y-%m-%d %H:%M:%S")

        ops = {"+": operator.add,
           "-": operator.sub,
           "*": operator.mul,
           "/": operator.floordiv
        }
        op_func = ops[op]
        days_earlier = op_func(datein, datetime.timedelta(days=day))
        return days_earlier

    @staticmethod
    def calculate_hours(datein, op, hour):
        if isinstance(datein, str):
            datein = datetime.datetime.strptime(datein, "%Y-%m-%d %H:%M:%S")

        ops = {"+": operator.add,
           "-": operator.sub,
           "*": operator.mul,
           "/": operator.floordiv
        }
        op_func = ops[op]
        hours_earlier = op_func(datein, datetime.timedelta(hours=hour))
        return hours_earlier

    def time_within_range(self, datein, range=0.5, now=datetime.datetime.now()):
        timefuture = self.calculate_hours(now, "+", range)
        timepast = self.calculate_hours(now, "-", range)

        if datein <= timefuture and datein >= timepast:
            return True
        else:
            return False

    @staticmethod
    def get_date_part(date_type):
        """
        Get part of a datetime object now by name.
        :param date_type: Parts include: year, month, day, hour, minute, second, microsecond
        :type date_type: str
        :return: One of the following based on selection: year, month, day, hour, minute, second, microsecond
        :rtype: float or int
        """
        now = datetime.datetime.now()

        switcher = {
            'year': now.year,
            'month': now.month,
            'day': now.day,
            'hour': now.hour,
            'minute': now.minute,
            'second': now.second,
            'microsecond': now.microsecond,
        }
        return switcher.get(date_type, "Invalid Date Type Specified")

    @staticmethod
    def month_builder(month_num=0):
        """
        Get month name by month number.

        :param month_num: Month by number.
        :type month_num: int
        :return: Chosen month name.
        :rtype: str
        """
        switcher = {
            0: "N/A",
            1: "January",
            2: "February",
            3: "March",
            4: "April",
            5: "May",
            6: "June",
            7: "July",
            8: "August",
            9: "September",
            10: "October",
            11: "November",
            12: "December",
        }
        return switcher.get(month_num, "Invalid Month Number")

    @staticmethod
    def round_timedelta(datein, period):
        """
        Rounds the given timedelta by a given timedelta period

        :param datein: `timedelta` to be rounded.
        :param period: `timedelta` period to round by.
        """
        period_seconds = period.total_seconds()
        half_period_seconds = period_seconds / 2
        remainder = datein.total_seconds() % period_seconds
        if remainder >= half_period_seconds:
            return datetime.timedelta(seconds=datein.total_seconds() + (period_seconds - remainder))
        else:
            return datetime.timedelta(seconds=datein.total_seconds() - remainder)

    def pretty_date(self, time_test=False, time_against=False):
        """
        Tests a datetime object against another date tiem object to create past or present pretty string.
        Example: 'an hour ago', 'Yesterday', '3 months ago', 'just time_against', etc.

        :param time_test:
        :type time_test: datetime
        :param time_against:
        :type time_against: datetime
        :return: human friendly time since/till message.
        :rtype: str
        """
        if not time_against:
            time_against = datetime.datetime.now()

        if type(time_test) is int:
            diff = time_against - datetime.datetime.fromtimestamp(time_test)
        elif type(time_test) is datetime.datetime:
            diff = time_against - time_test
        elif type(time_test) is str:
            diff = time_against - self.convert_todate(time_test)
        elif not time_test:
            diff = time_against - time_against
        else:
            return 'undetermined'

        second_diff = diff.seconds
        human_second_diff = Decimal(second_diff).quantize(Decimal('1e-0'))
        day_diff = diff.days

        if day_diff < 0:
            return 'undetermined'

        if day_diff == 0:
            if second_diff <= 0:
                return "undetermined interval"
            if second_diff < 10:
                return "just now"
            if second_diff < 60:
                return str(human_second_diff) + " seconds"
            if second_diff < 120:
                return "a minute"
            if second_diff < 3600:
                human_second_diff = Decimal(human_second_diff / 60).quantize(Decimal('1e-0'))
                return str(human_second_diff) + " minutes"
            if second_diff < 7200:
                return "an hour"
            if second_diff < 86400:
                human_second_diff = Decimal(human_second_diff / 3600).quantize(Decimal('1e-0'))
                return str(human_second_diff) + " hours"
        if day_diff == 1:
            return "Yesterday"
        if day_diff < 7:
            return str(day_diff) + " days"
        if day_diff < 31:
            return str(day_diff / 7) + " weeks"
        if day_diff < 365:
            return str(day_diff / 30) + " months"
        return str(day_diff / 365) + " years"

    @staticmethod
    def is_dst():
        """
        Is day light saving (DST) time active
        :return: True or False
        :rtype: bool
        """
        if time.localtime().tm_isdst > 0:
            return True
        else:
            return False

    @staticmethod
    def get_day_state(sunrise, test_time=datetime.datetime.now()):
        """
        Determines the day state by comparing two datetime object hour values against specific interval relating to:
        morning, afternoon, evening and night
        :param sunrise:
        :type sunrise: datetime
        :param sunset:
        :type sunset: datetime
        :param test_time:
        :type test_time: datetime
        :return: morning, afternoon, evening and night
        :rtype: str
        """
        if sunrise.hour <= test_time.hour < 12:
            return 'morning'
        elif 12 <= test_time.hour < 18:
            return 'afternoon'
        elif 18 <= test_time.hour < 21:
            return 'evening'
        else:
            return 'night'

    @staticmethod
    def ordinal(n):
        return str(n) + ("th" if 4 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th"))

    def datetime_british(self, dt, f):
        return dt.strftime(f).replace("{th}", self.ordinal(dt.day))
