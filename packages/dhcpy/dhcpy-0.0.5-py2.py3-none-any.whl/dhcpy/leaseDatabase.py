class LeaseDatabase(object):
    def __init__(self):
        self.name = ""
        self.persist = False
        self.type = ""
    def __dict__(self):
        return {"name": self.name, "persist": self.persist, "type": self.type}
    def fill_from_json(self, data):
        self.name = data["name"]
        self.persist = data["persist"]
        self.type = data["type"]
