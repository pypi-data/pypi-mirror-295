import ipaddress
from dhcpy.subnetType import SubnetType

class Pool(object):
    def __init__(self, ip_range=None):
        """Initialize a pool object (just the IP range for a rule)
        :param ip_range: A string in the format "Start-End"
        """
        if ip_range is not None:
            self.ip_range = ip_range
        else:
            self._ip_range = None

    def __dict__(self):
        """Return a dictionary representation of the pool, for making JSON in the format KEA expects"""
        if self.ip_range is not None:
            return {"pool": self.ip_range}
        else:
            raise ValueError("No IP range set")

    @property
    def ip_range(self):
        """Return the IP range as a string in the format "Start-End" """
        return self._ip_range

    @ip_range.setter
    def ip_range(self, ip_range):
        """Set the IP range from a string in the format "Start-End" """
        try:
            low, high = ip_range.split("-")
            if ipaddress.ip_address(low).version == 4:
                self.subnet_type = SubnetType.v4
            elif ipaddress.ip_address(low).version == 6:
                self.subnet_type = SubnetType.v6
            self._ip_range = ip_range
        except IndexError:
            raise ValueError("Invalid range, looking for a \"-\" in the range")
        except ValueError:
            raise ValueError("Invalid range, looking for two valid IP addresses")

    @ip_range.deleter
    def ip_range(self):
        """Delete the IP range. Don't do this, because it doesn't do anything."""
        raise ValueError("yeah, let's not do this, okay?")

    def fill_from_json(self, json_str):
        """Decode a JSON string into a pool object"""
        # print(json_str)
        try:
            data = json_str
            self.ip_range = data["pool"]

            # for key in data.keys():
            #     if key not in ["pool"]:
            #         print(f"Not handing this key yet: {key}")
            #         print(f"Value: {data[key]}")
        except:
            raise ValueError("Invalid value for json_str passed to fill_from_json")
