from math import ceil


class Process:
    def __init__(self, pid, arrival_time, burst_time, priority, name):
        self.pid = pid
        self.arrival_time = (float(arrival_time) / 1000)
        self.burst_time = (float(burst_time) / 1000)
        self.priority = priority if 1 < priority < 140 else exit()
        self.name = name
        self.time_slot = 1

    def get_arrival_time(self):
        return self.arrival_time

    def get_burst_time(self):
        return self.burst_time

    def update_burst_time(self, time):
        return self.burst_time - time

    def update_priority(self, priority):
        if priority < 100:
            self.time_slot = float((140 - priority) * 0.02)  # In Milliseconds
        else:
            self.time_slot = float((140 - priority) * 0.005)  # In Milliseconds

    def get_timeslot(self):
        return self.time_slot

    def update_priority(self, waiting_time, time_now, arrival_time):
        bonus = ceil(10 * waiting_time / (time_now - arrival_time))
        self.priority = max(100, min(self.get_priority() - bonus + 5, 139))

    def get_priority(self):
        return self.priority

    def get_pid(self):
        return self.pid

    def get_name(self):
        return self.name

    def get_process_from_pid(self, pid):
        return self if self.pid == pid else None
