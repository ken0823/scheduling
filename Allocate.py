#! /usr/bin/python
# *-* encoding: utf-8 *-*

import config
import time
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

    def allcate_all_search_static_consider(self, core_freqlist, core_powerlist,
                                           wcetlist, periodlist):
        self.core_freqlist = core_freqlist
        self.core_powerlist = core_powerlist
        self.wcetlist = wcetlist
        self.periodlist = periodlist
        task_load = sum(wcetlist[j]*1.0/periodlist[j] for j in range(config.TASK_NUM))
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
                    for j in range(config.TASK_NUM):
                        for i in range(config.CORE_NUM):
                            x[i, j] = m.addVar(vtype=GRB.BINARY,
                                               name="x"+str(i)+'_'+str(j))

                    m.update()

# Objective Functions
                    f = 0
                    for i in range(0, config.BIGCORE_NUM):
                        f = f + power_conf[i]* \
                            quicksum(self.wcetlist[j]*x[i,j]*1.0/(freq_conf[i]*self.periodlist[j])
                                     for j in range(config.TASK_NUM)) + \
                            config.BIGCORE_SLEEP_POWER* \
                            (1 - quicksum(self.wcetlist[j]*x[i,j]*1.0/(freq_conf[i]*self.periodlist[j])
                                          for j in range(config.TASK_NUM))) + \
                            config.SLEEP_CHANGE_TIMES*config.BIGCORE_SLEEP_CHANGE_POWER_OV
                    for i in range(config.BIGCORE_NUM, config.CORE_NUM):
                        f = f + power_conf[i]* \
                            quicksum(self.wcetlist[j]*x[i,j]*1.0/(freq_conf[i]*self.periodlist[j])
                                     for j in range(config.TASK_NUM)) + \
                            config.LITTLECORE_SLEEP_POWER* \
                            (1 - quicksum(self.wcetlist[j]*x[i,j]*1.0/(freq_conf[i]*self.periodlist[j])
                                          for j in range(config.TASK_NUM))) + \
                            config.SLEEP_CHANGE_TIMES*config.LITTLECORE_SLEEP_CHANGE_POWER_OV

                    m.setObjective(f, GRB.MINIMIZE)

# Add Constraints
                    for j in range(config.TASK_NUM):
                        m.addConstr(quicksum(x[i, j]
                                    for i in range(config.CORE_NUM)) == 1, "c0")

                    for i in range(config.CORE_NUM):
                        m.addConstr(quicksum(self.wcetlist[j]*x[i,j]*1.0/(freq_conf[i]*self.periodlist[j])
                                    for j in range(config.TASK_NUM)) + \
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

    def allcate_all_search_static_noconsider(self, core_freqlist, core_powerlist,
                                             wcetlist, periodlist):
        self.core_freqlist = core_freqlist
        self.core_powerlist = core_powerlist
        self.wcetlist = wcetlist
        self.periodlist = periodlist
        task_load = sum(wcetlist[j]*1.0/periodlist[j] for j in range(config.TASK_NUM))
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
                    for j in range(config.TASK_NUM):
                        for i in range(config.CORE_NUM):
                            x[i, j] = m.addVar(vtype=GRB.BINARY,
                                               name="x"+str(i)+'_'+str(j))

                    m.update()

# Objective Functions
                    f = 0
                    for i in range(config.CORE_NUM):
                        f = f + power_conf[i]*quicksum(wcetlist[j]*x[i,j]*1.0/(freq_conf[i]*periodlist[j])
                                                       for j in range(config.TASK_NUM))

                    m.setObjective(f, GRB.MINIMIZE)

# Add Constraints
                    for j in range(config.TASK_NUM):
                        m.addConstr(quicksum(x[i, j]
                                    for i in range(config.CORE_NUM)) == 1, "c0")

                    for i in range(config.CORE_NUM):
                        m.addConstr(quicksum(self.wcetlist[j]*x[i,j]*1.0/(freq_conf[i]*self.periodlist[j])
                                    for j in range(config.TASK_NUM)) + \
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

    def allcate_heuristic_static_consider(self, core_freqlist, core_powerlist,
                                          wcetlist, periodlist):
        self.core_freqlist = core_freqlist
        self.core_powerlist = core_powerlist
        self.wcetlist = wcetlist
        self.periodlist = periodlist
        task_load = sum(wcetlist[j]*1.0/periodlist[j] for j in range(config.TASK_NUM))
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
                    for j in range(config.TASK_NUM):
                        for i in range(config.CORE_NUM):
                            x[i, j] = m.addVar(vtype=GRB.BINARY,
                                               name="x"+str(i)+'_'+str(j))

                    m.update()

# Objective Functions
                    f = 0
                    for i in range(0, config.BIGCORE_NUM):
                        f = f + power_conf[i]* \
                            quicksum(self.wcetlist[j]*x[i,j]*1.0/(freq_conf[i]*self.periodlist[j])
                                     for j in range(config.TASK_NUM)) + \
                            config.BIGCORE_SLEEP_POWER* \
                            (1 - quicksum(self.wcetlist[j]*x[i,j]*1.0/(freq_conf[i]*self.periodlist[j])
                                          for j in range(config.TASK_NUM))) + \
                            config.SLEEP_CHANGE_TIMES*config.BIGCORE_SLEEP_CHANGE_POWER_OV
                    for i in range(config.BIGCORE_NUM, config.CORE_NUM):
                        f = f + power_conf[i]* \
                            quicksum(self.wcetlist[j]*x[i,j]*1.0/(freq_conf[i]*self.periodlist[j])
                                     for j in range(config.TASK_NUM)) + \
                            config.LITTLECORE_SLEEP_POWER* \
                            (1 - quicksum(self.wcetlist[j]*x[i,j]*1.0/(freq_conf[i]*self.periodlist[j])
                                          for j in range(config.TASK_NUM))) + \
                            config.SLEEP_CHANGE_TIMES*config.LITTLECORE_SLEEP_CHANGE_POWER_OV

                    m.setObjective(f, GRB.MINIMIZE)

# Add Constraints
                    for j in range(config.TASK_NUM):
                        m.addConstr(quicksum(x[i, j]
                                    for i in range(config.CORE_NUM)) == 1, "c0")

                    for i in range(config.CORE_NUM):
                        m.addConstr(quicksum(self.wcetlist[j]*x[i,j]*1.0/(freq_conf[i]*self.periodlist[j])
                                    for j in range(config.TASK_NUM)) + \
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

    def allcate_heuristic_static_noconsider(self, core_freqlist, core_powerlist,
                                          wcetlist, periodlist):
        self.core_freqlist = core_freqlist
        self.core_powerlist = core_powerlist
        self.wcetlist = wcetlist
        self.periodlist = periodlist
        task_load = sum(wcetlist[j]*1.0/periodlist[j] for j in range(config.TASK_NUM))
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
                    for j in range(config.TASK_NUM):
                        for i in range(config.CORE_NUM):
                            x[i, j] = m.addVar(vtype=GRB.BINARY,
                                               name="x"+str(i)+'_'+str(j))

                    m.update()

# Objective Functions
                    f = 0
                    for i in range(config.CORE_NUM):
                        f = f + power_conf[i]*quicksum(wcetlist[j]*x[i,j]*1.0/(freq_conf[i]*periodlist[j])
                                                       for j in range(config.TASK_NUM))

                    m.setObjective(f, GRB.MINIMIZE)

# Add Constraints
                    for j in range(config.TASK_NUM):
                        m.addConstr(quicksum(x[i, j]
                                    for i in range(config.CORE_NUM)) == 1, "c0")

                    for i in range(config.CORE_NUM):
                        m.addConstr(quicksum(self.wcetlist[j]*x[i,j]*1.0/(freq_conf[i]*self.periodlist[j])
                                    for j in range(config.TASK_NUM)) + \
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

    def print_Solution_Status(self):
        print("solve status: {0}" .format(self.solve_flag))
        print("elapsed time: {0}" .format(self.elapsed_time))
        print("best ObjVal: {0}" .format(self.best_ObjVal))
        print("best core_conf: freq {0}, power {1}"
              .format(self.best_core_freq, self.best_core_power))

t = taskset.Taskset("taskset1")
t.set_Taskset_Conf()
t.create_Taskset()
s = Coreset.Coreset("coreset1")
s.set_Coreset_Conf()
s.create_Coresets()
h = Allocate("allocate1")
h.allcate_heuristic_static_consider(s.get_Coreset_freqlist(), s.get_Coreset_powerlist(),
                                     t.get_Taskset_wcetlist(), t.get_Taskset_periodlist())
h.print_Solution_Status()
