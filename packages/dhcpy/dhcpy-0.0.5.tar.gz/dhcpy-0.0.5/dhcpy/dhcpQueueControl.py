class DHCPQueueControl(object):
    def __init__(self):
      self.capacity = 0
      self.enable_queue =  False
      self.queue_type = ""


    @property
    def capacity(self):
        return self._capacity
    @capacity.setter
    def capacity(self, capacity):
        if type(capacity) is not int:
            raise ValueError("Capacity must be an integer")
        self._capacity = capacity
    @property
    def enable_queue(self):
        return self._enable_queue
    @enable_queue.setter
    def enable_queue(self, enable_queue):
        if type(enable_queue) is not bool:
            if type(enable_queue) is str:
                if enable_queue.lower() == "true":
                    self._enable_queue = True
                    return
                elif enable_queue.lower() == "false":
                    self._enable_queue = False
                    return
            raise ValueError("Enable queue must be a boolean (or maybe a string)")
        self._enable_queue = enable_queue
    def __dict__(self):
        return {"capacity": self.capacity, "enable-queue": self.enable_queue, "queue-type": self.queue_type}

    def fill_from_json(self, data):
        self.capacity = data["capacity"]
        self.enable_queue = data["enable-queue"]
        self.queue_type = data["queue-type"]
