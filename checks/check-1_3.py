from checker import Checker

class Check_1_3(Checker):

    def __init__(self, config, verbose=False):
        
        super().__init__(config, verbose)

        self.id = "1.3"
        self.title = "Disable all management related services on WAN port"
        self.levels = [1]
        self.auto = False
        self.benchmark_version = "v1.1.0"

    def do_check(self):
        config_system_interface = self.get_config("system interface")
        interfaces = config_system_interface["edits"]

        question = 'Identify WAN interface and validate that "set allowaccess" does not have ping, https, http, ssh, snmp or radius-acct configured.\n\n'
        question += "The following interfaces have allowaccess not empty:\n\n"
        for interface in interfaces:
            name = interface["edit"]
            if "allowaccess" in interface.keys():
                allowaccess = interface["allowaccess"]
                question += f'{name}: {allowaccess}\n'
        question += "\nDoes it seems adequate? (Y/n)"

        answer = self.ask(question)
        
        if answer == 'n' or answer == 'N':
            self.set_message("Manually set to not compliant")
            return False
        else:
            self.set_message("Manually set to compliant")
            return True
