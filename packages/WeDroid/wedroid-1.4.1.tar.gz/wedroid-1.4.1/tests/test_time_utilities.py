from wedroid import time_utilities
time_utils = time_utilities.TimeUtilities()

# Test day state identification
sunrise = time_utils.convert_todate('2020-09-18 06:21:27')
test = time_utils.convert_todate('2020-09-18 21:21:27')
print(time_utils.get_day_state(sunrise, test))

test = time_utils.convert_todate('2020-09-18 19:21:27')
print(time_utils.get_day_state(sunrise, test))

test = time_utils.convert_todate('2020-09-18 15:21:27')
print(time_utils.get_day_state(sunrise, test))

test = time_utils.convert_todate('2020-09-18 17:21:27')
print(time_utils.get_day_state(sunrise, test))

test = time_utils.convert_todate('2020-09-18 11:21:27')
print(time_utils.get_day_state(sunrise, test))

test = time_utils.convert_todate('2020-09-18 09:21:27')
print(time_utils.get_day_state(sunrise, test))

test = time_utils.convert_todate('2020-09-18 04:21:27')
print(time_utils.get_day_state(sunrise, test))

test = time_utils.convert_todate('2020-09-18 01:21:27')
print(time_utils.get_day_state(sunrise, test))

test = time_utils.convert_todate('2020-09-18 00:21:27')
print(time_utils.get_day_state(sunrise, test))
