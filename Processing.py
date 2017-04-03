import threading


class ProcessThread(threading.Thread):
    def __init__(self, process_object):
        super(ProcessThread, self).__init__()
        self.process = process_object
        self.process_name = process_object.get_name()
        self.paused = False
        self.hasStarted = False
        self.pause_cond = threading.Condition(threading.Lock())

    def pause(self, pause_time):
        self.paused = True
        self.pause_cond.acquire()
        print str(self.process_name) + " process has paused at " + str(pause_time)

    def resume(self, resume_time):
        self.paused = False
        self.pause_cond.release()
        print str(self.process_name) + " process has resumed at " + str(resume_time)

    def start(self, start_time):
        print str(self.process_name) + " process has started at " + str(start_time)
        super(ProcessThread, self).start()
        self.hasStarted = True
