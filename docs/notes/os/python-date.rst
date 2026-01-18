.. meta::
    :description lang=en: Python datetime tutorial covering timestamps, date formatting, parsing, timezones, timedelta calculations, calendar operations, and time arithmetic
    :keywords: Python, Python3, datetime, date, time, timestamp, timezone, timedelta, strftime, strptime, calendar, UTC, ISO 8601, dateutil, zoneinfo

========
Datetime
========

:Source: `src/basic/datetime_.py <https://github.com/crazyguitar/pysheeet/blob/master/src/basic/datetime_.py>`_

.. contents:: Table of Contents
    :backlinks: none

Introduction
------------

Python's ``datetime`` module provides classes for manipulating dates and times.
The module includes ``date`` for calendar dates, ``time`` for clock times,
``datetime`` for combined date and time, ``timedelta`` for durations, and
``timezone`` for UTC offsets. Python 3.9+ also includes ``zoneinfo`` for
IANA timezone support. Understanding these classes is essential for logging,
scheduling, data analysis, and any application that works with temporal data.

Current Date and Time
---------------------

Getting the current date and time is one of the most common operations. Use
``datetime.now()`` for local time or ``datetime.utcnow()`` for UTC. In Python
3.11+, prefer ``datetime.now(timezone.utc)`` over ``utcnow()`` which is
deprecated.

.. code-block:: python

    from datetime import datetime, date, time, timezone

    # Current local datetime
    now = datetime.now()
    print(now)  # 2024-01-15 10:30:45.123456

    # Current UTC datetime (Python 3.11+ preferred)
    utc_now = datetime.now(timezone.utc)
    print(utc_now)  # 2024-01-15 02:30:45.123456+00:00

    # Current date only
    today = date.today()
    print(today)  # 2024-01-15

    # Current time only
    current_time = datetime.now().time()
    print(current_time)  # 10:30:45.123456

Creating Datetime Objects
-------------------------

You can create datetime objects by specifying year, month, day, and optionally
hour, minute, second, and microsecond. The ``date`` and ``time`` classes work
similarly for date-only or time-only values.

.. code-block:: python

    from datetime import datetime, date, time

    # Create specific datetime
    dt = datetime(2024, 1, 15, 10, 30, 45)
    print(dt)  # 2024-01-15 10:30:45

    # Create date only
    d = date(2024, 1, 15)
    print(d)  # 2024-01-15

    # Create time only
    t = time(10, 30, 45)
    print(t)  # 10:30:45

    # Combine date and time
    combined = datetime.combine(d, t)
    print(combined)  # 2024-01-15 10:30:45

    # Get date or time from datetime
    print(dt.date())  # 2024-01-15
    print(dt.time())  # 10:30:45

Timestamps
----------

Unix timestamps represent seconds since January 1, 1970 (the Unix epoch).
Converting between timestamps and datetime objects is common when working
with APIs, databases, and log files.

.. code-block:: python

    import time
    from datetime import datetime, timezone

    # Current timestamp
    ts = time.time()
    print(ts)  # 1705312245.123456

    # Timestamp to datetime (local time)
    dt = datetime.fromtimestamp(ts)
    print(dt)  # 2024-01-15 10:30:45.123456

    # Timestamp to datetime (UTC)
    dt_utc = datetime.fromtimestamp(ts, tz=timezone.utc)
    print(dt_utc)  # 2024-01-15 02:30:45.123456+00:00

    # Datetime to timestamp
    ts_back = dt.timestamp()
    print(ts_back)  # 1705312245.123456

    # Millisecond timestamp (common in JavaScript/APIs)
    ts_ms = int(ts * 1000)
    print(ts_ms)  # 1705312245123

Formatting Dates (strftime)
---------------------------

The ``strftime()`` method formats datetime objects as strings using format
codes. This is essential for displaying dates to users, generating filenames,
or formatting data for APIs.

.. code-block:: python

    from datetime import datetime

    dt = datetime(2024, 1, 15, 14, 30, 45)

    # Common formats
    print(dt.strftime("%Y-%m-%d"))           # 2024-01-15
    print(dt.strftime("%d/%m/%Y"))           # 15/01/2024
    print(dt.strftime("%B %d, %Y"))          # January 15, 2024
    print(dt.strftime("%Y-%m-%d %H:%M:%S"))  # 2024-01-15 14:30:45
    print(dt.strftime("%I:%M %p"))           # 02:30 PM
    print(dt.strftime("%A, %B %d"))          # Monday, January 15

    # ISO 8601 format
    print(dt.isoformat())                    # 2024-01-15T14:30:45

    # For filenames (no special characters)
    print(dt.strftime("%Y%m%d_%H%M%S"))      # 20240115_143045

Common format codes:

- ``%Y`` - 4-digit year (2024)
- ``%m`` - Month as zero-padded number (01-12)
- ``%d`` - Day as zero-padded number (01-31)
- ``%H`` - Hour 24-hour format (00-23)
- ``%I`` - Hour 12-hour format (01-12)
- ``%M`` - Minute (00-59)
- ``%S`` - Second (00-59)
- ``%p`` - AM/PM
- ``%A`` - Full weekday name
- ``%B`` - Full month name
- ``%z`` - UTC offset (+0000)
- ``%Z`` - Timezone name

Parsing Dates (strptime)
------------------------

The ``strptime()`` method parses strings into datetime objects. The format
string must match the input exactly. This is commonly used when reading
dates from files, user input, or APIs.

.. code-block:: python

    from datetime import datetime

    # Parse various formats
    dt1 = datetime.strptime("2024-01-15", "%Y-%m-%d")
    dt2 = datetime.strptime("15/01/2024", "%d/%m/%Y")
    dt3 = datetime.strptime("January 15, 2024", "%B %d, %Y")
    dt4 = datetime.strptime("2024-01-15 14:30:45", "%Y-%m-%d %H:%M:%S")

    print(dt1)  # 2024-01-15 00:00:00
    print(dt4)  # 2024-01-15 14:30:45

    # Parse ISO 8601 format
    dt5 = datetime.fromisoformat("2024-01-15T14:30:45")
    print(dt5)  # 2024-01-15 14:30:45

    # Parse with timezone (Python 3.11+)
    dt6 = datetime.fromisoformat("2024-01-15T14:30:45+00:00")
    print(dt6)  # 2024-01-15 14:30:45+00:00

Date Arithmetic with timedelta
------------------------------

The ``timedelta`` class represents a duration—the difference between two dates
or times. Use it to add or subtract time from datetime objects, or to calculate
the difference between two dates.

.. code-block:: python

    from datetime import datetime, timedelta

    now = datetime.now()

    # Add time
    tomorrow = now + timedelta(days=1)
    next_week = now + timedelta(weeks=1)
    in_2_hours = now + timedelta(hours=2)
    in_90_minutes = now + timedelta(minutes=90)

    # Subtract time
    yesterday = now - timedelta(days=1)
    last_month = now - timedelta(days=30)

    # Combine units
    future = now + timedelta(days=5, hours=3, minutes=30)

    # Calculate difference between dates
    date1 = datetime(2024, 1, 1)
    date2 = datetime(2024, 12, 31)
    diff = date2 - date1
    print(diff.days)          # 365
    print(diff.total_seconds())  # 31536000.0

    # Compare dates
    print(date2 > date1)      # True

Timezones
---------

Working with timezones correctly is crucial for applications serving users
across different regions. Python 3.9+ includes ``zoneinfo`` for IANA timezone
support. For earlier versions, use ``pytz`` or ``dateutil``.

.. code-block:: python

    from datetime import datetime, timezone, timedelta

    # UTC timezone
    utc = timezone.utc
    dt_utc = datetime.now(utc)
    print(dt_utc)  # 2024-01-15 02:30:45.123456+00:00

    # Fixed offset timezone
    pst = timezone(timedelta(hours=-8))
    dt_pst = datetime.now(pst)
    print(dt_pst)  # 2024-01-14 18:30:45.123456-08:00

    # Convert between timezones
    dt_converted = dt_utc.astimezone(pst)
    print(dt_converted)

    # Python 3.9+ with zoneinfo
    from zoneinfo import ZoneInfo

    eastern = ZoneInfo("America/New_York")
    tokyo = ZoneInfo("Asia/Tokyo")

    dt_eastern = datetime.now(eastern)
    dt_tokyo = dt_eastern.astimezone(tokyo)
    print(dt_tokyo)

    # Make naive datetime timezone-aware
    naive = datetime(2024, 1, 15, 10, 30)
    aware = naive.replace(tzinfo=utc)

Comparing Dates
---------------

Datetime objects support comparison operators. When comparing timezone-aware
and naive datetimes, Python raises a TypeError to prevent subtle bugs.

.. code-block:: python

    from datetime import datetime, date, timedelta

    dt1 = datetime(2024, 1, 15, 10, 0)
    dt2 = datetime(2024, 1, 15, 14, 0)
    dt3 = datetime(2024, 1, 16, 10, 0)

    # Comparisons
    print(dt1 < dt2)   # True
    print(dt1 == dt2)  # False
    print(dt3 > dt2)   # True

    # Check if date is in range
    start = datetime(2024, 1, 1)
    end = datetime(2024, 12, 31)
    check = datetime(2024, 6, 15)
    print(start <= check <= end)  # True

    # Check if date is today
    today = date.today()
    some_date = date(2024, 1, 15)
    print(some_date == today)

    # Days until a date
    future = date(2024, 12, 25)
    days_until = (future - today).days
    print(f"Days until: {days_until}")

Working with Weeks
------------------

Getting week numbers, weekdays, and working with ISO week dates is common
for reporting and scheduling applications.

.. code-block:: python

    from datetime import datetime, date, timedelta

    dt = datetime(2024, 1, 15)

    # Day of week (0=Monday, 6=Sunday)
    print(dt.weekday())     # 0 (Monday)
    print(dt.isoweekday())  # 1 (Monday, ISO format 1-7)

    # Week number
    print(dt.isocalendar())  # (2024, 3, 1) - year, week, weekday

    # Get start of week (Monday)
    start_of_week = dt - timedelta(days=dt.weekday())
    print(start_of_week)  # 2024-01-15 00:00:00

    # Get end of week (Sunday)
    end_of_week = start_of_week + timedelta(days=6)
    print(end_of_week)  # 2024-01-21 00:00:00

    # Check if weekend
    is_weekend = dt.weekday() >= 5
    print(is_weekend)  # False

Start and End of Day/Month/Year
-------------------------------

Getting the start or end of a time period is useful for date range queries
and reporting.

.. code-block:: python

    from datetime import datetime, date, time, timedelta
    import calendar

    dt = datetime(2024, 1, 15, 14, 30, 45)

    # Start of day
    start_of_day = datetime.combine(dt.date(), time.min)
    print(start_of_day)  # 2024-01-15 00:00:00

    # End of day
    end_of_day = datetime.combine(dt.date(), time.max)
    print(end_of_day)  # 2024-01-15 23:59:59.999999

    # Start of month
    start_of_month = dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    print(start_of_month)  # 2024-01-01 00:00:00

    # End of month
    last_day = calendar.monthrange(dt.year, dt.month)[1]
    end_of_month = dt.replace(day=last_day, hour=23, minute=59, second=59)
    print(end_of_month)  # 2024-01-31 23:59:59

    # Start of year
    start_of_year = dt.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    print(start_of_year)  # 2024-01-01 00:00:00

Calendar Operations
-------------------

The ``calendar`` module provides functions for working with calendars,
including checking leap years, getting month ranges, and generating
calendar displays.

.. code-block:: python

    import calendar
    from datetime import date

    # Check leap year
    print(calendar.isleap(2024))  # True
    print(calendar.isleap(2023))  # False

    # Days in month
    print(calendar.monthrange(2024, 2))  # (3, 29) - weekday of 1st, days in month
    days_in_feb = calendar.monthrange(2024, 2)[1]
    print(days_in_feb)  # 29

    # Generate month calendar
    print(calendar.month(2024, 1))

    # Iterate through month days
    cal = calendar.Calendar()
    for day in cal.itermonthdays(2024, 1):
        if day != 0:
            print(day, end=" ")  # 1 2 3 ... 31

Date Ranges
-----------

Generating sequences of dates is useful for reports, charts, and scheduling.

.. code-block:: python

    from datetime import datetime, date, timedelta

    def date_range(start, end, step=timedelta(days=1)):
        """Generate dates from start to end."""
        current = start
        while current <= end:
            yield current
            current += step

    # Daily dates
    start = date(2024, 1, 1)
    end = date(2024, 1, 7)
    for d in date_range(start, end):
        print(d)

    # Weekly dates
    for d in date_range(start, date(2024, 1, 31), timedelta(weeks=1)):
        print(d)

    # Business days (skip weekends)
    def business_days(start, end):
        current = start
        while current <= end:
            if current.weekday() < 5:  # Monday=0 to Friday=4
                yield current
            current += timedelta(days=1)

Age Calculation
---------------

Calculating age from a birthdate requires handling the edge case where the
birthday hasn't occurred yet this year.

.. code-block:: python

    from datetime import date

    def calculate_age(birthdate):
        """Calculate age in years from birthdate."""
        today = date.today()
        age = today.year - birthdate.year
        # Subtract 1 if birthday hasn't occurred this year
        if (today.month, today.day) < (birthdate.month, birthdate.day):
            age -= 1
        return age

    birthdate = date(1990, 6, 15)
    age = calculate_age(birthdate)
    print(f"Age: {age}")

    # Days until next birthday
    def days_until_birthday(birthdate):
        today = date.today()
        next_birthday = birthdate.replace(year=today.year)
        if next_birthday < today:
            next_birthday = next_birthday.replace(year=today.year + 1)
        return (next_birthday - today).days

Human Readable Time Differences
-------------------------------

Converting timedelta to human-readable strings like "2 hours ago" or
"in 3 days" improves user experience.

.. code-block:: python

    from datetime import datetime, timedelta

    def time_ago(dt):
        """Convert datetime to human-readable relative time."""
        now = datetime.now()
        diff = now - dt

        seconds = diff.total_seconds()
        if seconds < 60:
            return "just now"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        elif seconds < 86400:
            hours = int(seconds // 3600)
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif seconds < 604800:
            days = int(seconds // 86400)
            return f"{days} day{'s' if days != 1 else ''} ago"
        else:
            return dt.strftime("%B %d, %Y")

    # Examples
    print(time_ago(datetime.now() - timedelta(minutes=5)))   # 5 minutes ago
    print(time_ago(datetime.now() - timedelta(hours=2)))     # 2 hours ago
    print(time_ago(datetime.now() - timedelta(days=3)))      # 3 days ago

Using dateutil for Flexible Parsing
-----------------------------------

The ``python-dateutil`` library provides powerful parsing that handles many
date formats automatically, plus relative delta calculations.

.. code-block:: python

    # pip install python-dateutil
    from dateutil import parser
    from dateutil.relativedelta import relativedelta
    from datetime import datetime

    # Flexible parsing - handles many formats automatically
    dt1 = parser.parse("January 15, 2024")
    dt2 = parser.parse("15/01/2024")
    dt3 = parser.parse("2024-01-15T14:30:45Z")
    dt4 = parser.parse("Jan 15 2024 2:30 PM")

    # Relative delta - handles months and years correctly
    now = datetime.now()

    # Add 1 month (handles varying month lengths)
    next_month = now + relativedelta(months=1)

    # Add 1 year
    next_year = now + relativedelta(years=1)

    # Last day of next month
    last_of_next_month = now + relativedelta(months=1, day=31)

    # Complex relative: 2 months and 3 days ago
    past = now - relativedelta(months=2, days=3)
