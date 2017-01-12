#! /usr/bin/python
# *-* encoding: utf-8 *-*

import math
import config


class DVFS:

    def __init__(self, name=""):
        self.name = name
        self.count = 0

    def scla_edf(self, task_queuelist, ready_queue_id, current_time,
                 hyperperiod, core_freqlist, core_powerlist):
        t_periodlist = []
        t_wcetlist = []
        s = 0
        best_comsumption_value = float("inf")
        next_highpri_release_timelist = [hyperperiod]
        next_lowpri_release_timelist = [hyperperiod]

        for i in xrange(len(task_queuelist)):
            t_queue = task_queuelist[i]
            t_task = t_queue[1]
            t_periodlist.append(t_task[0])
            t_wcetlist.append(t_task[1])
        '''
        util = sum(t_wcetlist[i]*1.0/t_periodlist[i]
                   for i in xrange(len(task_queuelist)))
        '''
        util = 0
        util2 = 0
        x = 0
        util_origin = util

        exe_task = task_queuelist[ready_queue_id]
        exe_task_deadline = exe_task[0]
        exe_task_c_rem = exe_task[2]
        low_pri_queue = task_queuelist[ready_queue_id+1:]
        high_pri_queue = task_queuelist[:ready_queue_id]
        highest_pri_queue = task_queuelist[0]
        eariest_deadline = highest_pri_queue[0]
        max_core_freq = core_freqlist[0]
        min_core_power = core_powerlist[-1]
        best_core_freq = 0
        '''
        for task_queue in reversed(task_queuelist):
            deadline, task, c_rem, count = task_queue
            util = util - task[1]*1.0/task[0]
            rem_time = max(0, c_rem - (1 - util)*(deadline - eariest_deadline))
            if deadline > eariest_deadline:
                util = util + (c_rem - rem_time)*1.0/(deadline - eariest_deadline)
            s = s + rem_time
        '''
        
        for task_queue in reversed(task_queuelist):
            util2 = 0
            deadline, task, c_rem, count = task_queue
            for task_queue2 in task_queuelist:
                 deadline2, task2, c_rem2, count2 = task_queue2
                 if deadline2 < deadline:
                     util2 = util2 +  task2[1]*1.0/task2[0]
                 else:
                     break
            '''
            print "util2"
            print util2
            '''
            util = x + util2
            '''
            print "util"
            print util
            '''
            rem_time = max(0, c_rem - (1 - util)*(deadline - eariest_deadline))
            if deadline > eariest_deadline:
                x = x + (c_rem - rem_time)*1.0/(deadline - eariest_deadline)
            '''
            print "x"
            print x
            '''
            s = s + rem_time
        
        laedf_freq = max_core_freq*s*1.0/(eariest_deadline - current_time)
        '''
        print ""
        print "laedf"
        print laedf_freq
        '''
        laedf_origin = laedf_freq
        if laedf_freq >  max_core_freq:
            laedf_freq =  max_core_freq
            '''
            print("down to 1")
            '''
            self.count = self.count + 1
        if laedf_freq > max_core_freq:
            print("Error2: la_edf(), la_edf cannot schedule(task_set is overload)")
            print("laedf: {0}, utilzation: {1}"
                  .format(laedf_origin, util_origin))
            exit()
        for core_freq in reversed(core_freqlist):
            if core_freq >= laedf_freq:
                best_core_freq = core_freq
                break
            else:
                pass
        '''
        print "best_core_freq"
        print best_core_freq
        '''
        for high_pri_item in high_pri_queue:
            deadline, task, c_rem, count = high_pri_item
            release_time = task[2]
            next_highpri_release_timelist.append(release_time)

        for low_pri_item in low_pri_queue:
            deadline, task, c_rem, count = low_pri_item
            release_time = task[2]
            next_lowpri_release_timelist.append(release_time)
        self.next_highpri_release_time = min(next_highpri_release_timelist)
        self.next_lowpri_release_time = min(next_lowpri_release_timelist)
        high_core_freqlist = core_freqlist[0: core_freqlist.index(best_core_freq)+1]

        for core_freq in high_core_freqlist:
            core_power = core_powerlist[core_freqlist.index(core_freq)]
            self.task_exec_time = exe_task_c_rem*1.0/core_freq
            self.real_exec_time = min(self.task_exec_time,
                                      self.next_highpri_release_time - current_time)

            self.rem_exec_time = (self.task_exec_time - self.real_exec_time)*core_freq
            if  self.rem_exec_time > 0:
                self.slack_time = 0
            else:
                useful_time = min(self.next_highpri_release_time, self.next_lowpri_release_time, exe_task_deadline)
                useful_time = useful_time - current_time
                self.slack_time = max(0, useful_time - self.task_exec_time)
            if self.slack_time <= config.WAKEUP_TIME_OV*2:
                current_comsumption_value1 = core_power*self.real_exec_time + min_core_power*self.slack_time
                current_comsumption_value2 = float("inf")
                '''
                print "slack_time1"
                print self.slack_time
                print "current_comsumption_value"
                print current_comsumption_value1
                '''
                self.elapsed_time = self.real_exec_time + self.slack_time
            else:
                current_comsumption_value1 = core_power*self.real_exec_time + min_core_power*self.slack_time
                current_comsumption_value2 = core_power*self.real_exec_time +  \
                                             config.SLEEP_POWER*(self.slack_time - config.WAKEUP_TIME_OV*2) +  \
                                             config.WAKEUP_POWER_OV*2
                self.elapsed_time = self.real_exec_time + self.slack_time
                '''
                print "slack_time2"
                print self.slack_time
                print "current_comsumption_value"
                print "{0}, {1}" .format(current_comsumption_value1, current_comsumption_value2)
                '''
            current_comsumption_value = min(current_comsumption_value1, current_comsumption_value2)
            if current_comsumption_value < best_comsumption_value:
                best_comsumption_value = current_comsumption_value
                best_real_exec_time = self.real_exec_time
                best_elapsed_time = self.elapsed_time
                best_rem_exec_time = self.rem_exec_time
                best_freq = core_freq
                best_core = core_powerlist[core_freqlist.index(best_freq)]
            else:
                pass
        self.real_exec_time = best_real_exec_time
        self.rem_exec_time = best_rem_exec_time
        self.elapsed_time = best_elapsed_time
        self.best_active_comsumption_value = self.real_exec_time*best_core
        '''
        print "best_core(scla)"
        print best_freq
        print "best_slack_time"
        print self.slack_time
        '''
        return best_comsumption_value



    def scla2_edf(self, task_queuelist, ready_queue_id, current_time,
                 hyperperiod, core_freqlist, core_powerlist):
        t_periodlist = []
        t_wcetlist = []
        s = 0
        best_comsumption_value = float("inf")
        next_highpri_release_timelist = [hyperperiod]
        next_lowpri_release_timelist = [hyperperiod]

        for i in xrange(len(task_queuelist)):
            t_queue = task_queuelist[i]
            t_task = t_queue[1]
            t_periodlist.append(t_task[0])
            t_wcetlist.append(t_task[1])
        
        '''
        util = sum(t_wcetlist[i]*1.0/t_periodlist[i]
                   for i in xrange(len(task_queuelist)))
        '''
        util = 0
        util2 = 0
        x = 0
        util_origin = util
        util_origin = util

        exe_task = task_queuelist[ready_queue_id]
        exe_task_deadline = exe_task[0]
        exe_task_c_rem = exe_task[2]
        low_pri_queue = task_queuelist[ready_queue_id+1:]
        high_pri_queue = task_queuelist[:ready_queue_id]
        highest_pri_queue = task_queuelist[0]
        eariest_deadline = highest_pri_queue[0]
        max_core_freq = core_freqlist[0]
        min_core_power = core_powerlist[-1]
        best_core_freq = 0

        '''
        for task_queue in reversed(task_queuelist):
            deadline, task, c_rem, count = task_queue
            util = util - task[1]*1.0/task[0]
            rem_time = max(0, c_rem - (1 - util)*(deadline - eariest_deadline))
            if deadline > eariest_deadline:
                util = util + (c_rem - rem_time)*1.0/(deadline - eariest_deadline)
            s = s + rem_time
        '''

        for task_queue in reversed(task_queuelist):
            util2 = 0
            deadline, task, c_rem, count = task_queue
            for task_queue2 in task_queuelist:
                 deadline2, task2, c_rem2, count2 = task_queue2
                 if deadline2 < deadline:
                     util2 = util2 +  task2[1]*1.0/task2[0]
                 else:
                     break
            '''
            print "util2"
            print util2
            '''
            util = x + util2
            '''
            print "util"
            print util
            '''
            rem_time = max(0, c_rem - (1 - util)*(deadline - eariest_deadline))
            if deadline > eariest_deadline:
                x = x + (c_rem - rem_time)*1.0/(deadline - eariest_deadline)
            '''
            print "x"
            print x
            '''
            s = s + rem_time
        laedf_freq = max_core_freq*s*1.0/(eariest_deadline - current_time)
        '''
        print ""
        print "laedf"
        print laedf_freq
        '''
        laedf_origin = laedf_freq
        if laedf_freq >  max_core_freq:
            laedf_freq =  max_core_freq
            '''
            print("down to 1")
            '''
            self.count = self.count + 1
        if laedf_freq > max_core_freq:
            print("Error2: la_edf(), la_edf cannot schedule(task_set is overload)")
            print("laedf: {0}, utilzation: {1}"
                  .format(laedf_origin, util_origin))
            exit()
        for core_freq in reversed(core_freqlist):
            if core_freq >= laedf_freq:
                best_core_freq = core_freq
                break
            else:
                pass
        '''
        print "best_core_freq"
        print best_core_freq
        '''
        for high_pri_item in high_pri_queue:
            deadline, task, c_rem, count = high_pri_item
            release_time = task[2]
            next_highpri_release_timelist.append(release_time)

        for low_pri_item in low_pri_queue:
            deadline, task, c_rem, count = low_pri_item
            release_time = task[2]
            next_lowpri_release_timelist.append(release_time)
        self.next_highpri_release_time = min(next_highpri_release_timelist)
        self.next_lowpri_release_time = min(next_lowpri_release_timelist)
        high_core_freqlist = core_freqlist[0: core_freqlist.index(best_core_freq)+1]

        for core_freq in [best_core_freq]:
            core_power = core_powerlist[core_freqlist.index(core_freq)]
            self.task_exec_time = exe_task_c_rem*1.0/core_freq
            self.real_exec_time = min(self.task_exec_time,
                                      self.next_highpri_release_time - current_time)

            self.rem_exec_time = (self.task_exec_time - self.real_exec_time)*core_freq
            if  self.rem_exec_time > 0:
                self.slack_time = 0
            else:
                useful_time = min(self.next_highpri_release_time, self.next_lowpri_release_time, exe_task_deadline)
                useful_time = useful_time - current_time
                self.slack_time = max(0, useful_time - self.task_exec_time)
            if self.slack_time <= config.WAKEUP_TIME_OV*2:
                current_comsumption_value1 = core_power*self.real_exec_time + min_core_power*self.slack_time
                current_comsumption_value2 = float("inf")
                '''
                print "slack_time1"
                print self.slack_time
                print "current_comsumption_value"
                print current_comsumption_value1
                '''
                self.elapsed_time = self.real_exec_time + self.slack_time
            else:
                current_comsumption_value1 = core_power*self.real_exec_time + min_core_power*self.slack_time
                current_comsumption_value2 = core_power*self.real_exec_time +  \
                                             config.SLEEP_POWER*(self.slack_time - config.WAKEUP_TIME_OV*2) +  \
                                             config.WAKEUP_POWER_OV*2
                self.elapsed_time = self.real_exec_time + self.slack_time
                '''
                print "slack_time2"
                print self.slack_time
                print "current_comsumption_value"
                print "{0}, {1}" .format(current_comsumption_value1, current_comsumption_value2)
                '''
            current_comsumption_value = min(current_comsumption_value1, current_comsumption_value2)
            if current_comsumption_value < best_comsumption_value:
                best_comsumption_value = current_comsumption_value
                best_real_exec_time = self.real_exec_time
                best_elapsed_time = self.elapsed_time
                best_rem_exec_time = self.rem_exec_time
                best_freq = core_freq
                best_core = core_powerlist[core_freqlist.index(best_freq)]
            else:
                pass
        self.real_exec_time = best_real_exec_time
        self.rem_exec_time = best_rem_exec_time
        self.elapsed_time = best_elapsed_time
        self.best_active_comsumption_value = self.real_exec_time*best_core
        '''
        print "best_core(scla)"
        print best_core
        print "best_slack_time"
        print self.slack_time
        '''
        return best_comsumption_value


    def la_edf(self, task_queuelist, ready_queue_id, current_time,
                hyperperiod, core_freqlist, core_powerlist):
        t_periodlist = []
        t_wcetlist = []
        s = 0
        best_comsumption_value = float("inf")
        for i in xrange(len(task_queuelist)):
            t_queue = task_queuelist[i]
            t_task = t_queue[1]
            t_periodlist.append(t_task[0])
            t_wcetlist.append(t_task[1])
        '''
        util = sum(t_wcetlist[i]*1.0/t_periodlist[i]
                   for i in xrange(len(task_queuelist)))
        '''
        util = 0
        util2 = 0
        x = 0

        exe_task = task_queuelist[ready_queue_id]
        exe_task_deadline = exe_task[0]
        exe_task_c_rem = exe_task[2]
        highest_pri_queue = task_queuelist[0]
        eariest_deadline = highest_pri_queue[0]
        max_core_freq = core_freqlist[0]
        min_core_power = core_powerlist[-1]
        best_core_freq = 0
        '''
        for task_queue in reversed(task_queuelist):
            deadline, task, c_rem, count = task_queue
            util = util - task[1]*1.0/task[0]
            rem_time = max(0, c_rem - (1 - util)*(deadline - eariest_deadline))
            if deadline > eariest_deadline:
                util = util + (c_rem - rem_time)*1.0/(deadline - eariest_deadline)
            s = s + rem_time
        '''

        for task_queue in reversed(task_queuelist):
            util2 = 0
            deadline, task, c_rem, count = task_queue
            for task_queue2 in task_queuelist:
                 deadline2, task2, c_rem2, count2 = task_queue2
                 if deadline2 < deadline:
                     util2 = util2 +  task2[1]*1.0/task2[0]
                 else:
                     break
            '''
            print "util2"
            print util2
            '''
            util = x + util2
            '''
            print "util"
            print util
            '''
            rem_time = max(0, c_rem - (1 - util)*(deadline - eariest_deadline))
            if deadline > eariest_deadline:
                x = x + (c_rem - rem_time)*1.0/(deadline - eariest_deadline)
            '''
            print "x"
            print x
            '''
            s = s + rem_time

        laedf_freq = max_core_freq*s*1.0/(eariest_deadline - current_time)
        '''
        print "laedf"
        print laedf_freq
        '''
        laedf_origin = laedf_freq
        if laedf_freq >  max_core_freq:
            laedf_freq =  max_core_freq
            '''
            print("down to 1")
            '''
            self.count = self.count + 1
        if laedf_freq > max_core_freq:
            print("Error2: la_edf(), la_edf cannot schedule(task_set is overload)")
            print laedf_origin
            exit()
        for core_freq in reversed(core_freqlist):
            if core_freq >= laedf_freq:
                best_core_freq = core_freq
                break
            else:
                pass
        '''
        print "best_core_freq"
        print best_core_freq
        '''
        # for core_freq in [best_core_freq]:
        if laedf_freq == 0:
            best_active_comsumption_value = 0
            self.slack_time = eariest_deadline - current_time
            if self.slack_time <= config.WAKEUP_TIME_OV*2:
                best_comsumption_value = min_core_power*self.slack_time
            else:
                comsumption_value1 = min_core_power*self.slack_time
                comsumption_value2 = config.SLEEP_POWER*(self.slack_time - config.WAKEUP_TIME_OV*2) + \
                                     config.WAKEUP_POWER_OV*2
                best_comsumption_value = min(comsumption_value1, comsumption_value2)
            self.real_exec_time = self.slack_time
            self.rem_exec_time = exe_task_c_rem
        else:
            core_power = core_powerlist[core_freqlist.index(core_freq)]
            self.task_exec_time = exe_task_c_rem*1.0/core_freq
            self.real_exec_time = min(self.task_exec_time, eariest_deadline - current_time)
            self.rem_exec_time = (self.task_exec_time - self.real_exec_time)*core_freq
            best_comsumption_value = core_power*self.real_exec_time
            best_active_comsumption_value = core_power*self.real_exec_time
        self.best_active_comsumption_value = best_active_comsumption_value
        '''
        print "best_core(la2)"
        print best_core_freq
        '''

        return best_comsumption_value


    def la2_edf(self, task_queuelist, ready_queue_id, current_time,
                hyperperiod, core_freqlist, core_powerlist):
        t_periodlist = []
        t_wcetlist = []
        next_highpri_release_timelist = [hyperperiod]
        next_lowpri_release_timelist = [hyperperiod]
        s = 0
        best_comsumption_value = float("inf")
        for i in xrange(len(task_queuelist)):
            t_queue = task_queuelist[i]
            t_task = t_queue[1]
            t_periodlist.append(t_task[0])
            t_wcetlist.append(t_task[1])
        '''
        util = sum(t_wcetlist[i]*1.0/t_periodlist[i]
                   for i in xrange(len(task_queuelist)))
        '''
        util = 0
        util2 = 0
        x = 0

        exe_task = task_queuelist[ready_queue_id]
        exe_task_deadline = exe_task[0]
        exe_task_c_rem = exe_task[2]
        highest_pri_queue = task_queuelist[0]
        eariest_deadline = highest_pri_queue[0]
        low_pri_queue = task_queuelist[ready_queue_id+1:]
        high_pri_queue = task_queuelist[:ready_queue_id]
        max_core_freq = core_freqlist[0]
        min_core_power = core_powerlist[-1]
        best_core_freq = 0
        '''
        for task_queue in reversed(task_queuelist):
            deadline, task, c_rem, count = task_queue
            util = util - task[1]*1.0/task[0]
            rem_time = max(0, c_rem - (1 - util)*(deadline - eariest_deadline))
            if deadline > eariest_deadline:
                util = util + (c_rem - rem_time)*1.0/(deadline - eariest_deadline)
            s = s + rem_time
        '''

        for task_queue in reversed(task_queuelist):
            util2 = 0
            deadline, task, c_rem, count = task_queue
            for task_queue2 in task_queuelist:
                 deadline2, task2, c_rem2, count2 = task_queue2
                 if deadline2 < deadline:
                     util2 = util2 +  task2[1]*1.0/task2[0]
                 else:
                     break
            '''
            print "util2"
            print util2
            '''
            util = x + util2
            '''
            print "util"
            print util
            '''
            rem_time = max(0, c_rem - (1 - util)*(deadline - eariest_deadline))
            if deadline > eariest_deadline:
                x = x + (c_rem - rem_time)*1.0/(deadline - eariest_deadline)
            '''
            print "x"
            print x
            '''
            s = s + rem_time

        laedf_freq = max_core_freq*s*1.0/(eariest_deadline - current_time)
        '''
        print "laedf"
        print laedf_freq
        '''
        laedf_origin = laedf_freq
        if laedf_freq >  max_core_freq:
            laedf_freq =  max_core_freq
            '''
            print("down to 1")
            '''
            self.count = self.count + 1
        if laedf_freq > max_core_freq:
            print("Error2: la_edf(), la_edf cannot schedule(task_set is overload)")
            print laedf_origin
            exit()
        for core_freq in reversed(core_freqlist):
            if core_freq >= laedf_freq:
                best_core_freq = core_freq
                break
            else:
                pass
        '''
        print "best_core_freq"
        print best_core_freq
        '''
        high_core_freqlist = core_freqlist[0: core_freqlist.index(best_core_freq)+1]
        
        if laedf_freq == 0:
            self.best_active_comsumption_value = 0
            self.slack_time = eariest_deadline - current_time
            if self.slack_time <= config.WAKEUP_TIME_OV*2:
                best_comsumption_value = min_core_power*self.slack_time
                self.best_active_comsumption_value = best_comsumption_value
            else:
                comsumption_value1 = min_core_power*self.slack_time
                comsumption_value2 = config.SLEEP_POWER*(self.slack_time - config.WAKEUP_TIME_OV*2) + \
                                     config.WAKEUP_POWER_OV*2
                best_comsumption_value = min(comsumption_value1, comsumption_value2)
            self.real_exec_time = self.slack_time
            self.rem_exec_time = exe_task_c_rem
            self.elapsed_time = self.slack_time
        else:
            for high_pri_item in high_pri_queue:
                deadline, task, c_rem, count = high_pri_item
                if c_rem == 0:
                    release_time = deadline
                else:
                    release_time = task[2]
                next_highpri_release_timelist.append(release_time)

            for low_pri_item in low_pri_queue:
                deadline, task, c_rem, count = low_pri_item
                if c_rem == 0:
                    release_time = deadline
                else:
                    release_time = task[2]
                next_lowpri_release_timelist.append(release_time)
            self.next_highpri_release_time = min(next_highpri_release_timelist)
            self.next_lowpri_release_time = min(next_lowpri_release_timelist)
            '''
            print self.next_highpri_release_time
            print self.next_lowpri_release_time
            '''
            high_core_freqlist = core_freqlist[0: core_freqlist.index(best_core_freq)+1]

            for core_freq in high_core_freqlist:
                core_power = core_powerlist[core_freqlist.index(core_freq)]
                self.task_exec_time = exe_task_c_rem*1.0/core_freq
                self.real_exec_time = min(self.task_exec_time,
                                          self.next_highpri_release_time - current_time)

                self.rem_exec_time = (self.task_exec_time - self.real_exec_time)*core_freq
                if  self.rem_exec_time > 0:
                    self.slack_time = 0
                else:
                    useful_time = min(self.next_highpri_release_time, self.next_lowpri_release_time, exe_task_deadline)
                    useful_time = useful_time - current_time
                    self.slack_time = max(0, useful_time - self.task_exec_time)
                if self.slack_time <= config.WAKEUP_TIME_OV*2:
                    current_comsumption_value1 = core_power*self.real_exec_time + min_core_power*self.slack_time
                    current_comsumption_value2 = float("inf")
                    '''
                    print "slack_time1"
                    print self.slack_time
                    print "current_comsumption_value"
                    print current_comsumption_value1
                    '''
                    self.elapsed_time = self.real_exec_time + self.slack_time
                else:
                    current_comsumption_value1 = core_power*self.real_exec_time + min_core_power*self.slack_time
                    current_comsumption_value2 = core_power*self.real_exec_time +  \
                                                 config.SLEEP_POWER*(self.slack_time - config.WAKEUP_TIME_OV*2) +  \
                                                 config.WAKEUP_POWER_OV*2
                    self.elapsed_time = self.real_exec_time + self.slack_time
                '''
                print "slack_time2"
                print self.slack_time
                print "current_comsumption_value"
                print "{0}, {1}" .format(current_comsumption_value1, current_comsumption_value2)
                '''
                current_comsumption_value = min(current_comsumption_value1, current_comsumption_value2)
                if current_comsumption_value < best_comsumption_value:
                    best_comsumption_value = current_comsumption_value
                    best_real_exec_time = self.real_exec_time
                    best_elapsed_time = self.elapsed_time
                    best_rem_exec_time = self.rem_exec_time
                    best_freq = core_freq
                    best_core = core_powerlist[core_freqlist.index(best_freq)]
                else:
                    pass
                self.real_exec_time = best_real_exec_time
                self.rem_exec_time = best_rem_exec_time
                self.elapsed_time = best_elapsed_time
                self.best_active_comsumption_value = self.real_exec_time*best_core
        


        return best_comsumption_value

    def get_RealExeTime(self):
        return self.real_exec_time

    def get_ElapsedTime(self):
        return self.elapsed_time

    def get_RemExeTime(self):
        return self.rem_exec_time

    def get_OVfreqnum(self):
        return self.count

    def get_BestActiveComsumptionValue(self):
        return self.best_active_comsumption_value

'''
        max_pri_task = task_queuelist[0]
        max_pri_task_deadline = max_pri_task[0]
        max_pri_task_c_rem = max_pri_task[2]

        task_queuelist.pop(0)'''
