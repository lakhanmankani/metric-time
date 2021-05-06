import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name='metric-time',

    version='1.0.8',

    description='Implementation of decimal time and French Republican calendar.',
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",

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
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
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
