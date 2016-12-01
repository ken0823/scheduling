#! /usr/bin/python
# *-* encoding: utf-8 *-*

import config
import random


class Taskset:

    def __init__(self, name=""):
        self.name = name

    def set_Taskset_Conf(self, option=1):
        if option == 1:
            self.task_num = config.TASK_NUM
            self.max_wcet_value = config.MAX_WCET_VALUE
            self.min_wcet_value = config.MIN_WCET_VALUE
            self.max_period_value = config.MAX_PERIOD_VALUE
            self.min_period_value = config.MIN_PERIOD_VALUE
        else:
            print("Error: in function set_Taskset_Conf, Unexpected Option {0}"
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

    def delete_Taskset(self):
        self.wcetlist = []
        self.periodlist = []

    def print_Taskset_Status(self):
        print("task_num:  {0}" .format(self.task_num))
        print("wcet:  max_wcet {0}, min_wcet {1}"
              .format(self.max_wcet_value, self.min_wcet_value))
        print self.wcetlist
        print("period:  max_period {0}, min_period {1}"
              .format(self.max_period_value, self.min_period_value))
        print self.periodlist

    def print_Tasksetname(self):
        print("Tasksetname:  {0}" .format(self.task_num))

t = Taskset("taskset1")
#t.set_Taskset_Conf()
#t.create_Taskset()
t.print_Taskset_Status()
