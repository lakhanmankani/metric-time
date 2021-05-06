# metric-time
Implementation of decimal time and French Republican calendar.

During the French Revolution, attempts were made decimalise various measuring methods including time and calendars. Two things arose from this movement: The french Republican calendar and Decimal calendar.

### French Republic calendar
The [French Republic calendar](https://en.wikipedia.org/wiki/French_Republican_Calendar) calendar consists of 12 months, each with exactly 30 days. Each week (décade) had 10 days. Years are counted in relation to the year 1792. The year usually begins on the 22nd of September. The calendar was introduced in 1793 and abolished in 1805

### Decimal time
A [decimal clock](https://en.wikipedia.org/wiki/Decimal_time) consists of 10 hours, each containing 100 minutes with 100 seconds. This means that the definition of the second has to be changed to 1 decimal second = 0.864 normal seconds. It was introduced in 1794 and suspended in 1795.

## Installation
Pip
```bash
$ pip install metric-time
```

Git clone
```bash
$ git clone https://github.com/lakhanmankani/metric-time.git
```

## Usage
```bash
$ metric-time
```

```bash
$ python3 metric_time.py
```
or as a Python API
```python
>>> import metric_time
>>> import datetime
>>> import pytz.reference
>>> decimal_time = metric_time.DecimalTime()
>>> decimal_time.now()
"08:02:88.543" # Time in format hours:minutes:seconds.milliseconds
>>> republican_calendar = metric_time.RepublicanCalendar()
>>> republican_calendar.now()
"Décadi 10 Messidor 226" # Date in format day date month year
```

Convert from normal date time to metric
```python
>>> decimal_time.decimal_time(datetime.datetime(year=2018, month=6, day=28, hour=13, minute=50, second=30))
"05:76:73.611" # Time in format hours:minutes:seconds.milliseconds
>>> republican_calendar.republican_date(datetime.datetime(year=2020, month=5, day=20, tzinfo=pytz.reference.LocalTimezone()))
"Duodi 2 Prairial 228" # Date in format day date month year
```

Access time components
```python
>>> now_time = decimal_time.now()
>>> now_time.hours
8
>>> now_time.minutes
2
>>> now_time.seconds
88
>>> now_time.milliseconds
543
```
Access date components
```python
>>> now_date = republican_calendar.now()
>>> now_date.year
226.91780821917808
>>> now_date.month
"Prairial"
>>> now_date.day
10
>>> now_date.day_of_the_week
"Décadi"
```
