class ExpiredLeasesProcessing (object):
    """
    The Expired Leases Processing object for the DHCP service
    Tells KEA how to process expired leases
    """
    def __init__(self):
        """
        Initialize the Expired Leases Processing object
        """
        self.flush_reclaimed_timer_wait_time = 20
        """Seconds to wait after flushing reclaimed leases and restating the flush"""
        self.hold_reclaimed_time = 0
        """how long the lease should be kept after it is reclaimed"""
        self.max_reclaim_leases = 0
        """the maximum number of reclaimed leases that can be processed at one time"""
        self.max_reclaim_time = 0
        """the maximum time that can be spent reclaiming leases"""
        self.reclaim_timer_wait_time = 0
        """how often the server starts the lease reclamation procedure"""
        self.unwarned_reclaim_cycles= 0
        """how many consecutive clean-up cycles can end with remaining leases to be processed before a warning is printed"""
    def __dict__(self):
        """
        return a dictionary representation of the Expired Leases Processing object, for making the KEA JSON thing
        """
        return {"flush-reclaimed-timer-wait-time": self.flush_reclaimed_timer_wait_time, "hold-reclaimed-time": self.hold_reclaimed_time, "max-reclaim-leases": self.max_reclaim_leases, "max-reclaim-time": self.max_reclaim_time, "reclaim-timer-wait-time": self.reclaim_timer_wait_time, "unwarned-reclaim-cycles": self.unwarned_reclaim_cycles}
    def fill_from_json(self, data):
        """
        Fill from the JSON from the KEA web API
        """
        self.flush_reclaimed_timer_wait_time = data["flush-reclaimed-timer-wait-time"]
        self.hold_reclaimed_time = data["hold-reclaimed-time"]
        self.max_reclaim_leases = data["max-reclaim-leases"]
        self.max_reclaim_time = data["max-reclaim-time"]
        self.reclaim_timer_wait_time = data["reclaim-timer-wait-time"]
        self.unwarned_reclaim_cycles = data["unwarned-reclaim-cycles"]
