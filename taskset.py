#! /usr/bin/python
# *-* encoding: utf-8 *-*

import config
import random
import math


class Taskset:

    def __init__(self, name=""):
        self.name = name

    def set_TasksetConf(self, option=0, utilization=None, task_num=None,
                        max_wcet_value=None, min_wcet_value=None,
                        max_period_value=None, min_period_value=None,
                        aet_ratio=None):
        if option == 0:
            self.task_num = task_num
            self.max_wcet_value = max_wcet_value
            self.min_wcet_value = min_wcet_value
            self.max_period_value = max_period_value
            self.min_period_value = min_period_value
            self.aet_ratio = aet_ratio
        elif option == 1:
            self.utilization = config.UTILIZATION
            self.task_num = config.TASK_NUM
            self.max_wcet_value = config.MAX_WCET_VALUE
            self.min_wcet_value = config.MIN_WCET_VALUE
            self.max_period_value = config.MAX_PERIOD_VALUE
            self.min_period_value = config.MIN_PERIOD_VALUE
            self.aet_ratio = config.AET_RATIO
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
        self.aetlist = []
        if option == 1:
            random.seed(1)
            self.wcetlist = [random.randint(self.min_wcet_value, self.max_wcet_value)
                             for i in xrange(self.task_num)]
            self.periodlist = [random.randint(self.min_period_value, self.max_period_value)
                               for i in xrange(self.task_num)]
        if option == 2:
            random.seed(1)
            self.periodlist = [random.randint(self.min_period_value, self.max_period_value)
                               for i in xrange(self.task_num)]
            for i in xrange(self.task_num):
                while True:
                    gauss = (random.gauss(0,1.0)+3)/3
                    if gauss <= 0 or gauss >= 1:
                        pass
                    else:
                        break
                self.wcetlist.append(self.periodlist[i]*gauss)
            task_load = sum(self.wcetlist[i]*1.0/self.periodlist[i] for i in xrange(self.task_num))
            if task_load > self.utilization:
                load_prm = self.utilization*1.0/task_load
                for i in xrange(len(self.wcetlist)):
                    self.wcetlist[i] = int(round(self.wcetlist[i]*load_prm))
            for i in xrange(self.task_num):
                while True:
                    gauss = (random.gauss(0,1.0)+6)/6
                    if gauss <= 0 or gauss >= 1:
                        pass
                    else:
                        break
                self.aetlist.append(int(math.ceil(self.aet_ratio*self.wcetlist[i]*gauss)))
        if option ==3:
            random.seed(1)
            self.periodlist = [random.choice([1000,5000,10000,20000,50000])
                               for i in xrange(self.task_num)]
            for i in xrange(self.task_num):
                while True:
                    gauss = (random.gauss(0,1.0)+3)/3
                    if gauss <= 0 or gauss >= 1:
                        pass
                    else:
                        break
                self.wcetlist.append(self.periodlist[i]*gauss)
            task_load = sum(self.wcetlist[i]*1.0/self.periodlist[i] for i in xrange(self.task_num))
            print task_load
            print self.utilization
            load_prm = self.utilization*1.0/task_load
            for i in xrange(len(self.wcetlist)):
                if int(round(self.wcetlist[i]*load_prm)) == 0:
                       self.wcetlist[i] = 1
                else:
                    self.wcetlist[i] = int(round(self.wcetlist[i]*load_prm))
            for i in xrange(self.task_num):
                while True:
                    gauss = (random.gauss(0,1.0)+6)/6
                    if gauss <= 0 or gauss >= 1:
                        pass
                    else:
                        break
                self.aetlist.append(int(round(self.aet_ratio*self.wcetlist[i]*gauss)))
        else:
            print("Error: in function create_Taskset, Unexpected Option {0}"
                  .format(option))
            exit()

    def get_TaskNum(self):
        return self.task_num

    def set_RoundTaskset(self):
        self.wcetlist = [(int(round(self.wcetlist[i]*0.001)))
                         for i in xrange(len(self.wcetlist))]
        self.periodlist = [(int(round(self.periodlist[i]*0.001)))
                           for i in xrange(len(self.periodlist))]
        self.aetlist = [(int(round(self.aetlist[i]*0.001)))
                         for i in xrange(len(self.aetlist))]

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
        task_load = sum(self.wcetlist[i]*1.0/self.periodlist[i] for i in xrange(self.task_num))
        print("task_load: {0}" .format(task_load))
        print "periodlist"
        print self.periodlist
        print "wcetlist"
        print self.wcetlist
        print "aetlist"
        print self.aetlist

    def print_TasksetName(self):
        print("TasksetName: {0}" .format(self.name))
'''
t = Taskset("taskset1")
t.set_TasksetConf(option=1)
t.create_Taskset(option=3)
t.print_TasksetStatus()
'''
