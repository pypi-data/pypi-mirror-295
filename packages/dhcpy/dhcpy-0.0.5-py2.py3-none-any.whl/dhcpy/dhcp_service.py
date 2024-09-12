from dhcpy.subnet import Subnet, SubnetType
from dhcpy.allocatorType import AllocatorType
from dhcpy.allocator import Allocator
from dhcpy.sendToServer import get_v6_config, save_config, get_v4_config
from dhcpy.dhcpOption import DHCPOption, OptionUsage
from dhcpy.ClientClass import ClientClass
from dhcpy.dhcpQueueControl import DHCPQueueControl
from dhcpy.expiredLeaseProcessing import ExpiredLeasesProcessing
from dhcpy.interfacesConfig import InterfacesConfig
from dhcpy.leaseDatabase import LeaseDatabase
from dhcpy.Logger import Logger
from dhcpy.multiThreading import MultiThreading
from dhcpy.sanityChecks import SanityChecks
from dhcpy.serverID import ServerID
from dhcpy.hookLibrary import HookLibrary


class DhcpService(Allocator):
    def __init__(self):
        super().__init__()
        self.json_key = None
        """Initialize a DHCP service object, with empty strings and lists"""
        self.subnets = []
        """A list of Subnet objects"""
        self.control_socket = ""
        """The control socket for the DHCP service"""
        self.global_params = {}
        """A dictionary of global DHCP Options for the DHCP service"""
        self.default_nameservers = []
        """A list of default nameservers for the DHCP service"""
        self.client_classes = []
        self.option_defs = []
        self.subnet_ids = []
        """The IDs used by the subnets in this service, so you don't reuse one and break the world"""
        self.dhcp_queue_control = DHCPQueueControl()
        """The DHCP Queue Control Object for the DHCP service"""
        self.early_global_reservations_lookup = False
        """Whether to do an early global reservations lookup"""
        self.expired_leases_processing = ExpiredLeasesProcessing()
        """The Expired Leases Processing object for the DHCP service"""
        self.host_reservation_identifiers = []
        """A list of host reservation identifiers"""
        self.hostname_char_replacement = ""
        """The hostname character replacement because using banned characters is like a sport for some people"""
        self.hostname_char_set = ""
        """The hostname character set in case you want to put your foot down"""
        self.interfaces_config = InterfacesConfig()
        """The Interfaces Config object for the DHCP service"""
        self.ip_reservations_unique = False
        """Whether IP reservations are unique"""
        self.lease_database = LeaseDatabase()
        """The Lease Database object for the DHCP service"""
        self.loggers = []
        """A list of Logger objects for the DHCP service"""
        self.mac_sources = ["any"]
        """A list of MAC sources used by DHCP service"""
        self.multi_threading = MultiThreading()
        """The Multi Threading object for the DHCP service, sets the threading options"""
        self.relay_supplied_options = []
        """A list of the DHCP Options supplied by the relay"""
        self.reservations_global = False
        self.reservations_in_subnet = True
        self.reservations_lookup_first = False
        self.reservations_out_of_pool = False
        self.sanity_checks = SanityChecks()
        """The Sanity Checks object for the DHCP service, these are the checks that are done to make sure the service is not insane"""
        self.server_id = ServerID()
        """The Server ID object for the DHCP service"""
        self.server_tag = ""
        """The server tag for the DHCP service"""
        self.statistic_default_sample_age = 0
        """The default sample age for statistics"""
        self.statistic_default_sample_count = 20
        """The default sample count for statistics"""
        self.store_extended_info = False
        """Whether to store extended lease info"""
        self.hook_libraries = []
        """The KEA plugins on this server"""

    @property
    def client_classes(self):
        """the client classes"""
        return self._client_classes

    @client_classes.setter
    def client_classes(self, client_classes):
        """set the client classes"""
        for cc in client_classes:
            if type(cc) is not ClientClass:
                raise ValueError("This is a list of client classes, you can only add client classes")
        self._client_classes = client_classes

    def add_client_class(self, client_class):
        """Add a client class to the service"""
        if type(client_class) is not ClientClass:
            raise ValueError("This is a list of client classes, you can only add client classes")
        self.client_classes.append(client_class)

    @property
    def reservations_global(self):
        """
        fetch global reservations.  If true, reservations are global, if false, they are not
        """
        return self._reservations_global

    @reservations_global.setter
    def reservations_global(self, reservations_global):
        """
        set global reservations.  If true, reservations are global, if false, they are not
        """
        if type(reservations_global) is not bool:
            if type(reservations_global) is str:
                if reservations_global.lower() == "true":
                    self._reservations_global = True
                    return
                elif reservations_global.lower() == "false":
                    self._reservations_global = False
                    return
            raise ValueError("Reservations global must be a boolean (or maybe a string)")
        self._reservations_global = reservations_global

    @property
    def reservations_in_subnet(self):
        """
        fetch reservations in subnet.  If true, reservations are in subnet, if false, they are not
        """
        return self._reservations_in_subnet

    @reservations_in_subnet.setter
    def reservations_in_subnet(self, reservations_in_subnet):
        """
        set reservations in subnet.  If true, reservations are in subnet, if false, they are not
        """
        if type(reservations_in_subnet) is not bool:
            if type(reservations_in_subnet) is str:
                if reservations_in_subnet.lower() == "true":
                    self._reservations_in_subnet = True
                    return
                elif reservations_in_subnet.lower() == "false":
                    self._reservations_in_subnet = False
                    return
            raise ValueError("Reservations in subnet must be a boolean (or maybe a string)")
        self._reservations_in_subnet = reservations_in_subnet

    @property
    def reservations_lookup_first(self):
        """controls whether host reservations lookup should be performed before lease lookup"""
        return self._reservations_lookup_first

    @reservations_lookup_first.setter
    def reservations_lookup_first(self, reservations_lookup_first):
        """set whether host reservations lookup should be performed before lease lookup"""
        if type(reservations_lookup_first) is not bool:
            if type(reservations_lookup_first) is str:
                if reservations_lookup_first.lower() == "true":
                    self._reservations_lookup_first = True
                    return
                elif reservations_lookup_first.lower() == "false":
                    self._reservations_lookup_first = False
                    return
            raise ValueError("Reservations lookup first must be a boolean (or maybe a string)")
        self._reservations_lookup_first = reservations_lookup_first

    @property
    def reservations_out_of_pool(self):
        """controls whether host reservations can be made outside the pool when reservations-in-subnet is true"""
        return self._reservations_out_of_pool

    @reservations_out_of_pool.setter
    def reservations_out_of_pool(self, reservations_out_of_pool):
        """set whether host reservations can be made outside the pool when reservations-in-subnet is true"""
        if type(reservations_out_of_pool) is not bool:
            if type(reservations_out_of_pool) is str:
                if reservations_out_of_pool.lower() == "true":
                    self._reservations_out_of_pool = True
                    return
                elif reservations_out_of_pool.lower() == "false":
                    self._reservations_out_of_pool = False
                    return
            raise ValueError("Reservations out of pool must be a boolean (or maybe a string)")
        self._reservations_out_of_pool = reservations_out_of_pool

    @property
    def hook_libraries(self):
        """The KEA plugins on this server"""
        return self._hook_libraries
    @hook_libraries.setter
    def hook_libraries(self, hook_libraries):
        """Set the KEA plugins on this server"""
        for hl in hook_libraries:
            if not isinstance(hl, HookLibrary):
                raise ValueError("hook_libraries must be a list of HookLibrary objects")
        self._hook_libraries = hook_libraries
    def add_hook_library(self, hook_library):
        """Add a KEA plugin to the server"""
        if not isinstance(hook_library, HookLibrary):
            raise ValueError("hook_library must be a HookLibrary object")
        self._hook_libraries.append(hook_library)

    def __dict__(self):
        """Return a dictionary representation of the service, for making JSON in the format KEA expects"""
        retval = super().__dict__()
        retval["client-classes"] = []
        for cc in self.client_classes:
            retval["client-classes"].append(cc.__dict__())
        retval["option-def"] = []
        for od in self.option_defs:
            retval["option-def"].append(od.__dict__())
        retval["dhcp-queue-control"] = self.dhcp_queue_control.__dict__()
        retval["early-global-reservations-lookup"] = self.early_global_reservations_lookup
        retval["expired-leases-processing"] = self.expired_leases_processing.__dict__()
        retval["host-reservation-identifiers"] = self.host_reservation_identifiers
        retval["hostname-char-replacement"] = self.hostname_char_replacement
        retval["hostname-char-set"] = self.hostname_char_set
        retval["interfaces-config"] = self.interfaces_config.__dict__()
        retval["ip-reservations-unique"] = self.ip_reservations_unique
        retval["lease-database"] = self.lease_database.__dict__()
        retval["loggers"] = []
        for logger in self.loggers:
            retval["loggers"].append(logger.__dict__())
        retval["mac-sources"] = self.mac_sources
        retval["multi-threading"] = self.multi_threading.__dict__()
        retval["relay-supplied-options"] = self.relay_supplied_options
        retval["reservations-global"] = self.reservations_global
        retval["reservations-in-subnet"] = self.reservations_in_subnet
        retval["reservations-lookup-first"] = self.reservations_lookup_first
        retval["reservations-out-of-pool"] = self.reservations_out_of_pool
        retval["sanity-checks"] = self.sanity_checks.__dict__()
        retval["server-id"] = self.server_id.__dict__()
        retval["server-tag"] = self.server_tag
        retval["statistic-default-sample-age"] = self.statistic_default_sample_age
        retval["statistic-default-sample-count"] = self.statistic_default_sample_count
        retval["store-extended-info"] = self.store_extended_info
        retval["hook-libraries"] = []
        for hl in self.hook_libraries:
            retval["hook-libraries"].append(hl.__dict__())

        return retval

    def update_service(self, server, ssl=True):
        """
        Send the service to the server
        """
        return "Not implemented on the generic object"

class Dhcp4Service(DhcpService):
    def __init__(self):
        """Initialize a DHCP4 service object, with empty strings and lists"""
        super().__init__()
        self.control_socket = "/tmp/kea4-ctrl-socket"
        """The control socket for the DHCP4 service"""


class Dhcp6Service(DhcpService):
    def __init__(self):
        """Initialize a DHCP6 service object, with empty strings and lists"""
        self.json_key = "Dhcp6"
        super().__init__()
        self.control_socket = "/tmp/kea6-ctrl-socket"
        """The control socket for the DHCP6 service"""
        self.dhcp4o6_port = 0
        self.pd_allocator = AllocatorType.none
        """The allocator for prefix delegation (in a row or just all over the place)"""
        self.subnets = []

    @property
    def dhcp4o6_port(self):
        """The port for DHCP4 over DHCP6"""
        return self._dhcp4o6_port

    @dhcp4o6_port.setter
    def dhcp4o6_port(self, dhcp4o6_port):
        """Set the port for DHCP4 over DHCP6"""
        if type(dhcp4o6_port) is not int:
            raise ValueError("dhcp4o6_port must be an integer")
        self._dhcp4o6_port = dhcp4o6_port

    @property
    def subnets(self):
        return self._subnets

    @subnets.setter
    def subnets(self, subnets):
        self._subnets = subnets

    def add_subnet(self, subnet):
        """Add a subnet to the service"""
        if type(subnet) is not Subnet:
            raise ValueError("This is a DHCP6 service, you can only add DHCP6 subnets")

        if subnet.subnet_type not in [SubnetType.v6, SubnetType.pd]:
            raise ValueError("This is a DHCP6 service, you can only add DHCP6 subnets")
        self.subnets.append(subnet)

    def __dict__(self):
        """Return a dictionary representation of the service, for making JSON in the format KEA expects"""
        retval = super().__dict__()
        ctrl_sock = {"socket-type": "unix",
                     "socket-name": self.control_socket}  # set it to what KEA wants, and just guess it's a unix socket
        retval["control-socket"] = ctrl_sock
        retval["dhcp4o6-port"] = self.dhcp4o6_port
        retval["pd-allocator"] = self.pd_allocator.value
        retval["subnet6"] = []
        for subnet in self.subnets:
            retval["subnet6"].append(subnet.__dict__())
        return {"Dhcp6": dict(sorted(retval.items()))}

    def get_config(self, server, ssl=True):
        """
        Get the v6 settings of the server
        """
        rets = get_v6_config(server, ssl=ssl)
        if len(rets) == 0:
            print("No return from get_v6_config")
            return
        #print(rets)
        self.client_classes = []
        # self.option_defs = []
        self.subnets = []
        # try:
        super().fill_from_json(rets[0]["arguments"]["Dhcp6"])
        for key in rets[0]["arguments"]:
            if key == self.json_key:
                _ = False
                for subkey in rets[0]["arguments"]["Dhcp6"]:
                    if subkey == "subnet6":
                        i = 0
                        for subnet in rets[0]["arguments"]["Dhcp6"][subkey]:
                            this_sn = Subnet()
                            this_sn.fill_from_json(rets[0]["arguments"]["Dhcp6"][subkey][i])
                            i += 1
                            self.subnets.append(this_sn)
                    elif subkey == "client-classes":
                        i = 0
                        for _ in rets[0]["arguments"]["Dhcp6"][subkey]:
                            this_cc = ClientClass()
                            # print(rets[0]["arguments"]["Dhcp6"][subkey])
                            this_cc.fill_from_json(rets[0]["arguments"]["Dhcp6"][subkey][i])
                            i += 1
                            self.add_client_class(this_cc)
                    elif subkey == "dhcp-queue-control":
                        self.dhcp_queue_control.fill_from_json(rets[0]["arguments"]["Dhcp6"][subkey])
                    elif subkey == "early-global-reservations-lookup":
                        self.early_global_reservations_lookup = rets[0]["arguments"]["Dhcp6"][subkey]
                    elif subkey == "expired-leases-processing":
                        self.expired_leases_processing.fill_from_json(rets[0]["arguments"]["Dhcp6"][subkey])
                    elif subkey == "host-reservation-identifiers":
                        self.host_reservation_identifiers = rets[0]["arguments"]["Dhcp6"][subkey]
                    elif subkey == "hostname-char-replacement":
                        self.hostname_char_replacement = rets[0]["arguments"]["Dhcp6"][subkey]
                    elif subkey == "hostname-char-set":
                        self.hostname_char_set = rets[0]["arguments"]["Dhcp6"][subkey]
                    elif subkey == "interfaces-config":
                        self.interfaces_config.fill_from_json(rets[0]["arguments"]["Dhcp6"][subkey])
                    elif subkey == "ip-reservations-unique":
                        self.ip_reservations_unique = rets[0]["arguments"]["Dhcp6"][subkey]
                    elif subkey == "lease-database":
                        self.lease_database.fill_from_json(rets[0]["arguments"]["Dhcp6"][subkey])
                    elif subkey == "loggers":
                        i = 0
                        for _ in rets[0]["arguments"]["Dhcp6"][subkey]:
                            logger = Logger()
                            logger.fill_from_json(rets[0]["arguments"]["Dhcp6"][subkey][i])
                            i += 1
                            self.loggers.append(logger)
                    elif subkey == "mac-sources":
                        self.mac_sources = rets[0]["arguments"]["Dhcp6"][subkey]
                    elif subkey == "multi-threading":
                        self.multi_threading.fill_from_json(rets[0]["arguments"]["Dhcp6"][subkey])
                    elif subkey == "pd-allocator":
                        self.pd_allocator = AllocatorType(rets[0]["arguments"]["Dhcp6"][subkey])
                    elif subkey == "relay-supplied-options":
                        for sk in rets[0]["arguments"]["Dhcp6"][subkey]:
                            self.relay_supplied_options.append(sk)
                    elif subkey == "reservations-global":
                        self.reservations_global = rets[0]["arguments"]["Dhcp6"][subkey]
                    elif subkey == "reservations-in-subnet":
                        self.reservations_in_subnet = rets[0]["arguments"]["Dhcp6"][subkey]
                    elif subkey == "reservations-lookup-first":
                        self.reservations_lookup_first = rets[0]["arguments"]["Dhcp6"][subkey]
                    elif subkey == "reservations-out-of-pool":
                        self.reservations_out_of_pool = rets[0]["arguments"]["Dhcp6"][subkey]
                    elif subkey == "sanity-checks":
                        self.sanity_checks.fill_from_json(rets[0]["arguments"]["Dhcp6"][subkey])
                    elif subkey == "server-id":
                        self.server_id.fill_from_json(rets[0]["arguments"]["Dhcp6"][subkey])
                    elif subkey == "server-tag":
                        self.server_tag = rets[0]["arguments"]["Dhcp6"][subkey]
                    elif subkey == "statistic-default-sample-age":
                        self.statistic_default_sample_age = rets[0]["arguments"]["Dhcp6"][subkey]
                    elif subkey == "statistic-default-sample-count":
                        self.statistic_default_sample_count = rets[0]["arguments"]["Dhcp6"][subkey]
                    elif subkey == "store-extended-info":
                        self.store_extended_info = rets[0]["arguments"]["Dhcp6"][subkey]
                    elif subkey == "subnet6":
                        for sk in rets[0]["arguments"]["Dhcp6"][subkey]:
                            this_sn = Subnet()
                            this_sn.fill_from_json(sk)
                            this_sn.subnet_type = SubnetType.v6
                            self.add_subnet(this_sn)
                    elif subkey == "hooks-libraries":
                        i = 0
                        for _ in rets[0]["arguments"]["Dhcp6"][subkey]:
                            hl = HookLibrary()
                            hl.fill_from_json(rets[0]["arguments"]["Dhcp6"][subkey][i])
                            i += 1
                            self.add_hook_library(hl)

                    # else:
                    #     _ = True
                    #     print(f"key: {subkey}") #: {rets[0]["arguments"]["Dhcp6"][subkey]}")
            # else:
            #     print(f"Unknown key: {key}")

        # except Exception as e:
        #     print(f"Error: {e}")
        # print(json.dumps(rets, indent=4))
