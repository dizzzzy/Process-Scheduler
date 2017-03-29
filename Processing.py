import threading
import time



class ProcessThread(threading.Thread):
    def __init__(self, process_object):
        super(ProcessThread, self).__init__()
        self.process = process_object
        self.process_name = process_object.get_name()
        self.paused = False
        self.hasStarted = False
        self.pause_cond = threading.Condition(threading.Lock())

    def pause(self, pauseTime):
        self.paused = True
        self.pause_cond.acquire()
        print self.process_name + " process has paused at " + str(pauseTime)

    def resume(self, resumeTime):
        self.paused = False
        self.pause_cond.release()
        print self.process_name + " process has resumed at " + str(resumeTime)

    def start(self, startTime):
        print self.process_name + " process has started at " + str(startTime)
        super(ProcessThread, self).start()

        self.hasStarted = True