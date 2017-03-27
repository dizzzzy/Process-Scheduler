import threading
import time

from Processing import ProcessThread
from Queue import process_list
from timeit import default_timer


class SchedulerThread(threading.Thread):
    """
    Main Scheduler thread: Priority based scheduler
    1. Can pause/resume processes
    2. Switch between the active and expired queue
    3. Updates the priority of the processes if they run twice
    4. Give time slots to the processes\
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
                print "Starting process, Time: ", int(default_timer() - self.start_time), "Second"
                process_thread.start()
                st = True
            elif int(elapsed_time) > 1:
                print "Pausing process P1, Time: ", int(default_timer() - self.start_time), "Seconds"
                process_thread.pause()
                print "P1 paused, Time: ", int(default_timer() - self.start_time), "Seconds"
                print "Starting P2, Time: ", int(default_timer() - self.start_time), "Seconds"
                process_thread_2.start()
                time.sleep(2)
                process_thread_2.pause()
                print "Pausing Process P2, Time: ", int(default_timer() - self.start_time), "Seconds"
                process_thread.resume()
                time.sleep(3)
                process_thread.pause()
                print "Resuming Process P2, Time: ", int(default_timer() - self.start_time), "Seconds"
                process_thread_2.resume()
                process_thread_2.join()
                print "Finished P2, Time: ", int(default_timer() - self.start_time), "Seconds"
                print "P1 resumed, Time: ", int(default_timer() - self.start_time), "Seconds"
                process_thread.resume()
                process_thread.join()
                print "Finished at ", int(default_timer() - self.start_time), "Seconds"
                break
            else:
                time.sleep(1)
                pass
