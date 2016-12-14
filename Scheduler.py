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

    def run_LAEDFScheduler(self):
        tq = TaskQueue.TaskQueue("taskqueue1")
        df = DVFS.DVFS("DVFS1")
        current_time = 0
        for i in xrange(len(self.periodlist)):
            tq.add_TaskQueue(self.periodlist[i],
                            (self.periodlist[i],self.wcetlist[i],0),
                             self.actlist[i])
        print("ok")
        while True:
            queue_list = tq.get_TaskQueueList()
            if queue_list == []:
                print("All task is executed")
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
                    release_timelist.append(t_release)
                    if current_time >= t_release:
                        break
                    else:
                        pass
                if current_time < t_release:
                    current_time = min(release_timelist)
                else:
                    print ""
                    print "current_time"
                    print current_time
                    print "queue_list"
                    print queue_list
                    print "ready_queue"
                    print ready_queue
                    power = df.scla_edf(queue_list, ready_queue_id,
                                        current_time, self.hyperperiod,
                                        self.core_freq, self.core_power)
                    self.power = self.power + power
                    if df.get_RemExeTime() == 0:
                        tq.remove_TaskQueue(t_task)
                        if t_deadline + t_period <= self.hyperperiod:
                            tq.add_TaskQueue(t_deadline+t_period,
                                             (t_period,t_wcet,t_deadline),
                                             t_wcet)
                    else:
                        tq.add_TaskQueue(t_deadline, t_task, df.get_RemExeTime())
                    current_time = current_time + df.get_RealExeTime()
                    if current_time == self.hyperperiod:
                        break
                    elif current_time >= self.hyperperiod:
                        print("Error is occured; current time: {0}, hyperperiod:{1}"
                              .format(current_time, self.hyperperiod))
                        break
                    else:
                        pass

    def print_power(self):
        print self.power

t = taskset.Taskset("taskset1")
t.set_TasksetConf(option=1)
t.create_Taskset(option=3)
#t.set_RoundTaskset()


shed = Scheduler("schd")
shed.set_SchedulerConf([1.0, 0.7, 0.4], [2241, 938, 457],
                       t.get_TasksetPeriodList(), t.get_TasksetWcetList(), [1,1])
#shed.set_SchedulerConf([1.0, 0.5, 0.25], [2241, 938, 457],
 #                       [8, 40, 40, 10, 30], [1,5,2,1,5], [1,1])
#shed.set_SchedulerConf([1.0, 0.8, 0.6],[2241,938,457],[6,12,4,12],[1,1,1,2],[1,1])
shed.run_LAEDFScheduler()
t.print_TasksetStatus()
shed.print_power()

'''
tq = TaskQueue.TaskQueue("taskqueue1")
tq.add_TaskQueue(6,(6,1,6),1)
tq.add_TaskQueue(3,(3,1,3),1)
tq.add_TaskQueue(12,(12,2,12),1)
a = tq.get_TaskQueueList()
print a
freq = df.la_edf(a, 0, 0.666, [1.0, 0.6, 0.4, 0.1])
print freq'''
