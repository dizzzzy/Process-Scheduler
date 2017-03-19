class main_process:
    def __init__(self, pid, arrival_time, burst_time, priority):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority if 1 < priority < 140 else exit()

    def get_process(self):
        return self

    def get_arrival_time(self):
        return self.arrival_time

    def get_burst_time(self):
        return self.burst_time

    def get_priority(self):
        return self.priority

    def get_pid(self):
        return self.pid

    def get_process_from_pid(self, pid):
        return self if self.pid == pid else None

process_list = []
with open("input.txt") as f:
    for processes in f.readlines()[2:]:
        process = processes.split(" ")
        process_name = main_process(process[3], process[1], process[2], int(process[3]))
        process_list.append(process_name)
