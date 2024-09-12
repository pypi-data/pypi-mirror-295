class Logger(object):
    def __init__(self):
        self.debuglevel = 0
        self.name = ""
        self.output_options = {"flush": False, "maxsize": 0, "maxver": 0, "output": "", "pattern": ""}
        self.severity = ""
    def __dict__(self):
        return {"debuglevel": self.debuglevel, "name": self.name, "output-options": [self.output_options], "severity": self.severity}
    def fill_from_json(self, data):
        self.debuglevel = data["debuglevel"]
        self.name = data["name"]
        self.output_options = data["output-options"]
        self.severity = data["severity"]
    """
    "loggers": [
      {
        "debuglevel": 99,
        "name": "kea-dhcp6",
        "output-options": [
          {
            "flush": true,
            "maxsize": 40480000,
            "maxver": 8,
            "output": "/tmp/kea-debug.log",
            "pattern": ""
          }
        ],
        "severity": "DEBUG"
      }
    ],"""
