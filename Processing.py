import os
import threading
import time

from Process import Process
from Queue import Queue

Q1 = Queue()
Q2 = Queue()


class ProcessThread(threading.Thread):
    def __init__(self, process_object):
        super(ProcessThread, self).__init__()
        self.process = process_object
        self.process_name = process_object.get_name()
        self.paused = False
        self.pause_cond = threading.Condition(threading.Lock())

    def pause(self):
        self.paused = True
        self.pause_cond.acquire()

    def resume(self):
        self.paused = False
        self.pause_cond.release()

    def run(self):
        # Each process prints its name for 5 times
        for i in range(0, 5, 1):
            self.pause_cond.acquire()
            print "Printing %s" % self.process_name
            time.sleep(1)
            self.pause_cond.release()
