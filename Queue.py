from Process import *


class Queue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def enqueue_process(self, index, item):
        return self.items.insert(index, item)

    def de_queue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

    def get_pid(self, pid):
        return self.items.__getitem__(pid)

    def get_all_process(self):
        return self.items


process_list = []


with open("input.txt") as f:
    for processes in f.readlines()[2:]:
        process = processes.split(" ")
        process_name = Process(process[3], process[1], process[2], int(process[3]))
        process_list.append(process_name)
