from dhcpy.dhcpOption import DHCPOption, OptionUsage
from dhcpy.allocator import Allocator

class ClientClass(Allocator):
    """
    A class to represent a client class
    """

    def __init__(self, name="", test="", option_data=[]):
        """
        Initialize a client class
        :param name: The name of the client class
        :param test: The test for when to apply the client class
        :param option_data: A list of option data
        """
        super().__init__()
        self.name = name
        self._test = test
        if len(option_data) > 0:
            for od in option_data:
                self.add_option_data(od)

    def __dict__(self):
        """
        Return a dictionary representation of the client class, for making json for kea
        """
        retval = super().__dict__()
        retval["name"] = self.name
        retval["test"] = self.test
        return retval

    @property
    def name(self):
        """
        Return the name of the client class
        """
        return self._name
    @property
    def test(self):
        """
        Return the test of the client class
        """
        return self._test

    @name.setter
    def name(self, name):
        """
        Set the name of the client class
        """
        self._name = name

    @test.setter
    def test(self, test):
        """
        Set the test of the client class
        """
        self._test = test

    def add_option_data(self, option_data):
        """
        Add an option data to the client class
        """
        self._option_data.append(option_data)

    def fill_from_json(self, json_str):
        """
        Fill the client class from a json string
        """
        self.name = json_str["name"]
        self.test = json_str["test"]
        i = 0
        for option_data in json_str["option-data"]:
            this_option_data = DHCPOption()
            this_option_data.option_usage = OptionUsage.OPTION_IMPLEMENTATION
            # print(json_str["option-data"][i])
            this_option_data.fill_from_json(json_str["option-data"][i])
            i += 1
            self.add_option_data(this_option_data)