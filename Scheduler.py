#! /usr/bin/python
# *-* encoding: utf-8 *-*

import random
import config
import TaskQueue
import DVFS
import taskset


class Scheduler:

    def __init__(self, name=""):
        self.name = name
        self.current_time = 0
        self.power = 0
        self.activepower = 0

    def set_SchedulerConf(self, core_freq, core_power,
                          periodlist, wcetlist, act_prm):
        self.core_freq = core_freq
        self.core_power = core_power
        self.periodlist = periodlist
        self.wcetlist = wcetlist
        self.utilization = sum(wcetlist[i]*1.0/periodlist[i] for i in xrange(len(self.wcetlist)))

        print "-------------"
        print "utilize"
        print self.utilization

        random.seed(1)
        self.actlist = [(random.randint(act_prm[0],act_prm[1]))*self.wcetlist[i]
                        for i in xrange(len(self.wcetlist))]
        self.hyperperiod = config.lcm_iter(periodlist)
        #print self.hyperperiod
        #print type(self.hyperperiod)

    def run_SCLAEDFScheduler(self):
        tq = TaskQueue.TaskQueue("taskqueue1")
        df = DVFS.DVFS("DVFS1")
        current_time = 0
        for i in xrange(len(self.periodlist)):
            tq.add_TaskQueue(self.periodlist[i],
                            (self.periodlist[i],self.wcetlist[i],0,i),
                             self.actlist[i])
        while True:
            queue_list = tq.get_TaskQueueList()
            if queue_list == []:
                print("All task is executed(scla)")
                print("OV freq num")
                print df.get_OVfreqnum()
                break
            else:
                release_timelist =[]
                for i in xrange(len(queue_list)):
                    ready_queue = queue_list[i]
                    ready_queue_id = i
                    t_deadline, t_task, t_c_rem, t_count = ready_queue
                    t_period = t_task[0]
                    t_wcet = t_task[1]
                    t_release = t_task[2]
                    t_id = t_task[3]
                    release_timelist.append(t_release)
                    if current_time >= t_release:
                        break
                    else:
                        pass
                if current_time < t_release:
                    print "bad"
                    current_time = min(release_timelist)
                else:
                    '''
                    print ""
                    print "current_time"
                    print current_time
                    print "queue_list"
                    print queue_list
                    print "ready_queue"
                    print ready_queue
                    '''
                    power = df.scla_edf(queue_list, ready_queue_id,
                                        current_time, self.hyperperiod,
                                        self.core_freq, self.core_power)
                    self.power = self.power + power
                    self.activepower = self.activepower + df.get_BestActiveComsumptionValue()
                    '''
                    print df.get_BestActiveComsumptionValue()
                    '''
                    current_time = current_time + df.get_ElapsedTime()
                    if df.get_RemExeTime() == 0:
                        if t_deadline >= current_time:
                            tq.remove_TaskQueue(t_task)
                            if t_deadline + t_period <= self.hyperperiod:
                                tq.add_TaskQueue(t_deadline+t_period,
                                                 (t_period,t_wcet,t_deadline,t_id),
                                                 t_wcet)
                        else:
                            print("Error is occured; over deadline current time: {0}, hyperperiod:{1}"
                                  .format(current_time, self.hyperperiod))
                            exit()
                    else:
                        tq.add_TaskQueue(t_deadline, t_task, df.get_RemExeTime())
                    
                    if current_time == self.hyperperiod:
                        print("All task is executed(scla)")
                        print("OV freq num")
                        print df.get_OVfreqnum()
                        break
                    elif current_time > self.hyperperiod:
                        print("Error is occured; current time: {0}, hyperperiod:{1}"
                              .format(current_time, self.hyperperiod))
                        break
                    else:
                        pass

    def run_SCLAEDF2Scheduler(self):
        tq = TaskQueue.TaskQueue("taskqueue1")
        df = DVFS.DVFS("DVFS1")
        current_time = 0
        for i in xrange(len(self.periodlist)):
            tq.add_TaskQueue(self.periodlist[i],
                            (self.periodlist[i],self.wcetlist[i],0,i),
                             self.actlist[i])
        while True:
            queue_list = tq.get_TaskQueueList()
            if queue_list == []:
                print("All task is executed(scla)")
                print("OV freq num")
                print df.get_OVfreqnum()
                break
            else:
                release_timelist =[]
                for i in xrange(len(queue_list)):
                    ready_queue = queue_list[i]
                    ready_queue_id = i
                    t_deadline, t_task, t_c_rem, t_count = ready_queue
                    t_period = t_task[0]
                    t_wcet = t_task[1]
                    t_release = t_task[2]
                    t_id = t_task[3]
                    release_timelist.append(t_release)
                    if current_time >= t_release:
                        break
                    else:
                        pass
                if current_time < t_release:
                    print "bad"
                    current_time = min(release_timelist)
                else:
                    '''
                    print ""
                    print "current_time"
                    print current_time
                    print "queue_list"
                    print queue_list
                    print "ready_queue"
                    print ready_queue
                    '''
                    power = df.scla2_edf(queue_list, ready_queue_id,
                                        current_time, self.hyperperiod,
                                        self.core_freq, self.core_power)
                    self.power = self.power + power
                    self.activepower = self.activepower + df.get_BestActiveComsumptionValue()
                    current_time = current_time + df.get_ElapsedTime()
                    if df.get_RemExeTime() == 0:
                        if t_deadline >= current_time:
                            tq.remove_TaskQueue(t_task)
                            if t_deadline + t_period <= self.hyperperiod:
                                tq.add_TaskQueue(t_deadline+t_period,
                                                 (t_period,t_wcet,t_deadline,t_id),
                                                 t_wcet)
                        else:
                            print("Error is occured; current time: {0}, hyperperiod:{1}"
                                  .format(current_time, self.hyperperiod))
                            exit()
                    else:
                        tq.add_TaskQueue(t_deadline, t_task, df.get_RemExeTime())
                    
                    if current_time == self.hyperperiod:
                        print("All task is executed(scla2)")
                        print("OV freq num")
                        print df.get_OVfreqnum()
                        break
                    elif current_time > self.hyperperiod:
                        print("Error is occured; current time: {0}, hyperperiod:{1}"
                              .format(current_time, self.hyperperiod))
                        break
                    else:
                        pass

    def run_LAEDFScheduler(self):
        tq = TaskQueue.TaskQueue("taskqueue1")
        df = DVFS.DVFS("DVFS1")
        current_time = 0
        for i in xrange(len(self.periodlist)):
            tq.add_TaskQueue(self.periodlist[i],
                            (self.periodlist[i],self.wcetlist[i],0,i),
                             self.actlist[i])

        queue_list = tq.get_TaskQueueList()
        if queue_list == []:
            print("Error: Task is null")
            exit()

        while True:
            queue_list = tq.get_TaskQueueList()
            for i in xrange(len(queue_list)):
                deadline, task, c_rem, count = queue_list[i]
                period = task[0]
                wcet = task[1]
                release = task[2]
                task_id = task[3]
                if deadline == current_time and c_rem == 0:
                    tq.remove_TaskQueue(task)
                    tq.add_TaskQueue(deadline+period,
                                     (period,wcet,deadline,task_id),
                                     wcet)
                elif deadline == current_time and c_rem >= 0:
                    print("Error is occured; current time:{0}, task:{1}, deadline:{2}"
                          .format(current_time, task, deadline))
                else:
                    pass
            queue_list = tq.get_TaskQueueList()
            for i in xrange(len(queue_list)):
                ready_queue = queue_list[i]
                ready_queue_id = i
                rq_deadline, rq_task, rq_c_rem, rq_count = ready_queue
                if rq_c_rem == 0:
                    pass
                else:
                    break
            '''
            print ""
            print "current_time"
            print current_time
            print "queue_list"
            print queue_list
            print "ready_queue"
            print ready_queue
            '''
            power = df.la_edf(queue_list, ready_queue_id,
                              current_time, self.hyperperiod,
                              self.core_freq, self.core_power)
            self.power = self.power + power
            self.activepower = self.activepower + df.get_BestActiveComsumptionValue()
            '''
            print df.get_BestActiveComsumptionValue()
            print "power"
            print self.power
            '''
            tq.add_TaskQueue(rq_deadline,
                             rq_task,
                             df.get_RemExeTime())
            current_time = current_time + df.get_RealExeTime()
            if current_time == self.hyperperiod:
                queue_list = tq.get_TaskQueueList()
                for i in xrange(len(queue_list)):
                    deadline, task, c_rem, count = queue_list[i]
                    if c_rem == 0:
                        pass
                    else:
                        print("Error is occured; current time: {0}, hyperperiod:{1}"
                              .format(current_time, self.hyperperiod))
                        exit()
                print("All task is executed(la)")
                print("OV freq num")
                print df.get_OVfreqnum()
                break
            elif current_time > self.hyperperiod:
                print("Error is occured; current time: {0}, hyperperiod:{1}"
                      .format(current_time, self.hyperperiod))
                exit()
            else:
                pass

    def run_LAEDF2Scheduler(self):
        tq = TaskQueue.TaskQueue("taskqueue1")
        df = DVFS.DVFS("DVFS1")
        current_time = 0
        for i in xrange(len(self.periodlist)):
            tq.add_TaskQueue(self.periodlist[i],
                            (self.periodlist[i],self.wcetlist[i],0,i),
                             self.actlist[i])

        queue_list = tq.get_TaskQueueList()
        if queue_list == []:
            print("Error: Task is null")
            exit()

        while True:
            queue_list = tq.get_TaskQueueList()
            for i in xrange(len(queue_list)):
                deadline, task, c_rem, count = queue_list[i]
                period = task[0]
                wcet = task[1]
                release = task[2]
                task_id = task[3]
                if deadline == current_time and c_rem == 0:
                    tq.remove_TaskQueue(task)
                    tq.add_TaskQueue(deadline+period,
                                     (period,wcet,deadline,task_id),
                                     wcet)
                elif deadline == current_time and c_rem >= 0:
                    print("Error is occured; current time:{0}, task:{1}, deadline:{2}"
                          .format(current_time, task, deadline))
                else:
                    pass
            queue_list = tq.get_TaskQueueList()
            for i in xrange(len(queue_list)):
                ready_queue = queue_list[i]
                ready_queue_id = i
                rq_deadline, rq_task, rq_c_rem, rq_count = ready_queue
                if rq_c_rem == 0:
                    pass
                else:
                    break
            '''
            print ""
            print "current_time"
            print current_time
            print "queue_list"
            print queue_list
            print "ready_queue"
            print ready_queue
            '''
            power = df.la2_edf(queue_list, ready_queue_id,
                              current_time, self.hyperperiod,
                              self.core_freq, self.core_power)
            self.power = self.power + power
            self.activepower = self.activepower + df.get_BestActiveComsumptionValue()
            '''
            print df.get_BestActiveComsumptionValue()
            print "power"
            print self.power
            '''
            tq.add_TaskQueue(rq_deadline,
                             rq_task,
                             df.get_RemExeTime())
            #print df.get_ElapsedTime()
            current_time = current_time + df.get_ElapsedTime()
            if current_time == self.hyperperiod:
                queue_list = tq.get_TaskQueueList()
                for i in xrange(len(queue_list)):
                    deadline, task, c_rem, count = queue_list[i]
                    if c_rem == 0:
                        pass
                    else:
                        print("Error is occured; current time: {0}, hyperperiod:{1}"
                              .format(current_time, self.hyperperiod))
                        exit()
                print("All task is executed(la)")
                print("OV freq num")
                print df.get_OVfreqnum()
                break
            elif current_time > self.hyperperiod:
                print("Error is occured; current time: {0}, hyperperiod:{1}"
                      .format(current_time, self.hyperperiod))
                exit()
            else:
                pass


    def print_power(self):
        print self.power

    def print_activepower(self):
        print self.activepower

t = taskset.Taskset("taskset1")
t.set_TasksetConf(option=1)
t.create_Taskset(option=3)
#t.set_RoundTaskset()
t.print_TasksetStatus()

print ""
print "----laEDF----"
shed4 = Scheduler("schd4")
shed4.set_SchedulerConf([1.0, 0.95, 0.9, 0.85, 0.8, 0.75, 0.7, 0.65, 0.6, 0.55, 0.45, 0.4],
                        [2241, 1868, 1723, 1616, 1510, 1401, 1340, 1320, 1270, 1198, 1151, 1142],
                        t.get_TasksetPeriodList(), t.get_TasksetWcetList(), [1,1])
#shed3.set_SchedulerConf([1.0, 0.8, 0.6],[2241,938,457],[6,6,12],[1,1,1],[1,1])
shed4.run_LAEDFScheduler()
shed4.print_power()
shed4.print_activepower()

print ""
print "----laEDF + SCA-DVFS----"
shed = Scheduler("schd")
shed.set_SchedulerConf([1.0, 0.95, 0.9, 0.85, 0.8, 0.75, 0.7, 0.65, 0.6, 0.55, 0.45, 0.4],
                       [2241, 1868, 1723, 1616, 1510, 1401, 1340, 1320, 1270, 1198, 1151, 1142],
                       t.get_TasksetPeriodList(), t.get_TasksetWcetList(), [1,1])
#shed.set_SchedulerConf([1.0, 0.5, 0.25], [2241, 938, 457],
 #                       [8, 40, 40, 10, 30], [1,5,2,1,5], [1,1])
#shed.set_SchedulerConf([1.0, 0.8, 0.6],[2241,938,457],[6,4,12],[1,1,7],[1,1])
shed.run_LAEDF2Scheduler()
shed.print_power()
shed.print_activepower()

print ""
print "----SGlaedf----"
shed2 = Scheduler("schd2")
shed2.set_SchedulerConf([1.0, 0.95, 0.9, 0.85, 0.8, 0.75, 0.7, 0.65, 0.6, 0.55, 0.45, 0.4],
                        [2241, 1868, 1723, 1616, 1510, 1401, 1340, 1320, 1270, 1198, 1151, 1142],
                        t.get_TasksetPeriodList(), t.get_TasksetWcetList(), [1,1])
#shed2.set_SchedulerConf([1.0, 0.8, 0.6],[2241,938,457],[6,4,12],[1,1,1],[1,1])
shed2.run_SCLAEDF2Scheduler()
shed2.print_power()
shed2.print_activepower()

print ""
print "----SGlaedf + SCA-DVFS----"
shed3 = Scheduler("schd3")
shed3.set_SchedulerConf([1.0, 0.95, 0.9, 0.85, 0.8, 0.75, 0.7, 0.65, 0.6, 0.55, 0.45, 0.4],
                        [2241, 1868, 1723, 1616, 1510, 1401, 1340, 1320, 1270, 1198, 1151, 1142],
                        t.get_TasksetPeriodList(), t.get_TasksetWcetList(), [1,1])
#shed3.set_SchedulerConf([1.0, 0.8, 0.6],[2241,938,457],[6,6,12],[1,1,1],[1,1])
shed3.run_SCLAEDFScheduler()
shed3.print_power()
shed3.print_activepower()


print""
'''
tq = TaskQueue.TaskQueue("taskqueue1")
tq.add_TaskQueue(6,(6,1,6),1)
tq.add_TaskQueue(3,(3,1,3),1)
tq.add_TaskQueue(12,(12,2,12),1)
a = tq.get_TaskQueueList()
print a
freq = df.la_edf(a, 0, 0.666, [1.0, 0.6, 0.4, 0.1])
print freq'''
