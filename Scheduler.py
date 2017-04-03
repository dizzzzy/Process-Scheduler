import threading

import time
import sched
from Process import Process
from Processing import ProcessThread
from Q import Q

from timeit import default_timer

p_list = []
with open("input.txt") as f:
    process_list = f.readlines()[2:]
    for index, process in enumerate(process_list):
        process_sub_items = process.split(" ")
        p_list.append(Process(int(index + 1), process_sub_items[1], process_sub_items[2], int(process_sub_items[3]),
                              process_sub_items[0]))
Q1 = Q()
Q2 = Q()


class SchedulerThread(threading.Thread):
    """
        Main Scheduler thread: Priority based scheduler
        1. Can pause/resume processes - Done
        2. Switch between the active and expired queue - Done
        3. Updates the priority of the processes if they run twice
        4. Give time slots to the processes
        Each process is responsible to keep track of its total execution and inform the scheduler thread when it is
        finished. This process continues until all processes are done.
        Active/Expired Queue will contain the PID's of the processes.
    """

    def __init__(self):
        super(SchedulerThread, self).__init__()
        self.paused = False
        self.pause_cond = threading.Condition(threading.Lock())
        self.start_time = default_timer()

        self.process_list = p_list
        # At starting, Q1 is active queue and Q2 is expired queue
        self.active_queue = Q1
        self.expired_queue = Q2

    def swap(self):
        if len(self.active_queue.items) == 0 and len(self.expired_queue.items) != 0:  # swaps queues
            self.active_queue.items, self.expired_queue.items = self.expired_queue.items, self.active_queue.items
            # print "active queue: " + str(self.active_queue.items)
            # print "expired queue: " + str(self.expired_queue.items)

    def run(self):
        process_length = len(p_list)
        process_thread_list = []
        for i in range(0, process_length):
            temp = ProcessThread(self.process_list[i])
            process_thread_list.append(temp)
        flag = True
        terminated_processes = 0
        start_time = default_timer()
        while True and flag:
            if int((default_timer() - start_time) > 1):  # Start at time 1 second
                for i in range(0, process_length):
                    if process_thread_list[i].process.get_arrival_time() <= (default_timer() - start_time) and not \
                            process_thread_list[i].process.has_started:
                        # send process in expired queue
                        self.expired_queue.enqueue_process(process_thread_list[i])
                        process_thread_list[i].process.has_started = True
                        print process_thread_list[i].process_name + " arrived at " + str(default_timer() - start_time)
                        sorted_list_of_priorities = sorted([x.process.get_priority() for x in process_thread_list])
                        # Get Process from priority
                        
                        # temp_process_list = []
                        # for x in sorted_list_of_priorities:
                        #     temp_process_list.append()
                        # process_thread_list = temp_process_list

                self.swap()

                while len(self.active_queue.items) != 0:
                    if self.active_queue.getItem(0).process.get_burst_time() > 0:
                        if self.active_queue.getItem(0).hasStarted:
                            self.active_queue.getItem(0).resume(default_timer() - start_time)
                        else:
                            self.active_queue.getItem(0).start(default_timer() - start_time)
                        process_start_time = default_timer() - start_time
                        process_end_time = process_start_time + self.active_queue.getItem(0).process.get_timeslot()
                        going_to_finish = False
                        if self.active_queue.getItem(0).process.get_timeslot() >= self.active_queue.getItem(
                                0).process.get_burst_time():
                            process_end_time = process_start_time + self.active_queue.getItem(
                                0).process.get_burst_time()
                            going_to_finish = True
                        i = 0
                        while (default_timer() - start_time) < process_end_time:
                            # check if arrival time has passed
                            if process_thread_list[i].process.get_arrival_time() < (
                                    default_timer() - start_time) and not process_thread_list[i].process.has_started:
                                # check if process has higher priority than running process
                                process_thread_list[i].process.has_started = True
                                print process_thread_list[i].process_name + " arrived at " + str(
                                    default_timer() - start_time)
                                self.expired_queue.enqueue_process(process_thread_list[i])
                            i = (i + 1) % process_length
                        self.active_queue.getItem(0).pause(default_timer() - start_time)  # pause current process
                        if going_to_finish:
                            self.active_queue.getItem(0).process.update_burst_time(
                                self.active_queue.getItem(0).process.get_burst_time(),
                                (default_timer() - start_time))  # updates burst time
                            terminated_processes += 1
                            self.active_queue.pop()  # pops the first element in the queue
                            if terminated_processes == process_length:
                                flag = False
                        else:
                            self.active_queue.getItem(0).process.update_burst_time(
                                self.active_queue.getItem(0).process.get_timeslot(),
                                (default_timer() - start_time))  # updates burst time
                            self.expired_queue.enqueue_process(
                                self.active_queue.getItem(0))  # adds the process into expired queue
                            self.active_queue.pop()  # pops the first element in the queue
