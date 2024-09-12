from enum import Enum
from dhcpy.dhcpOption import DHCPOption, OptionUsage
from dhcpy.allocatorType import AllocatorType

class Allocator(object):
    """
    A base class for objects that allocate addresses.
    This class is not meant to be used directly, but to be inherited by classes that allocate addresses, like the DHCP6
    service, the subnet rules, and the pools. These classes share attributes and methods that act like global or specific
    settings.

    You know what, it's early and this makes sense in my head even if I can make it work in words.
    """
    def __init__(self):
        """
        Initialize the object
        """
        self.allocator_type = AllocatorType.none
        self.sets_allocator_type = False
        """Flag to indicate if the allocator type has been set"""
        self.calculate_tee_times = True
        self.sets_tee_times = False
        """Flag to indicate if tee times have been set"""
        self.valid_lifetime = 0
        self.sets_valid_lifetime = False
        """Flag to indicate if the valid lifetime has been set"""
        self.renew_timer= 0
        self.sets_renew_timer = False
        """Flag to indicate if the renew timer has been set"""
        self.rebind_timer = 0
        self.sets_rebind_timer = False
        """Flag to indicate if the rebind timer has been set"""
        self.preferred_lifetime = 0
        self.sets_preferred_lifetime = False
        """Flag to indicate if the preferred lifetime has been set"""
        self.decline_probation_period = 0
        self.sets_decline_probation_period = False
        """Flag to indicate if the probation period for declined leases has been set"""
        self.option_data = []
        self.option_defs = []
        self.parked_packet_limit = 0
        self.t1_percent = 0.5
        self.sets_t1_percent = False
        """Flag to indicate if the T1 percent has been set"""
        self.t2_percent = 0.8
        self.sets_t2_percent = False
        """Flag to indicate if the T2 percent has been set"""

    @property
    def allocator_type(self):
        """itterative or randomized. Assign using an AllocatorType enum or string, the object figures it out. """
        return self._allocator_type
    @allocator_type.setter
    def allocator_type(self, allocator_type):
        """
        Set the allocator type, making sure it's either an AllocatorType enum or a string that matches one of the
        AllocatorType values
        """
        if type(allocator_type) is not AllocatorType:
            if allocator_type not in [a.value for a in AllocatorType]:
                raise ValueError(f"{allocator_type} is not a valid allocator type")
            for a in AllocatorType:
                if a.value == allocator_type:
                    self._allocator_type = a
                    self.sets_allocator_type = True
                    return
        else:
            self._allocator_type = allocator_type
            self.sets_allocator_type = True
    @property
    def calculate_tee_times(self):
        """Calculate tee times. Default is True"""
        return self._calculate_tee_times
    @calculate_tee_times.setter
    def calculate_tee_times(self, calculate_tee_times):
        """
        Set the calculate tee times flag
        :param calculate_tee_times: A boolean to determine if tee times should be calculated
        """
        if type(calculate_tee_times) is not bool:
            if type(calculate_tee_times) is not str:
                raise ValueError("Calculate tee times must be a boolean")
            if calculate_tee_times == "true":
                calculate_tee_times = True
            elif calculate_tee_times == "false":
                calculate_tee_times = False
            else:
                raise ValueError("Calculate tee times must be a boolean")
        self._calculate_tee_times = calculate_tee_times
        self.sets_tee_times = True
    @property
    def valid_lifetime(self):
        """The valid lifetime of the lease. Default is 0"""
        return self._valid_lifetime
    @valid_lifetime.setter
    def valid_lifetime(self, valid_lifetime):
        """
        Set the valid lifetime of the lease
        :param valid_lifetime: The valid lifetime of the lease in seconds
        """
        if type(valid_lifetime) is not int:
            raise ValueError("Valid lifetime must be an integer")
        if valid_lifetime < 0:
            raise ValueError("Valid lifetime must be a positive integer")
        self._valid_lifetime = valid_lifetime
        self.sets_valid_lifetime = True
    @property
    def renew_timer(self):
        """The renew timer. Default is 0"""
        return self._renew_timer
    @renew_timer.setter
    def renew_timer(self, renew_timer):
        """
        Set the renew timer
        :param renew_timer: The renew timer in seconds
        """
        if type(renew_timer) is not int:
            raise ValueError("Renew timer must be an integer")
        if renew_timer < 0:
            raise ValueError("Renew timer must be a positive integer")
        self._renew_timer = renew_timer
        self.sets_renew_timer = True
    @property
    def rebind_timer(self):
        """The rebind timer. Default is 0"""
        return self._rebind_timer
    @rebind_timer.setter
    def rebind_timer(self, rebind_timer):
        """
        Set the rebind timer
        :param rebind_timer: The rebind timer in seconds
        """
        if type(rebind_timer) is not int:
            raise ValueError("Rebind timer must be an integer")
        if rebind_timer < 0:
            raise ValueError("Rebind timer must be a positive integer")
        self._rebind_timer = rebind_timer
        self.sets_rebind_timer = True
    @property
    def preferred_lifetime(self):
        """The preferred lifetime of the lease. Default is 0"""
        return self._preferred_lifetime
    @preferred_lifetime.setter
    def preferred_lifetime(self, preferred_lifetime):
        """
        Set the preferred lifetime of the lease
        :param preferred_lifetime: The preferred lifetime of the lease in seconds
        """
        if type(preferred_lifetime) is not int:
            raise ValueError("Preferred lifetime must be an integer")
        if preferred_lifetime < 0:
            raise ValueError("Preferred lifetime must be a positive integer")
        self._preferred_lifetime = preferred_lifetime
        self.sets_preferred_lifetime = True
    @property
    def decline_probation_period(self):
        """The probation period for declined leases. Default is 0"""
        return self._decline_probation_period
    @decline_probation_period.setter
    def decline_probation_period(self, decline_probation_period):
        """
        Set the probation period for declined leases
        :param decline_probation_period: The probation period in seconds
        """
        if type(decline_probation_period) is not int:
            raise ValueError("Decline probation period must be an integer")
        if decline_probation_period < 0:
            raise ValueError("Decline probation period must be a positive integer")
        self._decline_probation_period = decline_probation_period
        self.sets_decline_probation_period = True
    @property
    def option_data(self):
        """A list of DHCP options to be sent with the lease. These contain the settings for the lease"""
        return self._option_data
    @option_data.setter
    def option_data(self, option_data):
        """
        Set the list of DHCP Option objects to be sent to leases
        :param option_data: A list of DHCP Option objects, DHCPOption with option_usage set to OPTION_IMPLEMENTATION
        """
        for i in option_data:
            if type(i) is not DHCPOption:
                raise ValueError("Option data must be an OptionData object")
            if i.option_usage != OptionUsage.OPTION_IMPLEMENTATION:
                raise ValueError("Option data must be an OptionData object")
        self._option_data = option_data
    def add_option_data(self, option_data):
        """
        Add a DHCP Option object to the list of options sent to leases
        :param option_data: The DHCP Option object to add, DHCPOption with option_usage set to OPTION_IMPLEMENTATION
        """
        if type(option_data) is not DHCPOption:
            raise ValueError("Option data must be an OptionData object")
        if option_data not in self._option_data:
            self._option_data.append(option_data)
    @property
    def option_defs(self):
        """A list of DHCP options that define the option definitions used by option_data"""
        return self._option_defs
    @option_defs.setter
    def option_defs(self, option_defs):
        """
        Set the list of DHCP Option objects that define the options used by leases
        :param option_defs: A list of DHCP Option objects, DHCPOption with option_usage set to OPTION_DEFINITION
        """
        for i in option_defs:
            if type(i) is not DHCPOption:
                raise ValueError("Option data must be an OptionData object")
            if i.option_usage != OptionUsage.OPTION_DEFINITION:
                raise ValueError("Option data must be an OptionDefinition object")
        self._option_defs = option_defs
    def add_option_def(self, option_def):
        """
        Add a DHCP Option object to the list of options sent to leases
        :param option_def: The DHCP Option object to add, DHCPOption with option_usage set to OPTION_DEFINITION
        """
        if type(option_def) is not DHCPOption:
            raise ValueError("Option data must be an OptionData object")
        if option_def.option_usage != OptionUsage.OPTION_DEFINITION:
            raise ValueError("Option data must be an OptionDefinition object")
        if option_def not in self._option_defs:
            self._option_defs.append(option_def)
    @property
    def parked_packet_limit(self):
        """The max number of packets that can be parked. Default is 0"""
        return self._parked_packet_limit
    @parked_packet_limit.setter
    def parked_packet_limit(self, parked_packet_limit):
        """
        Set the parked packet limit
        :param parked_packet_limit: The max number of packets that can be parked
        """
        if type(parked_packet_limit) is not int:
            raise ValueError("Parked packet limit must be an integer")
        if parked_packet_limit < 0:
            raise ValueError("Parked packet limit must be a positive integer")
        self._parked_packet_limit = parked_packet_limit
    @property
    def t1_percent(self):
        """T1 is when renewal should be attempted. Default is 0.5. Should be between 0 and 1"""
        return self._t1_percent
    @t1_percent.setter
    def t1_percent(self, t1_percent):
        """
        Set the T1 percent
        :param t1_percent: The T1 percent. Should be between 0 and 1
        """
        if type(t1_percent) is not float:
            raise ValueError("T1 percent must be a float")
        if t1_percent < 0 or t1_percent > 1:
            raise ValueError("T1 percent must be between 0 and 1")
        self._t1_percent = t1_percent
        self.sets_t1_percent = True
    @property
    def t2_percent(self):
        """T2 is when rebind should be attempted. Default is 0.8. Should be between 0 and 1"""
        return self._t2_percent
    @t2_percent.setter
    def t2_percent(self, t2_percent):
        """
        Set the T2 percent
        :param t2_percent: The T2 percent. Should be between 0 and 1
        """
        if type(t2_percent) is not float:
            raise ValueError("T2 percent must be a float")
        if t2_percent < 0 or t2_percent > 1:
            raise ValueError("T2 percent must be between 0 and 1")
        self._t2_percent = t2_percent
        self.sets_t2_percent = True

    def __dict__(self):
        """Return a dictionary representation of the object, for making JSON in the format KEA expects"""
        rets = {}
        if self.sets_allocator_type:
            rets["allocator"] = self.allocator_type.value
        if self.sets_tee_times:
            rets["calculate-tee-times"] = self.calculate_tee_times
        if self.sets_valid_lifetime:
            rets["valid-lifetime"] = self.valid_lifetime
        if self.sets_renew_timer:
            rets["renew-timer"] = self.renew_timer
        if self.sets_rebind_timer:
            rets["rebind-timer"] = self.rebind_timer
        if self.sets_preferred_lifetime:
            rets["preferred-lifetime"] = self.preferred_lifetime
        if self.sets_decline_probation_period:
            rets["decline-probation-period"] = self.decline_probation_period
        if len(self.option_data) > 0:
            rets["option-data"] = []
            for od in self.option_data:
                rets["option-data"].append(od.__dict__())
        if len(self.option_defs) > 0:
            rets["option-def"] = []
            for od in self.option_defs:
                rets["option-def"].append(od.__dict__())
        if self.parked_packet_limit > 0:
            rets["parked-packet-limit"] = self.parked_packet_limit
        if self.sets_t1_percent:
            rets["t1-percent"] = self.t1_percent
        if self.sets_t2_percent:
            rets["t2-percent"] = self.t2_percent
        return rets

    def fill_from_json(self, json_data):
        """
        Fill the object from the JSON dictionary from the KEA web interface
        :param json_data: The JSON dictionary to fill the object from
        """
        if "allocator" in json_data:
            self.allocator_type = json_data["allocator"]
        else:
            self.allocator_type = AllocatorType.none
        if "calculate-tee-times" in json_data:
            self.calculate_tee_times = json_data["calculate-tee-times"]
            self.sets_tee_times = True # redundant, but a good reminder
        if "valid-lifetime" in json_data:
            self.valid_lifetime = json_data["valid-lifetime"]
            self.sets_valid_lifetime = True
        if "renew-timer" in json_data:
            self.renew_timer = json_data["renew-timer"]
            self.sets_renew_timer = True
        if "rebind-timer" in json_data:
            self.rebind_timer = json_data["rebind-timer"]
            self.sets_rebind_timer = True
        if "preferred-lifetime" in json_data:
            self.preferred_lifetime = json_data["preferred-lifetime"]
            self.sets_preferred_lifetime = True
        if "decline-probation-period" in json_data:
            self.decline_probation_period = json_data["decline-probation-period"]
            self.sets_decline_probation_period = True
        if "option-data" in json_data:
            self.option_data = []
            for od in json_data["option-data"]:
                o = DHCPOption()
                o.fill_from_json(od)
                o.option_usage = OptionUsage.OPTION_IMPLEMENTATION
                self.add_option_data(o)
        if "option-def" in json_data:
            self.option_defs = []
            for od in json_data["option-def"]:
                o = DHCPOption()
                o.fill_from_json(od)
                o.option_usage = OptionUsage.OPTION_DEFINITION
                self.add_option_def(o)
        if "t1-percent" in json_data:
            self.t1_percent = json_data["t1-percent"]
        if "t2-percent" in json_data:
            self.t2_percent = json_data["t2-percent"]