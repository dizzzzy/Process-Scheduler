import threading
import time

from Processing import ProcessThread
from Queue import process_list


class SchedulerThread(threading.Thread):
    """
    Main Scheduler thread: Priority based scheduler
    1. Can pause/resume child processes
    2. Allows uni-processing scheduling
    Each process is responsible to keep track of its total execution and inform the scheduler thread when it is
    finished. This process continues until all processes are done.
    Active/Expired Queue will contain the PID's of the processes.
    Default time slot is 0.
    """

    def __init__(self):
        super(SchedulerThread, self).__init__()
        self.paused = False
        self.pause_cond = threading.Condition(threading.Lock())
        self.time_slot = 0

    def pause(self):
        """
        Allows the current child process to pause until resumed is called
        """
        self.paused = True
        self.pause_cond.acquire()

    def resume(self):
        """
        Allows the paused child process in the expired queue to run again
        """
        self.paused = False
        self.pause_cond.release()

    def update_priority(self, priority):
        if priority < 100:
            self.time_slot = (140 - priority) * 0.02  # In Milliseconds
        else:
            self.time_slot = (140 - priority) * 0.005  # In Milliseconds

    def run(self):
        time.sleep(1)  # Runs after 1 second
        process_thread = ProcessThread(process_list)
        process_thread.run()
