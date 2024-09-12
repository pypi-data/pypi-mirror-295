"""
An object to store server information, like IP address, hostname, and interfaces
"""
import json

from dhcpy import Subnet
from dhcpy.dhcpOption import DHCPOption, OptionUsage
from dhcpy.dhcp_service import Dhcp6Service
from dhcpy.sendToServer import get_config, get_v6_config, save_config, get_v4_config
from dhcpy.ClientClass import ClientClass
from dhcpy.allocator import Allocator
from dhcpy.allocatorType import AllocatorType

from dhcpy.sendToServer import get_config
import json
class Server(object):
    """
    A KEA server, with an IP address, hostname, and interfaces
    """

    def __init__(self, mgmt_ip4=None, mgmt_ip6=None, hostname=None, interfaces=None):
        self.mgmt_ip4 = mgmt_ip4
        """
        The IPv4 address used the manage the server. This is not neccessarily the IP address used by the DHCP service
        """
        self.v4_socket = "/tmp/kea4-ctrl-socket"
        """
        The control socket for the DHCP6 service. Set to the default value. You can change it if you need to.
        """
        self.mgmt_ip6 = mgmt_ip6
        """
        The IPv6 address used the manage the server. This is not neccessarily the IP address used by the DHCP service
        """
        self.v6_socket = "/tmp/kea6-ctrl-socket"
        """
        The control socket for the DHCP6 service. Set to the default value. You can change it if you need to.
        """
        self.hostname = hostname
        """The hostname of the server, if your into that whole DNS thing"""
        self.interfaces = []
        """A list of interfaces on the server. These are the names used by KEA to identify the interfaces"""
        if interfaces is not None:
            self.interfaces = interfaces
        self.v6_allocator = "iterative"
        self.calculate_tee_times = True
        self.client_classes = []
        self.option_defs = []
        self.subnet_ids = []
        self.dhcp_v6_service = Dhcp6Service()

    @property
    def subnet_ids(self):
        self._subnet_ids = []
        for subnet in self.subnets:
            self._subnet_ids.append(subnet.id)
        return self._subnet_ids
    @subnet_ids.setter
    def subnet_ids(self, subnet_ids):
        self._subnet_ids = subnet_ids

    @property
    def subnets(self):
        return self.dhcp_v6_service.subnets



    def get_config(self, ssl=True):
        """
        Get the configuration of the server
        """
        conf = get_config(self, ssl=ssl)
        for key in conf[0]["arguments"]:
            if key == "Control-agent":
                for subkey in conf[0]["arguments"]["Control-agent"]:
                    if subkey == "control-sockets":
                        for subsubkey in conf[0]["arguments"]["Control-agent"][subkey]:
                            if subsubkey == "dhcp4":
                                self.v4_socket = conf[0]["arguments"]["Control-agent"][subkey][subsubkey]["socket-name"]
                            elif subsubkey == "dhcp6":
                                self.v6_socket = conf[0]["arguments"]["Control-agent"][subkey][subsubkey]["socket-name"]
                    # else:
                    #     print(f"key: {subkey}")



    def get_v6_config(self, ssl=True):
        """
        Get the v6 settings of the server
        """
        self.dhcp_v6_service.get_config(self, ssl=ssl)


    def get_v4_config(self, ssl=True):
        """
        Get the v6 settings of the server
        """
        return get_v4_config(self, ssl=ssl)

    def save_config(self, ssl=True):
        """
        Write the configuration to the server
        :return: the reply from kea
        """
        return save_config(self, ssl=ssl)


