#! /usr/bin/python
# *-* encoding: utf-8 *-*

import config


class Coreset:

    def __init__(self, name=""):
        self.name = name
        self.bigcore_num = config.BIGCORE_NUM
        self.littlecore_num = config.LITTLECORE_NUM
        self.core_num = config.CORE_NUM
        self.corepair_num = CORE_PAIR_NUM
        self.bigcore_freq = BIGCORE_FREQ
        self.littlecore_freq = LITTLECORE_FREQ
        self.bigcore_power = BIGCORE_POWER
        self.littlecore_power = LITTLECORE_POWER

    def set_bigcore_num(self, newvalue):
        self.bigcore_num = newvalue

    def set_littlecore_num(self, newvalue):
        self.littlecore_num = newvalue

    def set_core_num(self, newvalue):
        self.core_num = newvalue

    def set_corepair_num(self, newvalue):
        self.corepair_num = newvalue

    def set_bigcore_freq(self, newvalue):
        self.bigcore_freq = newvalue

    def set_bigcore_freq(self, newvalue):
        self.bigcore_freq = newvalue

    def set_bigcore_power(self, newvalue):
        self.bigcore_power = newvalue

    def set_littlecore_power(self, newvalue):
        self.littlecore_power = newvalue

    def create_coreset(self, option=1):
        if option == 1:
            
        self.wcetlist = [random.randint(self.min_wcet_value, self.max_wcet_value)
                         for i in xrange(self.task_num)]
        self.periodlist = [random.randint(self.min_period_value, self.max_period_value)
                           for i in xrange(self.task_num)]

    def delete_taskset(self):
        self.wcetlist = []
        self.periodlist = []

    def print_taskset(self):
        print "task_num"
        print self.task_num
        print("wcet  max_wcet {0} min_wcet {1}"
              .format(self.max_wcet_value, self.min_wcet_value))
        print self.wcetlist
        print("period  max_period {0} min_period {1}"
              .format(self.max_period_value, self.min_period_value))
        print self.periodlist

    def print_Coresetname(self):
        print("{0}" .format(self.task_num))
