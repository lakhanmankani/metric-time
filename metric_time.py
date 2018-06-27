import datetime
import pytz.reference
import sys
import time


def get_local_now():
    return datetime.datetime.now(pytz.reference.LocalTimezone())


def time_from_midnight(dt=None):
    if dt is None:
        dt = get_local_now()
    midnight = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    return (dt - midnight).total_seconds()


class MetricTime(object):
    @staticmethod
    def now():
        normal_seconds_from_midnight = time_from_midnight()
        metric_seconds_from_midnight = normal_seconds_from_midnight / 0.864

        metric_hours = metric_seconds_from_midnight / 10000
        metric_minutes = (metric_seconds_from_midnight / 100) % 100
        metric_seconds = metric_seconds_from_midnight % 100
        metric_milliseconds = (metric_seconds_from_midnight - int(metric_seconds_from_midnight)) * 1000
        return int(metric_hours), int(metric_minutes), int(metric_seconds), int(metric_milliseconds)


class RepublicanCalendar(object):
    WEEK_DAYS = ("Primidi", "Duodi", "Tridi", "Quartidi", "Quintidi",
                 "Sextidi", "Septidi", "Octidi", "Nonidi", "Décadi")

    MONTHS = (
        "Vendémiaire", "Brumaire", "Frimaire",  # Autumn
        "Nivôse", "Pluviôse", "Ventôse",  # Winter
        "Germinal", "Floréal", "Prairial",  # Spring
        "Messidor", "Thermidor", "Fructidor"  # Summer
    )

    def now(self):
        time_now = get_local_now()

        time_difference = datetime.datetime.now() - datetime.datetime(year=1791, month=9, day=21)
        year = time_difference.days / 365
        leap_year = year % 4 == 0 and year % 100 != 0

        if leap_year:
            # If leap year, add 1 day
            if time_now.month < 9 or (time_now.month == 9 and time_now.day < 23):
                # New years was last Gregorian year
                time_since_new_year = time_now - datetime.datetime(year=time_now.year-1, month=9, day=22,
                                                                   tzinfo=pytz.reference.LocalTimezone())
            else:
                # New years was this Gregorian year
                time_since_new_year = time_now - datetime.datetime(year=time_now.year, month=9, day=22,
                                                                   tzinfo=pytz.reference.LocalTimezone())
        else:
            if time_now.month < 9 or (time_now.month == 9 and time_now.day < 22):
                # New years was last Gregorian year
                time_since_new_year = time_now - datetime.datetime(year=time_now.year-1, month=9, day=21,
                                                                   tzinfo=pytz.reference.LocalTimezone())
            else:
                # New years was this Gregorian year
                time_since_new_year = time_now - datetime.datetime(year=time_now.year, month=9, day=21,
                                                                   tzinfo=pytz.reference.LocalTimezone())

        month = self.MONTHS[int(time_since_new_year.days / 30.0)]
        day = time_since_new_year.days % 30
        day_of_the_week = self.WEEK_DAYS[day % 10 - 1]
        return year, month, day, day_of_the_week


if __name__ == '__main__':
    file_write = sys.stdout.write
    file_flush = sys.stdout.flush

    try:
        republicanCalendar = RepublicanCalendar()
        metricTime = MetricTime()

        while True:
            time.sleep(0.01)
            republican_date = republicanCalendar.now()
            metric_time = metricTime.now()

            print("\rRepublican date: {} {} {} {};  Decimal time: {:02}:{:02}:{:02}.{:03}".format(republican_date[3],
                                                                                                  republican_date[2],
                                                                                                  republican_date[1],
                                                                                                  int(
                                                                                                      republican_date[0]
                                                                                                      ),
                                                                                                  metric_time[0],
                                                                                                  metric_time[1],
                                                                                                  metric_time[2],
                                                                                                  metric_time[3]),
                  end='')
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write('\n')
