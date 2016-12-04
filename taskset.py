#! /usr/bin/python
# *-* encoding: utf-8 *-*

import config
import random


class Taskset:

    def __init__(self, name=""):
        self.name = name

    def set_TasksetConf(self, option=0, task_num=None,
                        max_wcet_value=None, min_wcet_value=None,
                        max_period_value=None, min_period_value=None):
        if option == 0:
            self.task_num = task_num
            self.max_wcet_value = max_wcet_value
            self.min_wcet_value = min_wcet_value
            self.max_period_value = max_period_value
            self.min_period_value = min_period_value
        elif option == 1:
            self.task_num = config.TASK_NUM
            self.max_wcet_value = config.MAX_WCET_VALUE
            self.min_wcet_value = config.MIN_WCET_VALUE
            self.max_period_value = config.MAX_PERIOD_VALUE
            self.min_period_value = config.MIN_PERIOD_VALUE
        else:
            print("Error: in function set_TasksetConf, Unexpected Option {0}"
                  .format(option))
            exit()

    def set_task_num(self, newvalue):
        self.task_num = newvalue

    def set_max_wcet_value(self, newvalue):
        self.max_wcet_value = newvalue

    def set_min_wcet_value(self, newvalue):
        self.min_wcet_value = newvalue

    def set_max_period_value(self, newvalue):
        self.max_period_value = newvalue

    def set_min_period_value(self, newvalue):
        self.min_period_value = newvalue

    def create_Taskset(self, option=1):
        self.wcetlist = []
        self.periodlist = []
        if option == 1:
            random.seed(1)
            self.wcetlist = [random.randint(self.min_wcet_value, self.max_wcet_value)
                             for i in xrange(self.task_num)]
            self.periodlist = [random.randint(self.min_period_value, self.max_period_value)
                               for i in xrange(self.task_num)]
        else:
            print("Error: in function create_Taskset, Unexpected Option {0}"
                  .format(option))
            exit()

    def get_TaskNum(self):
        return self.task_num

    def get_TasksetList(self):
        return self.wcetlist, self.periodlist

    def get_TasksetWcetList(self):
        return self.wcetlist

    def get_TasksetPeriodList(self):
        return self.periodlist

    def delete_Taskset(self):
        self.wcetlist = []
        self.periodlist = []

    def print_TasksetStatus(self):
        print("TasksetName: {0}" .format(self.name))
        print("task_num: {0}" .format(self.task_num))
        print("wcet: max_wcet {0}, min_wcet {1}"
              .format(self.max_wcet_value, self.min_wcet_value))
        print("period: max_period {0}, min_period {1}"
              .format(self.max_period_value, self.min_period_value))
        print "wcetlist"
        print self.wcetlist
        print "periodlist"
        print self.periodlist

    def print_TasksetName(self):
        print("TasksetName: {0}" .format(self.name))

#t = Taskset("taskset1")
#t.set_TasksetConf()
#t.create_Taskset()
#t.print_TasksetStatus()
