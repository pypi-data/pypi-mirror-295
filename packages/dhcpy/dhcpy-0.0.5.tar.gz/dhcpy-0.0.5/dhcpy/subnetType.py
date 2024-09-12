from enum import Enum

class SubnetType(Enum):
    """Different types of subnets that KEA can handle. This is used to determine the type of pool to use and the
    commands to run on the server."""
    none = None
    v4 = "subnet4"  # TODO: This is a guess
    v6 = "subnet6"
    pd = "subnet6-pd"  # TODO: This is a guess
