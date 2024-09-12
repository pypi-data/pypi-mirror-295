from enum import Enum
# import ipaddress

class OptionUsage(Enum):
    """
    An enum to represent the possible usages of a DHCP option
    """
    NONE = 0
    """No usage was set"""
    OPTION_DEFINITION = 1
    """The option is defining an option (for option-def)"""
    OPTION_IMPLEMENTATION = 2
    """The option is implementing an option (for option-data)"""

class DHCPOption(object):
    """
    A class to represent a DHCP option
    """
    def __init__(self, space="", name="", code=-1, data="", always_send=False, never_send=False, array=False, type=""):
        """
        Initialize a DHCP option
        :param space: The vendor space of the option
        :param name: The name of the option
        :param code: The type code of the option
        :param data: The data of the option
        :param always_send: A boolean to determine if the option should always be sent
        """

        self.never_send_set = False
        """Never send option was set"""
        self.space = ""
        self.name = ""
        self.code = -1
        self.data = ""
        self.always_send = False
        self.always_send_set = False
        """Always send option was set"""
        self.never_send = False
        self.array = False
        self.array_set = False
        """Array option was set"""
        self.type = ""
        self.csv_format = False
        self.csv_format_set = False
        """CSV format option was set"""
        self.encapsulate = ""
        """the string that the encapsulated options use to identify this option"""
        self.encapsulate_set = ""
        """encapsulate option was set"""
        self.record_types = "" #I don't think I fully understand this yet
        self.record_types_set = "" #I don't think I fully understand this yet
        """record types option was set"""
        self.option_usage = OptionUsage.NONE
        """Is the option defining or implementing an option"""

    def __dict__(self):
        """
        Return a dictionary representation of the option, for making JSON in the format KEA expects
        """
        if self.option_usage == OptionUsage.OPTION_IMPLEMENTATION:
            retval = {"name": self.name, "code": self.code, "space": self.space,  "data": self.data}
            if self._csv_format_set:
                retval["csv-format"] = self.csv_format
            retval["always-send"] = self.always_send
            retval["never-send"] = self.never_send
            return retval
        elif self.option_usage == OptionUsage.OPTION_DEFINITION:
            retval = {"name": self.name, "code": self.code, "space": self.space, "type": self.type}
            if self._array_set:
                retval["array"] = self.array
            if self._encapsulate_set:
                retval["encapsulate"] = self.encapsulate
            if self._record_types_set:
                retval["record-types"] = self.record_types
            return retval

    @property
    def space(self):
        """
        Return the vendor space of the option
        """
        return self._space

    @property
    def name(self):
        """
        Return the name of the option
        """
        return self._name

    @property
    def code(self):
        """
        Return the code of the option
        """
        return self._code

    @property
    def data(self):
        """
        Return the data of the option
        """
        return self._data

    @property
    def always_send(self):
        """
        Return a boolean to determine if the option should always be sent
        """
        return self._always_send
    @property
    def never_send(self):
        """
        Return a boolean to determine if the option should always be sent
        """
        return self._never_send
    @property
    def array(self):
        """
        Return a boolean to determine if the option is an array
        """
        return self._array

    @property
    def type(self):
        """
        Return the data type
        """
        return self._type
    @property
    def csv_format(self):
        """
        Return the csv_format
        """
        return self._csv_format
    @property
    def encapsulate(self):
        """
        Return the encapsulated name
        """
        return self._encapsulate
    @property
    def record_types(self):
        """
        Return the record_types
        """
        return self._record_types
    def always_send_string(self):
        """
        Return always_send as a string, all lowercase, for the JSON output
        """
        if self._always_send:
            return "true"
        else:
            return "false"
    def array_string(self):
        """
        Return array as a string, all lowercase, for the JSON output
        """
        if self._array:
            return "true"
        else:
            return "false"

    @space.setter
    def space(self, space):
        """
        Set the vendor space of the option
        """
        self._space = space

    @name.setter
    def name(self, name):
        """
        Set the name of the option
        """
        self._name = name

    @code.setter
    def code(self, code):
        """
        Set the code of the option
        """
        self._code = code

    @data.setter
    def data(self, data):
        """
        Set the data of the option
        """
        self._data = data

    @always_send.setter
    def always_send(self, always_send):
        """
        Set a boolean to determine if the option should always be sent
        """
        self._always_send = always_send
    @never_send.setter
    def never_send(self, never_send):
        """
        Set a boolean to determine if the option should never be sent
        """
        self._never_send = never_send

    @array.setter
    def array(self, value):
        """Value of the option is an array"""
        self._array = value
        self._array_set = True

    @type.setter
    def type(self, type):
        """
        Set the name of the option
        """
        self._type = type
    @csv_format.setter
    def csv_format(self, value):
        """
        Set the csv_format
        """
        self._csv_format = value
        self._csv_format_set = True
    @encapsulate.setter
    def encapsulate(self, value):
        """
        Set the encapsulated name
        """
        self._encapsulate = value
        self._encapsulate_set = True
    @record_types.setter
    def record_types(self, value):
        """
        Set the record_types
        """
        self._record_types = value
        self._record_types_set = True
    def fill_from_json(self, json_str):
        """
        :param json_str:
        :return:
        """
        # print(json_str)
        self.space = json_str["space"]
        self.name = json_str["name"]
        self.code = json_str["code"]
        if "data" in json_str.keys():
            self.data = json_str["data"]
        if "always-send" in json_str.keys():
            self.always_send = json_str["always-send"]
        if "never-send" in json_str.keys():
            self.never_send = json_str["never-send"]
        if "csv-format" in json_str.keys():
            self.csv_format = json_str["csv-format"]
        if "array" in json_str.keys():
            self.array = json_str["array"]
        if "type" in json_str.keys():
            self.type = json_str["type"]
        if "encapsulate" in json_str.keys():
            self.encapsulate = json_str["encapsulate"]
        if "record-types" in json_str.keys():
            self.record_types = json_str["record-types"]
        for key in json_str.keys():
            if key not in ["space", "name", "code", "data", "always-send", "never-send", "csv-format", "type",
                           "encapsulate", "record-types", "array"]:
                print(f"Don't have code for key: {key}")
                print(f"value: {json_str[key]}")
                print(f"json_str: {json_str}")
        if self.csv_format:
            self.data = self.data.replace(", ", ",") #remove the space after the comma