from checker import Checker

class Check_CIS_1_3(Checker):

    def __init__(self, firewall, display, verbose=False):
        
        super().__init__(firewall, display, verbose)
        
        self.id = "1.3"
        self.title = "Disable all management related services on WAN port"
        self.levels = [1]
        self.auto = False
        self.benchmark_version = "v1.1.0"
        self.benchmark_author = "CIS"

    def do_check(self):
        wan_interfaces = self.firewall.get_wan_interfaces()

        self.add_question_context("The following WAN interfaces have allowaccess not empty:")
        for interface in wan_interfaces:
            name = interface["edit"]
            if "allowaccess" in interface.keys():
                allowaccess = interface["allowaccess"]
                self.add_question_context(f'{name}: {allowaccess}')
        answer = self.ask("Does it seems adequate? (Y/n)")
        
        if answer == 'n' or answer == 'N':
            self.set_message("Manually set to not compliant")
            return False
        else:
            self.set_message("Manually set to compliant")
            return True
