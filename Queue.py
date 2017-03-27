class Queue:
    """
        Queue functionality:
        1. Automatically sorts the processes in the queue based on priority
    """
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def enqueue_process(self, index, item):
        return self.items.insert(index, item)

    def de_queue(self, item):
        return self.items.remove(item)

    def size(self):
        return len(self.items)

    def get_pid(self, pid):
        return self.items.__getitem__(pid)

    def get_all_process(self):
        return self.items

