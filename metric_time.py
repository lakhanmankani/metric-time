#!/usr/bin/env python3

"""Metric time implementation"""

import datetime
import sys
import time

import pytz.reference


def get_local_now():
    """
    :return: Local time adjusted to time zone.
    :rtype: datetime
    """
    return datetime.datetime.now(pytz.reference.LocalTimezone())


def time_from_midnight(dt=None):
    """
    :param dt: (Optional) `datetime`. Defaults to current time
    :return: Seconds ellapsed from local midnight.
    :rtype: Float
    """
    if dt is None:
        dt = get_local_now()
    midnight = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    return (dt - midnight).total_seconds()


class DecimalTime(object):
    """
    Get specified datetime as decimal time.
    See more: https://en.wikipedia.org/wiki/Decimal_time)
    """
    @staticmethod
    def decimal_time(time):
        """
        :description: Get decimal time for given `datetime`.
        :param datetime.datetime time: Datetime containing time of day.
        :return: Decimal time in the format (hours, minutes, seconds, milliseconds).
        :rtype: tuple
        """

        normal_seconds_from_midnight = time_from_midnight(time)
        metric_seconds_from_midnight = normal_seconds_from_midnight / 0.864

        metric_hours = metric_seconds_from_midnight / 10000
        metric_minutes = (metric_seconds_from_midnight / 100) % 100
        metric_seconds = metric_seconds_from_midnight % 100
        metric_milliseconds = (metric_seconds_from_midnight - int(metric_seconds_from_midnight)) * 1000
        return int(metric_hours), int(metric_minutes), int(metric_seconds), int(metric_milliseconds)

    def now(self):
        """
        :description: Get decimal time for current time.
        :return: Decimal time in the format (hours, minutes, seconds, milliseconds).
        :rtype: tuple
        """
        return self.decimal_time(get_local_now())


class RepublicanCalendar(object):
    """
    Get specified datetime as a French Republican date.
    See more: https://en.wikipedia.org/wiki/French_Republican_Calendar
    """
    WEEK_DAYS = ("Primidi", "Duodi", "Tridi", "Quartidi", "Quintidi",
                 "Sextidi", "Septidi", "Octidi", "Nonidi", "Décadi")

    MONTHS = (
        "Vendémiaire", "Brumaire", "Frimaire",  # Autumn
        "Nivôse", "Pluviôse", "Ventôse",  # Winter
        "Germinal", "Floréal", "Prairial",  # Spring
        "Messidor", "Thermidor", "Fructidor"  # Summer
    )

    def republican_date(self, date):
        """
        :description: Get French Republican date for given `datetime`.
        :param datetime.datetime date: Datetime containing date.
        :return: French Republican date in the format (year, month, day, day_of_the_week).
        :rtype: tuple
        """

        time_difference = date - datetime.datetime(year=1791, month=9, day=21, tzinfo=datetime.timezone.utc)

        year = time_difference.days / 365
        leap_year = year % 4 == 0 and year % 100 != 0

        if leap_year:
            # If leap year, add 1 day
            if date.month < 9 or (date.month == 9 and date.day < 23):
                # New years was last Gregorian year
                time_since_new_year = date - datetime.datetime(year=date.year - 1, month=9, day=22,
                                                               tzinfo=pytz.reference.LocalTimezone())
            else:
                # New years was this Gregorian year
                time_since_new_year = date - datetime.datetime(year=date.year, month=9, day=22,
                                                               tzinfo=pytz.reference.LocalTimezone())
        else:
            if date.month < 9 or (date.month == 9 and date.day < 22):
                # New years was last Gregorian year
                time_since_new_year = date - datetime.datetime(year=date.year - 1, month=9, day=21,
                                                               tzinfo=pytz.reference.LocalTimezone())
            else:
                # New years was this Gregorian year
                time_since_new_year = date - datetime.datetime(year=date.year, month=9, day=21,
                                                               tzinfo=pytz.reference.LocalTimezone())

        month = self.MONTHS[int(time_since_new_year.days / 30.0)]
        day = time_since_new_year.days % 30
        day_of_the_week = self.WEEK_DAYS[day % 10 - 1]
        return year, month, day, day_of_the_week

    def now(self):
        """
        :description: Get French Republican date for current date.
        :return: French Republican date in the format (year, month, day, day_of_the_week).
        :rtype: tuple
        """
        return self.republican_date(get_local_now())


if __name__ == '__main__':
    try:
        republicanCalendar = RepublicanCalendar()
        metricTime = DecimalTime()

        while True:
            time.sleep(0.01)
            current_republican_date = republicanCalendar.now()
            current_metric_time = metricTime.now()

            print("\rRepublican date: {} {} {} {};  Decimal time: {:02}:{:02}:{:02}.{:03}".format(
                current_republican_date[3], current_republican_date[2], current_republican_date[1],
                int(current_republican_date[0]), current_metric_time[0], current_metric_time[1], current_metric_time[2],
                current_metric_time[3]), end='')
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write('\n')
