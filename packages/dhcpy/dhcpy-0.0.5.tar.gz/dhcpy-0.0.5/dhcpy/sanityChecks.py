class SanityChecks(object):
    def __init__(self):
        self.extended_info_checks = ""
        self.lease_checks = ""
    def __dict__(self):
        return {"extended-info-checks": self.extended_info_checks, "lease-checks": self.lease_checks}
    def fill_from_json(self, data):
        self.extended_info_checks = data["extended-info-checks"]
        self.lease_checks = data["lease-checks"]
