import threading
import time

from Queue import Queue

Q1 = Queue()
Q2 = Queue()


class ProcessThread(threading.Thread):
    def __init__(self, plist):
        super(ProcessThread, self).__init__()
        self.process_list = plist

    def run(self):
        Q2.enqueue_process(self.process_list[0])
        active_queue = Q2
        if Q1.is_empty() is True and Q2.is_empty() is not True:
            expired_queue = Q1
            active_queue = Q2
        elif Q2.is_empty() is True and Q1.is_empty() is not True:
            expired_queue = Q2
            active_queue = Q1
        else:
            print "No Processing left! Exiting!!!"
            exit(0)

        print "Process granted %s second" % active_queue.get_all_process()[0].get_timeslot()
        time.sleep(active_queue.get_all_process()[0].get_timeslot())  # Run P1 for desired time slot

        # active_queue.get_all_process()[0].update_priority(active_queue.get_all_process()[0].get_priority())
        print active_queue.get_all_process()[0].get_timeslot()
