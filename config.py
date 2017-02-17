#! /usr/bin/python
# *-* encoding: utf-8 *-*


TASK_NUM = 90
UTILIZATION = 0.9
AET_RATIO = 0.2
MAX_WCET_VALUE = 1
MIN_WCET_VALUE = 1
MAX_PERIOD_VALUE = 50000
MIN_PERIOD_VALUE = 1000

#BIGCORE_FREQ = [1.0, 0.7, 0.4]
LITTLECORE_FREQ = [0.237, 0.153, 0.102]
#BIGCORE_POWER = [2241, 938, 457]
LITTLECORE_POWER = [227, 103, 58]

BIGCORE_FREQ = [1.0, 0.7, 0.2]
BIGCORE_POWER = [2241, 938, 200]

BIGCORE_FREQ_HAS_SLEEP = [1.0, 0.7, 0.4, 0.00001]
LITTLECORE_FREQ_HAS_SLEEP = [0.237, 0.153, 0.102, 0.00001]
BIGCORE_POWER_HAS_SLEEP = [2241, 938, 457, 0]
LITTLECORE_POWER_HAS_SLEEP = [227, 103, 58, 0]

CortexA15_freq = [1.0, 0.95, 0.9, 0.85, 0.8, 0.75, 0.7, 0.65, 0.6, 0.55, 0.45, 0.4,0.35,0.3,0.25,0.2,0.15,0.1]
CortexA15_power = [2241,1776,1552,1375,1208,1051,938,858,762,659,600,518,457,407,358,311,257,202,142]
SLEEP_POWER = CortexA15_power[-1]/10
WAKEUP_TIME_OV = 300  # (us)
WAKEUP_POWER_OV = 5*SLEEP_POWER


BIGCORE_SLEEP_POWER = 50
LITTLECORE_SLEEP_POWER = 5

SLEEP_CHANGE_TIMES = 50
SLEEP_CHANGE_TIME_OV = 0.00002
BIGCORE_SLEEP_CHANGE_POWER_OV = 100
LITTLECORE_SLEEP_CHANGE_POWER_OV = 10

BIGCORE_NUM = 3
LITTLECORE_NUM = 3
CORE_NUM = BIGCORE_NUM + LITTLECORE_NUM
CORE_PAIR_NUM = min(BIGCORE_NUM, LITTLECORE_NUM)


def gcd(a, b):
    while b > 0:
        a, b = b, a%b
    return a


def lcm(a, b):
    return a*b/gcd(a, b)


def lcm_iter(list_a):
    if len(list_a) == 0:
        print("Error: Number of Tasks is Zero")
        exit()
    else:
        l = 1
        for i in range(len(list_a)):
            l = lcm(list_a[i], l)
    return l
