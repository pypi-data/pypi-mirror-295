"""KEA subnet pools"""
from enum import Enum
from dhcpy.allocatorType import AllocatorType
from dhcpy.allocator import Allocator
import ipaddress
from dhcpy.dhcpOption import DHCPOption, OptionUsage
from dhcpy.ClientClass import ClientClass
from dhcpy.subnetType import SubnetType
from dhcpy.pool import Pool

class Subnet(Allocator):
    def __init__(self):
        """Initialize a subnet object, with empty strings and lists"""
        super().__init__()
        self.subnet_type = SubnetType.none
        """The type of subnet, subnet_type.v4, subnet_type.v6, or subnet_type.pd"""
        self.pools = []
        """A list of Pool objects"""
        self.name = ""
        """The name of the subnet"""
        self.id = -1
        """The ID of the subnet. This must be unique on the server, but the only test so far is that it is not negative"""
        self.client_class = ""
        self.client_class_set = False
        """A client class for the subnet. Mostly a placeholder at this time"""
        self.pd_allocator = ""
        """The allocator for the subnet. Like, do the addresses all in a row, or randomize it"""
        self.calculate_tee_times = True
        self.interface = ""
        self.max_preferred_lifetime = 0
        self.max_valid_lifetime = 0
        self.min_valid_lifetime = 0
        self.valid_lifetime = 0
        self.min_preferred_lifetime = 0
        self.preferred_lifetime = 0
        self._rapid_commit = False
        self._rapid_commit_set = False
        self.t1_percent = 0.5
        self.t2_percent = 0.8
        self.store_extended_info = False
        self._renew_timer = 0
        self._renew_timer_set = False
        self._rebind_timer = 0
        self._rebind_timer_set = False
        self._relays = []
        self._relays_set = False

    @property
    def client_class(self):
        """Return the client class"""
        return self._client_class_name
    @client_class.setter
    def client_class(self, client_class):
        """Set the client class"""
        self._client_class_name = client_class
        self._client_class_set = True
    @property
    def relays(self):
        """Return the relays"""
        return self._relays
    @relays.setter
    def relays(self, relays):
        """Set the relays"""
        self._relays = relays
        self._relays_set = True
    def add_relay(self, relay):
        """Add a relay to the list of relays"""
        self._relays.append(relay)
        self._relays_set = True
    @property
    def renew_timer(self):
        """Return the renew timer"""
        return self._renew_timer
    @renew_timer.setter
    def renew_timer(self, renew_timer):
        """Set the renew timer"""
        self._renew_timer = renew_timer
        self._renew_timer_set = True
    @property
    def rebind_timer(self):
        """Return the renew timer"""
        return self._rebind_timer
    @rebind_timer.setter
    def rebind_timer(self, rebind_timer):
        """Set the renew timer"""
        self._rebind_timer = rebind_timer
        self._rebind_timer_set = True
    @property
    def rapid_commit(self):
        """Return the rapid commit setting"""
        return self._rapid_commit
    @rapid_commit.setter
    def rapid_commit(self, rapid_commit):
        """Set the rapid commit setting"""
        self._rapid_commit = rapid_commit
        self._rapid_commit_set = True

    def __dict__(self):
        """Return a dictionary representation of the subnet, for making JSON in the format KEA expects"""
        if self.id >= 0:
            rets = super().__dict__()
            rets["id"] = self.id
            rets["pools"] =  []
            rets["client-class"] =  self.client_class
            if len(self.pools) > 0:
                if self.subnet_type == SubnetType.none:
                    self.subnet_type = self.pools[0].subnet_type
                if self.name is "":
                    self.name = f"{self.pools[0].network}"
                for pool in self.pools:
                    if pool.subnet_type != self.subnet_type:
                        raise ValueError("Pool type does not match subnet type")
                for pool in self.pools:
                    rets["pools"].append(pool.__dict__())
                rets["subnet"] = self.name

                return rets
            else:
                raise ValueError("No pools set")

        else:
            raise ValueError("No ID set")

    def fill_from_json(self, json_str):
        """Decode a JSON object into a subnet object"""
        # print(type(json_str))
        # print(json_str)
        try:
            data = json_str # this doesn't need to be here, but I am keeping for debugging
            super().fill_from_json(data)

            self.pd_allocator = data["pd-allocator"]
            self.id = int(data["id"])
            self.max_preferred_lifetime = data["max-preferred-lifetime"]
            self.max_valid_lifetime = data["max-valid-lifetime"]
            self.min_valid_lifetime = data["min-valid-lifetime"]
            self.valid_lifetime = data["valid-lifetime"]
            self.min_preferred_lifetime = data["min-preferred-lifetime"]
            self.preferred_lifetime = data["preferred-lifetime"]
            self.interface = data["interface"]
            self.t1_percent = data["t1-percent"]
            self.t2_percent = data["t2-percent"]
            self.name = data["subnet"]
            self.store_extended_info = data["store-extended-info"]
            self.renew_timer = data["renew-timer"]
            self.rebind_timer = data["rebind-timer"]
            self.rapid_commit = data["rapid-commit"]
            if "relay" in data.keys():
                for relay in data["relay"]['ip-addresses']:
                    self.add_relay(relay)
            if "client-class" in data.keys():
                    self.client_class = data["client-class"]
            i = 0
            for _ in data["pools"]:
                this_pool = Pool()
                this_pool.fill_from_json(data["pools"][i])
                i += 1
                self.pools.append(this_pool)

            # for key in data.keys():
            #     if key not in ["id", "allocator", "pd-allocator", "calculate-tee-times", "max-preferred-lifetime", "interface",
            #                    "max-valid-lifetime", "valid-lifetime", "min-preferred-lifetime", "t1-percent", "t2-percent",
            #                    "subnet", "store-extended-info", "renew-timer", "relay", "client-class", "min-valid-lifetime",
            #                    "rebind-timer", "rapid-commit", "preferred-lifetime", "pools"]:
            #         print(f"Not handing this key yet: {key}")
            #         print(f"Value: {data[key]}")
        except:
            raise ValueError("Invalid value for json_str passed to fill_from_json")

