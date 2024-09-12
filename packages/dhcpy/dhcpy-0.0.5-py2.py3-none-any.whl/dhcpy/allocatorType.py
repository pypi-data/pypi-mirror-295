from enum import Enum

class AllocatorType(Enum):
    """
    Tells an allocator to give out IPs in a row (iterative) or randomly (randomized)
    """
    none = None
    """No allocator set"""
    iterative = "iterative"
    """Gives out IPs in a row"""
    randomized = "randomized"
    """Gives out IPs randomly"""