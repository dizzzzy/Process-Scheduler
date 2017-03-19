from Process import *


class Queue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def enqueue_pid(self, item):
        self.items.insert(0, item)

    def de_queue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

    def get_pid(self, pid):
        return self.items.__getitem__(pid)

    def get_all_pid(self):
        return self.items


process_list = []
active_queue = Queue()
expired_queue = Queue()

with open("input.txt") as f:
    for processes in f.readlines()[2:]:
        process = processes.split(" ")
        process_name = main_process(process[3], process[1], process[2], int(process[3]))
        active_queue.enqueue_pid(process_name.pid)