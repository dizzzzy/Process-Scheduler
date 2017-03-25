import os
import threading
import time

from Queue import Queue

Q1 = Queue()
Q2 = Queue()


class ProcessThread(threading.Thread):
    def __init__(self, plist):
        super(ProcessThread, self).__init__()
        self.process_list = plist
        self.paused = False
        self.pause_cond = threading.Condition(threading.Lock())

    def pause(self):
        # self.paused = True
        self.pause_cond.acquire()

    def resume(self):
        # self.paused = False
        # self.pause_cond.notify()
        self.pause_cond.release()

    def run(self):
        if self.process_list == 1:
            for i in range(1, 10, 1):
                self.pause_cond.acquire()
                print "Printing P1"
                time.sleep(1)
                self.pause_cond.release()

        elif self.process_list == 2:
            for i in range(1, 10, 1):
                self.pause_cond.acquire()
                print "Printing P2"
                time.sleep(1)
                self.pause_cond.release()
            # global active_queue, expired_queue
            # Q1.enqueue_process(0, self.process_list[0])
            # if Q1.is_empty() is True and Q2.is_empty() is not True:
            #     expired_queue = Q1
            #     active_queue = Q2
            # elif Q2.is_empty() is True and Q1.is_empty() is not True:
            #     expired_queue = Q2
            #     active_queue = Q1
            #
            # run_timeslot = active_queue.get_all_process()[0].get_timeslot()
            # print "Time %d, %s, Started, Granted %d" % (run_timeslot, 'P1', run_timeslot)
            # time.sleep(run_timeslot)
