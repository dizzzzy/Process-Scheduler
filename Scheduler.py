import threading

import time

from Queue import Queue

from Processing import ProcessThread
from timeit import default_timer

Q1 = Queue()
Q2 = Queue()


class SchedulerThread(threading.Thread):
    """
        Main Scheduler thread: Priority based scheduler
        1. Can pause/resume processes - Done
        2. Switch between the active and expired queue
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
        with open("input.txt") as f:
            process_list = f.readlines()[2:]
        self.process_list = process_list
        self.active_queue = Q1
        self.expired_queue = Q2

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
        process_thread_1 = ProcessThread(self.process_list, "P1")
        process_thread_2 = ProcessThread(self.process_list, "P2")
        process_thread_3 = ProcessThread(self.process_list, "P3")

        st = False
        while True:
            elapsed_time = default_timer() - self.start_time
            if int(elapsed_time) == 1 and not st:  # Start the thread at 1 second
                process_thread_1.start()
                print "P1 given 2500, Time: ", int(default_timer() - self.start_time), "Seconds"
                process_thread_1.pause()
                time.sleep(2.5)

                process_thread_2.start()
                print "P2 given 100, Time: ", int(default_timer() - self.start_time), "Seconds"
                process_thread_2.pause()
                time.sleep(0.1)

                process_thread_3.start()
                print "P3 given 100, Time: ", int(default_timer() - self.start_time), "Seconds"
                process_thread_3.pause()
                time.sleep(0.1)

                process_thread_1.resume()
                process_thread_1.join()
                process_thread_2.resume()
                process_thread_2.join()
                process_thread_3.resume()
                process_thread_3.join()
                print "Total Time: ", int(default_timer() - self.start_time), "Seconds"
                st = True
                break
            elif int(elapsed_time) > 1:
                print None



        # st = False
        # while True:
        #     elapsed_time = default_timer() - self.start_time
        #     if int(elapsed_time) == 1 and not st:  # Start the thread at 1 second
        #         print "Starting process, Time: ", int(default_timer() - self.start_time), "Second"
        #         process_thread.start()
        #         st = True
        #     elif int(elapsed_time) > 1:
        #         print "Pausing process P1, Time: ", int(default_timer() - self.start_time), "Seconds"
        #         process_thread.pause()
        #         print "P1 paused, Time: ", int(default_timer() - self.start_time), "Seconds"
        #         print "Starting P2, Time: ", int(default_timer() - self.start_time), "Seconds"
        #         process_thread_2.start()
        #         time.sleep(2)
        #         process_thread_2.pause()
        #         print "Pausing Process P2, Time: ", int(default_timer() - self.start_time), "Seconds"
        #         process_thread.resume()
        #         time.sleep(3)
        #         process_thread.pause()
        #         print "Resuming Process P2, Time: ", int(default_timer() - self.start_time), "Seconds"
        #         process_thread_2.resume()
        #         process_thread_2.join()
        #         print "Finished P2, Time: ", int(default_timer() - self.start_time), "Seconds"
        #         print "P1 resumed, Time: ", int(default_timer() - self.start_time), "Seconds"
        #         process_thread.resume()
        #         process_thread.join()
        #         print "Finished at ", int(default_timer() - self.start_time), "Seconds"
        #         break
        #     else:
        #         time.sleep(1)
        #         pass
