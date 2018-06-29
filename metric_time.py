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

    class Time:
        def __init__(self, hours, minutes, seconds, milliseconds):
            self.hours = hours
            self.minutes = minutes
            self.seconds = seconds
            self.milliseconds = milliseconds

    def decimal_time(self, time):
        """
        :description: Get decimal time for given `datetime`.
        :param datetime.datetime time: Datetime containing time of day.
        :return: Decimal time in the format (hours, minutes, seconds, milliseconds).
        :rtype: DecimalTime.Time
        """
        normal_seconds_from_midnight = time_from_midnight(time)
        metric_seconds_from_midnight = normal_seconds_from_midnight / 0.864

        metric_hours = metric_seconds_from_midnight / 10000
        metric_minutes = (metric_seconds_from_midnight / 100) % 100
        metric_seconds = metric_seconds_from_midnight % 100
        metric_milliseconds = (metric_seconds_from_midnight - int(metric_seconds_from_midnight)) * 1000
        return self.Time(hours=int(metric_hours), minutes=int(metric_minutes), seconds=int(metric_seconds),
                         milliseconds=int(metric_milliseconds))

    def now(self):
        """
        :description: Get decimal time for current time.
        :return: Decimal time.
        :rtype: DecimalTime.Time
        """
        return self.decimal_time(get_local_now())


class RepublicanCalendar(object):
    """
    Get specified datetime as a French Republican date.
    See more: https://en.wikipedia.org/wiki/French_Republican_Calendar
    """
    COMPLEMENTARY_DAYS = ("La Fête de la Vertu", "La Fête du Génie", "La Fête du Travail", "La Fête de l'Opinion",
                          "La Fête des Récompenses", "La Fête de la Révolution")

    WEEK_DAYS = ("Primidi", "Duodi", "Tridi", "Quartidi", "Quintidi",
                 "Sextidi", "Septidi", "Octidi", "Nonidi", "Décadi")

    MONTHS = (
        "Vendémiaire", "Brumaire", "Frimaire",  # Autumn
        "Nivôse", "Pluviôse", "Ventôse",  # Winter
        "Germinal", "Floréal", "Prairial",  # Spring
        "Messidor", "Thermidor", "Fructidor"  # Summer
    )

    class Date:
        def __init__(self, year, month, day, day_of_the_week):
            self.year = year
            self.month = month
            self.day = day
            self.day_of_the_week = day_of_the_week

    def republican_date(self, date):
        """
        :description: Get French Republican date for given `datetime`.
        :param datetime.datetime date: Datetime containing date.
        :return: French Republican date.
        :rtype: RepublicanCalendar.Date
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

        # Complementary days
        if time_since_new_year.days == 361:
            return self.Date(year=year, month=None, day=1, day_of_the_week=self.COMPLEMENTARY_DAYS[0])
        elif time_since_new_year.days == 362:
            return self.Date(year=year, month=None, day=2, day_of_the_week=self.COMPLEMENTARY_DAYS[1])
        elif time_since_new_year.days == 363:
            return self.Date(year=year, month=None, day=3, day_of_the_week=self.COMPLEMENTARY_DAYS[2])
        elif time_since_new_year.days == 364:
            return self.Date(year=year, month=None, day=4, day_of_the_week=self.COMPLEMENTARY_DAYS[3])
        elif time_since_new_year.days == 365:
            return self.Date(year=year, month=None, day=5, day_of_the_week=self.COMPLEMENTARY_DAYS[4])
        elif time_since_new_year.days == 366:
            return self.Date(year=year, month=None, day=6, day_of_the_week=self.COMPLEMENTARY_DAYS[5])

        month = self.MONTHS[int(time_since_new_year.days / 30.0)]
        day = time_since_new_year.days % 30
        day_of_the_week = self.WEEK_DAYS[day % 10 - 1]
        return self.Date(year=year, month=month, day=day, day_of_the_week=day_of_the_week)

    def now(self):
        """
        :description: Get French Republican date for current date.
        :return: French Republican date.
        :rtype: RepublicanCalendar.Date
        """
        return self.republican_date(get_local_now())


def main():
    try:
        republican_calendar = RepublicanCalendar()
        metric_time = DecimalTime()

        while True:
            time.sleep(0.01)
            current_republican_date = republican_calendar.now()
            current_metric_time = metric_time.now()

            print("\rRepublican date: {} {} {} {};  Decimal time: {:02}:{:02}:{:02}.{:03}".format(
                current_republican_date.day_of_the_week, current_republican_date.day, current_republican_date.month,
                int(current_republican_date.year), current_metric_time.hours, current_metric_time.minutes,
                current_metric_time.seconds, current_metric_time.milliseconds), end='')
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write('\n')


if __name__ == '__main__':
    main()
