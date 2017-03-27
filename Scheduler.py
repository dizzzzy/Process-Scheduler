import threading

import time

from Process import Process
from Processing import ProcessThread
from Queue import Queue

from timeit import default_timer

Q1 = Queue()
Q2 = Queue()

p_list = []
with open("input.txt") as f:
    process_list = f.readlines()[2:]
    for index, process in enumerate(process_list):
        process_sub_items = process.split(" ")
        p_list.append(Process(int(index + 1), process_sub_items[1], process_sub_items[2], int(process_sub_items[3]),
                              process_sub_items[0]))


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
        self.active_queue = Q1  # At starting, Q1 is active queue and Q2 is expired queue
        self.expired_queue = Q2
        self.timeslot = 1

    def switch(self):
        if self.active_queue.size() == 0 and self.expired_queue.size() != 0:
            self.active_queue, self.expired_queue = self.expired_queue, self.active_queue

    def run(self):
        process_thread_1 = ProcessThread(self.process_list[0])
        process_thread_2 = ProcessThread(self.process_list[1])
        process_thread_3 = ProcessThread(self.process_list[2])

        flag = True
        start_time = default_timer()
        while True and flag:
            if int(default_timer() == self.timeslot):
                self.expired_queue.enqueue_process(0, process_thread_1)
                self.switch()

                if process_thread_1.process.get_burst_time() > self.timeslot:
                    process_thread_1.start()
                    if int(default_timer() == 2):

                        process_thread_1.pause()
                        process_thread_1.process.update_burst_time(self.timeslot)

                        self.active_queue.de_queue(process_thread_1)
                        self.expired_queue.enqueue_process(0, process_thread_1)
                flag = False
