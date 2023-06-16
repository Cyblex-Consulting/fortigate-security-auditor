from checker import Checker

class Check_2_4_5(Checker):

    def __init__(self, config, verbose=False):
        
        super().__init__(config, verbose)

        self.id = "2.4.5"
        self.title = "Ensure only encrypted access channels are enabled"
        self.levels = [1]
        self.auto = True
        self.benchmark_version = "v1.1.0"

    def do_check(self):
        config_system_interface = self.get_config("system interface")
        interfaces = config_system_interface["edits"]

        fail = False
        for interface in interfaces:
            name = interface["edit"]
            if "allowaccess" in interface.keys():
                allowaccess = interface["allowaccess"]
                if not isinstance(allowaccess, list):
                    allowaccess = [allowaccess]
                #print(allowaccess)
                if "http" in allowaccess or "telnet" in allowaccess:
                    fail = True
                self.add_message(f'{name}: set allowaccess {" ".join(allowaccess)}')
        
        return not fail
