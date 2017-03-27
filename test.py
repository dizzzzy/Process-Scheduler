import time

from Queue import Queue

from Processing import ProcessThread

with open("input.txt") as f:
    process_list = f.readlines()[2:]

process_list_object = ProcessThread(process_list)

Q1 = Queue()
Q2 = Queue()

active_queue = Q1
expired_queue = Q2

new_process_1 = process_list_object.process_list[0]
new_process_2 = process_list_object.process_list[1]

expired_queue.enqueue_process(0, new_process_1)
expired_queue.enqueue_process(1, new_process_2)

if active_queue.size() == 0 and expired_queue.size() != 0:
    active_queue, expired_queue = expired_queue, active_queue

time_burst = active_queue.get_all_process()[0].split(" ")[2]

print "Processing for %s seconds" % time_burst

time.sleep(int(time_burst) / 1000)

active_queue.de_queue(new_process_1)
expired_queue.enqueue_process(0, new_process_1)

time_burst_2 = active_queue.get_all_process()[0].split(" ")[2]
print "Processing for %s seconds" % time_burst_2

time.sleep(int(time_burst_2) / 1000)
active_queue.de_queue(new_process_2)
expired_queue.enqueue_process(1, new_process_2)

if active_queue.size() == 0 and expired_queue.size() != 0:
    active_queue, expired_queue = expired_queue, active_queue

print active_queue.get_all_process()
print expired_queue.get_all_process()