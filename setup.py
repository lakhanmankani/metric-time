import setuptools

LONG_DESCRIPTION = r'''
metric-time
===========

Implementation of decimal time and French Republican calendar.
During the French Revolution, attempts were made decimalise various measuring methods including time and calendars. Two things arose from this movement: The french Republican calendar and Decimal calendar.

French Republic calendar:
The calendar consists of 12 months, each with exactly 30 days. Each week (décade) had 10 days. Years are counted in relation to the year 1792. The year usually begins on the 22nd of September. The calendar was introduced in 1793 and abolished in 1805

Decimal time:
A decimal clock consists of 10 hours, each containing 100 minutes with 100 seconds. This means that the definition of the second has to be changed to 1 decimal second = 0.864 normal seconds. It was introduced in 1794 and suspended in 1795.


Usage:

.. code-block:: bash

    $ metric-time

Or as a Python API:

.. code-block:: python

    >>> import metric_time
    >>> metric_time.DecimalTime.now()
    (8, 2, 88, 543) # Time in format (hours, minutes, seconds, milliseconds)
    >>> metric_time.DecimalTime.decimal_time(datetime.datetime(year=2018, month=6, day=28, hour=13, minute=50, second=30))
    (5, 76, 73, 611) # Time in format (hours, minutes, seconds, milliseconds)
    >>> metric_time.RepublicanCalendar().now()
    (226.91780821917808, 'Messidor', 10, 'Décadi') # Date in format (year, month, date, day)
    >>> metric_time.RepublicanCalendar().republican_date(datetime.datetime(year=2020, month=5, day=20, tzinfo=pytz.reference.LocalTimezone()))
    (228.81095890410958, 'Prairial', 2, 'Duodi') # Date in format (year, month, date, day)

'''.lstrip('\n')

setuptools.setup(
    name='metric-time',

    version='1.0.5',

    description='Implementation of decimal time and French Republican calendar.',
    long_description=LONG_DESCRIPTION,

    url='https://github.com/lakhanmankani/metric-time',

    author='Lakhan Mankani',
    author_email='lakhan.mankani@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Environment :: Console',

        'Intended Audience :: End Users/Desktop',

        'License :: OSI Approved :: MIT License',

        'Operating System :: OS Independent',

        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    keywords=['time', 'metric'],

    py_modules=['metric_time'],

    entry_points={
        'console_scripts': [
            'metric-time=metric_time:main',
        ]
    },

    test_suite='setup.test_suite'
)
