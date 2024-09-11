# Python Cron Expression Parser - cronexpr

`cronexpr` is a Python library for parsing and evaluating cron expressions. It is a simple wrapper of the parser that powers [supertinycron](https://github.com/exander77/supertinycron). This implementation was born out of a lack of cron libraries available for python that support all cron expression special characters including * / , - ? L W, # as well as 5, 6 (w/ seconds or year), or 7 (w/ seconds and year) part cron expressions.

## Credits and Complementary Libraries

* [supertinycron](https://github.com/exander77/supertinycron) - Active fork of the original ccronexpr library.
    - [gorhill's cronexpr on GitHub](https://github.com/gorhill/cronexpr/blob/master/README.md)
    - [Quartz Scheduler's CronExpression](https://www.javadoc.io/doc/org.quartz-scheduler/quartz/latest/org/quartz/CronExpression.html)
    - [ccronexpr by staticlibs on GitHub](https://github.com/staticlibs/ccronexpr/blob/master/README.md)
    - [ccronexpr by mdvorak on GitHub](https://github.com/mdvorak/ccronexpr/blob/main/README.md)
    - [Wikipedia on CRON Expression](https://en.wikipedia.org/wiki/Cron#CRON_expression)
* [gorhill/cronexpr](https://github.com/gorhill/cronexpr) - Go library with similar feature set
* [cron-descriptor](https://github.com/Salamek/cron-descriptor) - Python library for generating human-readable descriptions of cron expressions including the features of cronexpr. Ports are available in almost every language including [js](https://www.npmjs.com/package/cronstrue).
* [cronosjs](https://www.npmjs.com/package/cronosjs) - JavaScript library for parsing and evaluating cron expressions. Full support for all special characters and 5, 6, or 7 part cron expressions.
* [scikit-build tutorial](https://scikit-build-core.readthedocs.io/en/latest/getting_started.html)

## Installation

```bash
pip install cronexpr
```

## Usage

cronexpr exposes two methods, `prev_fire` and `next_fire`, which calculate the previous and next fire relative to the optional second datetime argument that specifies the date to start calculations from. Dates are processed in UTC and returned as a datetime with `tzinfo=timezone.utc`. 

```python
import cronexpr

# At 21:00, on the first Tuesday of the month, every 2 months
cron = "0 0 21 ? 1/2 TUE#1 *"
# Output: 
# Previous: 2024-09-03 21:00:00+00:00
# Next: 2024-11-05 21:00:00+00:00
print("Previous:", cronexpr.prev_fire(cron))
print("Next:", cronexpr.next_fire(cron))

# Output:
# Error parsing cron expression: Range - specified range exceeds maximum
try:
    # Invalid cron expression
    cronexpr.prev_fire("* 35 * * *")
except ValueError as e:
    print(e)
```

## Expressions

```
Field name     Mandatory?   Allowed values          Allowed special characters
----------     ----------   --------------          -------------------------
Second         No           0-59                    * / , - L
Minute         Yes          0-59                    * / , -
Hour           Yes          0-23                    * / , -
Day of month   Yes          1-31                    * / , - L W
Month          Yes          1-12 or JAN-DEC         * / , -
Day of week    Yes          0-7 or SUN-SAT          * / , - L #
Year           No           1970–2199               * / , -
```

Note: In the 'Day of week' field, both 0 and 7 represent SUN.

### Special Characters

#### Asterisk `*`

The asterisk indicates that the cron expression matches all values of the field. For instance, an asterisk in the 'Month' field matches every month.

#### Hyphen `-`

Hyphens define ranges. For instance, `2000-2010` in the 'Year' field matches every year from 2000 to 2010, inclusive.

#### Slash `/`

Slashes specify increments within ranges. For example, `3-59/15` in the 'Minute' field matches the third minute of the hour and every 15 minutes thereafter. The form `*/...` is equivalent to `first-last/...`, representing an increment over the full range of the field.

#### Comma `,`

Commas separate items in a list. For instance, `MON,WED,FRI` in the 'Day of week' field matches Mondays, Wednesdays, and Fridays.

#### `L`

The character `L` stands for "last". In the 'Day of week' field, `5L` denotes the last Friday of a given month. In the 'Day of month' field, it represents the last day of the month.

- Using `L` alone in the 'Day of week' field is equivalent to `0` or `SAT`. Hence, expressions `* * * * * L *` and `* * * * * 0 *` are the same.
  
- When followed by another value in the 'Day of week' field, like `6L`, it signifies the last Friday of the month.
  
- If followed by a negative number in the 'Day of month' field, such as `L-3`, it indicates the third-to-last day of the month.

- If `L` is present in the beginning of 'Second' field, it turns on non standard leap second functionality. Unless timezone specifies leap seconds, it will cycle indefinitely, because it will not be able to find any leap second!

When using 'L', avoid specifying lists or ranges to prevent ambiguous results.

#### `W`

The `W` character is exclusive to the 'Day of month' field. It indicates the closest business day (Monday-Friday) to the given day. For example, `15W` means the nearest business day to the 15th of the month. If you set 1W for the day-of-month and the 1st falls on a Saturday, the trigger activates on Monday the 3rd, since it respects the month's day boundaries and won't skip over them. Similarly, at the end of the month, the behavior ensures it doesn't "jump" over the boundary to the following month.

The `W` character can also pair with `L` (as `LW`), signifying the last business day of the month. Alone, it's equivalent to the range `1-5`, making the expressions `* * * W * * *` and `* * * * * 1-5 *` identical. This interpretation differs from [1,2].

#### Hash `#`

The `#` character is only for the 'Day of week' field and should be followed by a number between one and five, or their negative values. It lets you specify constructs like "the second Friday" of a month.

For example, `6#3` means the third Friday of the month. Note that if you use `#5` and there isn't a fifth occurrence of that weekday in the month, no firing occurs for that month. Using the '#' character requires a single expression in the 'Day of week' field.

Negative nth values are also valid. For instance, `6#-1` is equivalent to `6L`.

### Predefined cron expressions

```
    Entry       Description                                                             Equivalent to
    @annually   Run once a year at midnight in the morning of January 1                 0 0 0 1 1 *
    @yearly     Run once a year at midnight in the morning of January 1                 0 0 0 1 1 *
    @monthly    Run once a month at midnight in the morning of the first of the month   0 0 0 1 * *
    @weekly     Run once a week at midnight in the morning of Sunday                    0 0 0 * * 0
    @daily      Run once a day at midnight                                              0 0 0 * * *
    @hourly     Run once an hour at the beginning of the hour                           0 0 * * * *
    @minutely   Run once a minute at the beginning of minute                            0 * * * * *
    @secondly   Run once every second                                                   * * * * * * *
```