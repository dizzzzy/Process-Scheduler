import os
import threading
import time

from Queue import Queue

Q1 = Queue()
Q2 = Queue()


class ProcessThread(threading.Thread):
    def __init__(self, plist, pname):
        super(ProcessThread, self).__init__()
        self.process_list = plist
        self.process_name = pname
        self.paused = False
        self.pause_cond = threading.Condition(threading.Lock())

    def pause(self):
        self.pause_cond.acquire()

    def resume(self):
        self.pause_cond.release()

    def run(self):
        for i in range(1, 5, 1):
            self.pause_cond.acquire()
            print "Printing %s" % self.process_name
            time.sleep(1)
            self.pause_cond.release()
