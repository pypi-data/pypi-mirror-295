"""
Plugins for KEA are called hooks, and this is a hacked version of the hookLibrary class for the dhcpy project.
"""
class HookLibrary(object):
    def __init__(self):
        self.library = ""
        self.parameters = {}

    def __dict__(self):
        return {"library": self.library, "parameters": self.parameters}

    def fill_from_json(self, data):
        print(data)
        self.library = data["library"]
        self.parameters = data["parameters"]