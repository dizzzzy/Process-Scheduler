import threading
import time

from Processing import ProcessThread
from Queue import process_list
from timeit import default_timer


class SchedulerThread(threading.Thread):
    """
    Main Scheduler thread: Priority based scheduler
    1. Can pause/resume child processes
    2. Allows uni-processing scheduling
    Each process is responsible to keep track of its total execution and inform the scheduler thread when it is
    finished. This process continues until all processes are done.
    Active/Expired Queue will contain the PID's of the processes.

    """

    def __init__(self):
        super(SchedulerThread, self).__init__()
        self.paused = False
        self.pause_cond = threading.Condition(threading.Lock())
        self.start_time = default_timer()

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

    def run(self):
        process_thread = ProcessThread(1)
        process_thread_2 = ProcessThread(2)
        st = False
        while True:
            elapsed_time = default_timer() - self.start_time
            if int(elapsed_time) == 1 and not st:  # Start the thread at 1 second
                print "Starting process"
                process_thread.start()
                st = True
            if int(elapsed_time) == 3:
                print "Pausing process P1"
                process_thread.pause()
                print "P1 paused"
                print "Starting P2"
                process_thread_2.start()
                time.sleep(5)
                process_thread_2.join()
                print "Finished P2"
                print "P1 resumed"
                process_thread.resume()
                break
            else:
                time.sleep(1)
                pass
