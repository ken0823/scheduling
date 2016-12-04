#! /usr/bin/python
# *-* encoding: utf-8 *-*

import config
import time
import numpy as np
from gurobipy import *
import taskset
import Coreset


class Allocate:

    def __init__(self, name=""):
        self.name = name
        self.best_ObjVal = float("inf")
        self.best_core_freq = []
        self.best_core_power = []
        self.best_allocate = []
        self.solve_flag = -1
        self.elapsed_time = 0

    def allcate_all_search_static_consider(self, core_num, bigcore_num, littlecore_num,
                                           core_freqlist, core_powerlist,
                                           task_num, wcetlist, periodlist):
        self.core_num = core_num
        self.bigcore_num = bigcore_num
        self.littlecore_num = littlecore_num
        self.core_freqlist = core_freqlist
        self.core_powerlist = core_powerlist
        self.task_num = task_num
        self.wcetlist = wcetlist
        self.periodlist = periodlist
        task_load = sum(wcetlist[j]*1.0/periodlist[j] for j in range(self.task_num))
        start = time.clock()

        for i in range(len(self.core_freqlist)):
            if sum(self.core_freqlist[i]) < task_load:
                pass
            else:
                try:
                    freq_conf = self.core_freqlist[i]
                    power_conf = self.core_powerlist[i]
                    m = Model(self.name)

# Create variables
                    x = {}
                    for j in range(self.task_num):
                        for i in range(self.core_num):
                            x[i, j] = m.addVar(vtype=GRB.BINARY,
                                               name="x"+str(i)+'_'+str(j))

                    m.update()

# Objective Functions
                    f = 0
                    for i in range(0, self.bigcore_num):
                        f = f + power_conf[i]* \
                            quicksum(self.wcetlist[j]*x[i,j]*1.0/(freq_conf[i]*self.periodlist[j])
                                     for j in range(self.task_num)) + \
                            config.BIGCORE_SLEEP_POWER* \
                            (1 - quicksum(self.wcetlist[j]*x[i,j]*1.0/(freq_conf[i]*self.periodlist[j])
                                          for j in range(self.task_num))) + \
                            config.SLEEP_CHANGE_TIMES*config.BIGCORE_SLEEP_CHANGE_POWER_OV
                    for i in range(self.bigcore_num, self.core_num):
                        f = f + power_conf[i]* \
                            quicksum(self.wcetlist[j]*x[i,j]*1.0/(freq_conf[i]*self.periodlist[j])
                                     for j in range(self.task_num)) + \
                            config.LITTLECORE_SLEEP_POWER* \
                            (1 - quicksum(self.wcetlist[j]*x[i,j]*1.0/(freq_conf[i]*self.periodlist[j])
                                          for j in range(self.task_num))) + \
                            config.SLEEP_CHANGE_TIMES*config.LITTLECORE_SLEEP_CHANGE_POWER_OV

                    m.setObjective(f, GRB.MINIMIZE)

# Add Constraints
                    for j in range(self.task_num):
                        m.addConstr(quicksum(x[i, j]
                                    for i in range(config.CORE_NUM)) == 1, "c0")

                    for i in range(self.core_num):
                        m.addConstr(quicksum(self.wcetlist[j]*x[i,j]*1.0/(freq_conf[i]*self.periodlist[j])
                                    for j in range(self.task_num)) + \
                                    config.SLEEP_CHANGE_TIMES*config.SLEEP_CHANGE_TIME_OV <= 1.0, "c1")

                    m.update()

# execution
                    m.setParam('OutputFlag', 0)  # Turn off display execution log to Console
                    m.optimize()
                    if m.Status == 2:  # Optimal solution found
                        self.solve_flag = 0
                        cur_ObjVal = m.ObjVal
                        if cur_ObjVal < self.best_ObjVal:
                            self.best_ObjVal = cur_ObjVal
                            self.best_core_freq = freq_conf
                            self.best_core_power = power_conf
                            self.best_allocate = m.getAttr("x", m.getVars())
                        else:
                            pass
                    elif m.Status == 3:  # Model is infeasible
                        pass
                    else:
                        print("Error: in function allcate_all_search_static_consider, Unexpected Optimization Status Code '%d'" % m.Status)
                        m.setParam('OutputFlag', 1)  # Turn on display execution log to Console
                        m.optimize()
                        exit()

                except:
                    print("Error reported: in function allcate_all_search_static_consider")
                    raise
        self.elapsed_time = time.clock() - start

    def allcate_all_search_static_noconsider(self, core_num, bigcore_num, littlecore_num,
                                             core_freqlist, core_powerlist,
                                             task_num, wcetlist, periodlist):
        self.core_num = core_num
        self.bigcore_num = bigcore_num
        self.littlecore_num = littlecore_num
        self.core_freqlist = core_freqlist
        self.core_powerlist = core_powerlist
        self.task_num = task_num
        self.wcetlist = wcetlist
        self.periodlist = periodlist
        task_load = sum(wcetlist[j]*1.0/periodlist[j] for j in range(self.task_num))
        start = time.clock()

        for i in range(len(self.core_freqlist)):
            if sum(self.core_freqlist[i]) < task_load:
                pass
            else:
                try:
                    freq_conf = self.core_freqlist[i]
                    power_conf = self.core_powerlist[i]
                    m = Model(self.name)

# Create variables
                    x = {}
                    for j in range(self.task_num):
                        for i in range(self.core_num):
                            x[i, j] = m.addVar(vtype=GRB.BINARY,
                                               name="x"+str(i)+'_'+str(j))

                    m.update()

# Objective Functions
                    f = 0
                    for i in range(self.core_num):
                        f = f + power_conf[i]*quicksum(wcetlist[j]*x[i,j]*1.0/(freq_conf[i]*periodlist[j])
                                                       for j in range(self.task_num))

                    m.setObjective(f, GRB.MINIMIZE)

# Add Constraints
                    for j in range(self.task_num):
                        m.addConstr(quicksum(x[i, j]
                                    for i in range(config.CORE_NUM)) == 1, "c0")

                    for i in range(self.core_num):
                        m.addConstr(quicksum(self.wcetlist[j]*x[i,j]*1.0/(freq_conf[i]*self.periodlist[j])
                                    for j in range(self.task_num)) + \
                                    config.SLEEP_CHANGE_TIMES*config.SLEEP_CHANGE_TIME_OV <= 1.0, "c1")

                    m.update()

# execution
                    m.setParam('OutputFlag', 0)  # Turn off display execution log to Console
                    m.optimize()
                    if m.Status == 2:  # Optimal solution found
                        self.solve_flag = 0
                        cur_ObjVal = m.ObjVal
                        if cur_ObjVal < self.best_ObjVal:
                            self.best_ObjVal = cur_ObjVal
                            self.best_core_freq = freq_conf
                            self.best_core_power = power_conf
                            self.best_allocate = m.getAttr("x", m.getVars())
                        else:
                            pass
                    elif m.Status == 3:  # Model is infeasible
                        pass
                    else:
                        print("Error: in function allcate_all_search_static_consider, Unexpected Optimization Status Code '%d'" % m.Status)
                        m.setParam('OutputFlag', 1)  # Turn on display execution log to Console
                        m.optimize()
                        exit()

                except:
                    print("Error reported: in function allcate_all_search_static_consider")
                    raise
        self.elapsed_time = time.clock() - start

    def allcate_heuristic_static_consider(self, core_num, bigcore_num, littlecore_num,
                                          core_freqlist, core_powerlist,
                                          task_num, wcetlist, periodlist):
        self.core_num = core_num
        self.bigcore_num = bigcore_num
        self.littlecore_num = littlecore_num
        self.core_freqlist = core_freqlist
        self.core_powerlist = core_powerlist
        self.task_num = task_num
        self.wcetlist = wcetlist
        self.periodlist = periodlist
        task_load = sum(wcetlist[j]*1.0/periodlist[j] for j in range(self.task_num))
        start = time.clock()

        for i in range(len(self.core_freqlist)):
            if sum(self.core_freqlist[i]) < task_load:
                pass
            else:
                try:
                    freq_conf = self.core_freqlist[i]
                    power_conf = self.core_powerlist[i]
                    m = Model(self.name)

# Create variables
                    x = {}
                    for j in range(self.task_num):
                        for i in range(self.core_num):
                            x[i, j] = m.addVar(vtype=GRB.BINARY,
                                               name="x"+str(i)+'_'+str(j))

                    m.update()

# Objective Functions
                    f = 0
                    for i in range(0, self.bigcore_num):
                        f = f + power_conf[i]* \
                            quicksum(self.wcetlist[j]*x[i,j]*1.0/(freq_conf[i]*self.periodlist[j])
                                     for j in range(self.task_num)) + \
                            config.BIGCORE_SLEEP_POWER* \
                            (1 - quicksum(self.wcetlist[j]*x[i,j]*1.0/(freq_conf[i]*self.periodlist[j])
                                          for j in range(self.task_num))) + \
                            config.SLEEP_CHANGE_TIMES*config.BIGCORE_SLEEP_CHANGE_POWER_OV
                    for i in range(self.bigcore_num, self.core_num):
                        f = f + power_conf[i]* \
                            quicksum(self.wcetlist[j]*x[i,j]*1.0/(freq_conf[i]*self.periodlist[j])
                                     for j in range(self.task_num)) + \
                            config.LITTLECORE_SLEEP_POWER* \
                            (1 - quicksum(self.wcetlist[j]*x[i,j]*1.0/(freq_conf[i]*self.periodlist[j])
                                          for j in range(self.task_num))) + \
                            config.SLEEP_CHANGE_TIMES*config.LITTLECORE_SLEEP_CHANGE_POWER_OV

                    m.setObjective(f, GRB.MINIMIZE)

# Add Constraints
                    for j in range(self.task_num):
                        m.addConstr(quicksum(x[i, j]
                                    for i in range(config.CORE_NUM)) == 1, "c0")

                    for i in range(self.core_num):
                        m.addConstr(quicksum(self.wcetlist[j]*x[i,j]*1.0/(freq_conf[i]*self.periodlist[j])
                                    for j in range(self.task_num)) + \
                                    config.SLEEP_CHANGE_TIMES*config.SLEEP_CHANGE_TIME_OV <= 1.0, "c1")

                    m.update()

# execution
                    m.setParam('OutputFlag', 0)  # Turn off display execution log to Console
                    m.optimize()
                    if m.Status == 2:  # Optimal solution found
                        self.solve_flag = 0
                        cur_ObjVal = m.ObjVal
                        if cur_ObjVal < self.best_ObjVal:
                            self.best_ObjVal = cur_ObjVal
                            self.best_core_freq = freq_conf
                            self.best_core_power = power_conf
                            self.best_allocate = m.getAttr("x", m.getVars())
                            break
                        else:
                            pass
                    elif m.Status == 3:  # Model is infeasible
                        pass
                    else:
                        print("Error: in function allcate_all_search_static_consider, Unexpected Optimization Status Code '%d'" % m.Status)
                        m.setParam('OutputFlag', 1)  # Turn on display execution log to Console
                        m.optimize()
                        exit()

                except:
                    print("Error reported: in function allcate_all_search_static_consider")
                    raise
        self.elapsed_time = time.clock() - start

    def allcate_heuristic_static_noconsider(self, core_num, bigcore_num, littlecore_num,
                                            core_freqlist, core_powerlist,
                                            task_num, wcetlist, periodlist):
        self.core_num = core_num
        self.bigcore_num = bigcore_num
        self.littlecore_num = littlecore_num
        self.core_freqlist = core_freqlist
        self.core_powerlist = core_powerlist
        self.task_num = task_num
        self.wcetlist = wcetlist
        self.periodlist = periodlist
        task_load = sum(wcetlist[j]*1.0/periodlist[j] for j in range(self.task_num))
        start = time.clock()

        for i in range(len(self.core_freqlist)):
            if sum(self.core_freqlist[i]) < task_load:
                pass
            else:
                try:
                    freq_conf = self.core_freqlist[i]
                    power_conf = self.core_powerlist[i]
                    m = Model(self.name)

# Create variables
                    x = {}
                    for j in range(self.task_num):
                        for i in range(self.core_num):
                            x[i, j] = m.addVar(vtype=GRB.BINARY,
                                               name="x"+str(i)+'_'+str(j))

                    m.update()

# Objective Functions
                    f = 0
                    for i in range(self.core_num):
                        f = f + power_conf[i]*quicksum(wcetlist[j]*x[i,j]*1.0/(freq_conf[i]*periodlist[j])
                                                       for j in range(self.task_num))

                    m.setObjective(f, GRB.MINIMIZE)

# Add Constraints
                    for j in range(self.task_num):
                        m.addConstr(quicksum(x[i, j]
                                    for i in range(config.CORE_NUM)) == 1, "c0")

                    for i in range(self.core_num):
                        m.addConstr(quicksum(self.wcetlist[j]*x[i,j]*1.0/(freq_conf[i]*self.periodlist[j])
                                    for j in range(self.task_num)) + \
                                    config.SLEEP_CHANGE_TIMES*config.SLEEP_CHANGE_TIME_OV <= 1.0, "c1")

                    m.update()

# execution
                    m.setParam('OutputFlag', 0)  # Turn off display execution log to Console
                    m.optimize()
                    if m.Status == 2:  # Optimal solution found
                        self.solve_flag = 0
                        cur_ObjVal = m.ObjVal
                        if cur_ObjVal < self.best_ObjVal:
                            self.best_ObjVal = cur_ObjVal
                            self.best_core_freq = freq_conf
                            self.best_core_power = power_conf
                            self.best_allocate = m.getAttr("x", m.getVars())
                            break
                        else:
                            pass
                    elif m.Status == 3:  # Model is infeasible
                        pass
                    else:
                        print("Error: in function allcate_all_search_static_consider, Unexpected Optimization Status Code '%d'" % m.Status)
                        m.setParam('OutputFlag', 1)  # Turn on display execution log to Console
                        m.optimize()
                        exit()

                except:
                    print("Error reported: in function allcate_all_search_static_consider")
                    raise
        self.elapsed_time = time.clock() - start

    def get_AllocateArray(self):
        self.allocate_array = np.array(self.best_allocate)
        np.reshape(self.allocate_array, (-1, ))



    def print_SolutionStatus(self):
        print("solve status: {0}" .format(self.solve_flag))
        print("elapsed time: {0}" .format(self.elapsed_time))
        print("best ObjVal: {0}" .format(self.best_ObjVal))
        print("best core_conf: freq {0}, power {1}"
              .format(self.best_core_freq, self.best_core_power))

t = taskset.Taskset("taskset1")
t.set_TasksetConf(1)
t.create_Taskset()
c = Coreset.Coreset("coreset1")
c.set_CoresetConf()
c.create_Coresets()
a = Allocate("allocate1")
a.allcate_all_search_static_noconsider(c.get_CoresetCoreNum(), c.get_CoresetBigCoreNum(), c.get_CoresetLittleCoreNum(),
                                    c.get_CoresetFreqList(), c.get_CoresetPowerList(), t.get_TaskNum(),
                                    t.get_TasksetWcetList(), t.get_TasksetPeriodList())
a.print_SolutionStatus()
