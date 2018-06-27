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
    def metric_time(self):
        normal_seconds_from_midnight = time_from_midnight()
        metric_seconds_from_midnight = normal_seconds_from_midnight / 0.864

        metric_hours = metric_seconds_from_midnight / 10000
        metric_minutes = (metric_seconds_from_midnight / 100) % 100
        metric_seconds = metric_seconds_from_midnight % 100
        metric_milliseconds = (metric_seconds_from_midnight - int(metric_seconds_from_midnight)) * 1000
        return metric_hours, metric_minutes, metric_seconds, metric_milliseconds


if __name__ == '__main__':
    try:
        metricTime = MetricTime()
        while True:
            time.sleep(0.01)
            metric_time = metricTime.metric_time()
            print("\rDecimal time: {:02}:{:02}:{:02}.{:03}".format(int(metric_time[0]), int(metric_time[1]), int(metric_time[2]), int(metric_time[3])), end='')
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write('\n')