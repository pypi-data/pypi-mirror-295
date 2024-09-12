class InterfacesConfig(object):
    def __init__(self):
      self.interfaces = []
      self.re_detect = False
      self.re_detect_set = False
      self.service_sockets_require_all = False
    @property
    def re_detect(self):
        return self._re_detect
    @re_detect.setter
    def re_detect(self, re_detect):
        if type(re_detect) is not bool:
            if type(re_detect) is str:
                if re_detect.lower() == "true":
                    self._re_detect = True
                    self.re_detect_set = True
                    return
                elif re_detect.lower() == "false":
                    self._re_detect = False
                    self.re_detect_set = True
                    return
            raise ValueError("Re detect must be a boolean (or maybe a string)")
        self._re_detect = re_detect
        self.re_detect_set = True
    def __dict__(self):
        if self.re_detect_set:
            return {"interfaces": self.interfaces, "re-detect": self.re_detect, "service-sockets-require-all": self.service_sockets_require_all}
        else:
            return {"interfaces": self.interfaces, "service-sockets-require-all": self.service_sockets_require_all}
    def fill_from_json(self, data):
        self.interfaces = data["interfaces"]
        if self.re_detect_set:
            self.re_detect = data["re-detect"]
        self.service_sockets_require_all = data["service-sockets-require-all"]
