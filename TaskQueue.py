#! /usr/bin/python
# *-* encoding: utf-8 *-*

import heapq
import itertools


class TaskQueue:

    REMOVED = '<removed-task>'  # placeholder for a removed task

    def __init__(self, name=""):
        self.name = name
        self.pq = []  # list of entries arranged in a heap
        self.entry_finder = {}  # mapping of tasks to entries
        self.counter = itertools.count()  # unique sequence count

    def set_TaskQueue(self, task_queue):
        self.pq = task_queue
        heapq.heapify(self.pq)

    def add_TaskQueue(self, priority, task, c_rem):
        'Add a new task or update the priority of an existing task'
        if task in self.entry_finder:
            entry = self.entry_finder.pop(task)
            entry[1] = self.REMOVED
        count = next(self.counter)
        entry = [priority, task, c_rem, count]
        self.entry_finder[task] = entry
        heapq.heappush(self.pq, entry)

    def remove_TaskQueue(self, task):
        'Remove an existing task'
        if task in self.entry_finder:
            entry = self.entry_finder.pop(task)
            entry[1] = self.REMOVED

    def pop_TaskQueue(self):
        'Remove and return the lowest priority task. Raise KeyError if empty.'
        while self.pq:
            priority, task, c_rem, count = heapq.heappop(self.pq)
            if task is not self.REMOVED:
                del self.entry_finder[task]
                return [priority, task, c_rem, count]
        return 0

    def get_TaskQueueTop(self):
        'Return the lowest priority task without pop'
        while self.pq:
            priority, task, c_rem,  count = self.pq[0]
            if task is not self.REMOVED:
                return [priority, task, c_rem, count]
            else:
                heapq.heappop(self.pq)
        return 0

    def get_TaskQueueList(self):
        'Return the task queue without <removed-task> item by <list> type'
        queue_reallist = []
        queue_list = heapq.nsmallest(len(self.pq), self.pq)
        for i in range(len(queue_list)):
            priority, task, c_rem,  count = queue_list[i]
            if task is not self.REMOVED:
                queue_reallist.append(queue_list[i])
            else:
                pass
        return queue_reallist

    def get_TaskQueueLen(self):
        'Return the task queue length without <removed-task> item'
        length = 0
        for i in range(len(self.pq)):
            priority, task, c_rem,  count = self.pq[i]
            if task is not self.REMOVED:
                length = length + 1
            else:
                pass
        return length

    def print_entryfinder(self):
        print self.entry_finder

    def print_taskqueue(self):
        print self.pq
