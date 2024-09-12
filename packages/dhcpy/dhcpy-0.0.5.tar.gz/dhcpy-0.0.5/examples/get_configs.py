from dhcpy import Server, Subnet, Pool
from dhcpy.subnet import SubnetType
# from dhcpy.sendToServer import get_config
import json

# Create a server object
kea_server = Server(
    mgmt_ip4="198.19.249.59",
    hostname="kea0",
    interfaces=["prod"])
print("getting config")
# kea_server.get_config(ssl=False)
#
# print(f"v4_socket: {kea_server.v4_socket}")
# print(f"v6_socket: {kea_server.v6_socket}")

kea_server.get_v6_config(ssl=False)
print(json.dumps(dict(sorted(kea_server.dhcp_v6_service.__dict__().items())), indent=4))

# Create a subnet object
# subnet = Subnet()
# pool = Pool(subnet="2001:db8:1::/64")
# pool.subnet_type = subnet_type.v6
# subnet.pools.append(pool)
# subnet.id = 1
# print(json.dumps(subnet.__dict__(), indent=4))
#
# for cc in kea_server.client_classes:
#     # print(json.dumps(cc.__dict__(), indent=4))
#     print(f"Name: {cc.name}")
#     print(f"Test: {cc.test}")
#     i = 0
#     for option_data in cc.option_data:
#         print(f"Option Data {i}")
#         # print(json.dumps(option_data.__dict__(), indent=4))
#         print(f"Name: {option_data.name}")
#         print(f"Data: {option_data.data}")
#         print(f"Code: {option_data.code}")
#         print(f"Space: {option_data.space}")
#         # print(f"Type: {option_data.type}")
#         print(f"Always Send: {option_data.always_send}")
#         print(f"Never Send: {option_data.never_send}")
#         i += 1
# for od in kea_server.option_defs:
#     print(f"Option Def {i}")
#     print(f"Name: {od.name}")
#     print(f"Data: {od.data}")
#     print(f"Code: {od.code}")
#     print(f"Space: {od.space}")
#     print(f"Type: {od.type}")
#     print(f"Always Send: {od.always_send}")
#     print(f"Never Send: {od.never_send}")

# for subnet in kea_server.subnets:
#     print(f"Subnet {subnet.id}")
#     # print(f"Subnet Type: {subnet.subnet_type}")
#     # print(f"Client Class: {subnet.client_class}")
#     # print(f"Subnet: {subnet.pools[0].subnet}")
#     # print(f"Pool Type: {subnet.pools[0].pool_type}")
#     print(f"Allocator: {subnet.allocator_type}")
