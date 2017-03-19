class Process:
    def __init__(self, pid, arrival_time, burst_time, priority):
        self.pid = pid
        self.arrival_time = (float(arrival_time) / 1000)
        self.burst_time = (float(burst_time) / 1000)
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
