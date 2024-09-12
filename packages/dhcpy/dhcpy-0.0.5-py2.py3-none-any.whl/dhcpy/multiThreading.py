class MultiThreading(object):
    def __init__(self):
        self.enable_multithreading = False
        self.packet_queue_size = 0
        self.thread_pool_size = 0
    def __dict__(self):
        return {"enable-multithreading": self.enable_multithreading, "packet-queue-size": self.packet_queue_size, "thread-pool-size": self.thread_pool_size}
    def fill_from_json(self, data):
        if "enable-multi-threading" not in data:
            print(f"Data: {data}")
        self.enable_multithreading = data["enable-multi-threading"]
        self.packet_queue_size = data["packet-queue-size"]
        self.thread_pool_size = data["thread-pool-size"]
