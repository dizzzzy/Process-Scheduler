import threading

import time


class scheduler_thread(threading.Thread):
    """
    Main Scheduler thread: Priority based scheduler
    1. Can pause/resume child processes
    2. Allows uni-processing scheduling
    Each process is responsible to keep track of its total execution and inform the scheduler thread when it is
    finished. This process continues until all processes are done.
    Active/Expired Queue will contain the PID's of the processes.
    """

    def __init__(self):
        super(scheduler_thread, self).__init__()
        self.paused = False
        self.pause_cond = threading.Condition(threading.Lock())

    def pause(self):
        """
        Allows the current child process to pause until resumed is called
        """
        self.paused = True
        self.pause_cond.acquire()
        time.sleep(10)

    def resume(self):
        """
        Allows the paused child process in the expired queue to run again
        """
        self.paused = False
        self.pause_cond.notify()
        self.pause_cond.release()

    def run(self):
        print "Hello"
        process_thread = threading.Thread(main())
        process_thread.run()
        # while True:
        #     with self.pause_cond:
        #         while self.paused:
        #             self.pause_cond.wait()
        #         print 'do the thing'
        #     time.sleep(5)


def main():
    print "Hello"
    time.sleep(10)
    print "Nitesh"


main_scheduler_thread = scheduler_thread()
main_scheduler_thread.run()
