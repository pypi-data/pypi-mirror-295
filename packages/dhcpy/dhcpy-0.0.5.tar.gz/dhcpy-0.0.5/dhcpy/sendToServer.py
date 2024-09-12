"""Fucntions for sending commands to KEA server"""
import json
import os

import requests
# from dhcpy.server import Server
from dhcpy.subnet import Pool, Subnet, SubnetType
import sys
KEA_PORT = 8998

def send_subnet_to_server(server, subnet, ssl=True):
    """
    Send a subnet to a KEA server
    :param server: a server object with a management IP address and a list of interfaces
    :param subnet: a subnet object
    :return: No idea yet. But it should definitely return something
    """
    headers = {
        "Content-Type": "application/json",
    }
    url = f"https://{server.mgmt_ip4}:{KEA_PORT}"
    if not ssl:
        url = f"http://{server.mgmt_ip4}:{KEA_PORT}"
    data = {}
    if subnet.subnet_type == SubnetType.v6:
        data["command"] = "subnet6-add"
        data["service"] = ["dhcp6"]
        data["arguments"] = {}
        data["arguments"]["Dhcp6"] = {}
        data["arguments"]["Dhcp6"]["interfaces-config"] = {}
        data["arguments"]["Dhcp6"]["interfaces-config"]["interfaces"] = server.interfaces
        data["arguments"]["Dhcp6"]["calculate-tee-times"] = True
        data["arguments"]["Dhcp6"]["control-socket"] = {} # forget this and bad things happen
        data["arguments"]["Dhcp6"]["control-socket"]["socket-name"] = server.v6_socket
        data["arguments"]["Dhcp6"]["control-socket"]["socket-type"] = "unix"

        data["arguments"]["Dhcp6"]["subnet6"] = [subnet.__dict__()]
        r2 = requests.post(
            url,
            data=json.dumps(data),
            headers=headers,
            auth=(os.environ.get('KEAUser'), os.environ.get('KEAPass'))
        )
        expected_length = r2.headers.get("Content-Length")
        if expected_length is not None:
            actual_length = r2.raw.tell()
            expected_length = int(expected_length)
            if actual_length < expected_length:
                raise IOError(
                    "incomplete read ({} bytes read, {} more expected)".format(
                        actual_length, expected_length - actual_length
                    )
                )
        print(r2.content)

        # print(json.dumps(data, indent=4))
    elif subnet.SubnetType == SubnetType.v4:
        data["command"] = "subnet4-add"
        data["service"] = ["dhcp4"]
        data["arguments"] = {}
        data["arguments"]["Dhcp4"] = {}
        data["arguments"]["Dhcp4"]["interfaces-config"] = {}
        data["arguments"]["Dhcp4"]["interfaces-config"]["interfaces"] = server.interfaces
        data["arguments"]["Dhcp4"]["calculate-tee-times"] = True
        data["arguments"]["Dhcp4"]["control-socket"] = {} # forget this and bad things happen
        data["arguments"]["Dhcp4"]["control-socket"]["socket-name"] = server.v4_socket
        data["arguments"]["Dhcp4"]["control-socket"]["socket-type"] = "unix"

        data["arguments"]["Dhcp4"]["subnet4"] = [subnet.__dict__()]
        r2 = requests.post(
            url,
            data=json.dumps(data),
            headers=headers,
            auth=(os.environ.get('KEAUser'), os.environ.get('KEAPass'))
        )
        expected_length = r2.headers.get("Content-Length")
        if expected_length is not None:
            actual_length = r2.raw.tell()
            expected_length = int(expected_length)
            if actual_length < expected_length:
                raise IOError(
                    "incomplete read ({} bytes read, {} more expected)".format(
                        actual_length, expected_length - actual_length
                    )
                )
        print(r2.content)

        # print(json.dumps(data, indent=4))
    else:
        print(subnet.SubnetType)
    # print(json.dumps(data))

def get_config(server, ssl=True):
    """
    Get the configuration of a server
    :param server: a server object
    :return: a dictionary of the server configuration
    """
    headers = {
        "Content-Type": "application/json",
    }
    url = f"https://{server.mgmt_ip4}:{KEA_PORT}"
    if not ssl:
        url = f"http://{server.mgmt_ip4}:{KEA_PORT}"
    data = {}
    data["command"] = "config-get"
    print("Sending request to", url)
    r = requests.post(
        url,
        data=json.dumps(data),
        headers=headers,
        auth=(os.environ.get('KEAUser'), os.environ.get('KEAPass'))
        # verify=False
    )
    expected_length = r.headers.get("Content-Length")
    if expected_length is not None:
        actual_length = r.raw.tell()
        expected_length = int(expected_length)
        if actual_length < expected_length:
            raise IOError(
                "incomplete read ({} bytes read, {} more expected)".format(
                    actual_length, expected_length - actual_length
                )
            )
    return json.loads(r.content)

def get_v6_config(server, ssl=True):
    """
    Get the configuration of a server
    :param server: a server object
    :return: a dictionary of the server configuration
    """
    headers = {
        "Content-Type": "application/json",
    }
    url = f"https://{server.mgmt_ip4}:{KEA_PORT}"
    if not ssl:
        url = f"http://{server.mgmt_ip4}:{KEA_PORT}"
    data = {}
    data["command"] = "config-get"
    data["service"] = ["dhcp6"]
    print("Sending request to", url)
    r = requests.post(
        url,
        data=json.dumps(data),
        headers=headers,
        auth=(os.environ.get('KEAUser'), os.environ.get('KEAPass'))
        # verify=False
    )
    expected_length = r.headers.get("Content-Length")
    if expected_length is not None:
        actual_length = r.raw.tell()
        expected_length = int(expected_length)
        if actual_length < expected_length:
            raise IOError(
                "incomplete read ({} bytes read, {} more expected)".format(
                    actual_length, expected_length - actual_length
                )
            )
    return json.loads(r.content)

def get_v4_config(server, ssl=True):
    """
    Get the configuration of a server
    :param server: a server object
    :return: a dictionary of the server configuration
    """
    headers = {
        "Content-Type": "application/json",
    }
    url = f"https://{server.mgmt_ip4}:{KEA_PORT}"
    if not ssl:
        url = f"http://{server.mgmt_ip4}:{KEA_PORT}"
    data = {}
    data["command"] = "config-get"
    data["service"] = ["dhcp4"]
    print("Sending request to", url)
    r = requests.post(
        url,
        data=json.dumps(data),
        headers=headers,
        # verify=False
    )
    expected_length = r.headers.get("Content-Length")
    if expected_length is not None:
        actual_length = r.raw.tell()
        expected_length = int(expected_length)
        if actual_length < expected_length:
            raise IOError(
                "incomplete read ({} bytes read, {} more expected)".format(
                    actual_length, expected_length - actual_length
                )
            )
    return json.loads(r.content)

def save_config(server, ssl=True):
    """
    Get the configuration of a server
    :param server: a server object
    :return: a dictionary of the server configuration
    """
    headers = {
        "Content-Type": "application/json",
    }
    url = f"https://{server.mgmt_ip4}:{KEA_PORT}"
    if not ssl:
        url = f"http://{server.mgmt_ip4}:{KEA_PORT}"
    data = {}
    data["command"] = "config-write"
    data["service"] = ["dhcp6", "dhcp4"]
    print("Sending request to", url)
    r = requests.post(
        url,
        data=json.dumps(data),
        headers=headers,
        auth=(os.environ.get('KEAUser'), os.environ.get('KEAPass'))
        # verify=False
    )
    expected_length = r.headers.get("Content-Length")
    if expected_length is not None:
        actual_length = r.raw.tell()
        expected_length = int(expected_length)
        if actual_length < expected_length:
            raise IOError(
                "incomplete read ({} bytes read, {} more expected)".format(
                    actual_length, expected_length - actual_length
                )
            )

    return json.loads(r.content)
