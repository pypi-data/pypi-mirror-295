class ServerID(object):
    def __init__(self):
        self.enterprise_id = 0
        self.htype = 0
        self.identifier = ""
        self.persist = False
        self.time = 0
        self.type = ""
    def __dict__(self):
        return {"enterprise-id": self.enterprise_id, "htype": self.htype, "identifier": self.identifier, "persist": self.persist, "time": self.time, "type": self.type}
    def fill_from_json(self, data):
        self.enterprise_id = data["enterprise-id"]
        self.htype = data["htype"]
        self.identifier = data["identifier"]
        self.persist = data["persist"]
        self.time = data["time"]
        self.type = data["type"]
